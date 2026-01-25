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
Ollama Integration for PyFlow - Uses local LLM for intelligent code analysis
and visual node generation.
"""

import requests
import json
import ast
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class TypedVariable:
    """Variable with inferred type information."""
    name: str
    inferred_type: str
    default_value: Optional[str] = None
    description: str = ""


@dataclass
class TypedPin:
    """Represents a typed input/output pin for visual nodes."""
    name: str
    data_type: str  # int, float, str, bool, list, dict, Any, custom types
    direction: str  # 'input' or 'output'
    default_value: Optional[Any] = None
    description: str = ""
    is_exec: bool = False  # True for execution pins


@dataclass
class VisualNodeSpec:
    """Specification for generating a visual node."""
    name: str
    category: str
    description: str
    inputs: List[TypedPin] = field(default_factory=list)
    outputs: List[TypedPin] = field(default_factory=list)
    code: str = ""
    line_start: int = 0
    line_end: int = 0
    node_color: Tuple[int, int, int] = (70, 130, 180)


class OllamaClient:
    """Client for interacting with local Ollama API."""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.2"):
        self.base_url = base_url
        self.model = model
        self._is_available = None
        
    def is_available(self) -> bool:
        """Check if Ollama is running and accessible."""
        if self._is_available is not None:
            return self._is_available
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            self._is_available = response.status_code == 200
            return self._is_available
        except:
            self._is_available = False
            return False
            
    def get_available_models(self) -> List[str]:
        """Get list of available models."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [m['name'] for m in data.get('models', [])]
        except:
            pass
        return []
        
    def generate(self, prompt: str, system_prompt: str = None) -> str:
        """Generate a response from Ollama."""
        if not self.is_available():
            return ""
            
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,  # Lower temperature for more deterministic output
                    "num_predict": 2000
                }
            }
            
            if system_prompt:
                payload["system"] = system_prompt
                
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=180  # Increased to 3 minutes for complex code analysis
            )
            
            if response.status_code == 200:
                return response.json().get('response', '')
        except Exception as e:
            print(f"Ollama error: {e}")
            
        return ""
    
    def analyze_code_for_nodes(self, code: str) -> str:
        """Ask Ollama to analyze Python code and suggest visual node structure."""
        system_prompt = """You are an expert code analyzer for PyFlow, a visual node-based programming framework.
Your task is to analyze Python code and generate precise JSON specifications for visual nodes that will be rendered on a canvas.

## YOUR ROLE:
You are converting Python code into VISUAL PROGRAMMING NODES. Each node represents a discrete operation with:
- INPUT PINS: Data flowing INTO the node (left side)
- OUTPUT PINS: Data flowing OUT of the node (right side)
- EXECUTION PINS: Control flow (exec_in, exec_out) for sequencing operations

## NODE CATEGORIES (use EXACTLY these names):
- "Functions" - User-defined functions
- "Classes" - Class definitions
- "Variables" - Variable assignments (use prefix "Set " for assignments, "Get " for reads)
- "Control Flow" - if, for, while, try/except, match
- "Math" - Arithmetic operations (+, -, *, /, %, **)
- "Comparison" - ==, !=, <, >, <=, >=, in, is
- "Logic" - and, or, not, boolean operations
- "String" - String operations and methods
- "List" - List operations (append, extend, slice, etc.)
- "Dict" - Dictionary operations
- "IO" - print, input, file operations
- "Imports" - import statements
- "Calls" - Function/method calls

## PIN TYPE MAPPING (use EXACTLY these PyFlow types):
- Python int -> "IntPin"
- Python float -> "FloatPin"  
- Python str -> "StringPin"
- Python bool -> "BoolPin"
- Python list -> "ListPin"
- Python dict -> "DictPin"
- Python None -> "AnyPin"
- Unknown/generic -> "AnyPin"
- Execution flow -> "ExecPin" (set is_exec: true)

## CRITICAL RULES FOR NODE GENERATION:

1. **EXECUTION FLOW**: Every node that DOES something (not just computes) needs:
   - exec_in (input, is_exec: true) - When to run this node
   - exec_out (output, is_exec: true) - Continue to next node
   
2. **DATA FLOW**: Pure computation nodes (math, comparisons) don't need exec pins

3. **NAMING CONVENTIONS**:
   - Functions: Use the function name as-is
   - Variables: "Set varname" for assignment, "Get varname" for reading
   - Loops: "For Loop", "While Loop" 
   - Conditionals: "Branch" or "If"
   - Calls: "Call functionname"

4. **INPUT DETECTION**:
   - Function parameters become input pins
   - Variables READ in expressions become input pins
   - Loop iterables become input pins
   - Condition expressions become input pins

5. **OUTPUT DETECTION**:
   - Function return values become output pins
   - Assigned variables become output pins
   - Loop variables (for x in...) become output pins
   - Branches get "True" and "False" exec outputs

## JSON OUTPUT FORMAT (strict schema):
```json
[
  {
    "name": "NodeName",
    "category": "Category",
    "description": "What this node does in one sentence",
    "inputs": [
      {"name": "exec_in", "type": "ExecPin", "is_exec": true, "description": "Execute"},
      {"name": "paramName", "type": "IntPin", "description": "Parameter description"}
    ],
    "outputs": [
      {"name": "exec_out", "type": "ExecPin", "is_exec": true, "description": "Continue"},
      {"name": "result", "type": "FloatPin", "description": "The computed result"}
    ]
  }
]
```

## EXAMPLES:

### Example 1: Simple function
```python
def add(a, b):
    return a + b
```
Output:
```json
[{
  "name": "add",
  "category": "Functions",
  "description": "Adds two numbers and returns the sum",
  "inputs": [
    {"name": "exec_in", "type": "ExecPin", "is_exec": true, "description": "Execute"},
    {"name": "a", "type": "AnyPin", "description": "First operand"},
    {"name": "b", "type": "AnyPin", "description": "Second operand"}
  ],
  "outputs": [
    {"name": "exec_out", "type": "ExecPin", "is_exec": true, "description": "Continue"},
    {"name": "result", "type": "AnyPin", "description": "Sum of a and b"}
  ]
}]
```

### Example 2: Variable assignment
```python
x = 5
y = x * 2
```
Output:
```json
[
  {
    "name": "Set x",
    "category": "Variables",
    "description": "Assigns integer value 5 to variable x",
    "inputs": [{"name": "value", "type": "IntPin", "description": "Value to assign"}],
    "outputs": [{"name": "x", "type": "IntPin", "description": "Variable x"}]
  },
  {
    "name": "Set y", 
    "category": "Variables",
    "description": "Assigns x * 2 to variable y",
    "inputs": [{"name": "x", "type": "IntPin", "description": "Input variable x"}],
    "outputs": [{"name": "y", "type": "IntPin", "description": "Variable y = x * 2"}]
  }
]
```

### Example 3: For loop
```python
for item in items:
    print(item)
```
Output:
```json
[{
  "name": "For Loop",
  "category": "Control Flow",
  "description": "Iterates over items collection",
  "inputs": [
    {"name": "exec_in", "type": "ExecPin", "is_exec": true, "description": "Start loop"},
    {"name": "items", "type": "ListPin", "description": "Collection to iterate"}
  ],
  "outputs": [
    {"name": "loop_body", "type": "ExecPin", "is_exec": true, "description": "Execute for each item"},
    {"name": "completed", "type": "ExecPin", "is_exec": true, "description": "Loop finished"},
    {"name": "item", "type": "AnyPin", "description": "Current item"},
    {"name": "index", "type": "IntPin", "description": "Current index"}
  ]
}]
```

### Example 4: If statement
```python
if x > 0:
    result = "positive"
else:
    result = "non-positive"
```
Output:
```json
[{
  "name": "Branch",
  "category": "Control Flow", 
  "description": "Branches based on whether x is greater than 0",
  "inputs": [
    {"name": "exec_in", "type": "ExecPin", "is_exec": true, "description": "Execute"},
    {"name": "x", "type": "IntPin", "description": "Value to check"},
    {"name": "condition", "type": "BoolPin", "description": "x > 0"}
  ],
  "outputs": [
    {"name": "True", "type": "ExecPin", "is_exec": true, "description": "x is positive"},
    {"name": "False", "type": "ExecPin", "is_exec": true, "description": "x is not positive"}
  ]
}]
```

### Example 5: COMPLETE PROGRAM - Calculator with multiple operations
This example shows how to analyze a full program with imports, class, functions, loops, and conditionals.

```python
import math

class Calculator:
    def __init__(self, name):
        self.name = name
        self.history = []
    
    def add(self, a, b):
        result = a + b
        self.history.append(result)
        return result
    
    def calculate_average(self, numbers):
        if len(numbers) == 0:
            return 0
        total = 0
        for num in numbers:
            total = total + num
        return total / len(numbers)

# Main program
calc = Calculator("MyCalc")
x = 10
y = 20
sum_result = calc.add(x, y)
print(sum_result)

data = [1, 2, 3, 4, 5]
avg = calc.calculate_average(data)
if avg > 2.5:
    print("Above average")
else:
    print("Below average")
```

Output - The complete visual node graph:
```json
[
  {
    "name": "Import math",
    "category": "Imports",
    "description": "Imports the math module for mathematical operations",
    "inputs": [],
    "outputs": [
      {"name": "math", "type": "AnyPin", "description": "The math module"}
    ]
  },
  {
    "name": "Calculator",
    "category": "Classes",
    "description": "A calculator class that tracks operation history",
    "inputs": [
      {"name": "name", "type": "StringPin", "description": "Name of the calculator instance"}
    ],
    "outputs": [
      {"name": "Calculator", "type": "AnyPin", "description": "Calculator class type"},
      {"name": "instance", "type": "AnyPin", "description": "Created Calculator instance"}
    ]
  },
  {
    "name": "add",
    "category": "Functions",
    "description": "Adds two numbers and stores result in history",
    "inputs": [
      {"name": "exec_in", "type": "ExecPin", "is_exec": true, "description": "Execute"},
      {"name": "self", "type": "AnyPin", "description": "Calculator instance"},
      {"name": "a", "type": "FloatPin", "description": "First number to add"},
      {"name": "b", "type": "FloatPin", "description": "Second number to add"}
    ],
    "outputs": [
      {"name": "exec_out", "type": "ExecPin", "is_exec": true, "description": "Continue"},
      {"name": "result", "type": "FloatPin", "description": "Sum of a and b"}
    ]
  },
  {
    "name": "calculate_average",
    "category": "Functions",
    "description": "Calculates the average of a list of numbers",
    "inputs": [
      {"name": "exec_in", "type": "ExecPin", "is_exec": true, "description": "Execute"},
      {"name": "self", "type": "AnyPin", "description": "Calculator instance"},
      {"name": "numbers", "type": "ListPin", "description": "List of numbers to average"}
    ],
    "outputs": [
      {"name": "exec_out", "type": "ExecPin", "is_exec": true, "description": "Continue"},
      {"name": "result", "type": "FloatPin", "description": "Average value"}
    ]
  },
  {
    "name": "Set calc",
    "category": "Variables",
    "description": "Creates a new Calculator instance named 'MyCalc'",
    "inputs": [
      {"name": "exec_in", "type": "ExecPin", "is_exec": true, "description": "Execute"},
      {"name": "Calculator", "type": "AnyPin", "description": "Calculator class"},
      {"name": "name", "type": "StringPin", "description": "Instance name: 'MyCalc'"}
    ],
    "outputs": [
      {"name": "exec_out", "type": "ExecPin", "is_exec": true, "description": "Continue"},
      {"name": "calc", "type": "AnyPin", "description": "Calculator instance"}
    ]
  },
  {
    "name": "Set x",
    "category": "Variables",
    "description": "Assigns value 10 to variable x",
    "inputs": [
      {"name": "value", "type": "IntPin", "description": "Value 10"}
    ],
    "outputs": [
      {"name": "x", "type": "IntPin", "description": "Variable x = 10"}
    ]
  },
  {
    "name": "Set y",
    "category": "Variables",
    "description": "Assigns value 20 to variable y",
    "inputs": [
      {"name": "value", "type": "IntPin", "description": "Value 20"}
    ],
    "outputs": [
      {"name": "y", "type": "IntPin", "description": "Variable y = 20"}
    ]
  },
  {
    "name": "Call add",
    "category": "Calls",
    "description": "Calls calc.add(x, y) to add the two numbers",
    "inputs": [
      {"name": "exec_in", "type": "ExecPin", "is_exec": true, "description": "Execute"},
      {"name": "calc", "type": "AnyPin", "description": "Calculator instance"},
      {"name": "x", "type": "IntPin", "description": "First argument"},
      {"name": "y", "type": "IntPin", "description": "Second argument"}
    ],
    "outputs": [
      {"name": "exec_out", "type": "ExecPin", "is_exec": true, "description": "Continue"},
      {"name": "sum_result", "type": "FloatPin", "description": "Result of addition"}
    ]
  },
  {
    "name": "Print sum_result",
    "category": "IO",
    "description": "Prints the sum result to console",
    "inputs": [
      {"name": "exec_in", "type": "ExecPin", "is_exec": true, "description": "Execute"},
      {"name": "sum_result", "type": "FloatPin", "description": "Value to print"}
    ],
    "outputs": [
      {"name": "exec_out", "type": "ExecPin", "is_exec": true, "description": "Continue"}
    ]
  },
  {
    "name": "Set data",
    "category": "Variables",
    "description": "Creates a list of numbers [1, 2, 3, 4, 5]",
    "inputs": [
      {"name": "elements", "type": "ListPin", "description": "List literal [1,2,3,4,5]"}
    ],
    "outputs": [
      {"name": "data", "type": "ListPin", "description": "List variable data"}
    ]
  },
  {
    "name": "Call calculate_average",
    "category": "Calls",
    "description": "Calculates average of the data list",
    "inputs": [
      {"name": "exec_in", "type": "ExecPin", "is_exec": true, "description": "Execute"},
      {"name": "calc", "type": "AnyPin", "description": "Calculator instance"},
      {"name": "data", "type": "ListPin", "description": "List of numbers"}
    ],
    "outputs": [
      {"name": "exec_out", "type": "ExecPin", "is_exec": true, "description": "Continue"},
      {"name": "avg", "type": "FloatPin", "description": "Calculated average"}
    ]
  },
  {
    "name": "Branch avg > 2.5",
    "category": "Control Flow",
    "description": "Checks if average is greater than 2.5",
    "inputs": [
      {"name": "exec_in", "type": "ExecPin", "is_exec": true, "description": "Execute"},
      {"name": "avg", "type": "FloatPin", "description": "Average value to compare"},
      {"name": "threshold", "type": "FloatPin", "description": "Threshold value 2.5"}
    ],
    "outputs": [
      {"name": "True", "type": "ExecPin", "is_exec": true, "description": "avg > 2.5 is true"},
      {"name": "False", "type": "ExecPin", "is_exec": true, "description": "avg > 2.5 is false"}
    ]
  },
  {
    "name": "Print Above",
    "category": "IO",
    "description": "Prints 'Above average' message",
    "inputs": [
      {"name": "exec_in", "type": "ExecPin", "is_exec": true, "description": "Execute from True branch"}
    ],
    "outputs": [
      {"name": "exec_out", "type": "ExecPin", "is_exec": true, "description": "Continue"}
    ]
  },
  {
    "name": "Print Below",
    "category": "IO",
    "description": "Prints 'Below average' message",
    "inputs": [
      {"name": "exec_in", "type": "ExecPin", "is_exec": true, "description": "Execute from False branch"}
    ],
    "outputs": [
      {"name": "exec_out", "type": "ExecPin", "is_exec": true, "description": "Continue"}
    ]
  }
]
```

## EXECUTION FLOW CONNECTIONS (how nodes connect):
1. Import math → Set calc (exec flow)
2. Set calc → Set x → Set y (data setup)
3. Set y → Call add → Print sum_result (exec flow)
4. Print sum_result → Set data → Call calculate_average (exec flow)
5. Call calculate_average → Branch (exec flow)
6. Branch.True → Print Above (exec flow)
7. Branch.False → Print Below (exec flow)

## DATA FLOW CONNECTIONS:
- Calculator class → Set calc (class input)
- x, y → Call add (arguments)
- calc → Call add, Call calculate_average (object)
- sum_result → Print sum_result (value)
- data → Call calculate_average (list input)
- avg → Branch (condition value)

## IMPORTANT:
- Output ONLY the JSON array, no markdown, no explanations
- Every pin MUST have: name, type, description
- Exec pins MUST have is_exec: true
- Use descriptive names that explain the data
- Group related operations logically
- Preserve the execution order from the original code"""

        prompt = f"""Analyze this Python code and create visual node specifications following the exact schema and rules provided.
Focus on:
1. Identifying all discrete operations that should become nodes
2. Correctly typing all input and output pins
3. Properly connecting execution flow
4. Using the correct category names

Python code to analyze:
```python
{code}
```

Output ONLY a valid JSON array of node specifications:"""

        return self.generate(prompt, system_prompt)


