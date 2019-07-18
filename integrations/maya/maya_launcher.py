from PyFlow.App import PyFlow

if PyFlow.appInstance is None:
    instance = PyFlow.instance()
    instance.show()
