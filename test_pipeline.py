"""Test the enhanced Code → Nodes pipeline."""
import sys
sys.path.insert(0, r'c:\Users\ADMIN\Downloads\Pyflow2.4\PyFlow')

from PyFlow.Core.PythonCodeAnalyzer import CodeToNodesConverter

# Test code - find max in array
test_code = """
arr = [10, 324, 45]
res = arr[0]
for i in range(1, len(arr)):
    if arr[i] > res:
        res = arr[i]
print(res)
"""

print("=" * 60)
print("TESTING ENHANCED CODE-TO-NODES PIPELINE")
print("=" * 60)

# Create converter and analyze
converter = CodeToNodesConverter()
context = converter.analyze_code(test_code)

print("\n=== STEP 1: AST PARSING ===")
for block in context.ast_info:
    print(f"  {block.node_type.value}: {block.name}")
    print(f"    Inputs: {block.inputs}, Outputs: {block.outputs}")

print("\n=== STEP 2-3: EXECUTION TRACE ===")
print(f"Total events collected: {len(context.execution_events)}")
for event in context.execution_events[:10]:
    if event['event_type'] in ['assignment', 'loop_enter', 'branch', 'call']:
        print(f"  Line {event['line']}: [{event['event_type']}] {event['code'][:40]}")

print("\n=== STEP 4: DEPENDENCY GRAPH ===")
dep = context.dependency_graph
print(f"Variables: {list(dep['nodes'].keys())}")
print(f"Execution order: {dep['execution_order']}")
print("Data dependencies:")
for edge in dep['edges']:
    print(f"  {edge[0]} → {edge[1]} ({edge[2]})")
if dep['loops']:
    print(f"Loops: {dep['loops'][0]}")  # Just first loop
if dep['branches']:
    print(f"Branches: {dep['branches'][0]}")  # Just first branch

print("\n=== RUNTIME VALUES (GROUND TRUTH) ===")
for name, info in context.final_variable_values.items():
    print(f"  {name}: {info['value']} ({info['type']})")

print("\n=== STEP 5: NODE GENERATION ===")
# Test with fallback (LLM might not be available)
nodes = converter.generate_nodes_with_llm(test_code, use_fallback=True)
print(f"Generated {len(nodes)} nodes:")
for i, node in enumerate(nodes):
    if hasattr(node, 'name'):
        # VisualNode object
        print(f"  [{i}] {node.node_type.value}: {node.name}")
        print(f"      Inputs: {[p.name for p in node.inputs]}")
        print(f"      Outputs: {[p.name for p in node.outputs]}")
    elif isinstance(node, dict):
        # Dict format
        print(f"  [{i}] {node.get('type', node.get('name', 'unknown'))}")
        inputs = node.get('inputs', [])
        outputs = node.get('outputs', [])
        if inputs:
            print(f"      Inputs: {[p.get('name', p) if isinstance(p, dict) else p for p in inputs]}")
        if outputs:
            print(f"      Outputs: {[p.get('name', p) if isinstance(p, dict) else p for p in outputs]}")

print("\n" + "=" * 60)
print("PIPELINE TEST COMPLETE!")
print("=" * 60)
