# Code Visualization Nodes Documentation

## Overview

This document describes the custom **Code Visualization Nodes** created for PyFlow to visualize Python code execution. These nodes are designed specifically for the Python-to-Visual-Node conversion pipeline, providing consistent execution flow and predictable pin structures.

## Debug Logging

Since terminal output is not always visible, all debug output is written to a log file:

**Log File Location:** `PyFlow/pyflow_debug.log`

To view debug output:
1. Open `pyflow_debug.log` in VS Code
2. The file is refreshed each time you click "Generate Visual Nodes"

The logging module is at `PyFlow/Core/DebugLogger.py` and provides:
- `log(message)` - General message
- `log_error(message)` - Error message  
- `log_success(message)` - Success message
- `log_section(title)` - Section header
- `clear_log()` - Clear and reset log file
- `get_log_path()` - Get log file path

## Why Custom Nodes?

The existing PyFlow nodes (like `makeArray`, `constant`) were designed for manual visual programming and **lack execution pins** (`inExec`/`outExec`). This breaks sequential flow when auto-generating node graphs from Python code.

### Key Design Principles

1. **Consistent Exec Flow** - All statement nodes have `inExec` (input) and `outExec` (output) for sequential execution
2. **Embedded Values** - Nodes store their values/code directly as properties (not requiring external connections for literals)
3. **Predictable Pin Names** - Standardized names (`result`, `array`, `element`, `length`) for reliable auto-connection
4. **Source Code Display** - Each node stores and can display the original Python code

---

## Node Reference

### 1. codeAssign - Variable Assignment

**Purpose:** Represents `x = value` assignments with execution flow.

**File:** `codeAssign.py`

**Pins:**
| Direction | Name | Type | Description |
|-----------|------|------|-------------|
| Input | inExec | ExecPin | Execution trigger |
| Input | value | AnyPin | Value to assign |
| Output | outExec | ExecPin | Continue execution |
| Output | result | AnyPin | The assigned value |

**Properties:**
- `varName` (str): Variable name being assigned
- `sourceCode` (str): Original Python code
- `valueType` (str): Type of value (int, str, float, etc.)

**Example Usage:**
```python
x = 10  # Creates codeAssign node with varName="x", value=10
```

---

### 2. codeArray - Array Literal Creation

**Purpose:** Represents array/list literals like `[1, 2, 3]` with embedded elements.

**File:** `codeArray.py`

**Pins:**
| Direction | Name | Type | Description |
|-----------|------|------|-------------|
| Input | inExec | ExecPin | Execution trigger |
| Output | outExec | ExecPin | Continue execution |
| Output | array | AnyPin | The created array |

**Properties:**
- `varName` (str): Variable name for the array
- `elements` (str): JSON-encoded array elements
- `sourceCode` (str): Original Python code

**Key Feature:** Elements are stored directly in the node as a JSON string, so no external connections are needed for literal arrays.

**Example Usage:**
```python
arr = [10, 324, 45, 13, 29]  # Creates codeArray with elements stored internally
```

---

### 3. codeArrayAccess - Array Indexing

**Purpose:** Represents array element access `arr[i]`.

**File:** `codeArrayAccess.py`

**Pins:**
| Direction | Name | Type | Description |
|-----------|------|------|-------------|
| Input | inExec | ExecPin | Execution trigger |
| Input | array | AnyPin | The array to access |
| Input | index | IntPin | Index position |
| Output | outExec | ExecPin | Continue execution |
| Output | element | AnyPin | The accessed element |

**Properties:**
- `varName` (str): Result variable name
- `sourceCode` (str): Original Python code

**Example Usage:**
```python
value = arr[i]  # Creates codeArrayAccess node
```

---

### 4. codeCompare - Comparison Operations

**Purpose:** Represents comparison operations (`>`, `<`, `==`, `!=`, `>=`, `<=`).

**File:** `codeCompare.py`

**Pins:**
| Direction | Name | Type | Description |
|-----------|------|------|-------------|
| Input | a | AnyPin | Left operand |
| Input | b | AnyPin | Right operand |
| Output | result | BoolPin | Comparison result |

**Properties:**
- `operator` (str): The comparison operator (">", "<", "==", etc.)

**Note:** This is a **pure function node** - no exec pins because comparisons don't have side effects.

**Example Usage:**
```python
if i < len(arr):  # Creates codeCompare with operator="<"
```

