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
Python Code Analyzer - Parses Python code and generates visual node representations.
Includes execution tracing, variable tracking, and error detection.
"""

import ast
import sys
import traceback
import linecache
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum


class NodeType(Enum):
    """Types of visual nodes that can be generated."""
    FUNCTION_DEF = "function_def"
    CLASS_DEF = "class_def"
    VARIABLE_ASSIGN = "variable_assign"
    IF_STATEMENT = "if_statement"
    FOR_LOOP = "for_loop"
    WHILE_LOOP = "while_loop"
    RETURN = "return"
    FUNCTION_CALL = "function_call"
    IMPORT = "import"
    TRY_EXCEPT = "try_except"
    EXPRESSION = "expression"
    COMMENT = "comment"


@dataclass
class CodeBlock:
    """Represents a block of code that will become a visual node."""
    node_type: NodeType
    name: str
    line_start: int
    line_end: int
    code: str
    children: List['CodeBlock'] = field(default_factory=list)
    inputs: List[str] = field(default_factory=list)  # Variable dependencies
    outputs: List[str] = field(default_factory=list)  # Variables created/modified
    parent: Optional['CodeBlock'] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VariableState:
    """Tracks the state of a variable during execution."""
    name: str
    value: Any
    type_name: str
    line_number: int
    scope: str
    timestamp: float = 0.0


@dataclass 
class ExecutionStep:
    """Represents a single step in program execution."""
    line_number: int
    code: str
    variables: Dict[str, VariableState]
    event_type: str  # 'line', 'call', 'return', 'exception'
    function_name: str = ""
    error: Optional[str] = None


class PythonCodeAnalyzer:
    """Analyzes Python code and extracts structure for visualization."""
    
    def __init__(self):
        self.blocks: List[CodeBlock] = []
        self.variables: Dict[str, List[str]] = {}  # variable -> list of lines where used
        self.functions: Dict[str, CodeBlock] = {}
        self.classes: Dict[str, CodeBlock] = {}
        self.imports: List[CodeBlock] = []
        self.errors: List[Tuple[int, str]] = []
        self._source_lines: List[str] = []
        
    def analyze(self, code: str) -> List[CodeBlock]:
        """Parse Python code and extract structure.
        
        Args:
            code: Python source code string
            
        Returns:
            List of CodeBlock objects representing the code structure
        """
        self.blocks = []
        self.variables = {}
        self.functions = {}
        self.classes = {}
        self.imports = []
        self.errors = []
        self._source_lines = code.split('\n')
        
        try:
            tree = ast.parse(code)
            self._analyze_node(tree, None)
        except SyntaxError as e:
            self.errors.append((e.lineno or 1, f"Syntax Error: {e.msg}"))
            
        return self.blocks
    
    def _get_source_segment(self, start_line: int, end_line: int) -> str:
        """Extract source code for given line range."""
        if start_line < 1:
            start_line = 1
        if end_line > len(self._source_lines):
            end_line = len(self._source_lines)
        return '\n'.join(self._source_lines[start_line-1:end_line])
    
    def _analyze_node(self, node: ast.AST, parent: Optional[CodeBlock]) -> Optional[CodeBlock]:
        """Recursively analyze AST nodes."""
        
        if isinstance(node, ast.Module):
            for child in node.body:
                block = self._analyze_node(child, parent)
                if block:
                    self.blocks.append(block)
            return None
            
        elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            block = self._analyze_function(node, parent)
            self.functions[node.name] = block
            return block
            
        elif isinstance(node, ast.ClassDef):
            block = self._analyze_class(node, parent)
            self.classes[node.name] = block
            return block
            
        elif isinstance(node, ast.Assign):
            return self._analyze_assignment(node, parent)
            
        elif isinstance(node, ast.AugAssign):
            return self._analyze_aug_assignment(node, parent)
            
        elif isinstance(node, ast.If):
            return self._analyze_if(node, parent)
            
        elif isinstance(node, ast.For):
            return self._analyze_for(node, parent)
            
        elif isinstance(node, ast.While):
            return self._analyze_while(node, parent)
            
        elif isinstance(node, ast.Return):
            return self._analyze_return(node, parent)
            
        elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            block = self._analyze_import(node, parent)
            self.imports.append(block)
            return block
            
        elif isinstance(node, ast.Try):
            return self._analyze_try(node, parent)
            
        elif isinstance(node, ast.Expr):
            return self._analyze_expression(node, parent)
            
        elif isinstance(node, ast.With):
            return self._analyze_with(node, parent)
            
        return None
    
    def _analyze_function(self, node: ast.FunctionDef, parent: Optional[CodeBlock]) -> CodeBlock:
        """Analyze a function definition."""
        # Get arguments
        args = []
        for arg in node.args.args:
            args.append(arg.arg)
        
        # Get decorators
        decorators = []
        for dec in node.decorator_list:
            if isinstance(dec, ast.Name):
                decorators.append(dec.id)
            elif isinstance(dec, ast.Call) and isinstance(dec.func, ast.Name):
                decorators.append(dec.func.id)
        
        end_line = node.end_lineno or node.lineno
        block = CodeBlock(
            node_type=NodeType.FUNCTION_DEF,
            name=node.name,
            line_start=node.lineno,
            line_end=end_line,
            code=self._get_source_segment(node.lineno, end_line),
            inputs=args,
            outputs=[node.name],  # Function name is "created"
            parent=parent,
            metadata={
                'args': args,
                'decorators': decorators,
                'is_async': isinstance(node, ast.AsyncFunctionDef),
                'docstring': ast.get_docstring(node)
            }
        )
        
        # Analyze function body
        for child in node.body:
            child_block = self._analyze_node(child, block)
            if child_block:
                block.children.append(child_block)
                
        return block
    
    def _analyze_class(self, node: ast.ClassDef, parent: Optional[CodeBlock]) -> CodeBlock:
        """Analyze a class definition."""
        bases = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                bases.append(base.id)
        
        end_line = node.end_lineno or node.lineno
        block = CodeBlock(
            node_type=NodeType.CLASS_DEF,
            name=node.name,
            line_start=node.lineno,
            line_end=end_line,
            code=self._get_source_segment(node.lineno, end_line),
            inputs=bases,  # Base classes are dependencies
            outputs=[node.name],
            parent=parent,
            metadata={
                'bases': bases,
                'docstring': ast.get_docstring(node)
            }
        )
        
        # Analyze class body
        for child in node.body:
            child_block = self._analyze_node(child, block)
            if child_block:
                block.children.append(child_block)
                
        return block
    
    def _analyze_assignment(self, node: ast.Assign, parent: Optional[CodeBlock]) -> CodeBlock:
        """Analyze variable assignment."""
        targets = []
        for target in node.targets:
            targets.extend(self._extract_names(target))
        
        # Find dependencies (variables used on right side)
        dependencies = self._extract_dependencies(node.value)
        
        end_line = node.end_lineno or node.lineno
        block = CodeBlock(
            node_type=NodeType.VARIABLE_ASSIGN,
            name=', '.join(targets),
            line_start=node.lineno,
            line_end=end_line,
            code=self._get_source_segment(node.lineno, end_line),
            inputs=dependencies,
            outputs=targets,
            parent=parent,
            metadata={'targets': targets}
        )
        
        # Track variables
        for var in targets:
            if var not in self.variables:
                self.variables[var] = []
            self.variables[var].append(str(node.lineno))
            
        return block
    
    def _analyze_aug_assignment(self, node: ast.AugAssign, parent: Optional[CodeBlock]) -> CodeBlock:
        """Analyze augmented assignment (+=, -=, etc.)."""
        target = self._extract_names(node.target)[0] if self._extract_names(node.target) else "unknown"
        dependencies = self._extract_dependencies(node.value)
        dependencies.append(target)  # Also depends on itself
        
        end_line = node.end_lineno or node.lineno
        return CodeBlock(
            node_type=NodeType.VARIABLE_ASSIGN,
            name=target,
            line_start=node.lineno,
            line_end=end_line,
            code=self._get_source_segment(node.lineno, end_line),
            inputs=list(set(dependencies)),
            outputs=[target],
            parent=parent,
            metadata={'augmented': True}
        )
    
    def _analyze_if(self, node: ast.If, parent: Optional[CodeBlock]) -> CodeBlock:
        """Analyze if statement."""
        condition_deps = self._extract_dependencies(node.test)
        
        end_line = node.end_lineno or node.lineno
        block = CodeBlock(
            node_type=NodeType.IF_STATEMENT,
            name=f"if (line {node.lineno})",
            line_start=node.lineno,
            line_end=end_line,
            code=self._get_source_segment(node.lineno, end_line),
            inputs=condition_deps,
            outputs=[],
            parent=parent,
            metadata={'has_else': len(node.orelse) > 0}
        )
        
        # Analyze if body
        for child in node.body:
            child_block = self._analyze_node(child, block)
            if child_block:
                block.children.append(child_block)
                block.outputs.extend(child_block.outputs)
        
        # Analyze else body
        for child in node.orelse:
            child_block = self._analyze_node(child, block)
            if child_block:
                block.children.append(child_block)
                block.outputs.extend(child_block.outputs)
                
        block.outputs = list(set(block.outputs))
        return block
    
    def _analyze_for(self, node: ast.For, parent: Optional[CodeBlock]) -> CodeBlock:
        """Analyze for loop."""
        loop_var = self._extract_names(node.target)
        iterable_deps = self._extract_dependencies(node.iter)
        
        end_line = node.end_lineno or node.lineno
        block = CodeBlock(
            node_type=NodeType.FOR_LOOP,
            name=f"for {', '.join(loop_var)} (line {node.lineno})",
            line_start=node.lineno,
            line_end=end_line,
            code=self._get_source_segment(node.lineno, end_line),
            inputs=iterable_deps,
            outputs=loop_var,
            parent=parent,
            metadata={'loop_var': loop_var}
        )
        
        for child in node.body:
            child_block = self._analyze_node(child, block)
            if child_block:
                block.children.append(child_block)
                block.outputs.extend(child_block.outputs)
                
        block.outputs = list(set(block.outputs))
        return block
    
    def _analyze_while(self, node: ast.While, parent: Optional[CodeBlock]) -> CodeBlock:
        """Analyze while loop."""
        condition_deps = self._extract_dependencies(node.test)
        
        end_line = node.end_lineno or node.lineno
        block = CodeBlock(
            node_type=NodeType.WHILE_LOOP,
            name=f"while (line {node.lineno})",
            line_start=node.lineno,
            line_end=end_line,
            code=self._get_source_segment(node.lineno, end_line),
            inputs=condition_deps,
            outputs=[],
            parent=parent,
            metadata={}
        )
        
        for child in node.body:
            child_block = self._analyze_node(child, block)
            if child_block:
                block.children.append(child_block)
                block.outputs.extend(child_block.outputs)
                
        block.outputs = list(set(block.outputs))
        return block
    
    def _analyze_return(self, node: ast.Return, parent: Optional[CodeBlock]) -> CodeBlock:
        """Analyze return statement."""
        deps = self._extract_dependencies(node.value) if node.value else []
        
        end_line = node.end_lineno or node.lineno
        return CodeBlock(
            node_type=NodeType.RETURN,
            name=f"return (line {node.lineno})",
            line_start=node.lineno,
            line_end=end_line,
            code=self._get_source_segment(node.lineno, end_line),
            inputs=deps,
            outputs=[],
            parent=parent,
            metadata={}
        )
    
    def _analyze_import(self, node, parent: Optional[CodeBlock]) -> CodeBlock:
        """Analyze import statement."""
        imports = []
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.asname or alias.name)
        else:  # ImportFrom
            module = node.module or ""
            for alias in node.names:
                imports.append(alias.asname or alias.name)
        
        end_line = node.end_lineno or node.lineno
        return CodeBlock(
            node_type=NodeType.IMPORT,
            name=f"import (line {node.lineno})",
            line_start=node.lineno,
            line_end=end_line,
            code=self._get_source_segment(node.lineno, end_line),
            inputs=[],
            outputs=imports,
            parent=parent,
            metadata={'imports': imports}
        )
    
    def _analyze_try(self, node: ast.Try, parent: Optional[CodeBlock]) -> CodeBlock:
        """Analyze try-except block."""
        end_line = node.end_lineno or node.lineno
        block = CodeBlock(
            node_type=NodeType.TRY_EXCEPT,
            name=f"try-except (line {node.lineno})",
            line_start=node.lineno,
            line_end=end_line,
            code=self._get_source_segment(node.lineno, end_line),
            inputs=[],
            outputs=[],
            parent=parent,
            metadata={'num_handlers': len(node.handlers)}
        )
        
        for child in node.body:
            child_block = self._analyze_node(child, block)
            if child_block:
                block.children.append(child_block)
                
        return block
    
    def _analyze_expression(self, node: ast.Expr, parent: Optional[CodeBlock]) -> CodeBlock:
        """Analyze expression (usually function calls)."""
        deps = self._extract_dependencies(node.value)
        
        name = "expression"
        if isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Name):
                name = f"call {node.value.func.id}()"
            elif isinstance(node.value.func, ast.Attribute):
                name = f"call .{node.value.func.attr}()"
        
        end_line = node.end_lineno or node.lineno
        return CodeBlock(
            node_type=NodeType.EXPRESSION,
            name=name,
            line_start=node.lineno,
            line_end=end_line,
            code=self._get_source_segment(node.lineno, end_line),
            inputs=deps,
            outputs=[],
            parent=parent,
            metadata={}
        )
    
    def _analyze_with(self, node: ast.With, parent: Optional[CodeBlock]) -> CodeBlock:
        """Analyze with statement."""
        deps = []
        outputs = []
        for item in node.items:
            deps.extend(self._extract_dependencies(item.context_expr))
            if item.optional_vars:
                outputs.extend(self._extract_names(item.optional_vars))
        
        end_line = node.end_lineno or node.lineno
        block = CodeBlock(
            node_type=NodeType.EXPRESSION,
            name=f"with (line {node.lineno})",
            line_start=node.lineno,
            line_end=end_line,
            code=self._get_source_segment(node.lineno, end_line),
            inputs=deps,
            outputs=outputs,
            parent=parent,
            metadata={'is_with': True}
        )
        
        for child in node.body:
            child_block = self._analyze_node(child, block)
            if child_block:
                block.children.append(child_block)
                
        return block
    
    def _extract_names(self, node) -> List[str]:
        """Extract variable names from an AST node."""
        names = []
        if isinstance(node, ast.Name):
            names.append(node.id)
        elif isinstance(node, ast.Tuple) or isinstance(node, ast.List):
            for elt in node.elts:
                names.extend(self._extract_names(elt))
        elif isinstance(node, ast.Starred):
            names.extend(self._extract_names(node.value))
        return names
    
    def _extract_dependencies(self, node) -> List[str]:
        """Extract variable dependencies from an AST node."""
        deps = []
        if node is None:
            return deps
            
        for child in ast.walk(node):
            if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load):
                deps.append(child.id)
                
        # Filter out built-ins
        builtins = set(dir(__builtins__)) if isinstance(__builtins__, dict) else set(dir(__builtins__))
        deps = [d for d in deps if d not in builtins]
        
        return list(set(deps))
    
    def get_variable_flow(self) -> Dict[str, List[str]]:
        """Get the flow of variables through the code."""
        return self.variables
    
    def get_dependency_graph(self) -> Dict[str, List[str]]:
        """Get dependency graph showing which blocks depend on which variables."""
        graph = {}
        for block in self.blocks:
            graph[f"{block.name}@{block.line_start}"] = {
                'inputs': block.inputs,
                'outputs': block.outputs,
                'type': block.node_type.value
            }
        return graph


class PythonExecutionTracer:
    """Traces Python code execution and records variable states."""
    
    def __init__(self):
        self.execution_history: List[ExecutionStep] = []
        self.current_variables: Dict[str, VariableState] = {}
        self.errors: List[ExecutionStep] = []
        self._source_code: str = ""
        self._source_lines: List[str] = []
        self._tracing = False
        
    def trace(self, code: str, globals_dict: Optional[Dict] = None) -> List[ExecutionStep]:
        """Execute code with tracing enabled.
        
        Args:
            code: Python source code to execute
            globals_dict: Optional globals dictionary
            
        Returns:
            List of ExecutionStep objects recording the execution
        """
        self.execution_history = []
        self.current_variables = {}
        self.errors = []
        self._source_code = code
        self._source_lines = code.split('\n')
        
        if globals_dict is None:
            globals_dict = {'__name__': '__main__', '__builtins__': __builtins__}
        
        locals_dict = {}
        
        # Set up tracing
        self._tracing = True
        old_trace = sys.gettrace()
        
        try:
            sys.settrace(self._trace_callback)
            exec(compile(code, '<traced_code>', 'exec'), globals_dict, locals_dict)
        except Exception as e:
            # Record the error
            tb = traceback.extract_tb(sys.exc_info()[2])
            if tb:
                last_frame = tb[-1]
                error_step = ExecutionStep(
                    line_number=last_frame.lineno,
                    code=self._get_line(last_frame.lineno),
                    variables=dict(self.current_variables),
                    event_type='exception',
                    function_name=last_frame.name,
                    error=f"{type(e).__name__}: {str(e)}"
                )
                self.execution_history.append(error_step)
                self.errors.append(error_step)
        finally:
            sys.settrace(old_trace)
            self._tracing = False
            
        return self.execution_history
    
    def _get_line(self, lineno: int) -> str:
        """Get source line by number."""
        if 1 <= lineno <= len(self._source_lines):
            return self._source_lines[lineno - 1]
        return ""
    
    def _trace_callback(self, frame, event, arg):
        """Trace callback for sys.settrace."""
        if not self._tracing:
            return None
            
        # Only trace our code, not imported modules
        if frame.f_code.co_filename != '<traced_code>':
            return self._trace_callback
            
        import time
        
        # Record current state
        if event in ('line', 'call', 'return', 'exception'):
            # Update variable states
            for name, value in frame.f_locals.items():
                if not name.startswith('_'):
                    try:
                        self.current_variables[name] = VariableState(
                            name=name,
                            value=repr(value)[:100],  # Limit value length
                            type_name=type(value).__name__,
                            line_number=frame.f_lineno,
                            scope=frame.f_code.co_name,
                            timestamp=time.time()
                        )
                    except:
                        pass
            
            step = ExecutionStep(
                line_number=frame.f_lineno,
                code=self._get_line(frame.f_lineno),
                variables=dict(self.current_variables),
                event_type=event,
                function_name=frame.f_code.co_name,
                error=str(arg) if event == 'exception' else None
            )
            self.execution_history.append(step)
            
            if event == 'exception':
                self.errors.append(step)
        
        return self._trace_callback
    
    def get_variable_history(self, variable_name: str) -> List[VariableState]:
        """Get the history of a specific variable."""
        history = []
        for step in self.execution_history:
            if variable_name in step.variables:
                history.append(step.variables[variable_name])
        return history
    
    def get_errors(self) -> List[ExecutionStep]:
        """Get all errors that occurred during execution."""
        return self.errors
    
    def get_execution_path(self) -> List[int]:
        """Get the sequence of line numbers executed."""
        return [step.line_number for step in self.execution_history if step.event_type == 'line']
    
    def get_enhanced_events(self) -> List[Dict[str, Any]]:
        """Get structured events suitable for LLM consumption.
        
        Returns list of events with:
        - event_type: 'assignment', 'call', 'loop_enter', 'loop_iteration', 'branch', 'return'
        - line: source line number
        - code: source code at line
        - data: event-specific data (variable values, function args, loop index, etc.)
        """
        events = []
        loop_stack = []  # Track nested loop iterations
        prev_step = None
        
        for step in self.execution_history:
            code = step.code.strip()
            event = {
                'line': step.line_number,
                'code': code,
                'function': step.function_name,
                'event_type': step.event_type,
                'variables': {}
            }
            
            # Capture variable values at this step
            for name, var_state in step.variables.items():
                event['variables'][name] = {
                    'value': var_state.value,
                    'type': var_state.type_name
                }
            
            # Classify the event more specifically
            if step.event_type == 'line':
                if '=' in code and not code.startswith('if') and not code.startswith('while') and not code.startswith('for'):
                    if '+=' in code or '-=' in code or '*=' in code or '/=' in code:
                        event['event_type'] = 'augmented_assignment'
                    elif '==' not in code and '!=' not in code and '<=' not in code and '>=' not in code:
                        event['event_type'] = 'assignment'
                elif code.startswith('for '):
                    if 'for' in [e.get('event_type') for e in events[-3:] if e.get('line') == step.line_number]:
                        event['event_type'] = 'loop_iteration'
                        # Find loop variable value
                        for name in step.variables:
                            if name not in [v for v in (prev_step.variables if prev_step else {})]:
                                event['loop_variable'] = name
                                event['loop_value'] = step.variables[name].value
                    else:
                        event['event_type'] = 'loop_enter'
                elif code.startswith('while '):
                    event['event_type'] = 'loop_condition'
                elif code.startswith('if ') or code.startswith('elif '):
                    event['event_type'] = 'branch'
                elif code.startswith('return'):
                    event['event_type'] = 'return'
                elif '(' in code and ')' in code and not code.startswith('def '):
                    event['event_type'] = 'call'
                elif code.startswith('print('):
                    event['event_type'] = 'output'
            
            events.append(event)
            prev_step = step
            
        return events
    
    def build_dependency_graph(self) -> Dict[str, Any]:
        """Build a dependency graph from execution history.
        
        Returns a dict containing:
        - nodes: List of variable/expression nodes with values
        - edges: List of dependency edges (source -> target)
        - execution_order: Order variables were assigned/modified
        """
        graph = {
            'nodes': {},  # name -> {type, first_value, last_value, lines}
            'edges': [],  # (source, target, edge_type)
            'execution_order': [],
            'loops': [],  # loop iteration data
            'branches': []  # branch condition data
        }
        
        assigned_vars = set()
        
        for step in self.execution_history:
            code = step.code.strip()
            
            # Track variable assignments
            if step.event_type == 'line':
                # Simple assignment: var = expr
                if '=' in code and not code.startswith(('if', 'while', 'for', 'def', 'class')):
                    if '==' not in code and '!=' not in code and '<=' not in code and '>=' not in code:
                        parts = code.split('=', 1)
                        if len(parts) == 2:
                            target = parts[0].strip()
                            expr = parts[1].strip()
                            
                            # Handle augmented assignment
                            for op in ['+=', '-=', '*=', '/=', '//=', '%=', '**=']:
                                if op in code:
                                    target = code.split(op)[0].strip()
                                    break
                            
                            # Add target node
                            target_name = target.split('[')[0]  # Handle arr[i] = x
                            if target_name not in graph['nodes']:
                                graph['nodes'][target_name] = {
                                    'type': 'variable',
                                    'first_value': None,
                                    'last_value': None,
                                    'lines': []
                                }
                            
                            # Get current value
                            if target_name in step.variables:
                                val = step.variables[target_name].value
                                if graph['nodes'][target_name]['first_value'] is None:
                                    graph['nodes'][target_name]['first_value'] = val
                                graph['nodes'][target_name]['last_value'] = val
                                graph['nodes'][target_name]['type'] = step.variables[target_name].type_name
                            
                            graph['nodes'][target_name]['lines'].append(step.line_number)
                            
                            if target_name not in assigned_vars:
                                graph['execution_order'].append(target_name)
                                assigned_vars.add(target_name)
                            
                            # Add dependency edges
                            for var_name in step.variables:
                                if var_name in expr and var_name != target_name:
                                    edge = (var_name, target_name, 'data_dependency')
                                    if edge not in graph['edges']:
                                        graph['edges'].append(edge)
                
                # Track loops
                if code.startswith('for '):
                    # Extract loop variable and iterable
                    import re
                    match = re.match(r'for\s+(\w+)\s+in\s+(.+):', code)
                    if match:
                        loop_var = match.group(1)
                        iterable = match.group(2)
                        graph['loops'].append({
                            'line': step.line_number,
                            'variable': loop_var,
                            'iterable': iterable,
                            'type': 'for'
                        })
                
                # Track branches
                if code.startswith('if ') or code.startswith('elif '):
                    condition = code[3:].rstrip(':').strip() if code.startswith('if ') else code[5:].rstrip(':').strip()
                    graph['branches'].append({
                        'line': step.line_number,
                        'condition': condition
                    })
        
        return graph


@dataclass
class EnhancedCodeContext:
    """Complete context for LLM-based node generation."""
    source_code: str
    ast_info: List[CodeBlock]
    execution_events: List[Dict[str, Any]]
    dependency_graph: Dict[str, Any]
    final_variable_values: Dict[str, Any]


class CodeToNodesConverter:
    """Main pipeline: Parse → Trace → Collect → Dependency Graph → LLM → Nodes"""
    
    def __init__(self):
        self.analyzer = PythonCodeAnalyzer()
        self.tracer = PythonExecutionTracer()
        self._ollama_client = None
    
    @property
    def ollama_client(self):
        """Lazy load OllamaClient to avoid circular imports."""
        if self._ollama_client is None:
            try:
                from PyFlow.Core.OllamaIntegration import OllamaClient
                self._ollama_client = OllamaClient()
            except ImportError:
                self._ollama_client = None
        return self._ollama_client
    
    def analyze_code(self, code: str) -> EnhancedCodeContext:
        """Step 1-4: Parse, trace, collect events, build dependency graph."""
        # Step 1: Parse AST
        ast_blocks = self.analyzer.analyze(code)
        
        # Step 2-3: Run with tracer and collect events
        try:
            self.tracer.trace(code)
            events = self.tracer.get_enhanced_events()
        except Exception as e:
            events = []  # Code may have errors, continue with AST only
        
        # Step 4: Build dependency graph
        dep_graph = self.tracer.build_dependency_graph() if events else {'nodes': {}, 'edges': [], 'execution_order': [], 'loops': [], 'branches': []}
        
        # Get final values
        final_values = {}
        for name, var_state in self.tracer.current_variables.items():
            final_values[name] = {
                'value': var_state.value,
                'type': var_state.type_name
            }
        
        return EnhancedCodeContext(
            source_code=code,
            ast_info=ast_blocks,
            execution_events=events,
            dependency_graph=dep_graph,
            final_variable_values=final_values
        )
    
    def create_llm_prompt(self, context: EnhancedCodeContext) -> str:
        """Create a detailed prompt for LLM with all context."""
        prompt_parts = []
        
        # Source code
        prompt_parts.append("=== PYTHON SOURCE CODE ===")
        prompt_parts.append(context.source_code)
        
        # AST structure
        prompt_parts.append("\n=== AST STRUCTURE ===")
        for block in context.ast_info:
            prompt_parts.append(f"- {block.node_type.value}: '{block.name}' (lines {block.line_start}-{block.line_end})")
            prompt_parts.append(f"  Inputs: {block.inputs}")
            prompt_parts.append(f"  Outputs: {block.outputs}")
        
        # Dependency graph
        prompt_parts.append("\n=== DATA DEPENDENCIES ===")
        dep = context.dependency_graph
        prompt_parts.append(f"Variables created: {list(dep['nodes'].keys())}")
        prompt_parts.append(f"Execution order: {dep['execution_order']}")
        for edge in dep['edges']:
            prompt_parts.append(f"  {edge[0]} → {edge[1]} ({edge[2]})")
        
        # Loops and branches
        if dep['loops']:
            prompt_parts.append(f"Loops: {dep['loops']}")
        if dep['branches']:
            prompt_parts.append(f"Branches: {dep['branches']}")
        
        # Runtime values (key insight!)
        prompt_parts.append("\n=== RUNTIME VALUES (from execution trace) ===")
        for name, info in context.final_variable_values.items():
            prompt_parts.append(f"  {name}: {info['value']} (type: {info['type']})")
        
        # Key execution events
        prompt_parts.append("\n=== KEY EXECUTION EVENTS ===")
        for event in context.execution_events[:20]:  # Limit to avoid token overflow
            if event['event_type'] in ['assignment', 'loop_enter', 'branch', 'call', 'return']:
                prompt_parts.append(f"  Line {event['line']}: {event['event_type']} - {event['code'][:50]}")
        
        return "\n".join(prompt_parts)
    
    def generate_nodes_with_llm(self, code: str, use_fallback: bool = True) -> List[Dict[str, Any]]:
        """Step 5: Generate nodes using LLM with fallback to rule-based.
        
        Args:
            code: Python source code
            use_fallback: If True, fall back to RuleBasedConverter on LLM failure
            
        Returns:
            List of node specifications
        """
        # Gather context
        context = self.analyze_code(code)
        
        # Try LLM first
        if self.ollama_client and self.ollama_client.is_available():
            try:
                # Create enhanced prompt with runtime context
                llm_prompt = self.create_llm_prompt(context)
                
                # Prepend additional context to the code being analyzed
                enhanced_code = f"""# CONTEXT FROM EXECUTION TRACE:
