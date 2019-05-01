

# Concept: Each object that able to populate properties view have a set of references to views.
# View can be torn off and locked to prevent being purge.
# Each properties view have a weak reference to it's owner to be able to be torn off.
class IPropertiesViewSupport(object):
    """docstring for IPropertiesViewSupport."""
    def __init__(self):
        super(IPropertiesViewSupport, self).__init__()

    def addPropertiesView(self, view):
        pass

    # TODO: remove propertiesLayout arg in future
    # work with previously added views
    def onUpdatePropertiesView(self, propertiesLayout):
        pass