---

### 5. codeLen - Length Function

**Purpose:** Represents the `len()` function call.

**File:** `codeLen.py`

**Pins:**
| Direction | Name | Type | Description |
|-----------|------|------|-------------|
| Input | collection | AnyPin | Array/string/collection |
| Output | length | IntPin | The length value |

**Note:** This is a **pure function node** - no exec pins.

**Example Usage:**
```python
n = len(arr)  # Creates codeLen node
for i in range(len(arr)):  # Also creates codeLen
```

---

### 6. codePrint - Print Statement

**Purpose:** Represents `print()` function calls with execution flow.

**File:** `codePrint.py`

**Pins:**
| Direction | Name | Type | Description |
|-----------|------|------|-------------|
| Input | inExec | ExecPin | Execution trigger |
| Input | entity | AnyPin | Value(s) to print |
| Output | outExec | ExecPin | Continue execution |

**Properties:**
- `sourceCode` (str): Original print statement

**Example Usage:**
```python
print(arr[i])  # Creates codePrint node
```

---

### 7. codeBinaryOp - Binary Math Operations

**Purpose:** Represents binary operations (`+`, `-`, `*`, `/`, `//`, `%`, `**`).

**File:** `codeBinaryOp.py`

**Pins:**
| Direction | Name | Type | Description |
|-----------|------|------|-------------|
| Input | a | AnyPin | Left operand |
| Input | b | AnyPin | Right operand |
| Output | result | AnyPin | Operation result |

**Properties:**
- `operator` (str): The operator ("+", "-", "*", "/", etc.)

**Note:** This is a **pure function node** - no exec pins.

**Example Usage:**
```python
total = a + b  # Creates codeBinaryOp with operator="+"
```

---

### 8. codeForLoop - For Loop

**Purpose:** Represents `for` loops with visible loop variable and range.

**File:** `codeForLoop.py`

**Pins:**
| Direction | Name | Type | Description |
|-----------|------|------|-------------|
| Input | inExec | ExecPin | Start the loop |
| Input | Start | IntPin | Range start (default 0) |
| Input | Stop | IntPin | Range end |
| Input | Step | IntPin | Range step (default 1) |
| Output | LoopBody | ExecPin | Execute for each iteration |
| Output | Index | IntPin | Current loop index |
| Output | Completed | ExecPin | Execute when loop finishes |

**Properties:**
- `varName` (str): Loop variable name (e.g., "i")
- `iterableName` (str): What's being iterated (e.g., "range(0, 5)")
- `sourceCode` (str): Original for statement

**Example Usage:**
```python
for i in range(len(arr)):  # Creates codeForLoop with varName="i"
```

---

### 9. codeBranch - Conditional Branch

**Purpose:** Represents `if/else` statements with condition display.

**File:** `codeBranch.py`

**Pins:**
| Direction | Name | Type | Description |
|-----------|------|------|-------------|
| Input | In | ExecPin | Execution trigger |
| Input | Condition | BoolPin | Branch condition |
| Output | True | ExecPin | Execute if condition is true |
| Output | False | ExecPin | Execute if condition is false |

**Properties:**
- `conditionCode` (str): The condition expression (e.g., "i < len(arr)")
- `sourceCode` (str): Original if statement

**Example Usage:**
```python
if x > 10:  # Creates codeBranch with conditionCode="x > 10"
```

---

## Integration with RuleBasedConverter

### PyFlowNodeType Enum

The `RuleBasedConverter.py` defines these node types in the `PyFlowNodeType` enum:

```python
class PyFlowNodeType(Enum):
    # ... existing types ...
    
    # Custom code visualization nodes
    CODE_ASSIGN = "codeAssign"
    CODE_ARRAY = "codeArray"
    CODE_ARRAY_ACCESS = "codeArrayAccess"
    CODE_COMPARE = "codeCompare"
    CODE_LEN = "codeLen"
    CODE_PRINT = "codePrint"
    CODE_BINARY_OP = "codeBinaryOp"
    CODE_FOR_LOOP = "codeForLoop"
    CODE_BRANCH = "codeBranch"
```

### Conversion Methods

Each Python AST construct maps to a specific node type:

