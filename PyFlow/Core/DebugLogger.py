"""
Debug Logger for PyFlow Code Visualization

This module provides file-based logging since terminal output may not be visible.
All debug messages are written to a log file that can be viewed in VS Code.

Usage:
    from PyFlow.Core.DebugLogger import log, log_error, log_section, get_log_path

    log("Message here")
    log_error("Error message")
    log_section("Section Title")
"""

import os
import datetime
from pathlib import Path

# Log file location - in PyFlow root directory
_LOG_DIR = Path(__file__).parent.parent.parent  # PyFlow root
_LOG_FILE = _LOG_DIR / "pyflow_debug.log"

def _ensure_log_file():
    """Ensure log directory exists."""
    _LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

def get_log_path() -> str:
    """Get the path to the log file."""
    return str(_LOG_FILE)

def clear_log():
    """Clear the log file."""
    _ensure_log_file()
    with open(_LOG_FILE, 'w', encoding='utf-8') as f:
        f.write(f"=== PyFlow Debug Log ===\n")
        f.write(f"Started: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Log file: {_LOG_FILE}\n")
        f.write("=" * 50 + "\n\n")

def log(message: str, prefix: str = ""):
    """Write a message to the log file."""
    _ensure_log_file()
    timestamp = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
    with open(_LOG_FILE, 'a', encoding='utf-8') as f:
        if prefix:
            f.write(f"[{timestamp}] {prefix}: {message}\n")
        else:
            f.write(f"[{timestamp}] {message}\n")
        f.flush()  # Ensure immediate write

def log_error(message: str):
    """Log an error message."""
    log(message, prefix="ERROR")

def log_warning(message: str):
    """Log a warning message."""
    log(message, prefix="WARN")

def log_success(message: str):
    """Log a success message."""
    log(message, prefix="OK")

def log_section(title: str):
    """Log a section header."""
    _ensure_log_file()
    with open(_LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"\n{'=' * 50}\n")
        f.write(f"  {title}\n")
        f.write(f"{'=' * 50}\n")

def log_dict(data: dict, title: str = "Data"):
    """Log a dictionary in readable format."""
    log_section(title)
    for key, value in data.items():
        log(f"  {key}: {value}")

def log_list(items: list, title: str = "List"):
    """Log a list in readable format."""
    log_section(title)
    for i, item in enumerate(items):
        log(f"  [{i}] {item}")

def log_node_info(node, spec=None):
    """Log detailed node information."""
    log(f"Node: {node}")
    if hasattr(node, '_rawNode'):
        raw = node._rawNode
        log(f"  Type: {raw.__class__.__name__}")
        log(f"  Name: {raw.getName() if hasattr(raw, 'getName') else 'N/A'}")
    if hasattr(node, 'UIinputs'):
        log(f"  Inputs: {list(node.UIinputs.keys())}")
    if hasattr(node, 'UIoutputs'):
        log(f"  Outputs: {list(node.UIoutputs.keys())}")
    if spec:
        log(f"  Spec: {spec.name if hasattr(spec, 'name') else spec}")

def log_connection(src_node, src_pin, tgt_node, tgt_pin, success: bool):
    """Log a connection attempt."""
    status = "✓" if success else "✗"
    log(f"  {status} Connect: {src_pin} -> {tgt_pin}")

# Initialize log on import
if not _LOG_FILE.exists():
    clear_log()
