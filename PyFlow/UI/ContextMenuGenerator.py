from Qt.QtWidgets import QMenu
from Qt.QtWidgets import QAction


class ContextMenuGenerator(object):
    """docstring for ContextMenuGenerator."""
    def __init__(self, menuDataBuilder):
        super(ContextMenuGenerator, self).__init__()
        self.builder = menuDataBuilder

    def createMenuEntry(self, parentMenu, menuEntryData):
        if "separator" in menuEntryData:
            parentMenu.addSeparator()
            return
        icon = menuEntryData['icon']
        if "sub_menu" in menuEntryData:
            subMenuData = menuEntryData["sub_menu"]
            subMenu = parentMenu.addMenu(menuEntryData["title"])
            if icon is not None:
                subMenu.setIcon(icon)
            self.createMenuEntry(subMenu, subMenuData)
        else:
            action = parentMenu.addAction(menuEntryData['title'])
            if icon is not None:
                action.setIcon(icon)
            action.triggered.connect(menuEntryData['callback'])

    def generate(self):
        menuData = self.builder.get()
        menu = QMenu()
        for menuEntry in menuData:
            self.createMenuEntry(menu, menuEntry)
        return menu
