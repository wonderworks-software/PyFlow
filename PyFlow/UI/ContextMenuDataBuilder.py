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


from collections import OrderedDict


class ContextMenuDataBuilder(object):
    """docstring for ContextMenuDataBuilder."""

    def __init__(self):
        super(ContextMenuDataBuilder, self).__init__()
        self._storage = OrderedDict()
        self._menu = []

    def addSeparator(self):
        self._menu.append({"separator": True})

    def addEntry(self, name, title, callback=None, icon=None, parentEntry=None):
        if name not in self._menu:

            menu = OrderedDict()
            menu["name"] = name
            menu["title"] = title
            menu["icon"] = icon
            menu["callback"] = callback
            self._storage[name] = menu

            if parentEntry is not None and parentEntry in self._storage:
                self._storage[parentEntry]["sub_menu"] = menu
            else:
                self._menu.append(menu)
                self._storage[name] = menu

        return self

    def reset(self):
        self._storage.clear()
        self.menu.clear()

    def get(self):
        return self._menu
