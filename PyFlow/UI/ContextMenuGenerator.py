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


from qtpy.QtWidgets import QMenu


class ContextMenuGenerator(object):
    """docstring for ContextMenuGenerator."""

    def __init__(self, menuDataBuilder):
        super(ContextMenuGenerator, self).__init__()
        self.builder = menuDataBuilder

    def __createMenuEntry(self, parentMenu, menuEntryData):
        if "separator" in menuEntryData:
            parentMenu.addSeparator()
            return
        icon = menuEntryData["icon"]
        if "sub_menu" in menuEntryData:
            subMenuData = menuEntryData["sub_menu"]
            subMenu = parentMenu.addMenu(menuEntryData["title"])
            if icon is not None:
                subMenu.setIcon(icon)
            self.__createMenuEntry(subMenu, subMenuData)
        else:
            action = parentMenu.addAction(menuEntryData["title"])
            if icon is not None:
                action.setIcon(icon)
            action.triggered.connect(menuEntryData["callback"])

    def generate(self):
        menuData = self.builder.get()
        menu = QMenu()
        for menuEntry in menuData:
            self.__createMenuEntry(menu, menuEntry)
        return menu
