# PyFlow Visual Scripting Framework - Complete Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Architecture Overview](#architecture-overview)
3. [Node Types & Categories](#node-types--categories)
4. [Pin Types (Data Types)](#pin-types-data-types)
5. [Visual Scripting Concepts](#visual-scripting-concepts)
6. [How Python Code Maps to Visual Nodes](#how-python-code-maps-to-visual-nodes)
7. [Working with Variables](#working-with-variables)
8. [Flow Control Nodes](#flow-control-nodes)
9. [Creating Custom Nodes](#creating-custom-nodes)
10. [User Interface Guide](#user-interface-guide)
11. [Example: Converting Python to Visual Nodes](#example-converting-python-to-visual-nodes)

---

## Introduction

**PyFlow** is a general-purpose visual scripting framework for Python, inspired by:
- Unreal Engine Blueprints
- Autodesk Softimage ICE
- Fabric Engine

It allows you to create programs visually by connecting nodes on a canvas, where each node represents an operation and connections (wires) represent data flow.

### Key Features
- **Modular**: Add custom node sets, pins, tools, and widgets
- **Python 3 Support**: Full Python integration
- **Separated Logic/UI**: Nodes can run without GUI
- **Subgraphs**: Collapse complex graphs into reusable components
- **Python Nodes**: Write Python code directly in nodes
- **Variables System**: Create and manage variables visually

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      GraphManager                            │
│  (Top-level container for all graphs)                       │
├─────────────────────────────────────────────────────────────┤
│                         Graph                                │
│  (Contains nodes - can have multiple graphs/subgraphs)      │
├─────────────────────────────────────────────────────────────┤
│                         Node                                 │
│  (Individual operation unit with inputs/outputs)            │
├─────────────────────────────────────────────────────────────┤
│                         Pin                                  │
│  (Connection point - carries data or execution signal)      │
└─────────────────────────────────────────────────────────────┘
```

### Core Classes Location
```
PyFlow/Core/
├── GraphManager.py   # Manages all graphs
├── GraphBase.py      # Base class for graphs
├── NodeBase.py       # Base class for nodes
├── PinBase.py        # Base class for pins
├── Variable.py       # Variable management
└── Common.py         # Shared utilities
```

---

## Node Types & Categories

### 1. Flow Control Nodes (Execution)
Located in: `PyFlow/Packages/PyFlowBase/Nodes/`

| Node | Description | Python Equivalent |
|------|-------------|-------------------|
| `branch` | If-else conditional | `if condition: ... else: ...` |
| `forLoop` | For loop iteration | `for i in range(start, stop, step):` |
| `whileLoop` | While loop | `while condition:` |
| `forEachLoop` | Iterate over array | `for item in array:` |
| `sequence` | Execute multiple outputs in order | Sequential statements |
| `doOnce` | Execute only once | One-time initialization |
| `doN` | Execute N times | Limited repetition |
| `flipFlop` | Toggle between two outputs | State toggling |
| `switch` | Switch-case | `match/case` or `if-elif` chain |
| `delay` | Pause execution | `time.sleep()` |

### 2. Data Nodes
| Node | Description | Usage |
|------|-------------|-------|
| `constant` | Holds a constant value | Numbers, strings, bools |
| `getVar` | Get variable value | Read a variable |
| `setVar` | Set variable value | Write to a variable |
| `makeArray` | Create an array | `[1, 2, 3]` |
| `makeDict` | Create a dictionary | `{"key": value}` |

### 3. Output Nodes
| Node | Description |
|------|-------------|
| `consoleOutput` | Print to console |
| `imageDisplay` | Display an image |

### 4. Special Nodes
| Node | Description |
|------|-------------|
| `pythonNode` | Custom Python code |
| `compound` | Subgraph container |
| `stickyNote` | Documentation/comments |
| `commentNode` | Group nodes with comment |

---

## Pin Types (Data Types)

Located in: `PyFlow/Packages/PyFlowBase/Pins/`

| Pin Type | Color | Python Type | Description |
|----------|-------|-------------|-------------|
| `ExecPin` | White | N/A | Execution flow (not data) |
| `IntPin` | Cyan/Blue | `int` | Integer numbers |
| `FloatPin` | Green | `float` | Decimal numbers |
| `StringPin` | Magenta/Pink | `str` | Text strings |
| `BoolPin` | Red | `bool` | True/False |
| `AnyPin` | Gray | `Any` | Accepts any data type |

### Pin Directions
- **Input Pins**: Left side of node (receive data)
- **Output Pins**: Right side of node (send data)

### Pin Connection Rules
1. **ExecPin** can only connect to **ExecPin**
2. **Data pins** can connect if types are compatible
3. **AnyPin** accepts any data type
4. Green wire = valid connection
5. Red wire = invalid connection

---

## Visual Scripting Concepts

### Execution Flow (White Wires)
```
[Start] ──ExecPin──> [Do Something] ──ExecPin──> [Do Next Thing]
```
- White wires control **order of execution**
- Nodes with `inExec` pin execute when triggered
- Nodes with `outExec` pin trigger the next node

### Data Flow (Colored Wires)
```
[Number: 10] ──IntPin──> [Add] ──IntPin──> [Print]
                            ↑
[Number: 20] ──IntPin──────┘
```
- Colored wires carry **data values**
- Data flows from output pins to input pins

### Combined Example
```
┌─────────┐     ┌─────────────┐     ┌──────────────┐
│  Start  │────>│  For Loop   │────>│Console Output│
└─────────┘     │             │     │              │
                │ Start: 0    │     │ entity: ────────┐
                │ Stop: 10    │     └──────────────┘  │
                │ Index: ─────────────────────────────┘
                └─────────────┘
```

---

## How Python Code Maps to Visual Nodes

### Variable Assignment
```python
# Python
x = 10
```
```
Visual Nodes:
┌──────────────┐     ┌─────────────┐
│ constant     │     │  setVar     │
│ value: 10    │────>│  var: x     │
└──────────────┘     │  inp: ◄─────┘
                     └─────────────┘
```

### If-Else Condition
```python
# Python
if score >= 90:
    grade = "A"
else:
    grade = "B"
```
```
Visual Nodes:
┌──────────┐     ┌─────────────┐
│ compare  │     │   branch    │────True───> [setVar grade="A"]
│ a: score │────>│ Condition ◄─┘
│ b: 90    │     │             │────False──> [setVar grade="B"]
│ op: >=   │     └─────────────┘
└──────────┘
```

### For Loop
```python
# Python
for i in range(0, 10):
    print(i)
```
```
Visual Nodes:
┌─────────────────┐     ┌──────────────┐
│    forLoop      │     │consoleOutput │
│ Start: 0        │────>│ inExec       │
│ Stop: 10        │     │              │
│ Step: 1         │     │ entity: ◄────┼── Index
│ LoopBody: ──────┼────>│              │
│ Index: ─────────┼─────┘              │
│ Completed: ─────┼───> [Next Node]    │
└─────────────────┘     └──────────────┘
```

### While Loop
```python
# Python
while counter < 5:
    counter += 1
```
```
Visual Nodes:
┌────────────────┐     ┌─────────────┐
│  whileLoop     │     │    add      │
│ Condition: ◄───┼──── │ a: counter  │
│ LoopBody: ─────┼───> │ b: 1        │───> [setVar counter]
│ Completed: ────┼───> │             │
└────────────────┘     └─────────────┘
        ↑
┌───────┴────────┐
│    compare     │
│ a: counter     │
│ b: 5           │
│ op: <          │
└────────────────┘
```

### Function Call
```python
# Python
result = calculate(a, b)
print(result)
```
```
Visual Nodes:
┌──────────────┐     ┌──────────────┐
│  pythonNode  │     │consoleOutput │
│  calculate   │────>│              │
│  a: ◄────────│     │ entity: ◄────┼── output
│  b: ◄────────│     └──────────────┘
│  output: ────┼─────────────────────────┘
└──────────────┘
```

---

## Working with Variables

### Creating Variables
1. Open the **Variables** panel (View → Variables)
2. Click **+** to add new variable
3. Set **Name**, **Type**, and **Default Value**

### Variable Types
| Type | Description |
|------|-------------|
| Int | Integer numbers |
| Float | Decimal numbers |
| String | Text |
| Bool | True/False |
| Array | List of values |
| Dict | Key-value pairs |

### Using Variables in Graph

**Get Variable (Read)**
- Drag variable from Variables panel to canvas
- Creates `getVar` node
- Output pin contains the value

**Set Variable (Write)**
- Right-click variable → Create Setter
- Creates `setVar` node
- Connect `inp` pin to set value
- Requires `inExec` to trigger

### Example: Counter Variable
```
Variables Panel:
┌─────────────────────┐
│ counter (Int) = 0   │
└─────────────────────┘

Graph:
[getVar counter] ──> [add +1] ──> [setVar counter]
```

---

## Flow Control Nodes

### branch (If-Else)
```
Inputs:
  - In (ExecPin): Trigger execution
  - Condition (BoolPin): True/False value

Outputs:
  - True (ExecPin): Execute if condition is True
  - False (ExecPin): Execute if condition is False
```

### forLoop
```
Inputs:
  - inExec (ExecPin): Trigger loop
  - Start (IntPin): Starting index
  - Stop (IntPin): Ending index (exclusive)
  - Step (IntPin): Increment amount

Outputs:
  - LoopBody (ExecPin): Execute each iteration
  - Index (IntPin): Current loop index
  - Completed (ExecPin): Execute when loop finishes
```

### whileLoop
```
Inputs:
  - inExec (ExecPin): Trigger loop
  - Condition (BoolPin): Continue while True

Outputs:
  - LoopBody (ExecPin): Execute each iteration
  - Completed (ExecPin): Execute when loop finishes
```

### sequence
```
Inputs:
  - inExec (ExecPin): Trigger sequence

Outputs:
  - Then 0 (ExecPin): First execution
  - Then 1 (ExecPin): Second execution
  - Then 2 (ExecPin): Third execution
  - ... (can add more)
```

---

## Creating Custom Nodes

### Method 1: Python Node (Quick)
1. Right-click canvas → Add Node → pythonNode
2. Double-click to edit code
3. Define pins and compute function:

```python
def prepareNode(node):
    """Define the node's pins"""
    node.createInputPin("a", "IntPin", 0)
    node.createInputPin("b", "IntPin", 0)
    node.createOutputPin("result", "IntPin")

def compute(node):
    """Execute when node is triggered"""
    a = node.getPinByName("a").getData()
    b = node.getPinByName("b").getData()
    result = a + b
    node.getPinByName("result").setData(result)
```

### Method 2: Function Library (Recommended)
```python
# In PyFlow/Packages/MyPackage/FunctionLibraries/MyLib.py

from PyFlow.Core.FunctionLibrary import *

class MyMathLib(FunctionLibrary):
    """My custom math functions"""
    
    @staticmethod
    @IMPLEMENT_NODE(
        returns=("FloatPin", 0.0),
        meta={'Category': 'Math', 'Keywords': ['add']}
    )
    def addNumbers(a=("FloatPin", 0.0), b=("FloatPin", 0.0)):
        """Adds two numbers together"""
        return a + b
```

### Method 3: Full Node Class
```python
# In PyFlow/Packages/MyPackage/Nodes/myNode.py

from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *

class myNode(NodeBase):
    def __init__(self, name):
        super(myNode, self).__init__(name)
        # Create pins
        self.inExec = self.createInputPin("inExec", "ExecPin", None, self.compute)
        self.outExec = self.createOutputPin("outExec", "ExecPin")
        self.inputA = self.createInputPin("a", "IntPin", 0)
        self.inputB = self.createInputPin("b", "IntPin", 0)
        self.output = self.createOutputPin("result", "IntPin")
        
    @staticmethod
    def category():
        return "MyCategory"
    
    @staticmethod
    def description():
        return "My custom node description"
    
    def compute(self, *args, **kwargs):
        a = self.inputA.getData()
        b = self.inputB.getData()
        self.output.setData(a + b)
        self.outExec.call()
```

---

## User Interface Guide

### Navigation
| Action | Controls |
|--------|----------|
| Pan canvas | Middle Mouse Button OR Alt + Left Mouse |
| Zoom | Right Mouse Button drag |
| Select node | Left Click |
| Multi-select | Ctrl + Left Click |
| Box select | Left Click + Drag on empty space |

### Adding Nodes
1. **Right-click** on canvas → Node menu appears
2. **Type** node name in search box
3. **Click** or **drag** node to canvas

### Connecting Nodes
1. **Click** on output pin (right side)
2. **Drag** to input pin (left side)
3. **Release** when wire turns green

### Keyboard Shortcuts
| Key | Action |
|-----|--------|
| Ctrl+S | Save |
| Ctrl+Z | Undo |
| Ctrl+Y | Redo |
| Delete | Delete selected |
| Ctrl+C | Copy |
| Ctrl+V | Paste |
| Ctrl+D | Duplicate |

---

## Example: Converting Python to Visual Nodes

### Original Python Code
```python
# Calculate sum of numbers 1 to 10
total = 0
for i in range(1, 11):
    total = total + i
print(f"Sum: {total}")
```

### Visual Node Representation

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  ┌──────────────┐                                                       │
│  │   setVar     │  Set total = 0                                        │
│  │  var: total  │                                                       │
│  │  inp: 0      │                                                       │
│  │  outExec: ───┼──────────────────────┐                                │
│  └──────────────┘                      │                                │
│                                        ▼                                │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                        forLoop                                   │   │
│  │  inExec: ◄──────────────────────────┘                           │   │
│  │  Start: 1                                                        │   │
│  │  Stop: 11                                                        │   │
│  │  Step: 1                                                         │   │
│  │                                                                  │   │
│  │  LoopBody: ─────────┐                                           │   │
│  │  Index: ────────────┼─────────────────┐                         │   │
│  │  Completed: ────────┼─────────────────┼─────────┐               │   │
│  └─────────────────────┼─────────────────┼─────────┼───────────────┘   │
│                        │                 │         │                    │
│                        ▼                 │         │                    │
│  ┌─────────────────────────────────────┐ │         │                    │
│  │              add                    │ │         │                    │
│  │  a: ◄───────[getVar total]          │ │         │                    │
│  │  b: ◄─────────────────────────────────┘         │                    │
│  │  result: ───────┐                   │           │                    │
│  └─────────────────┼───────────────────┘           │                    │
│                    │                               │                    │
│                    ▼                               │                    │
│  ┌─────────────────────────────────────┐           │                    │
│  │            setVar                   │           │                    │
│  │  var: total                         │           │                    │
│  │  inp: ◄─────────────────────────────┘           │                    │
│  └─────────────────────────────────────┘           │                    │
│                                                    │                    │
│                        ┌───────────────────────────┘                    │
│                        ▼                                                │
│  ┌─────────────────────────────────────┐                                │
│  │         consoleOutput               │                                │
│  │  inExec: ◄──────────────────────────┘                                │
│  │  entity: ◄───── [getVar total]                                       │
│  └─────────────────────────────────────┘                                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Node-by-Node Breakdown

| Step | Node | Purpose |
|------|------|---------|
| 1 | `setVar (total=0)` | Initialize total variable |
| 2 | `forLoop (1, 11, 1)` | Loop from 1 to 10 |
| 3 | `getVar (total)` | Get current total value |
| 4 | `add` | Add index to total |
| 5 | `setVar (total)` | Store new total |
| 6 | `consoleOutput` | Print final result |

---

## Appendix: Complete Node Reference

### Pin Creation Methods
```python
# Input pins
node.createInputPin(name, dataType, defaultValue, callback)

# Output pins
node.createOutputPin(name, dataType, defaultValue)

# Examples:
self.createInputPin("value", "IntPin", 0)
self.createInputPin("text", "StringPin", "Hello")
self.createInputPin("flag", "BoolPin", False)
self.createInputPin("number", "FloatPin", 0.0)
self.createInputPin("data", "AnyPin", None)
self.createInputPin("trigger", "ExecPin", None, self.compute)
```

### Data Access Methods
```python
# Get data from input pin
value = self.pinName.getData()

# Set data on output pin
self.outputPin.setData(result)

# Trigger execution output
self.outExec.call()
```

### Node Categories
- `FlowControl` - Loops, conditions, sequences
- `GenericTypes` - Type conversion, constants
- `Common` - General utilities
- `Math` - Mathematical operations
- `String` - Text manipulation

---

## Quick Reference Card

### Pin Colors
| Color | Type | Example |
|-------|------|---------|
| ⬜ White | Execution | Trigger, inExec, outExec |
| 🔵 Blue/Cyan | Integer | 1, 42, -10 |
| 🟢 Green | Float | 3.14, 0.5 |
| 🟣 Magenta | String | "Hello", "World" |
| 🔴 Red | Boolean | True, False |
| ⬛ Gray | Any | Accepts anything |

### Common Node Patterns
```
SEQUENTIAL:    [Node1] ─exec─> [Node2] ─exec─> [Node3]

CONDITIONAL:   [branch] ─True─> [DoThis]
                       ─False─> [DoThat]

LOOP:          [forLoop] ─LoopBody─> [Process] ─────┐
                         ─Completed─> [Done]        │
                    ↑                               │
                    └───────────────────────────────┘

DATA FLOW:     [Source] ─data─> [Transform] ─data─> [Destination]
```

---

*This documentation is for PyFlow v3.0.0 with AI-enhanced Python Debugger Tool*
