class Tick(object):
    """ Element Fro Ramp Widgets___Basic U,V Attribute holder """
    def __init__(self):
        self._u = 0
        self._v = 0

    def getU(self):
        return self._u

    def getV(self):
        return self._v

    def setU(self, u):
        self._u = u

    def setV(self, v):
        self._v = v

class splineRamp(object):

    """ Ramp/Curve Editor with evaluateAt support , clamped to 0,1 in both x and y"""
    def __init__(self, bezier=True):
        self.bezier = bezier
        self.items = []

    def __getitem__(self,index):
        if index in range(0, len(self.items()) - 1):
            return self.sortedItems()[index].getV()
        else:
            return None

    @property
    def positions(self):
        return [x.getU() for x in self.sortedItems()]

    @property
    def values(self):
        return [x.getV() for x in self.sortedItems()]

    def sortedItems(self):
        itms = list(self.items)
        itms.sort(key=lambda x: x.getU())
        return itms

    def clear(self):
        self.items = []

    def addItem(self,u,v):
        item = Tick()
        item.setU(u)
        item.setV(v)
        self.items.append(item)

    def removeItem(self,item=None,index=-1):
        if item:
            if item in self.items:
                self.items.remove(item)
        elif index in range(0, len(self.items)- 1):
            self.items.remove(self.items[index])

    def setU(self, u, index=-1):
        if index in range(0, len(self.items) - 1):
            self.sortedItems()[index].setU(u)

    def setV(self, v, index=-1):
        if index in range(0, len(self.items) - 1):
            self.sortedItems()[index].setV(v)

    def evaluateAt(self, value):
        items = self.sortedItems()
        if len(items) > 1:
            if value >= items[-1].getU():
                return items[-1].getV()
            elif value <= items[0].getU():
                return items[0].getV()

            interval = len(items) - 1
            for i, x in enumerate(items):
                if value <= x.getU():
                    interval = i
                    break

            u = max(0, min(1, (((value - items[interval - 1].getU()) * (1.0 - 0.0)) / (
                items[interval].getU() - items[interval - 1].getU())) + 0.0))

            if self.bezier:
                v = self.interpolateBezier([p.getV() for p in items], 0, len(items) - 1, value)
            else:
                v = self.interpolateLinear(
                    items[interval].getV(), items[interval - 1].getV(), u)   

            return v
        elif len(items) == 1:
            return items[0].getV()
        else:
            return 0.0

    def interpolateBezier(self,coorArr, i, j, t):
        if j == 0:
            return coorArr[i]
        return self.interpolateBezier(coorArr, i, j - 1, t) * (1 - t) + self.interpolateBezier(coorArr, i + 1, j - 1, t) * t

    def interpolateLinear(self, start, end, ratio):
        v = (ratio * start + (1 - ratio) * end)
        return v   


ramp = splineRamp(bezier=True)
ramp.addItem(0.0,0.0)
ramp.addItem(0.5,0.1)
ramp.addItem(1,1.0)
print ramp.evaluateAt(0.5)