class PythonTypeInferrer:
    """Infers types from Python code using AST analysis."""
    
    # Mapping of common operations to result types
    OPERATOR_TYPES = {
        ast.Add: 'number',
        ast.Sub: 'number', 
        ast.Mult: 'number',
        ast.Div: 'float',
        ast.FloorDiv: 'int',
        ast.Mod: 'number',
        ast.Pow: 'number',
        ast.And: 'bool',
        ast.Or: 'bool',
        ast.Not: 'bool',
        ast.Eq: 'bool',
        ast.NotEq: 'bool',
        ast.Lt: 'bool',
        ast.LtE: 'bool',
        ast.Gt: 'bool',
        ast.GtE: 'bool',
    }
    
    # Built-in function return types
    BUILTIN_RETURN_TYPES = {
        'len': 'int',
        'int': 'int',
        'float': 'float',
        'str': 'str',
        'bool': 'bool',
        'list': 'list',
        'dict': 'dict',
        'set': 'set',
        'tuple': 'tuple',
        'range': 'range',
        'abs': 'number',
        'sum': 'number',
        'min': 'Any',
        'max': 'Any',
        'sorted': 'list',
        'reversed': 'iterator',
        'enumerate': 'iterator',
        'zip': 'iterator',
        'map': 'iterator',
        'filter': 'iterator',
        'open': 'file',
        'input': 'str',
        'print': 'None',
        'type': 'type',
        'isinstance': 'bool',
        'hasattr': 'bool',
        'getattr': 'Any',
        'setattr': 'None',
    }
    
    def __init__(self):
        self.variable_types: Dict[str, str] = {}
        self.function_return_types: Dict[str, str] = {}
        
    def infer_expression_type(self, node: ast.AST) -> str:
        """Infer the type of an expression node."""
        if node is None:
            return 'None'
            
        if isinstance(node, ast.Constant):
            return type(node.value).__name__
            
        elif isinstance(node, ast.Num):  # Legacy Python 3.7
            return 'int' if isinstance(node.n, int) else 'float'
            
        elif isinstance(node, ast.Str):  # Legacy Python 3.7
            return 'str'
            
        elif isinstance(node, ast.List):
            if node.elts:
                elem_type = self.infer_expression_type(node.elts[0])
                return f'List[{elem_type}]'
            return 'list'
            
        elif isinstance(node, ast.Dict):
            if node.keys and node.values:
                key_type = self.infer_expression_type(node.keys[0])
                val_type = self.infer_expression_type(node.values[0])
                return f'Dict[{key_type}, {val_type}]'
            return 'dict'
            
        elif isinstance(node, ast.Set):
            if node.elts:
                elem_type = self.infer_expression_type(node.elts[0])
                return f'Set[{elem_type}]'
            return 'set'
            
        elif isinstance(node, ast.Tuple):
            if node.elts:
                types = [self.infer_expression_type(e) for e in node.elts]
                return f'Tuple[{", ".join(types)}]'
            return 'tuple'
            
        elif isinstance(node, ast.Name):
            if node.id in self.variable_types:
                return self.variable_types[node.id]
            # Common conventions
            if node.id in ('True', 'False'):
                return 'bool'
            if node.id == 'None':
                return 'None'
            return 'Any'
            
        elif isinstance(node, ast.BinOp):
            left_type = self.infer_expression_type(node.left)
            right_type = self.infer_expression_type(node.right)
            
            # String concatenation
            if isinstance(node.op, ast.Add) and (left_type == 'str' or right_type == 'str'):
                return 'str'
            # List concatenation
            if isinstance(node.op, ast.Add) and ('list' in left_type.lower() or 'list' in right_type.lower()):
                return 'list'
            # Numeric operations
            if 'float' in (left_type, right_type):
                return 'float'
            if isinstance(node.op, ast.Div):
                return 'float'
            return 'int'
            
        elif isinstance(node, ast.Compare):
            return 'bool'
            
        elif isinstance(node, ast.BoolOp):
            return 'bool'
            
        elif isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.Not):
                return 'bool'
            return self.infer_expression_type(node.operand)
            
        elif isinstance(node, ast.Call):
            func_name = self._get_call_name(node)
            if func_name in self.BUILTIN_RETURN_TYPES:
                return self.BUILTIN_RETURN_TYPES[func_name]
            if func_name in self.function_return_types:
                return self.function_return_types[func_name]
            # Class instantiation (capitalized names)
            if func_name and func_name[0].isupper():
                return func_name
            return 'Any'
            
        elif isinstance(node, ast.Subscript):
            value_type = self.infer_expression_type(node.value)
            if 'List' in value_type or 'list' in value_type:
                # Extract element type from List[X]
                if '[' in value_type:
                    return value_type.split('[')[1].rstrip(']')
                return 'Any'
            if 'Dict' in value_type:
                # Return value type from Dict[K, V]
                if ',' in value_type:
                    return value_type.split(',')[1].strip().rstrip(']')
                return 'Any'
            if value_type == 'str':
                return 'str'
            return 'Any'
            
        elif isinstance(node, ast.Attribute):
            # Common attribute patterns
            attr = node.attr
            if attr.startswith('is_') or attr.startswith('has_'):
                return 'bool'
            if attr in ('count', 'index', 'find', 'rfind'):
                return 'int'
            if attr in ('lower', 'upper', 'strip', 'replace', 'format'):
                return 'str'
            if attr in ('keys', 'values', 'items'):
                return 'iterator'
            if attr in ('append', 'extend', 'insert', 'remove', 'pop', 'clear'):
                return 'None'
            return 'Any'
            
        elif isinstance(node, ast.IfExp):
            # Ternary - try to find common type
            body_type = self.infer_expression_type(node.body)
            else_type = self.infer_expression_type(node.orelse)
            if body_type == else_type:
                return body_type
            return 'Any'
            
        elif isinstance(node, ast.ListComp):
            if node.elt:
                elem_type = self.infer_expression_type(node.elt)
                return f'List[{elem_type}]'
            return 'list'
            
        elif isinstance(node, ast.DictComp):
            return 'dict'
            
        elif isinstance(node, ast.SetComp):
            return 'set'
            
        elif isinstance(node, ast.GeneratorExp):
            return 'generator'
            
        elif isinstance(node, ast.Lambda):
            return 'Callable'
            
        elif isinstance(node, ast.Await):
            return 'Awaitable'
            
        return 'Any'
    
    def _get_call_name(self, node: ast.Call) -> str:
        """Extract function name from a Call node."""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr
        return ''
        
    def infer_function_signature(self, node: ast.FunctionDef) -> Tuple[List[TypedPin], List[TypedPin]]:
        """Infer input and output types for a function."""
        inputs = []
        outputs = []
        
        # Add execution pin for callable functions
        inputs.append(TypedPin(
            name="exec_in",
            data_type="exec",
            direction="input",
            is_exec=True,
            description="Execution input"
        ))
        
        # Analyze arguments
        for arg in node.args.args:
            arg_name = arg.arg
            
            # Check for type annotation
            if arg.annotation:
                arg_type = self._annotation_to_string(arg.annotation)
            else:
                # Try to infer from default value or usage
                arg_type = self._infer_arg_type_from_body(arg_name, node.body)
                
            inputs.append(TypedPin(
                name=arg_name,
                data_type=arg_type,
                direction="input",
                description=f"Parameter {arg_name}"
            ))
            
            # Track for later inference
            self.variable_types[arg_name] = arg_type
            
        # Handle *args
        if node.args.vararg:
            inputs.append(TypedPin(
                name=node.args.vararg.arg,
                data_type="tuple",
                direction="input",
                description="Variable positional arguments"
            ))
            
        # Handle **kwargs
        if node.args.kwarg:
            inputs.append(TypedPin(
                name=node.args.kwarg.arg,
                data_type="dict",
                direction="input",
                description="Variable keyword arguments"
            ))
        
        # Analyze return type
        if node.returns:
            return_type = self._annotation_to_string(node.returns)
        else:
            return_type = self._infer_return_type(node)
            
        self.function_return_types[node.name] = return_type
        
        # Add execution output
        outputs.append(TypedPin(
            name="exec_out",
            data_type="exec",
            direction="output",
            is_exec=True,
            description="Execution output"
        ))
        
        # Add return value output
        if return_type != 'None':
            outputs.append(TypedPin(
                name="result",
                data_type=return_type,
                direction="output",
                description=f"Return value ({return_type})"
            ))
            
        return inputs, outputs
    
    def _annotation_to_string(self, annotation) -> str:
        """Convert AST annotation to string type."""
        if isinstance(annotation, ast.Name):
            return annotation.id
        elif isinstance(annotation, ast.Constant):
            return str(annotation.value)
        elif isinstance(annotation, ast.Subscript):
            # Handle things like List[int], Dict[str, int]
            value = self._annotation_to_string(annotation.value)
            if isinstance(annotation.slice, ast.Tuple):
                slices = [self._annotation_to_string(s) for s in annotation.slice.elts]
                return f"{value}[{', '.join(slices)}]"
            else:
                slice_str = self._annotation_to_string(annotation.slice)
                return f"{value}[{slice_str}]"
        elif isinstance(annotation, ast.Attribute):
            return annotation.attr
        elif isinstance(annotation, ast.BinOp) and isinstance(annotation.op, ast.BitOr):
            # Union type with | operator
            left = self._annotation_to_string(annotation.left)
            right = self._annotation_to_string(annotation.right)
            return f"Union[{left}, {right}]"
        return 'Any'
    
    def _infer_arg_type_from_body(self, arg_name: str, body: List[ast.stmt]) -> str:
        """Try to infer argument type from how it's used in function body."""
        for stmt in body:
            for node in ast.walk(stmt):
                # Check for comparisons
                if isinstance(node, ast.Compare):
                    if isinstance(node.left, ast.Name) and node.left.id == arg_name:
                        for comparator in node.comparators:
                            comp_type = self.infer_expression_type(comparator)
                            if comp_type != 'Any':
                                return comp_type
                                
                # Check for binary operations
                if isinstance(node, ast.BinOp):
                    if isinstance(node.left, ast.Name) and node.left.id == arg_name:
                        if isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
                            right_type = self.infer_expression_type(node.right)
                            if right_type in ('int', 'float'):
                                return right_type
                            if right_type == 'str':
                                return 'str'
                                
                # Check for method calls
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                    if isinstance(node.func.value, ast.Name) and node.func.value.id == arg_name:
                        method = node.func.attr
                        if method in ('append', 'extend', 'pop', 'insert'):
                            return 'list'
                        if method in ('keys', 'values', 'items', 'get', 'update'):
                            return 'dict'
                        if method in ('lower', 'upper', 'strip', 'split', 'join', 'format'):
                            return 'str'
                        if method in ('add', 'remove', 'discard'):
                            return 'set'
                            
                # Check for subscript access
                if isinstance(node, ast.Subscript):
                    if isinstance(node.value, ast.Name) and node.value.id == arg_name:
                        if isinstance(node.slice, ast.Constant):
                            if isinstance(node.slice.value, int):
                                return 'list'  # or str, tuple
                            if isinstance(node.slice.value, str):
                                return 'dict'
                                
        return 'Any'
    
    def _infer_return_type(self, node: ast.FunctionDef) -> str:
        """Infer return type from function body."""
        return_types = []
        
        for stmt in ast.walk(node):
            if isinstance(stmt, ast.Return) and stmt.value:
                ret_type = self.infer_expression_type(stmt.value)
                if ret_type not in return_types:
                    return_types.append(ret_type)
                    
        if not return_types:
            return 'None'
        if len(return_types) == 1:
            return return_types[0]
        # Multiple return types
        return f"Union[{', '.join(return_types)}]"


