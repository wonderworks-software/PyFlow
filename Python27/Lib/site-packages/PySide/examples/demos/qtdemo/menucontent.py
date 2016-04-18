from PySide import QtCore

from colors import Colors
from demoitem import DemoItem
from demoitemanimation import DemoItemAnimation
from demotextitem import DemoTextItem
from headingitem import HeadingItem


class MenuContentItem(DemoItem):
    def __init__(self, el, scene=None, parent=None):
        super(MenuContentItem, self).__init__(scene, parent)

        self.name = str(el.attribute('name'))
        self.heading = None
        self.description1 = None
        self.description2 = None

        readme_dir = QtCore.QFileInfo(__file__).dir()
        readme_dir.cdUp()

        if str(el.tagName()) != 'demos':
            readme_dir.cdUp()
            readme_dir.cd(el.attribute('dirname'))

        self.readmePath = readme_dir.absoluteFilePath('README')

    def prepare(self):
        if not self.prepared:
            self.prepared= True
            self.createContent()

    def animationStopped(self, id):
        if self.name == Colors.rootMenuName:
            # Optimization hack.
            return

        if id == DemoItemAnimation.ANIM_OUT:
            # Free up some memory
            self.heading = None
            self.description1 = None
            self.description2 = None
            self.prepared = False

    def loadDescription(self, startPara, nrPara):
        readme = QtCore.QFile(self.readmePath)
        if not readme.open(QtCore.QFile.ReadOnly):
            Colors.debug("- MenuContentItem.loadDescription: Could not load:", self.readmePath)
            return ""

        in_str = QtCore.QTextStream(readme)
        # Skip a certain number of paragraphs.
        while startPara:
            if not in_str.readLine():
                startPara -= 1

        # Read in the number of wanted paragraphs.
        result = ''
        line = in_str.readLine()
        while True:
            result += line + " "
            line = in_str.readLine()
            if not line:
                nrPara -= 1
                line = "<br><br>" + in_str.readLine()

            if nrPara == 0 or in_str.atEnd():
                break

        return Colors.contentColor + result

    def createContent(self):
        # Create the items.
        self.heading = HeadingItem(self.name, self.scene(), self)
        para1 = self.loadDescription(0, 1)
        if not para1:
            para1 = Colors.contentColor + "Could not load description. Ensure that the documentation for Qt is built."
        bgcolor = Colors.sceneBg1.darker(200)
        bgcolor.setAlpha(100)
        self.description1 = DemoTextItem(para1, Colors.contentFont(),
                Colors.heading, 500, self.scene(), self,
                DemoTextItem.STATIC_TEXT)
        self.description2 = DemoTextItem(self.loadDescription(1, 2),
                Colors.contentFont(), Colors.heading, 250, self.scene(), self,
                DemoTextItem.STATIC_TEXT)

        # Place the items on screen.
        self.heading.setPos(0, 3)
        self.description1.setPos(0, self.heading.pos().y() + self.heading.boundingRect().height() + 10)
        self.description2.setPos(0, self.description1.pos().y() + self.description1.boundingRect().height() + 15)

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 500, 350)
