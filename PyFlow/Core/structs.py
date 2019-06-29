class Tick(object):
    """ Element For Ramp Widget Basic U and V Attribute holder """
    def __init__(self):
        self._u = 0
        self._v = 0
        self._selected = False

    def getU(self):
        return self._u

    def getV(self):
        return self._v

    def setU(self, u):
        self._u = u

    def setV(self, v):
        self._v = v

    def setSelected(self, selected):
        self._selected = selected

    def isSelected(self):
        return self._selected


class splineRamp(object):
    """ Ramp/Curve Editor with evaluateAt support , clamped to 0-1 in both x and y"""
    def __init__(self):
        self.items = []

    def __getitem__(self, index):
        if len(self.items) and index in range(0, len(self.items)):
            return self.sortedItems()[index]
        else:
            return None

    @property
    def uValues(self):
        return [x.getU() for x in self.sortedItems()]

    @property
    def yValues(self):
        return [x.getV() for x in self.sortedItems()]

    def sortedItems(self):
        itms = list(self.items)
        itms.sort(key=lambda x: x.getU())
        return itms

    def clear(self):
        self.items = []

    def addItem(self, u, v):
        item = Tick()
        item.setU(u)
        item.setV(v)
        self.items.append(item)
        return(item)

    def removeItem(self, item=None, index=-1):
        if item:
            if item in self.items:
                self.items.remove(item)
        elif index in range(0, len(self.items) - 1):
            self.items.remove(self.items[index])

    def setU(self, u, index=-1):
        if index in range(0, len(self.items) - 1):
            self.sortedItems()[index].setU(u)

    def setV(self, v, index=-1):
        if index in range(0, len(self.items) - 1):
            self.sortedItems()[index].setV(v)

    def evaluateAt(self, value, bezier=False):
        items = self.sortedItems()
        if len(items) > 1:
            if value >= items[-1].getU():
                return items[-1].getV()
            elif value <= items[0].getU():
                return items[0].getV()

            if bezier:
                if isinstance(items[0].getV(), list):
                    v = []
                    for i in range(len(items[0].getV())):
                        v.append(self.interpolateBezier([p.getV()[i] for p in items], 0, len(items) - 1, value))
                else:
                    v = self.interpolateBezier([p.getV() for p in items], 0, len(items) - 1, value)
            else:
                interval = len(items) - 1
                for i, x in enumerate(items):
                    if value <= x.getU():
                        interval = i
                        break

                u = max(0, min(1, (((value - items[interval - 1].getU()) * (1.0 - 0.0)) / (
                    items[interval].getU() - items[interval - 1].getU())) + 0.0))

                start = items[interval].getV()
                end = items[interval - 1].getV()
                if isinstance(start, list) and isinstance(end, list) and len(start) == len(end):
                    v = []
                    for i, element in enumerate(start):
                        v.append(self.interpolateLinear(start[i], end[i], u))
                elif not isinstance(start, list) or not isinstance(end, list):
                    v = self.interpolateLinear(start, end, u)

            return v
        elif len(items) == 1:
            return items[0].getV()
        else:
            return 0.0

    def interpolateBezier(self, coorArr, i, j, t):
        if j == 0:
            return coorArr[i]
        return self.interpolateBezier(coorArr, i, j - 1, t) * (1 - t) + self.interpolateBezier(coorArr, i + 1, j - 1, t) * t

    def interpolateLinear(self, start, end, ratio):
        return (ratio * start + (1 - ratio) * end)

if __name__ == '__main__':
    ramp = splineRamp()
    ramp.addItem(0.1, [0.0, 0.0, 0.0])
    ramp.addItem(1.0, [1.0, 1.0, 1.0])

    print(ramp.evaluateAt(0.5, bezier=True))