# {llm_prompt.replace(chr(10), chr(10) + '# ')}

{code}"""
                
                # Use analyze_code_for_nodes which returns JSON string
                response = self.ollama_client.analyze_code_for_nodes(code)
                
                if response:
                    # Parse JSON from response
                    import json
                    import re
                    
                    # Extract JSON array from response (may have markdown)
                    json_match = re.search(r'\[[\s\S]*\]', response)
                    if json_match:
                        nodes_json = json.loads(json_match.group())
                        return [{
                            'type': node.get('name', ''),
                            'name': node.get('name', ''),
                            'category': node.get('category', 'General'),
                            'inputs': node.get('inputs', []),
                            'outputs': node.get('outputs', []),
                            'description': node.get('description', ''),
                            'position': None
                        } for node in nodes_json]
            except Exception as e:
                print(f"LLM generation failed: {e}")
        
        # Fallback to rule-based
        if use_fallback:
            try:
                from PyFlow.Core.RuleBasedConverter import RuleBasedConverter
                converter = RuleBasedConverter()
                converter.convert(code)
                return converter.nodes
            except Exception as e:
                print(f"Rule-based fallback also failed: {e}")
                return []
        
        return []
    
    def generate_nodes_with_layout(self, code: str) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Generate nodes with automatic layout based on dependencies.
        
        Returns:
            Tuple of (nodes, connections)
        """
        context = self.analyze_code(code)
        nodes = self.generate_nodes_with_llm(code)
        
        if not nodes:
            return [], []
        
        # Calculate positions based on dependency graph
        dep_graph = context.dependency_graph
        
        # Simple left-to-right layout based on execution order
        node_positions = {}
        x_spacing = 250
        y_spacing = 150
        
        # Map variable names to nodes
        var_to_node = {}
        for i, node in enumerate(nodes):
            for output in node.get('outputs', []):
                var_to_node[output.get('name', '')] = i
        
        # Calculate levels (topological sort based on dependencies)
        levels = {}
        for i, var_name in enumerate(dep_graph['execution_order']):
            levels[var_name] = i
        
        # Assign positions
        y_offset = {}  # Track y position per level
        for i, node in enumerate(nodes):
            # Find the level based on inputs
            max_input_level = -1
            for inp in node.get('inputs', []):
                if inp.get('name', '') in levels:
                    max_input_level = max(max_input_level, levels[inp['name']])
            
            level = max_input_level + 1
            
            if level not in y_offset:
                y_offset[level] = 0
            
            node['position'] = {
                'x': level * x_spacing,
                'y': y_offset[level] * y_spacing
            }
            y_offset[level] += 1
        
        # Generate connections from dependency graph
        connections = []
        for source, target, _ in dep_graph['edges']:
            source_node_idx = var_to_node.get(source)
            target_node_idx = var_to_node.get(target)
            if source_node_idx is not None and target_node_idx is not None:
                connections.append({
                    'from_node': source_node_idx,
                    'from_pin': source,
                    'to_node': target_node_idx,
                    'to_pin': target
                })
        
        return nodes, connections
