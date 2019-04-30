from collections import defaultdict
__REGISTERED_TOOLS = defaultdict(set)


def REGISTER_TOOL(packageName, toolInstance):
    registeredToolNames = [tool.name() for tool in __REGISTERED_TOOLS[packageName]]
    if toolInstance.name() not in registeredToolNames:
        __REGISTERED_TOOLS[packageName].add(toolInstance)
        print("registering", packageName, "tools")


def GET_TOOLS():
    return __REGISTERED_TOOLS.items()