class VisualNodeGenerator:
    """Generates visual node specifications from Python code."""
    
    # Color schemes for different node types
    NODE_COLORS = {
        'function': (70, 130, 180),    # Steel blue
        'class': (138, 43, 226),       # Blue violet
        'variable': (60, 179, 113),    # Medium sea green
        'if': (255, 165, 0),           # Orange
        'for': (30, 144, 255),         # Dodger blue
        'while': (65, 105, 225),       # Royal blue
        'return': (220, 20, 60),       # Crimson
        'import': (128, 128, 128),     # Gray
        'try': (255, 69, 0),           # Red orange
        'call': (75, 0, 130),          # Indigo
    }
    
    def __init__(self, use_ollama: bool = True, ollama_model: str = "llama3.2"):
        self.type_inferrer = PythonTypeInferrer()
        self.ollama = OllamaClient(model=ollama_model) if use_ollama else None
        self.use_ollama = use_ollama and self.ollama and self.ollama.is_available()
        
    def generate_from_code(self, code: str) -> List[VisualNodeSpec]:
        """Generate visual node specifications from Python code."""
        nodes = []
        
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            # Return error node
            return [VisualNodeSpec(
                name="Syntax Error",
                category="Error",
                description=f"Line {e.lineno}: {e.msg}",
                node_color=(255, 0, 0)
            )]
            
        source_lines = code.split('\n')
        
        # First pass - analyze all functions to build type knowledge
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                self.type_inferrer.infer_function_signature(node)
                
        # Second pass - generate nodes
        for node in ast.iter_child_nodes(tree):
            node_specs = self._process_ast_node(node, source_lines)
            nodes.extend(node_specs)
            
        # If Ollama is available, enhance with AI analysis
        if self.use_ollama and nodes:
            nodes = self._enhance_with_ollama(code, nodes)
            
        return nodes
    
    def _process_ast_node(self, node: ast.AST, source_lines: List[str]) -> List[VisualNodeSpec]:
        """Process an AST node and generate visual node specs."""
        nodes = []
        
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            nodes.append(self._process_function(node, source_lines))
            
        elif isinstance(node, ast.ClassDef):
            nodes.append(self._process_class(node, source_lines))
            
        elif isinstance(node, ast.Assign):
            nodes.append(self._process_assignment(node, source_lines))
            
        elif isinstance(node, ast.If):
            nodes.append(self._process_if(node, source_lines))
            
        elif isinstance(node, ast.For):
            nodes.append(self._process_for(node, source_lines))
            
        elif isinstance(node, ast.While):
            nodes.append(self._process_while(node, source_lines))
            
        elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            nodes.append(self._process_import(node, source_lines))
            
        elif isinstance(node, ast.Expr):
            if isinstance(node.value, ast.Call):
                nodes.append(self._process_call(node, source_lines))
                
        return nodes
    
    def _get_code_segment(self, start: int, end: int, source_lines: List[str]) -> str:
        """Extract code segment from source lines."""
        if start < 1:
            start = 1
        if end > len(source_lines):
            end = len(source_lines)
        return '\n'.join(source_lines[start-1:end])
    
    def _process_function(self, node: ast.FunctionDef, source_lines: List[str]) -> VisualNodeSpec:
        """Process a function definition."""
        inputs, outputs = self.type_inferrer.infer_function_signature(node)
        
        # Get docstring for description
        docstring = ast.get_docstring(node) or f"Function {node.name}"
        
        return VisualNodeSpec(
            name=node.name,
            category="Functions",
            description=docstring[:100] if len(docstring) > 100 else docstring,
            inputs=inputs,
            outputs=outputs,
            code=self._get_code_segment(node.lineno, node.end_lineno or node.lineno, source_lines),
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            node_color=self.NODE_COLORS['function']
        )
    
    def _process_class(self, node: ast.ClassDef, source_lines: List[str]) -> VisualNodeSpec:
        """Process a class definition."""
        inputs = []
        outputs = []
        
        # Base classes as inputs
        for base in node.bases:
            if isinstance(base, ast.Name):
                inputs.append(TypedPin(
                    name=f"base_{base.id}",
                    data_type=base.id,
                    direction="input",
                    description=f"Base class {base.id}"
                ))
                
        # Class as output
        outputs.append(TypedPin(
            name=node.name,
            data_type=node.name,
            direction="output",
            description=f"Class {node.name}"
        ))
        
        # Find __init__ to get constructor params
        for item in node.body:
            if isinstance(item, ast.FunctionDef) and item.name == '__init__':
                for arg in item.args.args[1:]:  # Skip self
                    arg_type = 'Any'
                    if arg.annotation:
                        arg_type = self.type_inferrer._annotation_to_string(arg.annotation)
                    inputs.append(TypedPin(
                        name=arg.arg,
                        data_type=arg_type,
                        direction="input",
                        description=f"Constructor param {arg.arg}"
                    ))
                break
                
        docstring = ast.get_docstring(node) or f"Class {node.name}"
        
        return VisualNodeSpec(
            name=node.name,
            category="Classes",
            description=docstring[:100] if len(docstring) > 100 else docstring,
            inputs=inputs,
            outputs=outputs,
            code=self._get_code_segment(node.lineno, node.end_lineno or node.lineno, source_lines),
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            node_color=self.NODE_COLORS['class']
        )
    
    def _process_assignment(self, node: ast.Assign, source_lines: List[str]) -> VisualNodeSpec:
        """Process variable assignment."""
        inputs = []
        outputs = []
        
        # Get assigned value type
        value_type = self.type_inferrer.infer_expression_type(node.value)
        
        # Dependencies as inputs
        deps = self._extract_dependencies(node.value)
        for dep in deps:
            dep_type = self.type_inferrer.variable_types.get(dep, 'Any')
            inputs.append(TypedPin(
                name=dep,
                data_type=dep_type,
                direction="input",
                description=f"Uses {dep}"
            ))
            
        # Targets as outputs
        for target in node.targets:
            target_names = self._extract_names(target)
            for name in target_names:
                self.type_inferrer.variable_types[name] = value_type
                outputs.append(TypedPin(
                    name=name,
                    data_type=value_type,
                    direction="output",
                    description=f"{name}: {value_type}"
                ))
                
        target_str = ', '.join([n for t in node.targets for n in self._extract_names(t)])
        
        return VisualNodeSpec(
            name=f"Set {target_str}",
            category="Variables",
            description=f"Assign {value_type} to {target_str}",
            inputs=inputs,
            outputs=outputs,
            code=self._get_code_segment(node.lineno, node.end_lineno or node.lineno, source_lines),
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            node_color=self.NODE_COLORS['variable']
        )
    
    def _process_if(self, node: ast.If, source_lines: List[str]) -> VisualNodeSpec:
        """Process if statement."""
        inputs = []
        outputs = []
        
        # Execution input
        inputs.append(TypedPin("exec_in", "exec", "input", is_exec=True))
        
        # Condition dependencies
        deps = self._extract_dependencies(node.test)
        for dep in deps:
            dep_type = self.type_inferrer.variable_types.get(dep, 'Any')
            inputs.append(TypedPin(dep, dep_type, "input", description=f"Condition uses {dep}"))
            
        # Condition as boolean input
        inputs.append(TypedPin("condition", "bool", "input", description="Branch condition"))
        
        # Two execution outputs
        outputs.append(TypedPin("exec_true", "exec", "output", is_exec=True, description="True branch"))
        outputs.append(TypedPin("exec_false", "exec", "output", is_exec=True, description="False branch"))
        
        return VisualNodeSpec(
            name=f"If (line {node.lineno})",
            category="Control Flow",
            description="Conditional branch",
            inputs=inputs,
            outputs=outputs,
            code=self._get_code_segment(node.lineno, node.end_lineno or node.lineno, source_lines),
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            node_color=self.NODE_COLORS['if']
        )
    
    def _process_for(self, node: ast.For, source_lines: List[str]) -> VisualNodeSpec:
        """Process for loop."""
        inputs = []
        outputs = []
        
        # Execution input
        inputs.append(TypedPin("exec_in", "exec", "input", is_exec=True))
        
        # Iterable input
        iter_type = self.type_inferrer.infer_expression_type(node.iter)
        deps = self._extract_dependencies(node.iter)
        for dep in deps:
            dep_type = self.type_inferrer.variable_types.get(dep, 'Any')
            inputs.append(TypedPin(dep, dep_type, "input", description=f"Iterable: {dep}"))
            
        # Loop variable output
        loop_vars = self._extract_names(node.target)
        for var in loop_vars:
            # Try to infer element type
            elem_type = 'Any'
            if 'List[' in iter_type:
                elem_type = iter_type.split('[')[1].rstrip(']')
            elif iter_type == 'str':
                elem_type = 'str'
            elif iter_type == 'range':
                elem_type = 'int'
                
            self.type_inferrer.variable_types[var] = elem_type
            outputs.append(TypedPin(var, elem_type, "output", description=f"Loop variable"))
            
        # Execution outputs
        outputs.append(TypedPin("loop_body", "exec", "output", is_exec=True, description="Loop body"))
        outputs.append(TypedPin("completed", "exec", "output", is_exec=True, description="Loop completed"))
        
        # Index output
        outputs.append(TypedPin("index", "int", "output", description="Current iteration index"))
        
        return VisualNodeSpec(
            name=f"For Loop (line {node.lineno})",
            category="Control Flow",
            description=f"Iterate over {iter_type}",
            inputs=inputs,
            outputs=outputs,
            code=self._get_code_segment(node.lineno, node.end_lineno or node.lineno, source_lines),
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            node_color=self.NODE_COLORS['for']
        )
    
    def _process_while(self, node: ast.While, source_lines: List[str]) -> VisualNodeSpec:
        """Process while loop."""
        inputs = []
        outputs = []
        
        inputs.append(TypedPin("exec_in", "exec", "input", is_exec=True))
        
        deps = self._extract_dependencies(node.test)
        for dep in deps:
            dep_type = self.type_inferrer.variable_types.get(dep, 'Any')
            inputs.append(TypedPin(dep, dep_type, "input", description=f"Condition uses {dep}"))
            
        inputs.append(TypedPin("condition", "bool", "input", description="Loop condition"))
        
        outputs.append(TypedPin("loop_body", "exec", "output", is_exec=True, description="Loop body"))
        outputs.append(TypedPin("completed", "exec", "output", is_exec=True, description="Loop completed"))
        
        return VisualNodeSpec(
            name=f"While Loop (line {node.lineno})",
            category="Control Flow",
            description="While loop",
            inputs=inputs,
            outputs=outputs,
            code=self._get_code_segment(node.lineno, node.end_lineno or node.lineno, source_lines),
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            node_color=self.NODE_COLORS['while']
        )
    
    def _process_import(self, node, source_lines: List[str]) -> VisualNodeSpec:
        """Process import statement."""
        outputs = []
        
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.asname or alias.name
                outputs.append(TypedPin(name, "module", "output", description=f"Module {alias.name}"))
        else:
            module = node.module or ""
            for alias in node.names:
                name = alias.asname or alias.name
                outputs.append(TypedPin(name, "Any", "output", description=f"From {module}"))
                
        return VisualNodeSpec(
            name=f"Import (line {node.lineno})",
            category="Imports",
            description="Import modules/functions",
            inputs=[],
            outputs=outputs,
            code=self._get_code_segment(node.lineno, node.end_lineno or node.lineno, source_lines),
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            node_color=self.NODE_COLORS['import']
        )
    
    def _process_call(self, node: ast.Expr, source_lines: List[str]) -> VisualNodeSpec:
        """Process function call expression."""
        call = node.value
        inputs = []
        outputs = []
        
        inputs.append(TypedPin("exec_in", "exec", "input", is_exec=True))
        
        # Get function name
        func_name = ""
        if isinstance(call.func, ast.Name):
            func_name = call.func.id
        elif isinstance(call.func, ast.Attribute):
            func_name = call.func.attr
            # Object input
            obj_type = self.type_inferrer.infer_expression_type(call.func.value)
            deps = self._extract_dependencies(call.func.value)
            for dep in deps:
                inputs.append(TypedPin(dep, obj_type, "input", description="Object"))
                
        # Arguments
        for i, arg in enumerate(call.args):
            arg_type = self.type_inferrer.infer_expression_type(arg)
            if isinstance(arg, ast.Name):
                inputs.append(TypedPin(arg.id, arg_type, "input", description=f"Arg {i+1}"))
            else:
                inputs.append(TypedPin(f"arg{i+1}", arg_type, "input", description=f"Arg {i+1}"))
                
        # Keyword arguments
        for kw in call.keywords:
            kw_type = self.type_inferrer.infer_expression_type(kw.value)
            inputs.append(TypedPin(kw.arg or "**kwargs", kw_type, "input", description=f"Kwarg {kw.arg}"))
            
        outputs.append(TypedPin("exec_out", "exec", "output", is_exec=True))
        
        # Return type
        ret_type = self.type_inferrer.function_return_types.get(func_name, 'Any')
        if ret_type != 'None':
            outputs.append(TypedPin("result", ret_type, "output", description=f"Returns {ret_type}"))
            
        return VisualNodeSpec(
            name=f"Call {func_name}()",
            category="Calls",
            description=f"Call function {func_name}",
            inputs=inputs,
            outputs=outputs,
            code=self._get_code_segment(node.lineno, node.end_lineno or node.lineno, source_lines),
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            node_color=self.NODE_COLORS['call']
        )
    
    def _extract_names(self, node) -> List[str]:
        """Extract variable names from AST node."""
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
        """Extract variable dependencies from AST node."""
        deps = []
        if node is None:
            return deps
            
        for child in ast.walk(node):
            if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load):
                if child.id not in ('True', 'False', 'None'):
                    deps.append(child.id)
                    
        # Filter builtins
        builtins_set = set(dir(__builtins__)) if isinstance(__builtins__, dict) else set(dir(__builtins__))
        deps = [d for d in deps if d not in builtins_set]
        
        return list(set(deps))
    
    # Mapping from AI pin types to PyFlow internal types
    PYFLOW_TYPE_MAP = {
        'IntPin': 'int',
        'FloatPin': 'float',
        'StringPin': 'str',
        'BoolPin': 'bool',
        'ListPin': 'list',
        'DictPin': 'dict',
        'AnyPin': 'Any',
        'ExecPin': 'exec',
        # Also handle lowercase/alternate forms
        'int': 'int',
        'float': 'float',
        'str': 'str',
        'string': 'str',
        'bool': 'bool',
        'boolean': 'bool',
        'list': 'list',
        'array': 'list',
        'dict': 'dict',
        'dictionary': 'dict',
        'any': 'Any',
        'exec': 'exec',
        'execution': 'exec',
    }
    
    def _normalize_pin_type(self, ai_type: str) -> str:
        """Convert AI-generated pin type to PyFlow internal type."""
        if not ai_type:
            return 'Any'
        # Check direct mapping
        normalized = self.PYFLOW_TYPE_MAP.get(ai_type, None)
        if normalized:
            return normalized
        # Check lowercase
        normalized = self.PYFLOW_TYPE_MAP.get(ai_type.lower(), None)
        if normalized:
            return normalized
        # Handle generic types like List[int]
        if '[' in ai_type:
            return ai_type  # Keep complex types as-is
        return 'Any'
    
    def _validate_ai_node(self, ai_node: dict) -> bool:
        """Validate that an AI-generated node has required fields."""
        required_fields = ['name', 'category', 'inputs', 'outputs']
        for field in required_fields:
            if field not in ai_node:
                return False
        if not isinstance(ai_node.get('inputs'), list):
            return False
        if not isinstance(ai_node.get('outputs'), list):
            return False
        return True
    
    def _ai_node_to_spec(self, ai_node: dict, source_lines: List[str] = None) -> Optional[VisualNodeSpec]:
        """Convert AI-generated node dict to VisualNodeSpec."""
        if not self._validate_ai_node(ai_node):
            return None
            
        inputs = []
        outputs = []
        
        # Process inputs
        for inp in ai_node.get('inputs', []):
            if not isinstance(inp, dict) or 'name' not in inp:
                continue
            pin_type = self._normalize_pin_type(inp.get('type', 'Any'))
            is_exec = inp.get('is_exec', False) or pin_type == 'exec'
            inputs.append(TypedPin(
                name=inp['name'],
                data_type=pin_type,
                direction='input',
                is_exec=is_exec,
                description=inp.get('description', '')
            ))
            
        # Process outputs
        for out in ai_node.get('outputs', []):
            if not isinstance(out, dict) or 'name' not in out:
                continue
            pin_type = self._normalize_pin_type(out.get('type', 'Any'))
            is_exec = out.get('is_exec', False) or pin_type == 'exec'
            outputs.append(TypedPin(
                name=out['name'],
                data_type=pin_type,
                direction='output',
                is_exec=is_exec,
                description=out.get('description', '')
            ))
        
        # Determine node color based on category
        category = ai_node.get('category', 'Functions')
        category_lower = category.lower()
        if 'function' in category_lower:
            color = self.NODE_COLORS.get('function', (70, 130, 180))
        elif 'class' in category_lower:
            color = self.NODE_COLORS.get('class', (138, 43, 226))
        elif 'variable' in category_lower:
            color = self.NODE_COLORS.get('variable', (60, 179, 113))
        elif 'control' in category_lower or 'flow' in category_lower:
            color = self.NODE_COLORS.get('if', (255, 165, 0))
        elif 'loop' in category_lower or 'for' in category_lower:
            color = self.NODE_COLORS.get('for', (30, 144, 255))
        elif 'import' in category_lower:
            color = self.NODE_COLORS.get('import', (128, 128, 128))
        elif 'call' in category_lower:
            color = self.NODE_COLORS.get('call', (75, 0, 130))
        else:
            color = (100, 100, 100)
            
        return VisualNodeSpec(
            name=ai_node['name'],
            category=category,
            description=ai_node.get('description', ''),
            inputs=inputs,
            outputs=outputs,
            code='',
            line_start=0,
            line_end=0,
            node_color=color
        )
    
    def _enhance_with_ollama(self, code: str, nodes: List[VisualNodeSpec]) -> List[VisualNodeSpec]:
        """Use Ollama to enhance node descriptions and add insights."""
        if not self.ollama:
            return nodes
            
        try:
            response = self.ollama.analyze_code_for_nodes(code)
            if response:
                # Try to parse JSON from response
                try:
                    # Find JSON in response - handle potential markdown wrapping
                    import re
                    # Remove markdown code block if present
                    cleaned = re.sub(r'```json\s*', '', response)
                    cleaned = re.sub(r'```\s*', '', cleaned)
                    
                    json_match = re.search(r'\[[\s\S]*\]', cleaned)
                    if json_match:
                        ai_analysis = json.loads(json_match.group())
                        
                        if not isinstance(ai_analysis, list):
                            return nodes
                        
                        # Merge AI insights with our nodes
                        for ai_node in ai_analysis:
                            if not isinstance(ai_node, dict):
                                continue
                                
                            ai_name = ai_node.get('name', '')
                            matched = False
                            
                            for node in nodes:
                                # Match by name similarity
                                if ai_name.lower() in node.name.lower() or node.name.lower() in ai_name.lower():
                                    matched = True
                                    # Enhance description if AI provides better one
                                    ai_desc = ai_node.get('description', '')
                                    if ai_desc and len(ai_desc) > len(node.description):
                                        node.description = ai_desc[:200]  # Limit length
                                    
                                    # Enhance pin descriptions
                                    ai_inputs = {p.get('name', ''): p for p in ai_node.get('inputs', []) if isinstance(p, dict)}
                                    ai_outputs = {p.get('name', ''): p for p in ai_node.get('outputs', []) if isinstance(p, dict)}
                                    
                                    for pin in node.inputs:
                                        if pin.name in ai_inputs and ai_inputs[pin.name].get('description'):
                                            pin.description = ai_inputs[pin.name]['description']
                                            
                                    for pin in node.outputs:
                                        if pin.name in ai_outputs and ai_outputs[pin.name].get('description'):
                                            pin.description = ai_outputs[pin.name]['description']
                                    break
                            
                            # If AI found a node we didn't, consider adding it
                            if not matched and self._validate_ai_node(ai_node):
                                new_spec = self._ai_node_to_spec(ai_node)
                                if new_spec:
                                    nodes.append(new_spec)
                                    
                except json.JSONDecodeError as e:
                    print(f"AI JSON parse error: {e}")
                    pass  # AI response wasn't valid JSON, keep our analysis
        except Exception as e:
            print(f"Ollama enhancement failed: {e}")
            
        return nodes
