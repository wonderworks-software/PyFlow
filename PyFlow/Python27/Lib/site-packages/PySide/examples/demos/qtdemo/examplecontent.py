from PySide import QtCore, QtGui, QtXml

from colors import Colors
from demoitem import DemoItem
from demoitemanimation import DemoItemAnimation
from demotextitem import DemoTextItem
from headingitem import HeadingItem
from imageitem import ImageItem


class ExampleContent(DemoItem):
    def __init__(self, name, scene=None, parent=None):
        super(ExampleContent, self).__init__(scene, parent)

        # Prevent a circular import.
        from menumanager import MenuManager
        self._menu_manager = MenuManager.instance()

        self.name = name
        self.heading = None
        self.description = None
        self.screenshot = None

    def prepare(self):
        if not self.prepared:
            self.prepared = True
            self.createContent()

    def animationStopped(self, id):
        if id == DemoItemAnimation.ANIM_OUT:
            # Free up some memory.
            self.heading = None
            self.description = None
            self.screenshot = None
            self.prepared = False

    def loadDescription(self):
        ba = self._menu_manager.getHtml(self.name)

        exampleDoc = QtXml.QDomDocument()
        exampleDoc.setContent(ba, False)

        paragraphs = exampleDoc.elementsByTagName('p')
        if paragraphs.length() < 1:
            Colors.debug("- ExampleContent.loadDescription(): Could not load description:", self._menu_manager.info[self.name].get('docfile'))

        description = Colors.contentColor + "Could not load description. Ensure that the documentation for Qt is built."
        for p in range(paragraphs.length()):
            description = self.extractTextFromParagraph(paragraphs.item(p))
            if self.isSummary(description):
                break

        return Colors.contentColor + description

    def isSummary(self, text):
        re = QtCore.QRegExp("(In )?((The|This) )?(%s )?.*(tutorial|example|demo|application)" % self.name, QtCore.Qt.CaseInsensitive)

        return ('[' not in text) and (re.indexIn(text) >= 0)

    def extractTextFromParagraph(self, parentNode):
        description = ''
        node = parentNode.firstChild()

        while not node.isNull():
            if node.isText():
                description += Colors.contentColor + node.nodeValue()
            elif node.hasChildNodes():
                if node.nodeName() == 'b':
                    beginTag = '<b>'
                    endTag = '</b>'
                elif node.nodeName() == 'a':
                    beginTag = Colors.contentColor
                    endTag = '</font>'
                elif node.nodeName() == 'i':
                    beginTag = '<i>'
                    endTag = '</i>'
                elif node.nodeName() == 'tt':
                    beginTag = '<tt>'
                    endTag = '</tt>'
                else:
                    beginTag = endTag = ''

                description += beginTag + self.extractTextFromParagraph(node) + endTag

            node = node.nextSibling()

        return description

    def createContent(self):
        # Create the items.
        self.heading = HeadingItem(self.name, self.scene(), self)
        self.description = DemoTextItem(self.loadDescription(),
                Colors.contentFont(), Colors.heading, 500, self.scene(), self)
        imgHeight = 340 - int(self.description.boundingRect().height()) + 50
        self.screenshot = ImageItem(QtGui.QImage.fromData(self._menu_manager.getImage(self.name)), 550, imgHeight, self.scene(), self)

        # Place the items on screen.
        self.heading.setPos(0, 3)
        self.description.setPos(0, self.heading.pos().y() + self.heading.boundingRect().height() + 10)
        self.screenshot.setPos(0, self.description.pos().y() + self.description.boundingRect().height() + 10)

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 500, 100)
