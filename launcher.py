from PyFlow import(
    INITIALIZE,
    GET_PACKAGES
)


from PyFlow.Core import(
    GraphBase,
    PinBase,
    NodeBase
)

INITIALIZE()
packages = GET_PACKAGES()
lib = packages['BasePackage'].GetFunctionLibraries()["MathLib"]
pins = packages['BasePackage'].GetPinClasses()

# g = GraphBase("Test")

# mathNodes = []
# foos = lib.getFunctions()
# for fooName, foo in foos:
#     n = NodeBase.initializeFromFunction(foo, g)
#     mathNodes.append(n)

print(pins)