| Python Construct | Conversion Method | Node Type |
|-----------------|-------------------|-----------|
| `x = 10` (literal) | `_convert_simple_assignment` | CODE_ASSIGN |
| `arr = [1,2,3]` | `_convert_simple_assignment` | CODE_ARRAY |
| `x = arr[i]` | `_convert_subscript_assignment` | CODE_ARRAY_ACCESS |
| `a > b` (in if) | `_convert_if_statement` | CODE_COMPARE |
| `len(arr)` | `_convert_call` / `_convert_call_assignment` | CODE_LEN |
| `print(x)` | `_convert_call` | CODE_PRINT |
| `x = a + b` | `_convert_binop_assignment` | CODE_BINARY_OP |
| `for i in range()` | `_convert_for_loop` | CODE_FOR_LOOP |
| `if condition:` | `_convert_if_statement` | CODE_BRANCH |

---

## Node Creation in PythonDebuggerTool

The `PythonDebuggerTool._create_node_from_spec()` method handles node creation:

```python
# Custom code visualization nodes are created with their type directly
elif node_type.startswith("code"):
    # Node is created, then properties are set
    if hasattr(raw_node, 'setVarName'):
        raw_node.setVarName(properties['varName'])
    if hasattr(raw_node, 'setSourceCode'):
        raw_node.setSourceCode(properties['sourceCode'])
    # ... etc
```

---

## Creating New Code Nodes

To add a new code visualization node:

### 1. Create the Node File

```python
from PyFlow.Core.NodeBase import NodeBase
from PyFlow.Core.Common import *

class newCodeNode(NodeBase):
    def __init__(self, name):
        super().__init__(name)
        # Create pins
        self.inExec = self.createInputPin("inExec", "ExecPin", None, self.compute)
        self.outExec = self.createOutputPin("outExec", "ExecPin")
        # Add data pins...
        
        # Properties
        self._varName = ""
        self._sourceCode = ""
        
    @staticmethod
    def category():
        return "CodeVisualization"
    
    def compute(self, *args, **kwargs):
        # Execute logic
        self.outExec.call()  # Continue execution flow
        
    # Property setters for RuleBasedConverter
    def setVarName(self, name):
        self._varName = name
        
    def setSourceCode(self, code):
        self._sourceCode = code
```

### 2. Add to PyFlowNodeType Enum

In `RuleBasedConverter.py`:
```python
NEW_CODE_NODE = "newCodeNode"
```

### 3. Update Conversion Method

Add handling in the appropriate `_convert_*` method.

### 4. Update PythonDebuggerTool

Add the node type to the handler in `_create_node_from_spec()`.

---

## Auto-Connection Logic

The `_auto_connect_nodes()` method in `PythonDebuggerTool.py` connects nodes:

### Execution Flow
- Sequential nodes: `outExec` → `inExec`
- Loops: `LoopBody` for body, `Completed` for after loop
- Branches: `True` and `False` for each path

### Data Flow
- Uses `RuleBasedConverter.get_data_flow_edges()` to find variable dependencies
- Matches output pins (`result`, `array`, `element`, `length`) to input pins (`value`, `entity`, `collection`, etc.)

---

## File Locations

```
PyFlow/
├── Core/
│   └── RuleBasedConverter.py    # Enum + conversion logic
├── Packages/
│   └── PyFlowBase/
│       ├── Nodes/
│       │   ├── codeAssign.py
│       │   ├── codeArray.py
│       │   ├── codeArrayAccess.py
│       │   ├── codeCompare.py
│       │   ├── codeLen.py
│       │   ├── codePrint.py
│       │   ├── codeBinaryOp.py
│       │   ├── codeForLoop.py
│       │   ├── codeBranch.py
│       │   └── CODE_NODES_DOCUMENTATION.md  (this file)
│       └── Tools/
│           └── PythonDebuggerTool.py  # Node creation + auto-connect
```

---

## Quick Reference: Pin Names

For auto-connection to work, use these standardized pin names:

### Input Pins
- `inExec` - Execution input
- `value` - Generic value input
- `entity` - For print statements
- `collection` - For len()
- `array` - Array input
- `index` - Integer index
- `a`, `b` - Binary operation operands
- `Condition` - Boolean condition
- `Start`, `Stop`, `Step` - Loop range

### Output Pins
- `outExec` - Execution output
- `result` - Generic result output
- `array` - Array output
- `element` - Array element output
- `length` - Integer length output
- `Index` - Loop index output
- `LoopBody` - Loop body execution
- `Completed` - Post-loop execution
- `True`, `False` - Branch paths
