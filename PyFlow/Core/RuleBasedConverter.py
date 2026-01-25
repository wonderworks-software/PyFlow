## Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.

"""
Rule-Based Python to PyFlow Node Converter

This module converts Python code to PyFlow visual nodes using AST parsing
and deterministic rules. No LLM required - fast and reliable.

Features:
- AST-based parsing (no LLM needed)
- Data flow analysis (tracks variable dependencies)
- Smart node type mapping
- Automatic pin creation based on inputs/outputs
- Connection hints based on data dependencies

Rules:
- for loop -> forLoop node
- while loop -> whileLoop node  
- if/elif/else -> branch node
- function def -> compound/pythonNode
- print() -> consoleOutput node
- variable assignment -> setVar node (via pythonNode)
- function call -> pythonNode
"""

import ast
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Tuple, Set
from enum import Enum


class PyFlowNodeType(Enum):
    """PyFlow node types for mapping."""
    # Original PyFlow nodes
    FOR_LOOP = "forLoop"
    FOREACH_LOOP = "forEachLoop"
    WHILE_LOOP = "whileLoop"
    BRANCH = "branch"
    SEQUENCE = "sequence"
    CONSOLE_OUTPUT = "consoleOutput"
    PYTHON_NODE = "pythonNode"
    MAKE_INT = "makeInt"
    MAKE_FLOAT = "makeFloat"  
    MAKE_STRING = "makeString"
    MAKE_ARRAY = "makeArray"
    CONSTANT = "constant"
    STICKY_NOTE = "stickyNote"
    DO_N = "doN"
    DELAY = "delay"
    GET_VAR = "getVar"
    SET_VAR = "setVar"
    COMPOUND = "compound"
    
    # Code visualization nodes (custom nodes with exec pins)
    CODE_ASSIGN = "codeAssign"
    CODE_ARRAY = "codeArray"
    CODE_ARRAY_ACCESS = "codeArrayAccess"
    CODE_COMPARE = "codeCompare"
    CODE_LEN = "codeLen"
    CODE_PRINT = "codePrint"
    CODE_BINARY_OP = "codeBinaryOp"
    CODE_FOR_LOOP = "codeForLoop"
    CODE_BRANCH = "codeBranch"


@dataclass
class NodePin:
    """Represents a pin on a PyFlow node."""
    name: str
    pin_type: str  # IntPin, FloatPin, StringPin, BoolPin, ExecPin, AnyPin
    direction: str  # 'input' or 'output'
    default_value: Any = None
    is_exec: bool = False
    connected_to: Optional[str] = None  # Name of connected pin for data flow


@dataclass
class DataFlowEdge:
    """Represents a data flow connection between nodes."""
    from_node_idx: int
    from_pin: str
    to_node_idx: int
    to_pin: str
    variable_name: str


@dataclass
class VisualNode:
    """Specification for a visual node to be created."""
    name: str
    node_type: PyFlowNodeType
    category: str
    description: str
    inputs: List[NodePin] = field(default_factory=list)
    outputs: List[NodePin] = field(default_factory=list)
    code: str = ""
    line_start: int = 0
    line_end: int = 0
    color: Tuple[int, int, int] = (100, 150, 200)
    properties: Dict[str, Any] = field(default_factory=dict)
    # Data flow tracking
    input_vars: List[str] = field(default_factory=list)   # Variables this node reads
    output_vars: List[str] = field(default_factory=list)  # Variables this node writes
    node_index: int = -1  # Index in the node list for connection lookup
    # Data flow tracking
    input_vars: List[str] = field(default_factory=list)   # Variables this node reads
    output_vars: List[str] = field(default_factory=list)  # Variables this node creates/modifies
    node_index: int = 0  # Index for connection tracking


# Color scheme for different node categories
NODE_COLORS = {
    'control_flow': (255, 128, 64),    # Orange
    'variables': (128, 100, 200),       # Purple
    'output': (255, 200, 64),           # Yellow
    'input': (100, 200, 100),           # Green
    'math': (100, 200, 150),            # Teal
    'function': (100, 150, 200),        # Blue
    'loop': (255, 150, 100),            # Light Orange
    'data': (150, 150, 200),            # Light Purple
}


