from collections import defaultdict
__REGISTERED_TOOLS = defaultdict(list)


def REGISTER_TOOL(packageName, toolClass):
    registeredToolNames = [tool.name() for tool in __REGISTERED_TOOLS[packageName]]
    if toolClass.name() not in registeredToolNames:
        __REGISTERED_TOOLS[packageName].append(toolClass)
        toolClass.packageName = packageName
        print("registering", packageName, "tools")


def GET_TOOLS():
    return __REGISTERED_TOOLS
