# PyFlow - AI Coding Agent Instructions

## Project Overview
PyFlow is a visual scripting framework for Python, inspired by Unreal Blueprints. Programs are created by connecting nodes on a canvas where execution flows through white "ExecPin" wires and data flows through colored wires.

## Architecture (Core → Package → UI)
```
GraphManager → Graph → Node → Pin
```
- **Core classes** (`PyFlow/Core/`): `NodeBase.py`, `PinBase.py`, `GraphBase.py`, `GraphManager.py`
- **Packages** (`PyFlow/Packages/`): Contain node implementations, pins, and function libraries
- **UI is separated** from logic - nodes can run headless without GUI

## Creating New Nodes

### Method 1: Full Node Class (for flow control)
```python
# PyFlow/Packages/PyFlowBase/Nodes/myNode.py
from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *

class myNode(NodeBase):
    def __init__(self, name):
        super(myNode, self).__init__(name)
        # ExecPin with callback triggers compute()
        self.inExec = self.createInputPin("inExec", "ExecPin", None, self.compute)
        self.outExec = self.createOutputPin("outExec", "ExecPin")
        self.inputA = self.createInputPin("a", "IntPin", 0)
        self.output = self.createOutputPin("result", "IntPin")
        
    @staticmethod
    def category():
        return "MyCategory"
    
    def compute(self, *args, **kwargs):
        self.output.setData(self.inputA.getData() * 2)
        self.outExec.call(*args, **kwargs)  # Trigger next node
```

### Method 2: Function Library (for pure functions)
```python
# PyFlow/Packages/PyFlowBase/FunctionLibraries/MyLib.py
from PyFlow.Core import FunctionLibraryBase, IMPLEMENT_NODE
from PyFlow.Core.Common import *

class MyLib(FunctionLibraryBase):
    @staticmethod
    @IMPLEMENT_NODE(returns=("FloatPin", 0.0), meta={NodeMeta.CATEGORY: "Math"})
    def addNumbers(a=("FloatPin", 0.0), b=("FloatPin", 0.0)):
        return a + b
```

## Pin Types & Colors
| Type | Color | Python | Usage |
|------|-------|--------|-------|
| `ExecPin` | White | N/A | Execution flow |
| `IntPin` | Cyan `(0,168,107)` | `int` | Integers |
| `FloatPin` | Green | `float` | Decimals |
| `StringPin` | Magenta | `str` | Text |
| `BoolPin` | Red | `bool` | True/False |
| `AnyPin` | Gray | `Any` | Dynamic type |

## Key Patterns

### Pin Data Access
```python
value = self.inputPin.getData()      # Read input
self.outputPin.setData(result)       # Write output
self.outExec.call(*args, **kwargs)   # Trigger execution flow
```

### Flow Control Nodes Pattern (see `forLoop.py`, `branch.py`)
- Always pass `*args, **kwargs` to `.call()` for proper execution chaining
- Use `push(pin)` to mark dirty pins in loops

### Python-to-Nodes Conversion
- `PythonCodeAnalyzer.py`: Parses Python AST into `CodeBlock` structures
- `RuleBasedConverter.py`: Maps Python constructs to PyFlow nodes (no LLM needed)

## Developer Workflows

### Run Application
```bash
python pyflow.py          # Standalone mode
python pyflow-mdi.py      # Multi-document interface
```

### Run Tests
```bash
python -m unittest discover "PyFlow/Tests"
# Or use: run_tests.bat
```

### Dependencies
```
PySide6, qtpy, blinker, docutils, SQLAlchemy, requests
```

## Compound Nodes & Subgraphs

Compounds encapsulate a graph inside a single node - like functions but visual.

### Key Classes
- `compound.py` - Node that contains a `rawGraph` (inner graph)
- `graphInputs` - Node inside compound that exposes input pins to parent
- `graphOutputs` - Node inside compound that exposes output pins to parent

### How Compounds Work
```python
# compound node has inner graph
self.rawGraph = GraphBase(name, graphManager, parentGraph)

# Pins are synced between inner graphInputs/graphOutputs and outer compound
def syncPins(self):
    # graphInputs output pins → compound input pins
    # graphOutputs input pins → compound output pins
```

### Creating Compound Pins
```python
# Inside compound's inner graph, use graphInputs node:
graphInputNode.addOutPin("myInput", "IntPin")  # Creates input on compound

# Data flows: compound.input → graphInputs.output → inner nodes → graphOutputs.input → compound.output
```

### Compound Data Flow
```
[External] → compound.inputPin → graphInputs.outputPin → [Inner Graph] → graphOutputs.inputPin → compound.outputPin → [External]
```

## UI Architecture

UI is separated from Core logic using wrapper pattern.

### Core ↔ UI Relationship
| Core Class | UI Wrapper | Location |
|------------|------------|----------|
| `NodeBase` | `UINodeBase` | `UI/Canvas/UINodeBase.py` |
| `PinBase` | `UIPinBase` | `UI/Canvas/UIPinBase.py` |
| `GraphBase` | `BlueprintCanvas` | `UI/Widgets/BlueprintCanvas.py` |

### UI Signal Pattern
```python
# Core emits signals, UI listens
self.pinExposed = Signal(object)  # In compound.py
self.pinExposed.send(subgraphInputPin)  # Broadcast to UI wrapper
```

### Key UI Directories
| Path | Purpose |
|------|---------|
| `UI/Canvas/` | Node/Pin visual representation, connections |
| `UI/Widgets/` | Qt widgets (canvas, dialogs, input widgets) |
| `UI/Views/` | Panels and views |
| `UI/Utils/` | Stylesheets, helpers |

### Qt Framework
Uses `qtpy` abstraction layer over PySide6. Import pattern:
```python
from qtpy import QtCore, QtGui
from qtpy.QtWidgets import *
```

## File Reference
| Path | Purpose |
|------|---------|
| `PyFlow/Core/NodeBase.py` | Base class for all nodes |
| `PyFlow/Core/PinBase.py` | Base class for all pins |
| `PyFlow/Core/GraphBase.py` | Graph container for nodes |
| `PyFlow/Packages/PyFlowBase/Nodes/compound.py` | Subgraph/compound implementation |
| `PyFlow/Packages/PyFlowBase/Nodes/graphNodes.py` | graphInputs/graphOutputs nodes |
| `PyFlow/UI/Canvas/UINodeBase.py` | Visual node wrapper |
| `PyFlow/Packages/PyFlowBase/Nodes/` | Built-in node implementations |
| `PyFlow/Packages/PyFlowBase/Pins/` | Pin type implementations |
| `PyFlow/Packages/PyFlowBase/FunctionLibraries/` | Math, String, Array operations |