class RuleBasedConverter:
    """
    Converts Python AST to PyFlow visual nodes using deterministic rules.
    
    This is a fast, reliable alternative to LLM-based conversion.
    
    Features:
    - Data flow analysis: tracks which variables each node reads/writes
    - Smart connections: suggests connections based on variable dependencies
    - Type inference: infers variable types from assignments
    """
    
    def __init__(self):
        self.nodes: List[VisualNode] = []
        self.source_lines: List[str] = []
        self.variables: Dict[str, str] = {}  # variable name -> inferred type
        self.variable_definitions: Dict[str, int] = {}  # variable name -> node index that defines it
        self.data_flow_edges: List[DataFlowEdge] = []  # Data connections between nodes
        self.node_index: int = 0
        
    def convert(self, source_code: str) -> List[VisualNode]:
        """
        Convert Python source code to a list of visual node specifications.
        
        Args:
            source_code: Python source code string
            
        Returns:
            List of VisualNode objects ready for PyFlow canvas
        """
        self.nodes = []
        self.source_lines = source_code.split('\n')
        self.variables = {}
        self.variable_definitions = {}
        self.data_flow_edges = []
        self.node_index = 0
        
        try:
            tree = ast.parse(source_code)
            self._process_module(tree)
            # After processing, analyze data flow connections
            self._analyze_data_flow()
        except SyntaxError as e:
            # Create error node
            self.nodes.append(VisualNode(
                name="Syntax Error",
                node_type=PyFlowNodeType.STICKY_NOTE,
                category="Error",
                description=f"Line {e.lineno}: {e.msg}",
                line_start=e.lineno or 1,
                line_end=e.lineno or 1,
                color=(255, 100, 100)
            ))
            
        return self.nodes
    
    def get_data_flow_edges(self) -> List[DataFlowEdge]:
        """Get the list of data flow connections between nodes."""
        return self.data_flow_edges
    
    def _analyze_data_flow(self):
        """Analyze data flow between nodes based on variable dependencies."""
        for node in self.nodes:
            for input_var in node.input_vars:
                # Find which node defines this variable
                if input_var in self.variable_definitions:
                    source_node_idx = self.variable_definitions[input_var]
                    if source_node_idx != node.node_index:
                        # Create a data flow edge
                        edge = DataFlowEdge(
                            from_node_idx=source_node_idx,
                            from_pin=input_var,
                            to_node_idx=node.node_index,
                            to_pin=input_var,
                            variable_name=input_var
                        )
                        self.data_flow_edges.append(edge)
        
        print(f"Data flow analysis: {len(self.data_flow_edges)} connections found")
        for edge in self.data_flow_edges[:10]:  # Show first 10
            print(f"  {edge.variable_name}: node[{edge.from_node_idx}] -> node[{edge.to_node_idx}]")
    
    def _register_node(self, node: VisualNode, input_vars: List[str] = None, output_vars: List[str] = None) -> VisualNode:
        """Register a node and track its input/output variables for data flow analysis."""
        # Set input/output vars if provided
        if input_vars is not None:
            node.input_vars = input_vars
        if output_vars is not None:
            node.output_vars = output_vars
        
        # Assign index first, then increment
        node.node_index = self.node_index
        
        # Track which node defines each variable (using current index before increment)
        for var in node.output_vars:
            self.variable_definitions[var] = self.node_index
        
        self.node_index += 1
        self.nodes.append(node)
        return node
    
    def _process_module(self, tree: ast.Module):
        """Process the top-level module."""
        for node in tree.body:
            self._process_node(node)
    
    def _process_node(self, node: ast.AST):
        """Process a single AST node and convert to visual nodes."""
        
        if isinstance(node, ast.For):
            self._convert_for_loop(node)
            
        elif isinstance(node, ast.While):
            self._convert_while_loop(node)
            
        elif isinstance(node, ast.If):
            self._convert_if_statement(node)
            
        elif isinstance(node, ast.FunctionDef):
            self._convert_function_def(node)
            
        elif isinstance(node, ast.ClassDef):
            self._convert_class_def(node)
            
        elif isinstance(node, ast.Assign):
            self._convert_assignment(node)
            
        elif isinstance(node, ast.AugAssign):
            self._convert_aug_assignment(node)
            
        elif isinstance(node, ast.Expr):
            # Expression statement (like print(), function call)
            if isinstance(node.value, ast.Call):
                self._convert_call(node.value, node.lineno, node.end_lineno or node.lineno)
                
        elif isinstance(node, ast.Return):
            self._convert_return(node)
    
    def _convert_for_loop(self, node: ast.For):
        """Convert for loop to codeForLoop node - custom code visualization node."""
        line_start = node.lineno
        line_end = node.end_lineno or node.lineno
        code = self._get_source_lines(line_start, line_end)
        
        # Get loop variable name
        loop_var = node.target.id if isinstance(node.target, ast.Name) else "i"
        
        # Check if it's a range-based for loop
        is_range_loop = (
            isinstance(node.iter, ast.Call) and
            isinstance(node.iter.func, ast.Name) and
            node.iter.func.id == 'range'
        )
        
        if is_range_loop:
            # Extract range parameters - handle expressions like len(arr)
            range_args = node.iter.args
            start_val = 0
            stop_val = 10
            step_val = 1
            stop_expr = None
            
            if len(range_args) >= 1:
                if len(range_args) == 1:
                    stop_val, stop_expr = self._get_value_or_expr(range_args[0])
                else:
                    start_val, _ = self._get_value_or_expr(range_args[0])
                    stop_val, stop_expr = self._get_value_or_expr(range_args[1])
            if len(range_args) >= 3:
                step_val, _ = self._get_value_or_expr(range_args[2])
            
            range_deps = self._extract_dependencies(node.iter)
            stop_str = stop_expr if stop_expr else str(stop_val)
            iter_name = f"range({start_val}, {stop_str})"
            
            visual_node = VisualNode(
                name=f"for {loop_var} in range({start_val}, {stop_str})",
                node_type=PyFlowNodeType.CODE_FOR_LOOP,
                category="CodeVisualization",
                description=f"For loop: {loop_var} from {start_val} to {stop_str}",
                inputs=[
                    NodePin("inExec", "ExecPin", "input", is_exec=True),
                    NodePin("Start", "IntPin", "input", default_value=start_val),
                    NodePin("Stop", "IntPin", "input", default_value=stop_val if not stop_expr else 0),
                    NodePin("Step", "IntPin", "input", default_value=step_val),
                ],
                outputs=[
                    NodePin("LoopBody", "ExecPin", "output", is_exec=True),
                    NodePin("Index", "IntPin", "output"),
                    NodePin("Completed", "ExecPin", "output", is_exec=True),
                ],
                code=code,
                line_start=line_start,
                line_end=line_end,
                color=NODE_COLORS['loop'],
                properties={
                    "varName": loop_var,
                    "iterableName": iter_name,
                    "sourceCode": code,
                    "start": start_val, 
                    "stop": stop_val if not stop_expr else 0, 
                    "step": step_val,
                },
                input_vars=list(set(range_deps)),
                output_vars=[loop_var],
            )
        else:
            # forEach loop over iterable
            iter_name = self._get_name(node.iter)
            
            visual_node = VisualNode(
                name=f"for {loop_var} in {iter_name}",
                node_type=PyFlowNodeType.CODE_FOR_LOOP,
                category="CodeVisualization",
                description=f"For-each loop over {iter_name}",
                inputs=[
                    NodePin("inExec", "ExecPin", "input", is_exec=True),
                    NodePin("Start", "IntPin", "input", default_value=0),
                    NodePin("Stop", "IntPin", "input", default_value=0),  # Will be set via connection
                    NodePin("Step", "IntPin", "input", default_value=1),
                ],
                outputs=[
                    NodePin("LoopBody", "ExecPin", "output", is_exec=True),
                    NodePin("Index", "IntPin", "output"),
                    NodePin("Completed", "ExecPin", "output", is_exec=True),
                ],
                code=code,
                line_start=line_start,
                line_end=line_end,
                color=NODE_COLORS['loop'],
                properties={
                    "varName": loop_var,
                    "iterableName": iter_name,
                    "sourceCode": code,
                },
                input_vars=[iter_name] if iter_name != "unknown" else [],
                output_vars=[loop_var],
            )
        
        self._register_node(visual_node)
        
        # Process loop body
        for stmt in node.body:
            self._process_node(stmt)
    
    def _convert_while_loop(self, node: ast.While):
        """Convert while loop to whileLoop node."""
        line_start = node.lineno
        line_end = node.end_lineno or node.lineno
        code = self._get_source_lines(line_start, line_end)
        
        condition_str = self._get_source_lines(line_start, line_start).split('while')[1].split(':')[0].strip()
        condition_deps = self._extract_dependencies(node.test)
        
        visual_node = VisualNode(
            name=f"while {condition_str[:30]}",
            node_type=PyFlowNodeType.WHILE_LOOP,
            category="Control Flow",
            description=f"While loop: {condition_str}",
            inputs=[
                NodePin("inExec", "ExecPin", "input", is_exec=True),
                NodePin("Condition", "BoolPin", "input"),
            ],
            outputs=[
                NodePin("LoopBody", "ExecPin", "output", is_exec=True),
                NodePin("Completed", "ExecPin", "output", is_exec=True),
            ],
            code=code,
            line_start=line_start,
            line_end=line_end,
            color=NODE_COLORS['loop'],
            input_vars=condition_deps,
            output_vars=[],
        )
        
        self._register_node(visual_node)
        
        # Process loop body
        for stmt in node.body:
            self._process_node(stmt)
    
    def _convert_if_statement(self, node: ast.If):
        """Convert if/elif/else to branch node(s) using custom code nodes.
        
        Creates a codeCompare node for the condition if it's a comparison,
        then creates the codeBranch node.
        """
        line_start = node.lineno
        line_end = node.end_lineno or node.lineno
        code = self._get_source_lines(line_start, line_end)
        
        condition_str = self._get_source_lines(line_start, line_start)
        if 'if ' in condition_str:
            condition_str = condition_str.split('if ')[1].split(':')[0].strip()
        else:
            condition_str = "condition"
        
        condition_deps = self._extract_dependencies(node.test)
        
        # If condition is a comparison, create a codeCompare node
        if isinstance(node.test, ast.Compare):
            left_str = self._get_value_str(node.test.left)
            op_map = {
                ast.Gt: ">", ast.Lt: "<", ast.GtE: ">=", ast.LtE: "<=",
                ast.Eq: "==", ast.NotEq: "!=", ast.Is: "is", ast.IsNot: "is not",
                ast.In: "in", ast.NotIn: "not in"
            }
            op_str = op_map.get(type(node.test.ops[0]), "==") if node.test.ops else "=="
            comparators_str = self._get_value_str(node.test.comparators[0]) if node.test.comparators else "?"
            
            # Create codeCompare node
            compare_node = VisualNode(
                name=f"{left_str[:10]} {op_str} {comparators_str[:10]}",
                node_type=PyFlowNodeType.CODE_COMPARE,
                category="CodeVisualization",
                description=f"Compare: {left_str} {op_str} {comparators_str}",
                inputs=[
                    NodePin("a", "AnyPin", "input"),
                    NodePin("b", "AnyPin", "input"),
                ],
                outputs=[
                    NodePin("result", "BoolPin", "output"),
                ],
                code=condition_str,
                line_start=line_start,
                line_end=line_start,
                color=NODE_COLORS['math'],
                properties={
                    "operator": op_str,
                    "feeds_branch": True,
                },
            )
            self._register_node(compare_node, input_vars=condition_deps, output_vars=["_condition"])
        
        # Create codeBranch node
        branch_node = VisualNode(
            name=f"if {condition_str[:25]}",
            node_type=PyFlowNodeType.CODE_BRANCH,
            category="CodeVisualization",
            description=f"Branch: if {condition_str}",
            inputs=[
                NodePin("In", "ExecPin", "input", is_exec=True),
                NodePin("Condition", "BoolPin", "input"),
            ],
            outputs=[
                NodePin("True", "ExecPin", "output", is_exec=True),
                NodePin("False", "ExecPin", "output", is_exec=True),
            ],
            code=code,
            line_start=line_start,
            line_end=line_end,
            color=NODE_COLORS['control_flow'],
            properties={
                "conditionCode": condition_str,
                "sourceCode": code,
            },
        )
        
        # If we created a comparison node, the branch depends on it
        if isinstance(node.test, ast.Compare):
            self._register_node(branch_node, input_vars=["_condition"], output_vars=[])
        else:
            self._register_node(branch_node, input_vars=condition_deps, output_vars=[])
            self._register_node(branch_node, input_vars=condition_deps, output_vars=[])
        
        # Process if body
        for stmt in node.body:
            self._process_node(stmt)
            
        # Process else/elif
        for stmt in node.orelse:
            self._process_node(stmt)
    
    def _convert_function_def(self, node: ast.FunctionDef):
        """Convert function definition to pythonNode."""
        line_start = node.lineno
        line_end = node.end_lineno or node.lineno
        code = self._get_source_lines(line_start, line_end)
        
        # Extract parameters
        inputs = [NodePin("inExec", "ExecPin", "input", is_exec=True)]
        for arg in node.args.args:
            arg_name = arg.arg
            arg_type = self._get_annotation_type(arg.annotation) if arg.annotation else "AnyPin"
            inputs.append(NodePin(arg_name, arg_type, "input"))
        
        # Determine return type
        return_type = "AnyPin"
        if node.returns:
            return_type = self._get_annotation_type(node.returns)
        
        outputs = [
            NodePin("outExec", "ExecPin", "output", is_exec=True),
            NodePin("return", return_type, "output"),
        ]
        
        # Extract inputs/outputs from function
        param_names = [arg.arg for arg in node.args.args]
        return_vars = []  # Could analyze body for return statements
        
        visual_node = VisualNode(
            name=f"def {node.name}()",
            node_type=PyFlowNodeType.PYTHON_NODE,
            category="Functions",
            description=ast.get_docstring(node) or f"Function: {node.name}",
            inputs=inputs,
            outputs=outputs,
            code=code,
            line_start=line_start,
            line_end=line_end,
            color=NODE_COLORS['function'],
        )
        
        self._register_node(visual_node, input_vars=param_names, output_vars=[node.name])
    
    def _convert_class_def(self, node: ast.ClassDef):
        """Convert class definition to a pythonNode or compound."""
        line_start = node.lineno
        line_end = node.end_lineno or node.lineno
        code = self._get_source_lines(line_start, line_end)
        
        visual_node = VisualNode(
            name=f"class {node.name}",
            node_type=PyFlowNodeType.PYTHON_NODE,
            category="Classes",
            description=ast.get_docstring(node) or f"Class: {node.name}",
            inputs=[NodePin("inExec", "ExecPin", "input", is_exec=True)],
            outputs=[NodePin("outExec", "ExecPin", "output", is_exec=True)],
            code=code,
            line_start=line_start,
            line_end=line_end,
            color=(100, 100, 180),
        )
        
        self._register_node(visual_node, input_vars=[], output_vars=[node.name])
        
        # Process class methods
        for stmt in node.body:
            if isinstance(stmt, ast.FunctionDef):
                self._convert_function_def(stmt)
    
    def _convert_assignment(self, node: ast.Assign):
        """Convert variable assignment to appropriate node.
        
        Handles:
        - Simple constants: x = 10
        - Array literals: arr = [1, 2, 3]
        - Array access: res = arr[0]
        - Function calls: length = len(arr)
        - Complex expressions: result = a + b
        """
        line_start = node.lineno
        line_end = node.end_lineno or node.lineno
        code = self._get_source_lines(line_start, line_end)
        
        # Get target variable name(s)
        targets = []
        for target in node.targets:
            if isinstance(target, ast.Name):
                targets.append(target.id)
            elif isinstance(target, ast.Tuple):
                for elt in target.elts:
                    if isinstance(elt, ast.Name):
                        targets.append(elt.id)
        
        target_str = ", ".join(targets) if targets else "var"
        
        # Check if value is a complex expression that needs its own node
        value = node.value
        
        # Case 1: Array subscript access like arr[0] or arr[i]
        if isinstance(value, ast.Subscript):
            self._convert_subscript_assignment(node, targets, target_str, line_start, line_end, code)
            return
        
        # Case 2: Function call like len(arr) or max(a, b)
        if isinstance(value, ast.Call):
            self._convert_call_assignment(node, targets, target_str, line_start, line_end, code)
            return
        
        # Case 3: Comparison like a > b
        if isinstance(value, ast.Compare):
            self._convert_comparison_assignment(node, targets, target_str, line_start, line_end, code)
            return
        
        # Case 4: Binary operation like a + b
        if isinstance(value, ast.BinOp):
            self._convert_binop_assignment(node, targets, target_str, line_start, line_end, code)
            return
        
        # Case 5: Simple value (constant, variable, list literal)
        self._convert_simple_assignment(node, targets, target_str, line_start, line_end, code)
    
    def _convert_subscript_assignment(self, node, targets, target_str, line_start, line_end, code):
        """Handle assignment from array access: res = arr[i] using codeArrayAccess node."""
        value = node.value
        array_name = self._get_name(value.value)
        index_str = self._get_value_str(value.slice)
        index_deps = self._extract_dependencies(value.slice)
        
        # Determine if index is a constant or variable
        if isinstance(value.slice, ast.Constant):
            index_val = value.slice.value
            description = f"Get {array_name}[{index_val}] → {target_str}"
        else:
            description = f"Get {array_name}[{index_str}] → {target_str}"
        
        visual_node = VisualNode(
            name=f"{target_str} = {array_name}[{index_str[:10]}]",
            node_type=PyFlowNodeType.CODE_ARRAY_ACCESS,
            category="CodeVisualization",
            description=description,
            inputs=[
                NodePin("inExec", "ExecPin", "input", is_exec=True),
                NodePin("array", "AnyPin", "input"),
                NodePin("index", "IntPin", "input"),
            ],
            outputs=[
                NodePin("outExec", "ExecPin", "output", is_exec=True),
                NodePin("element", "AnyPin", "output"),
            ],
            code=code,
            line_start=line_start,
            line_end=line_end,
            color=NODE_COLORS['data'],
            properties={
                "varName": target_str,
                "sourceCode": code,
                "array_name": array_name,
            },
        )
        
        all_deps = [array_name] + index_deps
        self._register_node(visual_node, input_vars=all_deps, output_vars=targets)
        
        # Track variable type
        for t in targets:
            self.variables[t] = "any"
    
    def _convert_call_assignment(self, node, targets, target_str, line_start, line_end, code):
        """Handle assignment from function call: length = len(arr)"""
        value = node.value
        func_name = self._get_name(value.func)
        args_str = ", ".join(self._get_value_str(arg) for arg in value.args)
        
        # Collect dependencies from arguments
        all_deps = []
        for arg in value.args:
            all_deps.extend(self._extract_dependencies(arg))
        
        # Special handling for len() - use CODE_LEN
        if func_name == "len" and value.args:
            arg_str = self._get_value_str(value.args[0])
            
            visual_node = VisualNode(
                name=f"{target_str} = len({arg_str[:15]})",
                node_type=PyFlowNodeType.CODE_LEN,
                category="CodeVisualization",
                description=f"Get length of {arg_str} → {target_str}",
                inputs=[
                    NodePin("collection", "AnyPin", "input"),
                ],
                outputs=[
                    NodePin("length", "IntPin", "output"),
                ],
                code=code,
                line_start=line_start,
                line_end=line_end,
                color=NODE_COLORS['function'],
            )
            
            self._register_node(visual_node, input_vars=all_deps, output_vars=targets)
            
            for t in targets:
                self.variables[t] = "int"
            return
        
        # Create input pins for each argument
        input_pins = [NodePin("inExec", "ExecPin", "input", is_exec=True)]
        for i, arg in enumerate(value.args):
            arg_name = self._get_value_str(arg)[:15] if isinstance(arg, ast.Name) else f"arg{i}"
            input_pins.append(NodePin(arg_name, "AnyPin", "input"))
        
        visual_node = VisualNode(
            name=f"{target_str} = {func_name}({args_str[:15]})",
            node_type=PyFlowNodeType.PYTHON_NODE,
            category="Functions",
            description=f"Call {func_name}({args_str}) → {target_str}",
            inputs=input_pins,
            outputs=[
                NodePin("outExec", "ExecPin", "output", is_exec=True),
                NodePin(target_str, "AnyPin", "output"),
            ],
            code=code,
            line_start=line_start,
            line_end=line_end,
            color=NODE_COLORS['function'],
            properties={"func_name": func_name},
        )
        
        self._register_node(visual_node, input_vars=all_deps, output_vars=targets)
        
        # Track variable type
        for t in targets:
            self.variables[t] = "any"
    
    def _convert_comparison_assignment(self, node, targets, target_str, line_start, line_end, code):
        """Handle assignment from comparison: is_bigger = a > b"""
        value = node.value
        left_str = self._get_value_str(value.left)
        op_map = {
            ast.Gt: ">", ast.Lt: "<", ast.GtE: ">=", ast.LtE: "<=",
            ast.Eq: "==", ast.NotEq: "!=", ast.Is: "is", ast.IsNot: "is not",
            ast.In: "in", ast.NotIn: "not in"
        }
        ops_str = " ".join(op_map.get(type(op), "?") for op in value.ops)
        comparators_str = " ".join(self._get_value_str(c) for c in value.comparators)
        
        all_deps = self._extract_dependencies(value)
        
        visual_node = VisualNode(
            name=f"{target_str} = {left_str[:8]} {ops_str} {comparators_str[:8]}",
            node_type=PyFlowNodeType.PYTHON_NODE,
            category="Comparison",
            description=f"Compare: {left_str} {ops_str} {comparators_str}",
            inputs=[
                NodePin("inExec", "ExecPin", "input", is_exec=True),
                NodePin("a", "AnyPin", "input"),
                NodePin("b", "AnyPin", "input"),
            ],
            outputs=[
                NodePin("outExec", "ExecPin", "output", is_exec=True),
                NodePin(target_str, "BoolPin", "output"),
            ],
            code=code,
            line_start=line_start,
            line_end=line_end,
            color=NODE_COLORS['math'],
            properties={"is_comparison": True},
        )
        
        self._register_node(visual_node, input_vars=all_deps, output_vars=targets)
        
        for t in targets:
            self.variables[t] = "bool"
    
    def _convert_binop_assignment(self, node, targets, target_str, line_start, line_end, code):
        """Handle assignment from binary operation: result = a + b using codeBinaryOp node."""
        value = node.value
        left_str = self._get_value_str(value.left)
        right_str = self._get_value_str(value.right)
        op_map = {
            ast.Add: "+", ast.Sub: "-", ast.Mult: "*", ast.Div: "/",
            ast.Mod: "%", ast.Pow: "**", ast.FloorDiv: "//",
        }
        op_str = op_map.get(type(value.op), "?")
        
        all_deps = self._extract_dependencies(value)
        
        visual_node = VisualNode(
            name=f"{target_str} = {left_str[:8]} {op_str} {right_str[:8]}",
            node_type=PyFlowNodeType.CODE_BINARY_OP,
            category="CodeVisualization",
            description=f"Calculate: {left_str} {op_str} {right_str}",
            inputs=[
                NodePin("a", "AnyPin", "input"),
                NodePin("b", "AnyPin", "input"),
            ],
            outputs=[
                NodePin("result", "AnyPin", "output"),
            ],
            code=code,
            line_start=line_start,
            line_end=line_end,
            color=NODE_COLORS['math'],
            properties={
                "operator": op_str,
                "varName": target_str,
            },
        )
        
        self._register_node(visual_node, input_vars=all_deps, output_vars=targets)
        
        for t in targets:
            self.variables[t] = "any"
    
    def _convert_simple_assignment(self, node, targets, target_str, line_start, line_end, code):
        """Handle simple assignment: x = 10, arr = [1,2,3], y = x"""
        value = node.value
        value_type, value_str = self._analyze_value(value)
        
        # Track variable types
        for t in targets:
            self.variables[t] = value_type
        
        # Extract dependencies from the value expression
        value_deps = self._extract_dependencies(value)
        pin_type = self._type_to_pin(value_type)
        
        # Create node based on value type - USE CUSTOM CODE NODES
        if value_type == "list" and isinstance(value, ast.List):
            # Use CODE_ARRAY for array literals
            import json
            elements = [self._get_value_str(e) for e in value.elts]
            elts_preview = ", ".join(elements[:3])
            if len(elements) > 3:
                elts_preview += ", ..."
            
            visual_node = VisualNode(
                name=f"{target_str} = [{elts_preview}]",
                node_type=PyFlowNodeType.CODE_ARRAY,
                category="CodeVisualization",
                description=f"Create array {target_str} with {len(elements)} elements",
                inputs=[
                    NodePin("inExec", "ExecPin", "input", is_exec=True),
                ],
                outputs=[
                    NodePin("outExec", "ExecPin", "output", is_exec=True),
                    NodePin("array", "AnyPin", "output"),
                ],
                code=code,
                line_start=line_start,
                line_end=line_end,
                color=NODE_COLORS['variables'],
                properties={
                    "varName": target_str,
                    "elements": json.dumps(elements),  # Store as JSON
                    "sourceCode": code,
                }
            )
            # Array creation has no input vars (literals), outputs the array variable
            self._register_node(visual_node, input_vars=[], output_vars=targets)
            
        else:
            # Use CODE_ASSIGN for all other assignments
            if value_type == "int" and isinstance(value, ast.Constant):
                description = f"Set {target_str} = {value.value}"
                default_value = value.value
            elif value_type == "float" and isinstance(value, ast.Constant):
                description = f"Set {target_str} = {value.value}"
                default_value = value.value
            elif value_type == "str" and isinstance(value, ast.Constant):
                val_preview = str(value.value)[:20]
                description = f'Set {target_str} = "{val_preview}"'
                default_value = value.value
            else:
                description = f"Assign: {target_str} = {value_str[:30]}"
                default_value = None
            
            visual_node = VisualNode(
                name=f"{target_str} = {value_str[:20]}",
                node_type=PyFlowNodeType.CODE_ASSIGN,
                category="CodeVisualization",
                description=description,
                inputs=[
                    NodePin("inExec", "ExecPin", "input", is_exec=True),
                    NodePin("value", pin_type, "input"),
                ],
                outputs=[
                    NodePin("outExec", "ExecPin", "output", is_exec=True),
                    NodePin("result", pin_type, "output"),
                ],
                code=code,
                line_start=line_start,
                line_end=line_end,
                color=NODE_COLORS['variables'],
                properties={
                    "varName": target_str,
                    "sourceCode": code,
                    "valueType": value_type,
                    "defaultValue": default_value,
                }
            )
            # Register: input deps from RHS, output is the target variable(s)
            self._register_node(visual_node, input_vars=value_deps, output_vars=targets)
    
    def _convert_aug_assignment(self, node: ast.AugAssign):
        """Convert augmented assignment (+=, -=, etc.)."""
        line_start = node.lineno
        line_end = node.end_lineno or node.lineno
        code = self._get_source_lines(line_start, line_end)
        
        target = node.target.id if isinstance(node.target, ast.Name) else "var"
        op_map = {
            ast.Add: "+=", ast.Sub: "-=", ast.Mult: "*=", ast.Div: "/=",
            ast.Mod: "%=", ast.Pow: "**=", ast.FloorDiv: "//=",
        }
        op_str = op_map.get(type(node.op), "?=")
        value_str = self._get_value_str(node.value)
        
        visual_node = VisualNode(
            name=f"{target} {op_str} {value_str[:15]}",
            node_type=PyFlowNodeType.PYTHON_NODE,
            category="Math",
            description=f"Update {target} with {op_str}",
            inputs=[
                NodePin("inExec", "ExecPin", "input", is_exec=True),
                NodePin(target, "AnyPin", "input"),
                NodePin("value", "AnyPin", "input"),
            ],
            outputs=[
                NodePin("outExec", "ExecPin", "output", is_exec=True),
                NodePin("result", "AnyPin", "output"),
            ],
            code=code,
            line_start=line_start,
            line_end=line_end,
            color=NODE_COLORS['math'],
        )
        
        # AugAssign depends on target + value, outputs target
        value_deps = self._extract_dependencies(node.value)
        all_deps = [target] + value_deps
        self._register_node(visual_node, input_vars=all_deps, output_vars=[target])
    
    def _convert_call(self, node: ast.Call, line_start: int, line_end: int):
        """Convert function call to appropriate node."""
        code = self._get_source_lines(line_start, line_end)
        
        # Get function name
        func_name = self._get_name(node.func)
        
        # Collect all argument dependencies
        all_arg_deps = []
        for arg in node.args:
            all_arg_deps.extend(self._extract_dependencies(arg))
        
        # Special handling for print - use CODE_PRINT
        if func_name == "print":
            args_str = ", ".join(self._get_value_str(arg) for arg in node.args)
            
            visual_node = VisualNode(
                name=f"print({args_str[:25]})",
                node_type=PyFlowNodeType.CODE_PRINT,
                category="CodeVisualization",
                description=f"Print: {args_str[:50]}",
                inputs=[
                    NodePin("inExec", "ExecPin", "input", is_exec=True),
                    NodePin("entity", "AnyPin", "input"),
                ],
                outputs=[
                    NodePin("outExec", "ExecPin", "output", is_exec=True),
                ],
                code=code,
                line_start=line_start,
                line_end=line_end,
                color=NODE_COLORS['output'],
                properties={
                    "sourceCode": code,
                }
            )
            # print has no output variables
            self._register_node(visual_node, input_vars=all_arg_deps, output_vars=[])
            
        # Special handling for len() - use CODE_LEN
        elif func_name == "len":
            arg_str = self._get_value_str(node.args[0]) if node.args else "?"
            
            visual_node = VisualNode(
                name=f"len({arg_str[:15]})",
                node_type=PyFlowNodeType.CODE_LEN,
                category="CodeVisualization",
                description=f"Get length of {arg_str}",
                inputs=[
                    NodePin("collection", "AnyPin", "input"),
                ],
                outputs=[
                    NodePin("length", "IntPin", "output"),
                ],
                code=code,
                line_start=line_start,
                line_end=line_end,
                color=NODE_COLORS['function'],
            )
            # len() is a pure function - outputs a value
            self._register_node(visual_node, input_vars=all_arg_deps, output_vars=[])
        else:
            # Generic function call
            inputs = [NodePin("inExec", "ExecPin", "input", is_exec=True)]
            for i, arg in enumerate(node.args):
                arg_name = f"arg{i}"
                inputs.append(NodePin(arg_name, "AnyPin", "input"))
            
            visual_node = VisualNode(
                name=f"{func_name}()",
                node_type=PyFlowNodeType.PYTHON_NODE,
                category="Functions",
                description=f"Call function: {func_name}",
                inputs=inputs,
                outputs=[
                    NodePin("outExec", "ExecPin", "output", is_exec=True),
                    NodePin("result", "AnyPin", "output"),
                ],
                code=code,
                line_start=line_start,
                line_end=line_end,
                color=NODE_COLORS['function'],
            )
            # Function call outputs a result
            self._register_node(visual_node, input_vars=all_arg_deps, output_vars=[])
    
    def _convert_return(self, node: ast.Return):
        """Convert return statement."""
        line_start = node.lineno
        line_end = node.end_lineno or node.lineno
        code = self._get_source_lines(line_start, line_end)
        
        value_str = self._get_value_str(node.value) if node.value else "None"
        
        # Get dependencies from return value
        return_deps = self._extract_dependencies(node.value) if node.value else []
        
        visual_node = VisualNode(
            name=f"return {value_str[:20]}",
            node_type=PyFlowNodeType.PYTHON_NODE,
            category="Control Flow",
            description=f"Return: {value_str}",
            inputs=[
                NodePin("inExec", "ExecPin", "input", is_exec=True),
                NodePin("value", "AnyPin", "input"),
            ],
            outputs=[],
            code=code,
            line_start=line_start,
            line_end=line_end,
            color=NODE_COLORS['control_flow'],
        )
        
        self._register_node(visual_node, input_vars=return_deps, output_vars=[])
    
    # ===== Helper Methods =====
    
    # Built-in functions that should not be treated as variable dependencies
    BUILTIN_NAMES = {
        'len', 'range', 'print', 'int', 'float', 'str', 'bool', 'list', 'dict', 'set', 'tuple',
        'abs', 'max', 'min', 'sum', 'sorted', 'reversed', 'enumerate', 'zip', 'map', 'filter',
        'open', 'input', 'type', 'isinstance', 'hasattr', 'getattr', 'setattr', 'delattr',
        'all', 'any', 'round', 'pow', 'divmod', 'ord', 'chr', 'hex', 'bin', 'oct',
        'True', 'False', 'None'
    }
    
    def _extract_dependencies(self, node: ast.AST) -> List[str]:
        """
        Extract variable names that this AST node depends on (reads from).
        
        Recursively walks the AST to find all Name nodes, which represent
        variable references. Filters out built-in function names.
        
        Args:
            node: AST node to analyze
            
        Returns:
            List of variable names this expression depends on
        """
        if node is None:
            return []
        
        deps = []
        
        if isinstance(node, ast.Name):
            # Direct variable reference - filter out builtins
            if node.id not in self.BUILTIN_NAMES:
                deps.append(node.id)
        elif isinstance(node, ast.BinOp):
            # Binary operation: a + b
            deps.extend(self._extract_dependencies(node.left))
            deps.extend(self._extract_dependencies(node.right))
        elif isinstance(node, ast.UnaryOp):
            # Unary operation: -x, not x
            deps.extend(self._extract_dependencies(node.operand))
        elif isinstance(node, ast.Compare):
            # Comparison: a < b < c
            deps.extend(self._extract_dependencies(node.left))
            for comparator in node.comparators:
                deps.extend(self._extract_dependencies(comparator))
        elif isinstance(node, ast.BoolOp):
            # Boolean operation: a and b or c
            for value in node.values:
                deps.extend(self._extract_dependencies(value))
        elif isinstance(node, ast.Call):
            # Function call: func(a, b) - only extract arg dependencies, not func name
            # Skip function name, just get arguments
            for arg in node.args:
                deps.extend(self._extract_dependencies(arg))
            for keyword in node.keywords:
                deps.extend(self._extract_dependencies(keyword.value))
        elif isinstance(node, ast.Subscript):
            # Subscript: arr[i]
            deps.extend(self._extract_dependencies(node.value))
            deps.extend(self._extract_dependencies(node.slice))
        elif isinstance(node, ast.Attribute):
            # Attribute access: obj.attr
            deps.extend(self._extract_dependencies(node.value))
        elif isinstance(node, ast.List):
            # List literal: [a, b, c]
            for elt in node.elts:
                deps.extend(self._extract_dependencies(elt))
        elif isinstance(node, ast.Tuple):
            # Tuple literal: (a, b, c)
            for elt in node.elts:
                deps.extend(self._extract_dependencies(elt))
        elif isinstance(node, ast.Dict):
            # Dict literal: {k: v}
            for key in node.keys:
                if key is not None:
                    deps.extend(self._extract_dependencies(key))
            for value in node.values:
                deps.extend(self._extract_dependencies(value))
        elif isinstance(node, ast.IfExp):
            # Ternary: a if cond else b
            deps.extend(self._extract_dependencies(node.test))
            deps.extend(self._extract_dependencies(node.body))
            deps.extend(self._extract_dependencies(node.orelse))
        elif isinstance(node, ast.ListComp):
            # List comprehension
            deps.extend(self._extract_dependencies(node.elt))
            for generator in node.generators:
                deps.extend(self._extract_dependencies(generator.iter))
        elif isinstance(node, ast.JoinedStr):
            # f-string
            for value in node.values:
                deps.extend(self._extract_dependencies(value))
        elif isinstance(node, ast.FormattedValue):
            # Value inside f-string
            deps.extend(self._extract_dependencies(node.value))
        elif isinstance(node, ast.Slice):
            # Slice: [start:stop:step]
            if node.lower:
                deps.extend(self._extract_dependencies(node.lower))
            if node.upper:
                deps.extend(self._extract_dependencies(node.upper))
            if node.step:
                deps.extend(self._extract_dependencies(node.step))
        
        # Remove duplicates while preserving order
        seen = set()
        unique_deps = []
        for d in deps:
            if d not in seen:
                seen.add(d)
                unique_deps.append(d)
        
        return unique_deps
    
    def _get_source_lines(self, start: int, end: int) -> str:
        """Get source code lines."""
        if start < 1:
            start = 1
        if end > len(self.source_lines):
            end = len(self.source_lines)
        return '\n'.join(self.source_lines[start-1:end])
    
    def _get_value(self, node: ast.AST) -> Any:
        """Extract value from AST node."""
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Num):  # Python 3.7 compat
            return node.n
        elif isinstance(node, ast.Str):  # Python 3.7 compat
            return node.s
        elif isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -self._get_value(node.operand)
        return 0
    
    def _get_value_str(self, node: ast.AST) -> str:
        """Get string representation of a value node."""
        if node is None:
            return "None"
        if isinstance(node, ast.Constant):
            if isinstance(node.value, str):
                return f'"{node.value}"'
            return str(node.value)
        elif isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.BinOp):
            left = self._get_value_str(node.left)
            right = self._get_value_str(node.right)
            op_map = {
                ast.Add: "+", ast.Sub: "-", ast.Mult: "*", ast.Div: "/",
                ast.Mod: "%", ast.Pow: "**", ast.FloorDiv: "//",
            }
            op = op_map.get(type(node.op), "?")
            return f"{left} {op} {right}"
        elif isinstance(node, ast.Call):
            return f"{self._get_name(node.func)}(...)"
        elif isinstance(node, ast.List):
            return f"[{len(node.elts)} items]"
        elif isinstance(node, ast.Dict):
            return f"{{dict: {len(node.keys)} keys}}"
        elif isinstance(node, ast.Subscript):
            return f"{self._get_name(node.value)}[...]"
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Compare):
            return f"{self._get_value_str(node.left)} cmp ..."
        elif isinstance(node, ast.JoinedStr):  # f-string
            return 'f"..."'
        return "expr"
    
    def _get_name(self, node: ast.AST) -> str:
        """Get name from various AST node types."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Subscript):
            return f"{self._get_name(node.value)}[...]"
        return "unknown"
    
    def _analyze_value(self, node: ast.AST) -> Tuple[str, str]:
        """Analyze value node and return (type, string_representation)."""
        if isinstance(node, ast.Constant):
            val = node.value
            if isinstance(val, int):
                return ("int", str(val))
            elif isinstance(val, float):
                return ("float", str(val))
            elif isinstance(val, str):
                return ("str", f'"{val[:30]}"')
            elif isinstance(val, bool):
                return ("bool", str(val))
            elif val is None:
                return ("none", "None")
        elif isinstance(node, ast.List):
            return ("list", f"[{len(node.elts)} items]")
        elif isinstance(node, ast.Dict):
            return ("dict", f"{{dict}}")
        elif isinstance(node, ast.Call):
            return ("any", f"{self._get_name(node.func)}()")
        elif isinstance(node, ast.BinOp):
            return ("any", self._get_value_str(node))
        elif isinstance(node, ast.Name):
            # Variable reference - check if we know the type
            var_type = self.variables.get(node.id, "any")
            return (var_type, node.id)
        
        return ("any", self._get_value_str(node))
    
    def _get_value_or_expr(self, node: ast.AST) -> Tuple[Any, Optional[str]]:
        """
        Get a value from an AST node, or return the expression string if it's complex.
        
        Returns:
            (value, expression_string) - value is the actual value if simple constant,
            expression_string is set if it's a complex expression like len(arr)
        """
        if isinstance(node, ast.Constant):
            return (node.value, None)
        elif isinstance(node, ast.Num):  # Python 3.7 compat
            return (node.n, None)
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            val, expr = self._get_value_or_expr(node.operand)
            if expr is None:
                return (-val, None)
            return (0, f"-{expr}")
        elif isinstance(node, ast.Name):
            # Variable reference
            return (0, node.id)
        elif isinstance(node, ast.Call):
            # Function call like len(arr)
            func_name = self._get_name(node.func)
            args_str = ", ".join(self._get_value_str(arg) for arg in node.args)
            return (0, f"{func_name}({args_str})")
        elif isinstance(node, ast.BinOp):
            # Binary operation
            return (0, self._get_value_str(node))
        elif isinstance(node, ast.Subscript):
            # Array access
            return (0, self._get_value_str(node))
        
        return (0, self._get_value_str(node))
    
    def _create_expression_node(self, expr_node: ast.AST, output_name: str, line_num: int) -> Optional[VisualNode]:
        """
        Create a node for a complex expression like len(arr), arr[i], etc.
        
        Returns the created node or None if not needed.
        """
        if isinstance(expr_node, ast.Constant):
            # Simple constant, no node needed
            return None
        
        if isinstance(expr_node, ast.Call):
            # Function call like len(arr), max(a, b), etc.
            func_name = self._get_name(expr_node.func)
            args_deps = []
            for arg in expr_node.args:
                args_deps.extend(self._extract_dependencies(arg))
            
            args_str = ", ".join(self._get_value_str(arg) for arg in expr_node.args)
            
            visual_node = VisualNode(
                name=f"{func_name}({args_str[:20]})",
                node_type=PyFlowNodeType.PYTHON_NODE,
                category="Functions",
                description=f"Call {func_name}({args_str})",
                inputs=[
                    NodePin("inExec", "ExecPin", "input", is_exec=True),
                ] + [NodePin(f"arg{i}", "AnyPin", "input") for i in range(len(expr_node.args))],
                outputs=[
                    NodePin("outExec", "ExecPin", "output", is_exec=True),
                    NodePin("result", "IntPin" if func_name == "len" else "AnyPin", "output"),
                ],
                code=f"{func_name}({args_str})",
                line_start=line_num,
                line_end=line_num,
                color=NODE_COLORS['function'],
                properties={"func_name": func_name},
            )
            
            self._register_node(visual_node, input_vars=args_deps, output_vars=[output_name])
            return visual_node
        
        elif isinstance(expr_node, ast.Subscript):
            # Array access like arr[i]
            array_name = self._get_name(expr_node.value)
            index_deps = self._extract_dependencies(expr_node.slice)
            index_str = self._get_value_str(expr_node.slice)
            
            visual_node = VisualNode(
                name=f"{array_name}[{index_str[:15]}]",
                node_type=PyFlowNodeType.PYTHON_NODE,
                category="Data",
                description=f"Get element from {array_name} at index {index_str}",
                inputs=[
                    NodePin("inExec", "ExecPin", "input", is_exec=True),
                    NodePin("array", "AnyPin", "input"),
                    NodePin("index", "IntPin", "input"),
                ],
                outputs=[
                    NodePin("outExec", "ExecPin", "output", is_exec=True),
                    NodePin("element", "AnyPin", "output"),
                ],
                code=f"{array_name}[{index_str}]",
                line_start=line_num,
                line_end=line_num,
                color=NODE_COLORS['data'],
                properties={"array_name": array_name, "is_array_access": True},
            )
            
            all_deps = [array_name] + index_deps
            self._register_node(visual_node, input_vars=all_deps, output_vars=[output_name])
            return visual_node
        
        elif isinstance(expr_node, ast.Compare):
            # Comparison like arr[i] > res
            left_str = self._get_value_str(expr_node.left)
            op_map = {
                ast.Gt: ">", ast.Lt: "<", ast.GtE: ">=", ast.LtE: "<=",
                ast.Eq: "==", ast.NotEq: "!=", ast.Is: "is", ast.IsNot: "is not",
                ast.In: "in", ast.NotIn: "not in"
            }
            ops_str = " ".join(op_map.get(type(op), "?") for op in expr_node.ops)
            comparators_str = " ".join(self._get_value_str(c) for c in expr_node.comparators)
            
            all_deps = self._extract_dependencies(expr_node)
            
            visual_node = VisualNode(
                name=f"{left_str[:10]} {ops_str} {comparators_str[:10]}",
                node_type=PyFlowNodeType.PYTHON_NODE,
                category="Comparison",
                description=f"Compare: {left_str} {ops_str} {comparators_str}",
                inputs=[
                    NodePin("a", "AnyPin", "input"),
                    NodePin("b", "AnyPin", "input"),
                ],
                outputs=[
                    NodePin("result", "BoolPin", "output"),
                ],
                code=f"{left_str} {ops_str} {comparators_str}",
                line_start=line_num,
                line_end=line_num,
                color=NODE_COLORS['math'],
                properties={"is_comparison": True},
            )
            
            self._register_node(visual_node, input_vars=all_deps, output_vars=[output_name])
            return visual_node
        
        return None

    def _get_annotation_type(self, annotation: ast.AST) -> str:
        """Convert type annotation to pin type."""
        if isinstance(annotation, ast.Name):
            type_map = {
                'int': 'IntPin',
                'float': 'FloatPin',
                'str': 'StringPin',
                'bool': 'BoolPin',
                'list': 'AnyPin',
                'dict': 'AnyPin',
                'List': 'AnyPin',
                'Dict': 'AnyPin',
                'Any': 'AnyPin',
                'None': 'AnyPin',
            }
            return type_map.get(annotation.id, 'AnyPin')
        elif isinstance(annotation, ast.Constant) and annotation.value is None:
            return 'AnyPin'
        return 'AnyPin'
    
    def _type_to_pin(self, python_type: str) -> str:
        """Convert Python type string to PyFlow pin type."""
        type_map = {
            'int': 'IntPin',
            'float': 'FloatPin',
            'str': 'StringPin',
            'string': 'StringPin',
            'bool': 'BoolPin',
            'list': 'AnyPin',
            'dict': 'AnyPin',
            'any': 'AnyPin',
            'none': 'AnyPin',
        }
        return type_map.get(python_type.lower(), 'AnyPin')


def convert_python_to_nodes(source_code: str) -> List[VisualNode]:
    """
    Convenience function to convert Python code to visual nodes.
    
    Args:
        source_code: Python source code string
        
    Returns:
        List of VisualNode specifications
    """
    converter = RuleBasedConverter()
    return converter.convert(source_code)
