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
Python Visual Debugger Tool - Load Python files and visualize their execution.
Shows variable flow, execution path, and error locations.
"""

import os
import sys
from qtpy import QtCore
from qtpy import QtGui
from qtpy.QtWidgets import *

from PyFlow.UI.Tool.Tool import DockTool
from PyFlow.Core.PythonCodeAnalyzer import PythonCodeAnalyzer, PythonExecutionTracer, NodeType
from PyFlow.Core.RuleBasedConverter import RuleBasedConverter, VisualNode, PyFlowNodeType

# Import debug logger for file-based output
try:
    from PyFlow.Core.DebugLogger import log, log_error, log_section, log_success, log_node_info, clear_log, get_log_path
    DEBUG_LOGGER_AVAILABLE = True
except ImportError:
    DEBUG_LOGGER_AVAILABLE = False
    # Fallback to print if logger not available
    def log(msg, prefix=""): print(f"{prefix}: {msg}" if prefix else msg)
    def log_error(msg): print(f"ERROR: {msg}")
    def log_section(title): print(f"\n=== {title} ===")
    def log_success(msg): print(f"OK: {msg}")
    def log_node_info(node, spec=None): print(f"Node: {node}")
    def clear_log(): pass
    def get_log_path(): return ""

# Optional Ollama import - only if user wants AI enhancement
try:
    from PyFlow.Core.OllamaIntegration import OllamaClient, VisualNodeGenerator, TypedPin
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    OllamaClient = None
    VisualNodeGenerator = None


class CodeLineWidget(QWidget):
    """Widget representing a single line of code with execution info."""
    
    lineClicked = QtCore.Signal(int)
    
    def __init__(self, line_number: int, code: str, parent=None):
        super(CodeLineWidget, self).__init__(parent)
        self.line_number = line_number
        self.code = code
        self._is_error_line = False
        self._is_current_line = False
        self._execution_count = 0
        self._has_breakpoint = False
        self._variables_at_line = {}
        
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(2, 1, 2, 1)
        layout.setSpacing(4)
        
        # Line number label
        self.lineNumLabel = QLabel(f"{self.line_number:4d}")
        self.lineNumLabel.setFixedWidth(40)
        self.lineNumLabel.setFont(QtGui.QFont("Consolas", 9))
        self.lineNumLabel.setStyleSheet("color: #666; background: #2a2a2a; padding: 2px;")
        layout.addWidget(self.lineNumLabel)
        
        # Execution indicator
        self.execIndicator = QLabel()
        self.execIndicator.setFixedWidth(20)
        self.execIndicator.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.execIndicator)
        
        # Code label
        self.codeLabel = QLabel(self.code)
        self.codeLabel.setFont(QtGui.QFont("Consolas", 10))
        self.codeLabel.setStyleSheet("color: #ddd;")
        layout.addWidget(self.codeLabel, 1)
        
        # Variable info (shows on hover)
        self.varLabel = QLabel()
        self.varLabel.setFont(QtGui.QFont("Consolas", 8))
        self.varLabel.setStyleSheet("color: #88c; background: #333; padding: 2px; border-radius: 3px;")
        self.varLabel.hide()
        layout.addWidget(self.varLabel)
        
        self.setMouseTracking(True)
        self.update_appearance()
        
    def set_error(self, is_error: bool, error_msg: str = ""):
        self._is_error_line = is_error
        self._error_msg = error_msg
        self.update_appearance()
        
    def set_current(self, is_current: bool):
        self._is_current_line = is_current
        self.update_appearance()
        
    def set_execution_count(self, count: int):
        self._execution_count = count
        if count > 0:
            self.execIndicator.setText(f"→{count}" if count > 1 else "→")
            self.execIndicator.setStyleSheet("color: #4a4; font-weight: bold;")
        else:
            self.execIndicator.setText("")
        self.update_appearance()
        
    def set_variables(self, variables: dict):
        self._variables_at_line = variables
        if variables:
            var_text = ", ".join([f"{k}={v.value}" for k, v in list(variables.items())[:3]])
            if len(variables) > 3:
                var_text += f" (+{len(variables)-3} more)"
            self.varLabel.setText(var_text)
        
    def update_appearance(self):
        if self._is_error_line:
            self.setStyleSheet("background: #4a2020;")
            self.codeLabel.setStyleSheet("color: #ff6666;")
            self.setToolTip(f"Error: {self._error_msg}" if hasattr(self, '_error_msg') else "Error on this line")
        elif self._is_current_line:
            self.setStyleSheet("background: #2a3a2a;")
            self.codeLabel.setStyleSheet("color: #aaffaa;")
        elif self._execution_count > 0:
            self.setStyleSheet("background: #252530;")
            self.codeLabel.setStyleSheet("color: #ccccff;")
        else:
            self.setStyleSheet("background: transparent;")
            self.codeLabel.setStyleSheet("color: #888;")
            
    def enterEvent(self, event):
        if self._variables_at_line:
            self.varLabel.show()
        super(CodeLineWidget, self).enterEvent(event)
        
    def leaveEvent(self, event):
        self.varLabel.hide()
        super(CodeLineWidget, self).leaveEvent(event)
        
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.lineClicked.emit(self.line_number)
        super(CodeLineWidget, self).mousePressEvent(event)


class VariableWatchWidget(QWidget):
    """Widget showing variable values and their changes."""
    
    def __init__(self, parent=None):
        super(VariableWatchWidget, self).__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = QLabel("Variables")
        header.setStyleSheet("font-weight: bold; padding: 5px; background: #333;")
        layout.addWidget(header)
        
        # Variable table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Name", "Value", "Type", "Line"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setStyleSheet("""
            QTableWidget { background: #1e1e1e; color: #ddd; gridline-color: #333; }
            QHeaderView::section { background: #333; color: #ddd; padding: 5px; }
        """)
        layout.addWidget(self.table)
        
    def update_variables(self, variables: dict):
        self.table.setRowCount(len(variables))
        for row, (name, var_state) in enumerate(variables.items()):
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(str(var_state.value)[:50]))
            self.table.setItem(row, 2, QTableWidgetItem(var_state.type_name))
            self.table.setItem(row, 3, QTableWidgetItem(str(var_state.line_number)))
            
    def clear(self):
        self.table.setRowCount(0)


class ExecutionTimelineWidget(QWidget):
    """Shows execution timeline/history."""
    
    stepSelected = QtCore.Signal(int)  # Emits step index
    
    def __init__(self, parent=None):
        super(ExecutionTimelineWidget, self).__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header with controls
        header_layout = QHBoxLayout()
        header = QLabel("Execution Timeline")
        header.setStyleSheet("font-weight: bold; padding: 5px;")
        header_layout.addWidget(header)
        
        self.stepLabel = QLabel("Step: 0/0")
        header_layout.addWidget(self.stepLabel)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Timeline slider
        self.slider = QSlider(QtCore.Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.valueChanged.connect(self._on_slider_changed)
        layout.addWidget(self.slider)
        
        # Step list
        self.stepList = QListWidget()
        self.stepList.setMaximumHeight(150)
        self.stepList.setStyleSheet("""
            QListWidget { background: #1e1e1e; color: #ddd; }
            QListWidget::item:selected { background: #3a3a5a; }
        """)
        self.stepList.currentRowChanged.connect(self._on_list_selection)
        layout.addWidget(self.stepList)
        
        self._steps = []
        
    def set_steps(self, steps: list):
        self._steps = steps
        self.slider.setMaximum(max(0, len(steps) - 1))
        self.stepList.clear()
        
        for i, step in enumerate(steps):
            event_icon = "→" if step.event_type == 'line' else \
                        "⤴" if step.event_type == 'call' else \
                        "⤵" if step.event_type == 'return' else \
                        "⚠" if step.event_type == 'exception' else "?"
            text = f"{event_icon} L{step.line_number}: {step.code[:40]}..."
            item = QListWidgetItem(text)
            if step.event_type == 'exception':
                item.setForeground(QtGui.QColor("#ff6666"))
            self.stepList.addItem(item)
            
        self.stepLabel.setText(f"Step: 0/{len(steps)}")
        
    def _on_slider_changed(self, value):
        self.stepLabel.setText(f"Step: {value}/{len(self._steps)}")
        self.stepList.setCurrentRow(value)
        self.stepSelected.emit(value)
        
    def _on_list_selection(self, row):
        if row >= 0:
            self.slider.setValue(row)


class CodeStructureWidget(QWidget):
    """Shows the structure of the code (functions, classes, etc.)."""
    
    blockSelected = QtCore.Signal(object)  # Emits CodeBlock
    
    def __init__(self, parent=None):
        super(CodeStructureWidget, self).__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        header = QLabel("Code Structure")
        header.setStyleSheet("font-weight: bold; padding: 5px; background: #333;")
        layout.addWidget(header)
        
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Element", "Type", "Lines"])
        self.tree.setStyleSheet("""
            QTreeWidget { background: #1e1e1e; color: #ddd; }
            QTreeWidget::item:selected { background: #3a3a5a; }
        """)
        self.tree.itemClicked.connect(self._on_item_clicked)
        layout.addWidget(self.tree)
        
        self._blocks = {}
        
    def set_blocks(self, blocks: list):
        self.tree.clear()
        self._blocks = {}
        
        for block in blocks:
            self._add_block_to_tree(block, None)
            
    def _add_block_to_tree(self, block, parent_item):
        # Icon based on type
        icons = {
            NodeType.FUNCTION_DEF: "🔵",
            NodeType.CLASS_DEF: "🟣",
            NodeType.IF_STATEMENT: "🔶",
            NodeType.FOR_LOOP: "🔄",
            NodeType.WHILE_LOOP: "🔁",
            NodeType.VARIABLE_ASSIGN: "📦",
            NodeType.IMPORT: "📥",
            NodeType.RETURN: "↩️",
            NodeType.TRY_EXCEPT: "⚡",
        }
        icon = icons.get(block.node_type, "•")
        
        if parent_item is None:
            item = QTreeWidgetItem(self.tree)
        else:
            item = QTreeWidgetItem(parent_item)
            
        item.setText(0, f"{icon} {block.name}")
        item.setText(1, block.node_type.value)
        item.setText(2, f"{block.line_start}-{block.line_end}")
        
        self._blocks[id(item)] = block
        
        for child in block.children:
            self._add_block_to_tree(child, item)
            
        if parent_item is None:
            item.setExpanded(True)
            
    def _on_item_clicked(self, item, column):
        block = self._blocks.get(id(item))
        if block:
            self.blockSelected.emit(block)


class PythonDebuggerTool(DockTool):
    """Main Python Visual Debugger dock tool."""
    
    def __init__(self):
        super(PythonDebuggerTool, self).__init__()
        self.setMinimumSize(QtCore.QSize(400, 300))
        self.analyzer = PythonCodeAnalyzer()
        self.tracer = PythonExecutionTracer()
        self.rule_converter = RuleBasedConverter()  # Fast rule-based converter
        self.node_generator = None  # Optional Ollama-based generator
        self._current_file = None
        self._source_code = ""
        self._execution_steps = []
        self._ollama_available = False
        self._ollama_model = "llama3.2"
        
        # Track created nodes for update functionality
        self._created_nodes = []  # List of created PyFlow nodes
        self._node_specs = []     # Corresponding node specs
        self._node_map = {}       # Map of spec names to (node, spec) tuples
        
        # Check Ollama availability (optional)
        self._check_ollama()
        
        self.setup_ui()
        
    def _check_ollama(self):
        """Check if Ollama is available (optional enhancement)."""
        if not OLLAMA_AVAILABLE or OllamaClient is None:
            self._ollama_available = False
            return
            
        try:
            client = OllamaClient()
            self._ollama_available = client.is_available()
            if self._ollama_available:
                models = client.get_available_models()
                if models:
                    self._ollama_model = models[0]
        except:
            self._ollama_available = False
        
    def setup_ui(self):
        # Main widget
        self.content = QWidget()
        self.content.setObjectName("debuggerToolContent")
        self.content.setStyleSheet("background: #1e1e1e; color: #ddd;")
        
        main_layout = QVBoxLayout(self.content)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)
        
        # Toolbar
        toolbar = QHBoxLayout()
        
        self.btnLoad = QPushButton("📂 Load Python File")
        self.btnLoad.clicked.connect(self.load_file)
        toolbar.addWidget(self.btnLoad)
        
        self.btnAnalyze = QPushButton("🔍 Analyze")
        self.btnAnalyze.clicked.connect(self.analyze_code)
        self.btnAnalyze.setEnabled(False)
        toolbar.addWidget(self.btnAnalyze)
        
        self.btnRun = QPushButton("▶ Run & Trace")
        self.btnRun.clicked.connect(self.run_and_trace)
        self.btnRun.setEnabled(False)
        toolbar.addWidget(self.btnRun)
        
        self.btnGenerateNodes = QPushButton("🔷 Generate Visual Nodes")
        self.btnGenerateNodes.clicked.connect(self.generate_visual_nodes)
        self.btnGenerateNodes.setEnabled(False)
        toolbar.addWidget(self.btnGenerateNodes)
        
        self.btnUpdateNodes = QPushButton("🔄 Update Nodes")
        self.btnUpdateNodes.clicked.connect(self.update_visual_nodes)
        self.btnUpdateNodes.setEnabled(False)
        self.btnUpdateNodes.setToolTip("Update existing nodes without recreating")
        toolbar.addWidget(self.btnUpdateNodes)
        
        # Ollama options (optional AI enhancement)
        toolbar.addWidget(QLabel("  |  "))
        self.chkUseOllama = QCheckBox("🤖 Use Ollama AI")
        self.chkUseOllama.setChecked(False)  # Default: use fast rule-based converter
        self.chkUseOllama.setEnabled(self._ollama_available)
        ollama_tip = "Enable AI enhancement (slower but may improve results)" if self._ollama_available else "Ollama not available - using fast rule-based converter"
        self.chkUseOllama.setToolTip(ollama_tip)
        toolbar.addWidget(self.chkUseOllama)
        
        self.cmbOllamaModel = QComboBox()
        self.cmbOllamaModel.setMinimumWidth(120)
        self.cmbOllamaModel.setEnabled(self._ollama_available)
        if self._ollama_available:
            try:
                client = OllamaClient()
                models = client.get_available_models()
                self.cmbOllamaModel.addItems(models if models else ["llama3.2"])
            except:
                self.cmbOllamaModel.addItem("llama3.2")
        else:
            self.cmbOllamaModel.addItem("(Ollama not found)")
        toolbar.addWidget(self.cmbOllamaModel)
        
        # Status indicator
        self.ollamaStatus = QLabel("🟢" if self._ollama_available else "🔴")
        self.ollamaStatus.setToolTip("Ollama connected" if self._ollama_available else "Ollama not available")
        toolbar.addWidget(self.ollamaStatus)
        
        toolbar.addStretch()
        main_layout.addLayout(toolbar)
        
        # File info
        self.fileLabel = QLabel("No file loaded")
        self.fileLabel.setStyleSheet("color: #888; padding: 5px;")
        main_layout.addWidget(self.fileLabel)
        
        # Main splitter
        splitter = QSplitter(QtCore.Qt.Horizontal)
        
        # Left side - Code view (EDITABLE)
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        code_header = QLabel("Source Code (Editable)")
        code_header.setStyleSheet("font-weight: bold; padding: 5px; background: #333;")
        left_layout.addWidget(code_header)
        
        # Use QTextEdit for editable code
        self.codeEditor = QTextEdit()
        self.codeEditor.setStyleSheet("""
            QTextEdit {
                background: #1e1e1e;
                color: #d4d4d4;
                font-family: Consolas, 'Courier New', monospace;
                font-size: 12px;
                border: none;
                padding: 10px;
            }
        """)
        self.codeEditor.setPlaceholderText("Enter Python code here or load a file...")
        self.codeEditor.setLineWrapMode(QTextEdit.NoWrap)
        self.codeEditor.textChanged.connect(self._on_code_changed)
        left_layout.addWidget(self.codeEditor)
        
        splitter.addWidget(left_widget)
        
        # Right side - Info panels
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Tabs for different views
        self.infoTabs = QTabWidget()
        self.infoTabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #333; background: #1e1e1e; }
            QTabBar::tab { background: #2a2a2a; color: #888; padding: 8px 15px; }
            QTabBar::tab:selected { background: #3a3a3a; color: #ddd; }
        """)
        
        # Structure tab
        self.structureWidget = CodeStructureWidget()
        self.structureWidget.blockSelected.connect(self._on_block_selected)
        self.infoTabs.addTab(self.structureWidget, "Structure")
        
        # Variables tab
        self.variableWidget = VariableWatchWidget()
        self.infoTabs.addTab(self.variableWidget, "Variables")
        
        # Timeline tab
        self.timelineWidget = ExecutionTimelineWidget()
        self.timelineWidget.stepSelected.connect(self._on_step_selected)
        self.infoTabs.addTab(self.timelineWidget, "Timeline")
        
        # Errors tab
        self.errorList = QListWidget()
        self.errorList.setStyleSheet("background: #1e1e1e; color: #ff6666;")
        self.infoTabs.addTab(self.errorList, "Errors")
        
        # Log Viewer tab (for debug output)
        self.logViewer = QTextEdit()
        self.logViewer.setReadOnly(True)
        self.logViewer.setStyleSheet("""
            QTextEdit {
                background: #0d0d0d;
                color: #00ff00;
                font-family: Consolas, 'Courier New', monospace;
                font-size: 11px;
                border: none;
            }
        """)
        self.logViewer.setPlaceholderText("Debug log will appear here after generating nodes...")
        self.infoTabs.addTab(self.logViewer, "Log")
        
        # Refresh log button in log tab
        self.btnRefreshLog = QPushButton("🔄 Refresh Log")
        self.btnRefreshLog.clicked.connect(self._refresh_log)
        
        right_layout.addWidget(self.infoTabs)
        splitter.addWidget(right_widget)
        
        splitter.setSizes([500, 300])
        main_layout.addWidget(splitter)
        
        self.setWidget(self.content)
        self._line_widgets = []
        
    def _on_code_changed(self):
        """Called when code in the editor changes."""
        self._source_code = self.codeEditor.toPlainText()
        # Enable buttons if there's code
        has_code = len(self._source_code.strip()) > 0
        self.btnAnalyze.setEnabled(has_code)
        self.btnRun.setEnabled(has_code)
        self.btnGenerateNodes.setEnabled(has_code)
        
    def _refresh_log(self):
        """Refresh the log viewer with current log file contents."""
        try:
            log_path = get_log_path()
            if os.path.exists(log_path):
                with open(log_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.logViewer.setPlainText(content)
                # Scroll to bottom - use QtGui.QTextCursor.MoveOperation.End for PySide6
                cursor = self.logViewer.textCursor()
                cursor.movePosition(QtGui.QTextCursor.MoveOperation.End)
                self.logViewer.setTextCursor(cursor)
            else:
                self.logViewer.setPlainText("No log file found yet. Generate nodes to create log.")
        except Exception as e:
            self.logViewer.setPlainText(f"Error reading log: {e}")
        
    def _add_error(self, error_msg: str, line_num: int = 0):
        """Add an error to the errors list."""
        item = QListWidgetItem(f"Line {line_num}: {error_msg}" if line_num else error_msg)
        item.setForeground(QtGui.QColor("#ff6666"))
        self.errorList.addItem(item)
        
    def _clear_errors(self):
        """Clear all errors."""
        self.errorList.clear()
        
    def load_file(self):
        """Load a Python file for analysis."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Python File", "", "Python Files (*.py);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self._source_code = f.read()
                self._current_file = file_path
                self.fileLabel.setText(f"📄 {os.path.basename(file_path)}")
                # Display in editable text editor
                self.codeEditor.setPlainText(self._source_code)
                self.btnAnalyze.setEnabled(True)
                self.btnRun.setEnabled(True)
                self.btnGenerateNodes.setEnabled(True)
                self._clear_errors()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load file:\n{str(e)}")
                self._add_error(str(e))
                
    def _display_code(self):
        """Display the source code in the editor."""
        # Simply set the text in the editor
        self.codeEditor.setPlainText(self._source_code)
        
    def analyze_code(self):
        """Analyze the loaded code structure."""
        if not self._source_code:
            return
        
        # Update source code from editor
        self._source_code = self.codeEditor.toPlainText()
            
        blocks = self.analyzer.analyze(self._source_code)
        self.structureWidget.set_blocks(blocks)
        
        # Show any syntax errors
        self._clear_errors()
        for line, error in self.analyzer.errors:
            self._add_error(error, line)
                
        # Switch to structure tab
        self.infoTabs.setCurrentIndex(0)
        
    def run_and_trace(self):
        """Execute the code and trace its execution."""
        if not self._source_code:
            return
            
        # Reset line widgets
        for widget in self._line_widgets:
            widget.set_error(False)
            widget.set_current(False)
            widget.set_execution_count(0)
            
        self.errorList.clear()
        
        # Run with tracing
        try:
            self._execution_steps = self.tracer.trace(self._source_code)
        except Exception as e:
            QMessageBox.critical(self, "Execution Error", str(e))
            return
            
        # Update timeline
        self.timelineWidget.set_steps(self._execution_steps)
        
        # Count executions per line
        line_counts = {}
        for step in self._execution_steps:
            if step.event_type == 'line':
                line_counts[step.line_number] = line_counts.get(step.line_number, 0) + 1
                
        for line_num, count in line_counts.items():
            if line_num <= len(self._line_widgets):
                self._line_widgets[line_num-1].set_execution_count(count)
                
        # Show errors
        for error_step in self.tracer.get_errors():
            self.errorList.addItem(f"Line {error_step.line_number}: {error_step.error}")
            if error_step.line_number <= len(self._line_widgets):
                self._line_widgets[error_step.line_number-1].set_error(True, error_step.error)
                
        # Update variables with final state
        if self._execution_steps:
            final_vars = self._execution_steps[-1].variables
            self.variableWidget.update_variables(final_vars)
            
        # Switch to timeline tab
        self.infoTabs.setCurrentIndex(2)
        
    def generate_visual_nodes(self):
        """Generate visual nodes on the PyFlow canvas.
        
        Uses fast rule-based converter by default.
        Optionally uses Ollama AI for enhanced analysis if enabled.
        """
        # Get source code from editor (editable)
        self._source_code = self.codeEditor.toPlainText()
        
        # Clear and initialize log file
        clear_log()
        log_section("GENERATE VISUAL NODES")
        log(f"Source code length: {len(self._source_code)} chars")
        
        if not self._source_code or not self._source_code.strip():
            log_error("No source code to process")
            QMessageBox.warning(self, "Warning", "Please enter or load Python code first")
            return
            
        if not self.pyFlowInstance:
            log_error("PyFlow instance not available")
            QMessageBox.warning(self, "Warning", "PyFlow instance not available")
            return
            
        canvas = self.pyFlowInstance.getCanvas()
        if not canvas:
            log_error("Canvas not available")
            QMessageBox.warning(self, "Warning", "Canvas not available")
            return
        
        # Clear previous errors
        self._clear_errors()
        
        # Check if user wants Ollama AI enhancement
        use_ollama = self.chkUseOllama.isChecked() and self._ollama_available and OLLAMA_AVAILABLE
        log(f"Using Ollama: {use_ollama}")
        
        # Show progress
        progress = QProgressDialog("Analyzing code...", "Cancel", 0, 100, self)
        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setValue(10)
        
        try:
            if use_ollama:
                # Use Ollama-enhanced generator (slower but may be more accurate)
                ollama_model = self.cmbOllamaModel.currentText()
                progress.setLabelText(f"Using Ollama AI ({ollama_model})...")
                log(f"Ollama model: {ollama_model}")
                self.node_generator = VisualNodeGenerator(
                    use_ollama=True, 
                    ollama_model=ollama_model
                )
                progress.setValue(30)
                node_specs = self.node_generator.generate_from_code(self._source_code)
            else:
                # Use fast rule-based converter (default)
                progress.setLabelText("Using fast rule-based analyzer...")
                progress.setValue(30)
                node_specs = self.rule_converter.convert(self._source_code)
            
            log_section("NODE SPECS GENERATED")
            log(f"Total specs: {len(node_specs)}")
            for i, spec in enumerate(node_specs):
                spec_name = getattr(spec, 'name', f"Node_{i}")
                spec_type = getattr(spec, 'node_type', 'unknown')
                if hasattr(spec_type, 'value'):
                    spec_type = spec_type.value
                log(f"  [{i}] {spec_name} (type: {spec_type})")
            
            progress.setLabelText("Creating PyFlow nodes...")
            progress.setValue(50)
            
            # Calculate layout - use flow-based positioning
            x_start = 100
            y_start = 150
            x_spacing = 220  # Horizontal spacing between sequential nodes
            y_spacing = 120  # Vertical offset for loops/branches
            
            created_nodes = []
            node_map = {}  # Map spec names to created nodes for later connection
            
            # Track nesting level for indentation
            nesting_level = 0
            x_pos = x_start
            y_pos = y_start
            
            log_section("CREATING NODES")
            
            for i, spec in enumerate(node_specs):
                if progress.wasCanceled():
                    break
                    
                progress.setValue(50 + int(35 * (i + 1) / len(node_specs)))
                
                # Determine node type for layout (use category since VisualNodeSpec uses category)
                node_category = getattr(spec, 'category', "Unknown")
                spec_name = getattr(spec, 'name', f"Node_{i}")
                is_loop = 'loop' in node_category.lower() or 'loop' in spec_name.lower()
                is_branch = 'branch' in node_category.lower() or 'if' in spec_name.lower()
                is_return = 'return' in spec_name.lower()
                
                # Update position based on node type
                if is_loop or is_branch:
                    # Move down for loop/branch to show nesting
                    nesting_level += 1
                    y_pos += y_spacing * 0.5
                    
                # Calculate position
                node_x = x_pos
                node_y = y_pos + (nesting_level * 40)
                
                # Move x position for next node
                x_pos += x_spacing
                
                # Reset to new row after certain number of nodes or after function defs
                if x_pos > x_start + x_spacing * 6:
                    x_pos = x_start
                    y_pos += y_spacing
                    nesting_level = max(0, nesting_level - 1)
                
                # Log node creation
                log(f"Creating node [{i}]: {spec_name} at ({node_x}, {node_y})")
                
                # Create the PyFlow node
                node = self._create_node_from_spec(canvas, spec, node_x, node_y)
                if node:
                    created_nodes.append(node)
                    log_success(f"Created: {spec_name}")
                    node_map[spec_name] = (node, spec)
                else:
                    log_error(f"Failed to create: {spec_name}")
            
            # Process Qt events to ensure UI is fully updated before connecting
            from qtpy.QtWidgets import QApplication
            QApplication.processEvents()
            
            # Try to auto-connect nodes based on data flow
            progress.setLabelText("Connecting nodes...")
            progress.setValue(90)
            self._auto_connect_nodes(canvas, created_nodes, node_specs, node_map)
                    
            progress.setValue(100)
            progress.close()
            
            log_section("GENERATION COMPLETE")
            log(f"Created {len(created_nodes)} nodes")
            log(f"Log file: {get_log_path()}")
            
            # Refresh log viewer and switch to Log tab
            self._refresh_log()
            self.infoTabs.setCurrentIndex(4)  # Switch to Log tab
            
            # Show summary
            method = "Ollama AI" if use_ollama else "Rule-based analyzer"
            summary = f"Generated {len(created_nodes)} PyFlow nodes!\n\n"
            summary += f"🔧 Method: {method}\n"
            summary += f"📊 Nodes created and ready\n"
            summary += f"\n📝 Check the 'Log' tab for debug details"
            
            # Store references for update functionality
            self._created_nodes = created_nodes
            self._node_specs = node_specs
            self._node_map = node_map
            
            # Enable update button now that nodes exist
            self.btnUpdateNodes.setEnabled(True)
            
            QMessageBox.information(self, "Success", summary)
            
        except Exception as e:
            progress.close()
            import traceback
            error_msg = str(e)
            log_error(f"Generation failed: {error_msg}")
            log_error(traceback.format_exc())
            self._refresh_log()
            self.infoTabs.setCurrentIndex(4)  # Switch to Log tab
            self._add_error(error_msg)
            QMessageBox.critical(self, "Error", f"Failed to generate nodes:\n{str(e)}")
    
    def update_visual_nodes(self):
        """Update existing nodes with new code changes instead of recreating.
        
        This method:
        1. Re-analyzes the code
        2. Updates existing nodes with new property values
        3. Only creates new nodes for new code blocks
        4. Removes nodes for deleted code blocks
        """
        # Get source code from editor
        self._source_code = self.codeEditor.toPlainText()
        
        clear_log()
        log_section("UPDATE VISUAL NODES")
        log(f"Source code length: {len(self._source_code)} chars")
        log(f"Existing nodes: {len(self._created_nodes)}")
        
        if not self._source_code or not self._source_code.strip():
            log_error("No source code to process")
            QMessageBox.warning(self, "Warning", "Please enter or load Python code first")
            return
            
        if not self._created_nodes:
            log("No existing nodes - redirecting to Generate")
            self.generate_visual_nodes()
            return
            
        if not self.pyFlowInstance:
            log_error("PyFlow instance not available")
            QMessageBox.warning(self, "Warning", "PyFlow instance not available")
            return
            
        canvas = self.pyFlowInstance.getCanvas()
        if not canvas:
            log_error("Canvas not available")
            QMessageBox.warning(self, "Warning", "Canvas not available")
            return
        
        self._clear_errors()
        
        # Show progress
        progress = QProgressDialog("Re-analyzing code...", "Cancel", 0, 100, self)
        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setValue(10)
        
        try:
            # Re-analyze the code
            new_node_specs = self.rule_converter.convert(self._source_code)
            log(f"New specs: {len(new_node_specs)}")
            
            progress.setLabelText("Comparing with existing nodes...")
            progress.setValue(30)
            
            updated_count = 0
            created_count = 0
            removed_count = 0
            
            # Build lookup of existing nodes by name pattern
            existing_by_pattern = {}
            for i, node in enumerate(self._created_nodes):
                if i < len(self._node_specs):
                    spec = self._node_specs[i]
                    # Create a pattern key: node_type + line range
                    key = f"{spec.node_type.value if hasattr(spec.node_type, 'value') else spec.node_type}_{spec.line_start}"
                    existing_by_pattern[key] = (node, spec, i)
            
            log(f"Existing patterns: {list(existing_by_pattern.keys())}")
            
            progress.setLabelText("Updating nodes...")
            progress.setValue(50)
            
            # Track which existing nodes we've matched
            matched_indices = set()
            new_nodes_list = []
            
            for new_spec in new_node_specs:
                new_key = f"{new_spec.node_type.value if hasattr(new_spec.node_type, 'value') else new_spec.node_type}_{new_spec.line_start}"
                log(f"Processing: {new_key}")
                
                if new_key in existing_by_pattern:
                    # Found matching node - update it
                    node, old_spec, idx = existing_by_pattern[new_key]
                    matched_indices.add(idx)
                    
                    # Update properties on the node
                    if self._update_node_properties(node, new_spec):
                        updated_count += 1
                        log_success(f"Updated: {new_spec.name}")
                    
                    new_nodes_list.append(node)
                else:
                    # New node needed - create it
                    # Calculate position based on where existing nodes are
                    if self._created_nodes:
                        last_node = self._created_nodes[-1]
                        if hasattr(last_node, 'scenePos'):
                            pos = last_node.scenePos()
                            x = pos.x() + 220
                            y = pos.y()
                        else:
                            x = 100 + len(new_nodes_list) * 220
                            y = 150
                    else:
                        x = 100 + len(new_nodes_list) * 220
                        y = 150
                    
                    node = self._create_node_from_spec(canvas, new_spec, x, y)
                    if node:
                        created_count += 1
                        new_nodes_list.append(node)
                        log_success(f"Created new: {new_spec.name}")
            
            # Remove nodes that no longer exist in code
            progress.setLabelText("Removing obsolete nodes...")
            progress.setValue(80)
            
            for i, node in enumerate(self._created_nodes):
                if i not in matched_indices:
                    try:
                        # Remove the node from canvas
                        if hasattr(canvas, 'removeNode'):
                            canvas.removeNode(node)
                        elif hasattr(node, 'kill'):
                            node.kill()
                        removed_count += 1
                        log(f"Removed obsolete node at index {i}")
                    except Exception as e:
                        log_error(f"Error removing node: {e}")
            
            # Update stored references
            self._created_nodes = new_nodes_list
            self._node_specs = new_node_specs
            
            # Re-establish connections
            progress.setLabelText("Reconnecting nodes...")
            progress.setValue(90)
            self._auto_connect_nodes(canvas, self._created_nodes, self._node_specs, self._node_map)
            
            progress.setValue(100)
            progress.close()
            
            log_section("UPDATE COMPLETE")
            log(f"Updated: {updated_count}")
            log(f"Created: {created_count}")
            log(f"Removed: {removed_count}")
            
            self._refresh_log()
            self.infoTabs.setCurrentIndex(4)  # Switch to Log tab
            
            summary = f"Update complete!\n\n"
            summary += f"🔄 Updated: {updated_count} nodes\n"
            summary += f"➕ Created: {created_count} new nodes\n"
            summary += f"➖ Removed: {removed_count} obsolete nodes\n"
            summary += f"\n📝 Check the 'Log' tab for details"
            
            QMessageBox.information(self, "Update Complete", summary)
            
        except Exception as e:
            progress.close()
            import traceback
            error_msg = str(e)
            log_error(f"Update failed: {error_msg}")
            log_error(traceback.format_exc())
            self._refresh_log()
            self.infoTabs.setCurrentIndex(4)
            self._add_error(error_msg)
            QMessageBox.critical(self, "Error", f"Failed to update nodes:\n{str(e)}")
    
    def _update_node_properties(self, node, new_spec):
        """Update an existing node's properties from a new spec.
        
        Returns True if properties were updated successfully.
        """
        try:
            properties = getattr(new_spec, 'properties', {})
            if not properties:
                return True  # No properties to update
            
            # Get the raw node (not UI wrapper)
            raw_node = node._rawNode if hasattr(node, '_rawNode') else node
            
            # Update properties using setter methods
            if hasattr(raw_node, 'setVarName') and 'varName' in properties:
                raw_node.setVarName(properties['varName'])
            if hasattr(raw_node, 'setSourceCode') and 'sourceCode' in properties:
                raw_node.setSourceCode(properties['sourceCode'])
            if hasattr(raw_node, 'setElements') and 'elements' in properties:
                raw_node.setElements(properties['elements'])
            if hasattr(raw_node, 'setOperator') and 'operator' in properties:
                raw_node.setOperator(properties['operator'])
            if hasattr(raw_node, 'setConditionCode') and 'conditionCode' in properties:
                raw_node.setConditionCode(properties['conditionCode'])
            if hasattr(raw_node, 'setIterableName') and 'iterableName' in properties:
                raw_node.setIterableName(properties['iterableName'])
                
            return True
            
        except Exception as e:
            log_error(f"Error updating node properties: {e}")
            return False

    def _create_node_from_spec(self, canvas, spec, x, y):
        """Create a PyFlow node from a VisualNode specification.
        
        Handles both rule-based VisualNode and Ollama-based specs.
        Maps abstract node types to real PyFlow nodes with proper pins.
        """
        try:
            from PyFlow.Core.NodeBase import NodeBase
            from PyFlow.Core.Common import connectPins
            import uuid
            
            # Determine node type from spec - use hasattr for robustness
            # VisualNode (from RuleBasedConverter) has: node_type, category, color
            # VisualNodeSpec (from OllamaIntegration) has: category, node_color
            if hasattr(spec, 'node_type') and hasattr(spec, 'color'):
                # Rule-based converter output (VisualNode)
                node_type = spec.node_type.value if hasattr(spec.node_type, 'value') else str(spec.node_type)
                package = "PyFlowBase"
                node_name = spec.name
                node_color = spec.color
                node_code = spec.code if hasattr(spec, 'code') else ""
                description = spec.description if hasattr(spec, 'description') else ""
                inputs = spec.inputs if hasattr(spec, 'inputs') else []
                outputs = spec.outputs if hasattr(spec, 'outputs') else []
                properties = spec.properties if hasattr(spec, 'properties') else {}
            else:
                # Ollama-based generator output (VisualNodeSpec) or unknown format
                return self._create_functional_node(canvas, spec, x, y)
            
            # Create appropriate node based on type
            template = NodeBase.jsonTemplate()
            template["package"] = package
            template["type"] = node_type
            template["name"] = node_name.replace(" ", "_").replace("[", "").replace("]", "")[:30]
            template["uuid"] = str(uuid.uuid4())
            template["x"] = x
            template["y"] = y
            template["meta"]["label"] = node_name
            
            # Handle different node types specifically
            if node_type == "forLoop":
                # ForLoop has specific pins: Start, Stop, Step, Index
                if properties:
                    # Store values in template for forLoop
                    pass  # forLoop creates its own pins
                    
            elif node_type == "makeArray":
                # makeArray node - we'll need to connect constant values to it
                # For now create the node, values can be connected after
                pass
            
            # === CUSTOM CODE VISUALIZATION NODES ===
            elif node_type == "codeAssign":
                # Variable assignment with exec flow
                # Set properties on the node after creation
                pass
                
            elif node_type == "codeArray":
                # Array literal creation
                # Node has embedded elements stored as property
                pass
                
            elif node_type == "codeArrayAccess":
                # Array indexing arr[i]
                pass
                
            elif node_type == "codeCompare":
                # Comparison operation (pure function)
                pass
                
            elif node_type == "codeLen":
                # len() function (pure function)
                pass
                
            elif node_type == "codePrint":
                # print() with exec flow
                pass
                
            elif node_type == "codeBinaryOp":
                # Binary math operation (pure function)
                pass
                
            elif node_type == "codeForLoop":
                # For loop with code display
                pass
                
            elif node_type == "codeBranch":
                # Branch with condition display
                pass
            # === END CUSTOM CODE VISUALIZATION NODES ===
                    
            elif node_type == "pythonNode":
                # Generate code for pythonNode - this creates a functional node
                template["nodeData"] = self._generate_python_node_code_from_spec(spec)
                
            elif node_type == "consoleOutput":
                # Console output is straightforward - has inExec, entity, outExec
                pass
                
            elif node_type == "branch":
                # Branch node - has In, Condition, True, False
                pass
            
            elif node_type == "constant":
                # For constant values, we might need to use a different approach
                # Convert to pythonNode instead
                template["type"] = "pythonNode"
                template["nodeData"] = self._generate_python_node_code_from_spec(spec)
                
            elif node_type == "stickyNote":
                # Fallback to sticky note for documentation
                content = self._build_sticky_content(spec)
                template["wrapper"] = {
                    "currentText": content.replace("\n", "<br/>"),
                    "color": self._rgb_to_rgba(node_color[0], node_color[1], node_color[2], 220),
                    "textColor": self._rgb_to_rgba(0, 0, 0, 255),
                    "resize": {"w": 280, "h": 180}
                }
            
            # Create the node
            log(f"  Template: type={template['type']}, name={template['name']}")
            node = canvas._createNode(template)
            
            if node:
                # Log node info
                log(f"  Node created: {node}")
                if hasattr(node, 'UIinputs'):
                    log(f"    Inputs: {list(node.UIinputs.keys())}")
                if hasattr(node, 'UIoutputs'):
                    log(f"    Outputs: {list(node.UIoutputs.keys())}")
                
                # Set properties on custom code nodes
                if node_type.startswith("code") and properties:
                    # Get the raw node (not UI wrapper)
                    raw_node = node._rawNode if hasattr(node, '_rawNode') else node
                    
                    # Set properties using setter methods
                    if hasattr(raw_node, 'setVarName') and 'varName' in properties:
                        raw_node.setVarName(properties['varName'])
                    if hasattr(raw_node, 'setSourceCode') and 'sourceCode' in properties:
                        raw_node.setSourceCode(properties['sourceCode'])
                    if hasattr(raw_node, 'setElements') and 'elements' in properties:
                        raw_node.setElements(properties['elements'])
                    if hasattr(raw_node, 'setOperator') and 'operator' in properties:
                        raw_node.setOperator(properties['operator'])
                    if hasattr(raw_node, 'setConditionCode') and 'conditionCode' in properties:
                        raw_node.setConditionCode(properties['conditionCode'])
                    if hasattr(raw_node, 'setIterableName') and 'iterableName' in properties:
                        raw_node.setIterableName(properties['iterableName'])
                    
                    log(f"    Properties set: {list(properties.keys())}")
                    
            return node
            
        except Exception as e:
            log_error(f"Creating node '{getattr(spec, 'name', 'Unknown')}': {e}")
            import traceback
            log_error(traceback.format_exc())
            # Fallback to sticky note
            return self._create_sticky_note_from_spec(canvas, spec, x, y)
    
    def _generate_python_node_code_from_spec(self, spec):
        """Generate pythonNode code from a VisualNode spec.
        
        Creates prepareNode and compute functions that define pins and execute code.
        Handles both NodePin (pin_type) and TypedPin (data_type).
        """
        lines = []
        
        # prepareNode function - defines node name and pins
        lines.append("def prepareNode(node):")
        spec_name = getattr(spec, 'name', 'Node')
        node_name = spec_name.replace(" ", "_").replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace("=", "")[:20]
        lines.append(f'    node.setName("{node_name}")')
        
        # Helper to get pin type - handles both NodePin and TypedPin
        def get_pin_type(pin):
            if hasattr(pin, 'pin_type'):
                return pin.pin_type  # NodePin
            elif hasattr(pin, 'data_type'):
                # TypedPin - map data_type to PyFlow pin type
                type_map = {
                    'int': 'IntPin', 'float': 'FloatPin', 'str': 'StringPin',
                    'bool': 'BoolPin', 'list': 'AnyPin', 'dict': 'AnyPin',
                    'Any': 'AnyPin', 'None': 'AnyPin'
                }
                return type_map.get(pin.data_type, 'AnyPin')
            return 'AnyPin'
        
        # Create input pins
        for pin in spec.inputs if hasattr(spec, 'inputs') else []:
            if hasattr(pin, 'is_exec') and pin.is_exec:
                lines.append(f'    node.createInputPin("{pin.name}", "ExecPin", None, node.compute)')
            else:
                lines.append(f'    node.createInputPin("{pin.name}", "{get_pin_type(pin)}")')
        
        # Create output pins
        output_vars = []
        for pin in spec.outputs if hasattr(spec, 'outputs') else []:
            if hasattr(pin, 'is_exec') and pin.is_exec:
                lines.append(f'    node.createOutputPin("{pin.name}", "ExecPin")')
            else:
                lines.append(f'    node.createOutputPin("{pin.name}", "{get_pin_type(pin)}")')
                output_vars.append(pin.name)
        
        lines.append("")
        
        # compute function - execute the actual code
        lines.append("def compute(node):")
        
        code = spec.code if hasattr(spec, 'code') else ""
        if code and code.strip():
            # Parse the code to understand what it does
            code_stripped = code.strip()
            
            # Check if this is an assignment like "arr = [10, 324, 45]"
            if '=' in code_stripped and not code_stripped.startswith(('if', 'for', 'while', 'def', 'class')):
                # Simple assignment - extract variable and value
                parts = code_stripped.split('=', 1)
                if len(parts) == 2:
                    var_name = parts[0].strip()
                    value_expr = parts[1].strip()
                    
                    # Handle array subscript on left side (arr[i] = x)
                    if '[' in var_name:
                        lines.append(f"    # {code_stripped}")
                        lines.append(f"    # Array index assignment - get inputs and compute")
                        lines.append(f"    pass  # Complex assignment")
                    else:
                        # Simple variable assignment
                        lines.append(f"    # Execute: {code_stripped}")
                        lines.append(f"    result = {value_expr}")
                        # Set output pin data
                        if var_name in output_vars:
                            lines.append(f'    out_pin = node.getPinByName("{var_name}")')
                            lines.append(f"    if out_pin:")
                            lines.append(f"        out_pin.setData(result)")
                        elif output_vars:
                            # Use first output if var_name doesn't match
                            lines.append(f'    out_pin = node.getPinByName("{output_vars[0]}")')
                            lines.append(f"    if out_pin:")
                            lines.append(f"        out_pin.setData(result)")
            else:
                # Other code - just comment it
                code_lines = code.split('\n')
                for code_line in code_lines[:5]:
                    if code_line.strip():
                        lines.append(f"    # {code_line.strip()}")
                if len(code_lines) > 5:
                    lines.append("    # ...")
                lines.append("    pass")
        else:
            lines.append("    pass")
        
        # Trigger output exec pin
        lines.append('    out_exec = node.getPinByName("outExec")')
        lines.append("    if out_exec:")
        lines.append("        out_exec.call()")
        
        return '\n'.join(lines)
    
    def _create_sticky_note_from_spec(self, canvas, spec, x, y):
        """Create a sticky note node as fallback."""
        try:
            from PyFlow.Core.NodeBase import NodeBase
            import uuid
            
            content = self._build_sticky_content(spec)
            # VisualNode uses 'color', VisualNodeSpec uses 'node_color'
            if hasattr(spec, 'color'):
                color = spec.color
            elif hasattr(spec, 'node_color'):
                color = spec.node_color
            else:
                color = (255, 255, 136)  # Default yellow
            
            node_name = getattr(spec, 'name', 'Note')
            
            template = NodeBase.jsonTemplate()
            template["package"] = "PyFlowBase"
            template["type"] = "stickyNote"
            template["name"] = node_name
            template["uuid"] = str(uuid.uuid4())
            template["x"] = x
            template["y"] = y
            template["meta"]["label"] = node_name
            template["wrapper"] = {
                "currentText": content.replace("\n", "<br/>"),
                "color": self._rgb_to_rgba(color[0], color[1], color[2], 220),
                "textColor": self._rgb_to_rgba(0, 0, 0, 255),
                "resize": {"w": 280, "h": 180}
            }
            
            return canvas._createNode(template)
        except Exception as e:
            print(f"Error creating sticky note: {e}")
            return None
    
    def _build_sticky_content(self, spec):
        """Build content for sticky note.
        
        Handles both VisualNode and VisualNodeSpec with robust attribute access.
        """
        lines = []
        
        # Get category (both types have this)
        category = getattr(spec, 'category', 'Node')
        lines.append(f"[{category}]")
        lines.append("")
        
        # Description
        description = getattr(spec, 'description', "")
        if description:
            lines.append(description[:60])
            lines.append("")
        
        # Inputs
        inputs = getattr(spec, 'inputs', [])
        if inputs:
            lines.append("📥 Inputs:")
            for pin in inputs[:4]:
                is_exec = getattr(pin, 'is_exec', False)
                symbol = "⚡" if is_exec else "→"
                lines.append(f"  {symbol} {getattr(pin, 'name', 'pin')}")
        
        # Outputs
        outputs = getattr(spec, 'outputs', [])
        if outputs:
            lines.append("📤 Outputs:")
            for pin in outputs[:4]:
                is_exec = getattr(pin, 'is_exec', False)
                symbol = "⚡" if is_exec else "←"
                lines.append(f"  {symbol} {getattr(pin, 'name', 'pin')}")
        
        # Code location
        code = getattr(spec, 'code', "")
        line_start = getattr(spec, 'line_start', 0)
        line_end = getattr(spec, 'line_end', 0)
        if code and line_start > 0:
            lines.append(f"📝 Lines {line_start}-{line_end}")
        
        return '\n'.join(lines)
    
    # Mapping from Python/analysis categories to PyFlow node types
    PYFLOW_NODE_MAP = {
        # Control flow
        'for_loop': {'package': 'PyFlowBase', 'type': 'forLoop'},
        'foreach_loop': {'package': 'PyFlowBase', 'type': 'forEachLoop'},
        'while_loop': {'package': 'PyFlowBase', 'type': 'whileLoop'},
        'branch': {'package': 'PyFlowBase', 'type': 'branch'},
        'if': {'package': 'PyFlowBase', 'type': 'branch'},
        'sequence': {'package': 'PyFlowBase', 'type': 'sequence'},
        
        # I/O
        'print': {'package': 'PyFlowBase', 'type': 'consoleOutput'},
        'console': {'package': 'PyFlowBase', 'type': 'consoleOutput'},
        
        # Data types - use constant for make operations
        'make_int': {'package': 'PyFlowBase', 'type': 'constant', 'lib': 'DefaultLib', 'libFunc': 'makeInt'},
        'make_float': {'package': 'PyFlowBase', 'type': 'constant', 'lib': 'DefaultLib', 'libFunc': 'makeFloat'},
        'make_string': {'package': 'PyFlowBase', 'type': 'constant', 'lib': 'DefaultLib', 'libFunc': 'makeString'},
        'make_array': {'package': 'PyFlowBase', 'type': 'makeArray'},
        'make_list': {'package': 'PyFlowBase', 'type': 'makeList'},
        
        # Variables - need special handling
        'set_variable': {'package': 'PyFlowBase', 'type': 'setVar'},
        'get_variable': {'package': 'PyFlowBase', 'type': 'getVar'},
        
        # Python code - most flexible option
        'python': {'package': 'PyFlowBase', 'type': 'pythonNode'},
        'function': {'package': 'PyFlowBase', 'type': 'pythonNode'},
        'custom': {'package': 'PyFlowBase', 'type': 'pythonNode'},
    }
    
    def _get_pyflow_node_type(self, spec):
        """Determine the best PyFlow node type for a given spec."""
        category = spec.category.lower() if spec.category else ''
        name = spec.name.lower() if spec.name else ''
        
        # Check for control flow
        if 'for loop' in name or 'for_loop' in name:
            if 'foreach' in name or 'each' in name:
                return self.PYFLOW_NODE_MAP['foreach_loop']
            return self.PYFLOW_NODE_MAP['for_loop']
        
        if 'while' in name:
            return self.PYFLOW_NODE_MAP['while_loop']
        
        if 'branch' in name or 'if' in name or category == 'control flow':
            return self.PYFLOW_NODE_MAP['branch']
        
        # Check for I/O
        if 'print' in name or 'console' in name:
            return self.PYFLOW_NODE_MAP['print']
        
        # Check for data creation
        if 'set ' in name.lower():
            # Variable assignment - use pythonNode for flexibility
            return self.PYFLOW_NODE_MAP['python']
        
        if 'make' in name.lower() or category == 'variables':
            if 'int' in name.lower():
                return self.PYFLOW_NODE_MAP['make_int']
            if 'float' in name.lower():
                return self.PYFLOW_NODE_MAP['make_float']
            if 'string' in name.lower() or 'str' in name.lower():
                return self.PYFLOW_NODE_MAP['make_string']
            if 'array' in name.lower() or 'list' in name.lower():
                return self.PYFLOW_NODE_MAP['make_array']
        
        # Check for function definitions or calls
        if category == 'functions' or 'call' in name.lower() or 'def ' in name.lower():
            return self.PYFLOW_NODE_MAP['python']
        
        # Default to pythonNode for maximum flexibility
        return self.PYFLOW_NODE_MAP['python']
        
    def _create_functional_node(self, canvas, spec, x, y):
        """Create a real functional PyFlow node from a VisualNodeSpec or VisualNode."""
        try:
            from PyFlow.Core.NodeBase import NodeBase
            import uuid
            
            spec_name = getattr(spec, 'name', 'Node')
            
            # Determine the best PyFlow node type
            node_info = self._get_pyflow_node_type(spec)
            node_type = node_info['type']
            package = node_info['package']
            
            # Create base template
            template = NodeBase.jsonTemplate()
            template["package"] = package
            template["type"] = node_type
            template["name"] = spec_name.replace(" ", "_")
            template["uuid"] = str(uuid.uuid4())
            template["x"] = x
            template["y"] = y
            template["meta"]["label"] = spec_name
            
            # Special handling for pythonNode - embed the actual code
            if node_type == "pythonNode":
                template["nodeData"] = self._generate_python_node_code(spec)
            
            # Create the node on canvas
            node = canvas._createNode(template)
            
            if node:
                # For pythonNode, set the node data after creation
                if node_type == "pythonNode" and hasattr(node, '_rawNode'):
                    raw_node = node._rawNode
                    if hasattr(raw_node, 'nodeData'):
                        raw_node.nodeData = self._generate_python_node_code(spec)
                        
            return node
            
        except Exception as e:
            print(f"Error creating functional node '{getattr(spec, 'name', 'Unknown')}': {e}")
            import traceback
            traceback.print_exc()
            # Fallback to sticky note
            return self._create_sticky_note_node(canvas, spec, x, y)
    
    def _generate_python_node_code(self, spec):
        """Generate Python node code from a VisualNodeSpec or VisualNode.
        
        Handles both TypedPin (data_type) and NodePin (pin_type).
        """
        lines = []
        
        # Helper to get pin type - handles both NodePin and TypedPin
        def get_pin_type_str(pin):
            if hasattr(pin, 'pin_type'):
                return pin.pin_type  # NodePin
            elif hasattr(pin, 'data_type'):
                return self._map_type_to_pin(pin.data_type)  # TypedPin
            return 'AnyPin'
        
        # Generate prepareNode function to set up pins
        lines.append("def prepareNode(node):")
        node_name = spec.name.replace(" ", "_") if hasattr(spec, 'name') else "Node"
        lines.append(f'    node.setName("{node_name}")')
        
        # Create input pins
        inputs = spec.inputs if hasattr(spec, 'inputs') else []
        for pin in inputs:
            is_exec = getattr(pin, 'is_exec', False)
            if is_exec:
                lines.append(f'    node.createInputPin("{pin.name}", "ExecPin", None, node.compute)')
            else:
                pin_type = get_pin_type_str(pin)
                lines.append(f'    node.createInputPin("{pin.name}", "{pin_type}")')
        
        # Create output pins
        outputs = spec.outputs if hasattr(spec, 'outputs') else []
        for pin in outputs:
            is_exec = getattr(pin, 'is_exec', False)
            if is_exec:
                lines.append(f'    node.createOutputPin("{pin.name}", "ExecPin")')
            else:
                pin_type = get_pin_type_str(pin)
                lines.append(f'    node.createOutputPin("{pin.name}", "{pin_type}")')
        
        lines.append("")
        
        # Generate compute function
        lines.append("def compute(node):")
        
        # If we have original code, use it
        code = getattr(spec, 'code', "") or ""
        if code.strip():
            # Indent the original code
            code_lines = code.split('\n')
            for code_line in code_lines:
                if code_line.strip():
                    lines.append(f"    {code_line}")
            
            # Call output exec if present
            has_exec_out = any(getattr(p, 'is_exec', False) and getattr(p, 'direction', '') == 'output' for p in outputs)
            if has_exec_out:
                lines.append('    # Call next node')
                for pin in outputs:
                    if getattr(pin, 'is_exec', False):
                        lines.append(f'    node["{pin.name}"].call()')
                        break
        else:
            lines.append("    # TODO: Implement node logic")
            lines.append("    pass")
        
        return '\n'.join(lines)
    
    def _map_type_to_pin(self, data_type):
        """Map analysis data type to PyFlow pin type."""
        type_map = {
            'int': 'IntPin',
            'float': 'FloatPin',
            'str': 'StringPin',
            'string': 'StringPin',
            'bool': 'BoolPin',
            'list': 'AnyPin',
            'dict': 'AnyPin',
            'any': 'AnyPin',
            'exec': 'ExecPin',
            'none': 'AnyPin',
        }
        
        # Check direct mapping
        lower_type = data_type.lower() if data_type else 'any'
        if lower_type in type_map:
            return type_map[lower_type]
        
        # Check for List[X], Dict[X,Y] patterns
        if 'list' in lower_type or 'array' in lower_type:
            return 'AnyPin'
        if 'dict' in lower_type:
            return 'AnyPin'
        
        # Check if it's already a pin type
        if lower_type.endswith('pin'):
            return data_type
        
        return 'AnyPin'
    
    def _create_sticky_note_node(self, canvas, spec, x, y):
        """Fallback: Create a sticky note node for documentation."""
        try:
            from PyFlow.Core.NodeBase import NodeBase
            import uuid
            
            content = self._build_node_content(spec)
            node_name = getattr(spec, 'name', 'Note')
            
            template = NodeBase.jsonTemplate()
            template["package"] = "PyFlowBase"
            template["type"] = "stickyNote"
            template["name"] = node_name
            template["uuid"] = str(uuid.uuid4())
            template["x"] = x
            template["y"] = y
            template["meta"]["label"] = node_name
            
            # VisualNode uses 'color', VisualNodeSpec uses 'node_color'
            if hasattr(spec, 'color'):
                node_color = spec.color
            elif hasattr(spec, 'node_color'):
                node_color = spec.node_color
            else:
                node_color = (255, 255, 136)
            
            template["wrapper"] = {
                "currentText": content.replace("\n", "<br/>"),
                "color": self._rgb_to_rgba(node_color[0], node_color[1], node_color[2], 220),
                "textColor": self._rgb_to_rgba(0, 0, 0, 255),
                "resize": {"w": 280, "h": 200}
            }
            
            return canvas._createNode(template)
            
        except Exception as e:
            print(f"Error creating sticky note: {e}")
            return None
    
    def _auto_connect_nodes(self, canvas, created_nodes, node_specs, node_map):
        """Automatically connect nodes based on execution flow and data dependencies.
        
        Uses data flow analysis from RuleBasedConverter for smarter connections.
        """
        try:
            from PyFlow.Core.Common import connectPins, canConnectPins
            
            log_section("AUTO-CONNECTING NODES")
            
            if not created_nodes:
                log("No nodes to connect")
                return
                
            log(f"Connecting {len(created_nodes)} nodes")
            
            # Track which nodes have been connected
            exec_connect_count = 0
            data_connect_count = 0
            
            # Build a mapping of node types for smarter connection
            node_info = []
            for i, node in enumerate(created_nodes):
                spec = node_specs[i] if i < len(node_specs) else None
                
                # Log all available pins on this node
                ui_inputs = list(node.UIinputs.keys()) if hasattr(node, 'UIinputs') else []
                ui_outputs = list(node.UIoutputs.keys()) if hasattr(node, 'UIoutputs') else []
                log(f"  Node[{i}] pins: IN={ui_inputs}, OUT={ui_outputs}")
                
                info = {
                    'node': node,
                    'spec': spec,
                    'index': i,
                    'is_loop': self._is_loop_node(node, spec),
                    'is_branch': self._is_branch_node(node, spec),
                    'has_out_exec': self._has_output_exec(node),
                    'has_in_exec': self._has_input_exec(node),
                }
                node_info.append(info)
                log(f"  Node[{i}]: {spec.name if spec else 'unknown'}, loop={info['is_loop']}, branch={info['is_branch']}, out={info['has_out_exec']}, in={info['has_in_exec']}")
            
            # Connect execution flow: sequential order
            log("\n--- Execution Flow ---")
            for i in range(len(node_info) - 1):
                current = node_info[i]
                next_node = node_info[i + 1]
                
                if not current['has_out_exec']:
                    log(f"  Skip [{i}]: no output exec")
                    continue
                    
                if not next_node['has_in_exec']:
                    log(f"  Skip [{i+1}]: no input exec")
                    continue
                
                if current['is_loop']:
                    # For loops: connect Completed to next node (after loop ends)
                    if self._try_connect_specific_exec(canvas, current['node'], next_node['node'], out_pin_name="Completed"):
                        exec_connect_count += 1
                        log_success(f"Loop[{i}] Completed -> Node[{i+1}]")
                    else:
                        log_error(f"Loop[{i}] Completed -> Node[{i+1}]")
                        
                elif current['is_branch']:
                    # For branches: connect True to next node
                    if self._try_connect_specific_exec(canvas, current['node'], next_node['node'], out_pin_name="True"):
                        exec_connect_count += 1
                        log_success(f"Branch[{i}] True -> Node[{i+1}]")
                    else:
                        log_error(f"Branch[{i}] True -> Node[{i+1}]")
                else:
                    # Normal sequential connection
                    if self._try_connect_exec(canvas, current['node'], next_node['node']):
                        exec_connect_count += 1
                        log_success(f"Node[{i}] -> Node[{i+1}]")
                    else:
                        log_error(f"Node[{i}] -> Node[{i+1}]")
            
            # Phase 2: Data flow connections based on variable usage
            log("\n--- Data Flow ---")
            data_flow_edges = self.rule_converter.get_data_flow_edges()
            log(f"Found {len(data_flow_edges)} data flow edges")
            
            for edge in data_flow_edges:
                # Find the source and target nodes by index
                src_idx = edge.from_node_idx
                tgt_idx = edge.to_node_idx
                
                if 0 <= src_idx < len(created_nodes) and 0 <= tgt_idx < len(created_nodes):
                    src_node = created_nodes[src_idx]
                    tgt_node = created_nodes[tgt_idx]
                    
                    # Try to connect data pins matching the variable name
                    if self._try_connect_data_by_variable(canvas, src_node, tgt_node, edge.variable_name, node_specs):
                        data_connect_count += 1
                        log_success(f"Data: {edge.variable_name} [{src_idx}] -> [{tgt_idx}]")
                    else:
                        log_error(f"Data: {edge.variable_name} [{src_idx}] -> [{tgt_idx}]")
            
            log_section("CONNECTION SUMMARY")
            log(f"Exec connections: {exec_connect_count}")
            log(f"Data connections: {data_connect_count}")
            log(f"Total: {exec_connect_count + data_connect_count}")
            
        except Exception as e:
            log_error(f"Auto-connect error: {e}")
            import traceback
            log_error(traceback.format_exc())
    
    def _try_connect_data_by_variable(self, canvas, src_node, tgt_node, variable_name, node_specs):
        """Try to connect data pins based on variable name matching."""
        try:
            # Find output pin on source that matches variable name
            out_pin = None
            out_pin_name = None
            if hasattr(src_node, 'UIoutputs'):
                for pin_name, pin in src_node.UIoutputs.items():
                    if hasattr(pin, '_rawPin') and not pin._rawPin.isExec():
                        # Match by variable name (case insensitive, partial match allowed)
                        if variable_name.lower() in pin_name.lower() or pin_name.lower() in variable_name.lower():
                            out_pin = pin
                            out_pin_name = pin_name
                            break
                        # Also try generic output pins like "result" or the first data pin
                        if 'result' in pin_name.lower() or 'output' in pin_name.lower() or 'out' in pin_name.lower() or 'array' in pin_name.lower() or 'element' in pin_name.lower() or 'length' in pin_name.lower():
                            if out_pin is None:
                                out_pin = pin
                                out_pin_name = pin_name
                # Last resort: first non-exec output
                if out_pin is None:
                    for pin_name, pin in src_node.UIoutputs.items():
                        if hasattr(pin, '_rawPin') and not pin._rawPin.isExec():
                            out_pin = pin
                            out_pin_name = pin_name
                            break
            
            # Find input pin on target that matches or accepts data
            in_pin = None
            in_pin_name = None
            if hasattr(tgt_node, 'UIinputs'):
                for pin_name, pin in tgt_node.UIinputs.items():
                    if hasattr(pin, '_rawPin') and not pin._rawPin.isExec():
                        # Match by variable name
                        if variable_name.lower() in pin_name.lower() or pin_name.lower() in variable_name.lower():
                            in_pin = pin
                            in_pin_name = pin_name
                            break
                        # Try common input names
                        if 'entity' in pin_name.lower() or 'value' in pin_name.lower() or 'input' in pin_name.lower() or 'array' in pin_name.lower() or 'collection' in pin_name.lower():
                            if in_pin is None:
                                in_pin = pin
                                in_pin_name = pin_name
                # Last resort: first non-exec input
                if in_pin is None:
                    for pin_name, pin in tgt_node.UIinputs.items():
                        if hasattr(pin, '_rawPin') and not pin._rawPin.isExec():
                            in_pin = pin
                            in_pin_name = pin_name
                            break
            
            if out_pin and in_pin:
                from PyFlow.Core.Common import connectPins, canConnectPins
                can_connect = canConnectPins(out_pin._rawPin, in_pin._rawPin)
                log(f"    Data: {out_pin_name} -> {in_pin_name} (var={variable_name}), canConnect={can_connect}")
                
                if can_connect:
                    result = connectPins(out_pin._rawPin, in_pin._rawPin)
                    if result:
                        canvas.createUIConnectionForConnectedPins(out_pin, in_pin)
                        return True
                    else:
                        log_error(f"    Data connectPins returned False")
                else:
                    log_error(f"    Data canConnectPins returned False")
                return False
            else:
                if not out_pin:
                    log_error(f"    No output data pin for {variable_name}")
                if not in_pin:
                    log_error(f"    No input data pin for {variable_name}")
                
        except Exception as e:
            log_error(f"Data connection error for {variable_name}: {e}")
        
        return False

    def _is_loop_node(self, node, spec):
        """Check if node is a loop type."""
        if spec and hasattr(spec, 'node_type'):
            node_type = spec.node_type.value if hasattr(spec.node_type, 'value') else str(spec.node_type)
            return 'loop' in node_type.lower() or 'Loop' in node_type
        if hasattr(node, '_rawNode'):
            return 'loop' in node._rawNode.__class__.__name__.lower()
        return False
    
    def _is_branch_node(self, node, spec):
        """Check if node is a branch type."""
        if spec and hasattr(spec, 'node_type'):
            node_type = spec.node_type.value if hasattr(spec.node_type, 'value') else str(spec.node_type)
            return 'branch' in node_type.lower()
        if hasattr(node, '_rawNode'):
            return 'branch' in node._rawNode.__class__.__name__.lower()
        return False
    
    def _has_output_exec(self, node):
        """Check if node has output exec pins."""
        if hasattr(node, 'UIoutputs'):
            for pin in node.UIoutputs.values():
                if hasattr(pin, '_rawPin') and pin._rawPin.isExec():
                    return True
        return False
    
    def _has_input_exec(self, node):
        """Check if node has input exec pins."""
        if hasattr(node, 'UIinputs'):
            for pin in node.UIinputs.values():
                if hasattr(pin, '_rawPin') and pin._rawPin.isExec():
                    return True
        return False
    
    def _try_connect_specific_exec(self, canvas, from_node, to_node, out_pin_name=None, in_pin_name=None):
        """Try to connect specific exec pins by name."""
        try:
            from PyFlow.Core.Common import connectPins, canConnectPins
            
            out_exec = None
            in_exec = None
            found_out_name = None
            found_in_name = None
            
            # Find output exec pin
            if hasattr(from_node, 'UIoutputs'):
                for pin_name, pin in from_node.UIoutputs.items():
                    if hasattr(pin, '_rawPin') and pin._rawPin.isExec():
                        if out_pin_name is None or pin_name == out_pin_name or out_pin_name.lower() in pin_name.lower():
                            out_exec = pin
                            found_out_name = pin_name
                            break
            
            # Find input exec pin
            if hasattr(to_node, 'UIinputs'):
                for pin_name, pin in to_node.UIinputs.items():
                    if hasattr(pin, '_rawPin') and pin._rawPin.isExec():
                        if in_pin_name is None or pin_name == in_pin_name or in_pin_name.lower() in pin_name.lower():
                            in_exec = pin
                            found_in_name = pin_name
                            break
            
            if out_exec and in_exec:
                # Check if can connect first
                can_connect = canConnectPins(out_exec._rawPin, in_exec._rawPin)
                log(f"    Connecting {found_out_name} -> {found_in_name}, canConnect={can_connect}")
                
                if can_connect:
                    # Use raw pin connection
                    result = connectPins(out_exec._rawPin, in_exec._rawPin)
                    if result:
                        # Create UI wire
                        canvas.createUIConnectionForConnectedPins(out_exec, in_exec)
                        log_success(f"    Connected: {found_out_name} -> {found_in_name}")
                        return True
                    else:
                        log_error(f"    connectPins returned False")
                else:
                    log_error(f"    canConnectPins returned False")
                return False
            else:
                if not out_exec:
                    avail_outs = list(from_node.UIoutputs.keys()) if hasattr(from_node, 'UIoutputs') else []
                    log_error(f"    No output exec '{out_pin_name}' found. Available: {avail_outs}")
                if not in_exec:
                    avail_ins = list(to_node.UIinputs.keys()) if hasattr(to_node, 'UIinputs') else []
                    log_error(f"    No input exec '{in_pin_name}' found. Available: {avail_ins}")
                
        except Exception as e:
            log_error(f"    Specific exec connection error: {e}")
            import traceback
            log_error(traceback.format_exc())
        
        return False

    def _try_connect_exec(self, canvas, from_node, to_node):
        """Try to connect execution pins between two nodes."""
        try:
            from PyFlow.Core.Common import connectPins, canConnectPins
            
            # Find output exec pin on from_node
            out_exec = None
            out_pin_name = None
            if hasattr(from_node, 'UIoutputs'):
                for pin_name, pin in from_node.UIoutputs.items():
                    if hasattr(pin, '_rawPin') and pin._rawPin.isExec():
                        # Prefer "outExec" or first exec pin found
                        if 'out' in pin_name.lower() or out_exec is None:
                            out_exec = pin
                            out_pin_name = pin_name
                        if 'out' in pin_name.lower():
                            break
            
            # Find input exec pin on to_node  
            in_exec = None
            in_pin_name = None
            if hasattr(to_node, 'UIinputs'):
                for pin_name, pin in to_node.UIinputs.items():
                    if hasattr(pin, '_rawPin') and pin._rawPin.isExec():
                        in_exec = pin
                        in_pin_name = pin_name
                        break
            
            if out_exec and in_exec:
                # Check if can connect
                can_connect = canConnectPins(out_exec._rawPin, in_exec._rawPin)
                log(f"    Connecting {out_pin_name} -> {in_pin_name}, canConnect={can_connect}")
                
                if can_connect:
                    result = connectPins(out_exec._rawPin, in_exec._rawPin)
                    if result:
                        canvas.createUIConnectionForConnectedPins(out_exec, in_exec)
                        log_success(f"    Connected: {out_pin_name} -> {in_pin_name}")
                        return True
                    else:
                        log_error(f"    connectPins returned False")
                else:
                    log_error(f"    canConnectPins returned False")
                return False
            else:
                if not out_exec:
                    log_error(f"    No output exec pin found on source node")
                if not in_exec:
                    log_error(f"    No input exec pin found on target node")
                
        except Exception as e:
            log_error(f"    Exec connection error: {e}")
            import traceback
            log_error(traceback.format_exc())
        
        return False
        
    def _create_typed_node(self, canvas, spec, x, y):
        """Create a visual node with typed pins from a VisualNodeSpec."""
        # Redirect to functional node creation
        return self._create_functional_node(canvas, spec, x, y)
    
    def _rgb_to_rgba(self, r, g, b, a=255):
        """Convert RGB values to a single RGBA integer for Qt."""
        from qtpy.QtGui import QColor
        color = QColor(r, g, b, a)
        return color.rgba()
            
    def _build_node_content(self, spec):
        """Build rich content string for a node with type info.
        
        Handles both VisualNode (NodePin with pin_type) and VisualNodeSpec (TypedPin with data_type).
        """
        lines = []
        
        # Helper to get pin type string
        def get_pin_type_display(pin):
            if hasattr(pin, 'data_type'):
                return pin.data_type
            elif hasattr(pin, 'pin_type'):
                return pin.pin_type
            return "Any"
        
        # Category tag
        category = getattr(spec, 'category', 'Node')
        lines.append(f"[{category}]")
        lines.append("")
        
        # Description
        description = getattr(spec, 'description', "")
        if description:
            desc = description[:80] + "..." if len(description) > 80 else description
            lines.append(desc)
            lines.append("")
        
        # Inputs with types
        inputs = getattr(spec, 'inputs', [])
        if inputs:
            lines.append("📥 INPUTS:")
            for pin in inputs:
                is_exec = getattr(pin, 'is_exec', False)
                if is_exec:
                    lines.append(f"  ⚡ {getattr(pin, 'name', 'pin')}")
                else:
                    lines.append(f"  → {getattr(pin, 'name', 'pin')}: {get_pin_type_display(pin)}")
            lines.append("")
            
        # Outputs with types
        outputs = getattr(spec, 'outputs', [])
        if outputs:
            lines.append("📤 OUTPUTS:")
            for pin in outputs:
                is_exec = getattr(pin, 'is_exec', False)
                if is_exec:
                    lines.append(f"  ⚡ {getattr(pin, 'name', 'pin')}")
                else:
                    lines.append(f"  ← {getattr(pin, 'name', 'pin')}: {get_pin_type_display(pin)}")
            lines.append("")
        
        # Code snippet (first few lines)
        code = getattr(spec, 'code', "")
        line_start = getattr(spec, 'line_start', 0)
        line_end = getattr(spec, 'line_end', 0)
        if code and line_start > 0:
            lines.append(f"📝 Lines {line_start}-{line_end}:")
            code_lines = code.split('\n')[:4]
            for code_line in code_lines:
                truncated = code_line[:35] + ".." if len(code_line) > 35 else code_line
                lines.append(f"  {truncated}")
            if len(code.split('\n')) > 4:
                lines.append("  ...")
        
        return '\n'.join(lines)
        
        return '\n'.join(lines)
            
    def _create_node_for_block(self, canvas, block, x, y):
        """Legacy: Create a visual node for a code block."""
        # This is the old method, kept for compatibility
        try:
            from PyFlow.Core.NodeBase import NodeBase
            import uuid
            
            # Use stickyNote for visualization
            template = NodeBase.jsonTemplate()
            template["package"] = "PyFlowBase"
            template["type"] = "stickyNote"
            template["name"] = block.name
            template["uuid"] = str(uuid.uuid4())
            template["x"] = x
            template["y"] = y
            template["meta"]["label"] = f"{block.node_type.value}: {block.name}"
            
            # Create the node
            node = canvas._createNode(template)
            if node and hasattr(node, 'labelTextChanged'):
                # Set content
                content = f"[{block.node_type.value.upper()}]\n"
                content += f"Lines: {block.line_start}-{block.line_end}\n"
                content += f"Inputs: {', '.join(block.inputs) if block.inputs else 'None'}\n"
                content += f"Outputs: {', '.join(block.outputs) if block.outputs else 'None'}\n"
                content += "─" * 20 + "\n"
                content += block.code[:200]
                if len(block.code) > 200:
                    content += "..."
                    
        except Exception as e:
            print(f"Error creating node: {e}")
            
    def _on_block_selected(self, block):
        """Handle block selection in structure tree."""
        # Highlight corresponding lines
        for widget in self._line_widgets:
            widget.set_current(False)
            
        for line_num in range(block.line_start, block.line_end + 1):
            if line_num <= len(self._line_widgets):
                self._line_widgets[line_num-1].set_current(True)
                
        # Scroll to first line
        if block.line_start <= len(self._line_widgets):
            self.codeScrollArea.ensureWidgetVisible(
                self._line_widgets[block.line_start-1]
            )
            
    def _on_step_selected(self, step_index):
        """Handle step selection in timeline."""
        if step_index >= len(self._execution_steps):
            return
            
        step = self._execution_steps[step_index]
        
        # Highlight current line
        for widget in self._line_widgets:
            widget.set_current(False)
            
        if step.line_number <= len(self._line_widgets):
            self._line_widgets[step.line_number-1].set_current(True)
            # Set variables for this step
            self._line_widgets[step.line_number-1].set_variables(step.variables)
            
            # Scroll to line
            self.codeScrollArea.ensureWidgetVisible(
                self._line_widgets[step.line_number-1]
            )
            
        # Update variables panel
        self.variableWidget.update_variables(step.variables)
        
    def _on_line_clicked(self, line_number):
        """Handle line click - show variables at this line."""
        # Find latest step at this line
        for step in reversed(self._execution_steps):
            if step.line_number == line_number:
                self.variableWidget.update_variables(step.variables)
                break
                
    @staticmethod
    def isSingleton():
        return True
        
    @staticmethod
    def defaultDockArea():
        return QtCore.Qt.BottomDockWidgetArea
        
    @staticmethod
    def toolTip():
        return "Python Visual Debugger - Load and visualize Python code execution"
        
    @staticmethod
    def name():
        return "Python Debugger"
