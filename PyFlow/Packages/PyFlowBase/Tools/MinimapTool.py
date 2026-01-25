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


from qtpy import QtCore
from qtpy import QtGui
from qtpy.QtWidgets import *

from PyFlow.UI.Tool.Tool import DockTool


class MinimapWidget(QGraphicsView):
    """A minimap widget that shows an overview of the entire graph canvas.
    
    Displays all nodes as simplified rectangles and shows the current viewport
    as a highlighted rectangle that can be dragged to navigate.
    """
    
    def __init__(self, parent=None):
        super(MinimapWidget, self).__init__(parent)
        self._sourceCanvas = None
        self._viewportRect = None
        self._isDragging = False
        self._updateTimer = None
        
        # Setup the minimap scene
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)
        
        # Minimap styling
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setInteractive(True)
        self.setDragMode(QGraphicsView.NoDrag)
        
        # Background color
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(30, 30, 30)))
        
        # Viewport rectangle item (represents what user is currently seeing)
        self._viewportRectItem = QGraphicsRectItem()
        self._viewportRectItem.setPen(QtGui.QPen(QtGui.QColor(100, 150, 255), 2))
        self._viewportRectItem.setBrush(QtGui.QBrush(QtGui.QColor(100, 150, 255, 40)))
        self._viewportRectItem.setZValue(1000)  # Always on top
        self._scene.addItem(self._viewportRectItem)
        
        # Setup update timer for periodic refresh
        self._updateTimer = QtCore.QTimer(self)
        self._updateTimer.timeout.connect(self.refreshMinimap)
        self._updateTimer.start(100)  # Update every 100ms
        
        # Node items cache
        self._nodeItems = {}
        
    def setSourceCanvas(self, canvas):
        """Set the source canvas to mirror in the minimap."""
        self._sourceCanvas = canvas
        self.refreshMinimap()
        
    def refreshMinimap(self):
        """Refresh the minimap to reflect current canvas state."""
        if self._sourceCanvas is None:
            return
            
        # Clear old node items but keep viewport rect
        for item in list(self._nodeItems.values()):
            self._scene.removeItem(item)
        self._nodeItems.clear()
        
        # Get all nodes from the canvas
        try:
            nodes = self._sourceCanvas.nodes
        except:
            return
            
        if not nodes:
            return
            
        # Calculate bounds of all nodes
        allRects = []
        for uid, node in nodes.items():
            if node.isVisible():
                rect = node.sceneBoundingRect()
                allRects.append(rect)
                
                # Create simplified node representation
                nodeItem = QGraphicsRectItem(rect)
                
                # Color based on node type/state
                if node.isSelected():
                    nodeItem.setBrush(QtGui.QBrush(QtGui.QColor(255, 200, 100)))
                    nodeItem.setPen(QtGui.QPen(QtGui.QColor(255, 220, 150), 1))
                elif hasattr(node, 'isCommentNode') and node.isCommentNode:
                    nodeItem.setBrush(QtGui.QBrush(QtGui.QColor(80, 80, 80, 150)))
                    nodeItem.setPen(QtGui.QPen(QtGui.QColor(100, 100, 100), 1))
                else:
                    # Use node's header color if available
                    color = QtGui.QColor(70, 100, 150)
                    if hasattr(node, '_rawNode') and hasattr(node._rawNode, 'headerColor'):
                        hc = node._rawNode.headerColor
                        if hc:
                            color = QtGui.QColor(hc[0], hc[1], hc[2])
                    nodeItem.setBrush(QtGui.QBrush(color))
                    nodeItem.setPen(QtGui.QPen(color.lighter(120), 1))
                
                self._scene.addItem(nodeItem)
                self._nodeItems[uid] = nodeItem
        
        # Update viewport rectangle
        self._updateViewportRect()
        
        # Fit the entire scene in view with some padding
        if allRects:
            bounds = QtCore.QRectF()
            for r in allRects:
                bounds = bounds.united(r)
            # Add padding
            bounds.adjust(-100, -100, 100, 100)
            # Include viewport rect in bounds
            viewportSceneRect = self._getSourceViewportRect()
            if viewportSceneRect:
                bounds = bounds.united(viewportSceneRect)
            self.fitInView(bounds, QtCore.Qt.KeepAspectRatio)
        
    def _getSourceViewportRect(self):
        """Get the viewport rectangle from source canvas in scene coordinates."""
        if self._sourceCanvas is None:
            return None
        try:
            # Get the visible rectangle in scene coordinates
            viewRect = self._sourceCanvas.viewport().rect()
            topLeft = self._sourceCanvas.mapToScene(viewRect.topLeft())
            bottomRight = self._sourceCanvas.mapToScene(viewRect.bottomRight())
            return QtCore.QRectF(topLeft, bottomRight)
        except:
            return None
            
    def _updateViewportRect(self):
        """Update the viewport rectangle position and size."""
        viewportRect = self._getSourceViewportRect()
        if viewportRect:
            self._viewportRectItem.setRect(viewportRect)
            
    def _navigateToPoint(self, scenePos):
        """Navigate the source canvas to center on the given scene position."""
        if self._sourceCanvas is None:
            return
            
        # Convert minimap scene position to source canvas scene position
        # (they share the same coordinate system)
        try:
            # Get current viewport rect
            viewportRect = self._getSourceViewportRect()
            if viewportRect is None:
                return
                
            # Calculate the delta to move
            currentCenter = viewportRect.center()
            delta = currentCenter - scenePos
            
            # Apply the pan
            scale = self._sourceCanvas.currentViewScale()
            self._sourceCanvas.pan(delta * scale)
            
            # Refresh to show new position
            self._updateViewportRect()
        except Exception as e:
            pass
            
    def mousePressEvent(self, event):
        """Handle mouse press for navigation."""
        if event.button() == QtCore.Qt.LeftButton:
            self._isDragging = True
            scenePos = self.mapToScene(event.pos())
            self._navigateToPoint(scenePos)
        super(MinimapWidget, self).mousePressEvent(event)
        
    def mouseMoveEvent(self, event):
        """Handle mouse drag for continuous navigation."""
        if self._isDragging:
            scenePos = self.mapToScene(event.pos())
            self._navigateToPoint(scenePos)
        super(MinimapWidget, self).mouseMoveEvent(event)
        
    def mouseReleaseEvent(self, event):
        """Handle mouse release."""
        if event.button() == QtCore.Qt.LeftButton:
            self._isDragging = False
        super(MinimapWidget, self).mouseReleaseEvent(event)
        
    def wheelEvent(self, event):
        """Forward wheel events to source canvas for zooming."""
        if self._sourceCanvas:
            # Forward the wheel event to source canvas
            self._sourceCanvas.wheelEvent(event)
            self.refreshMinimap()
        else:
            super(MinimapWidget, self).wheelEvent(event)


class MinimapTool(DockTool):
    """Dock tool that provides a minimap overview of the graph canvas.
    
    Shows all nodes in a bird's-eye view with a viewport indicator
    that can be dragged to navigate the main canvas.
    """
    
    def __init__(self):
        super(MinimapTool, self).__init__()
        self.setMinimumSize(QtCore.QSize(200, 150))
        self.setMaximumHeight(300)
        
        # Create content widget
        self.content = QWidget()
        self.content.setObjectName("minimapToolContent")
        
        # Layout
        self.verticalLayout = QVBoxLayout(self.content)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        
        # Minimap widget
        self.minimapWidget = MinimapWidget(self)
        self.minimapWidget.setObjectName("minimapWidget")
        self.verticalLayout.addWidget(self.minimapWidget)
        
        # Refresh button
        self.refreshButton = QPushButton("Refresh")
        self.refreshButton.setMaximumHeight(25)
        self.refreshButton.clicked.connect(self.onRefresh)
        self.verticalLayout.addWidget(self.refreshButton)
        
        self.setWidget(self.content)
        
    def onShow(self):
        super(MinimapTool, self).onShow()
        # Connect to the canvas
        if self.pyFlowInstance:
            canvas = self.pyFlowInstance.getCanvas()
            self.minimapWidget.setSourceCanvas(canvas)
            
    def onRefresh(self):
        """Manual refresh of the minimap."""
        self.minimapWidget.refreshMinimap()
        
    @staticmethod
    def isSingleton():
        return True
        
    @staticmethod
    def defaultDockArea():
        return QtCore.Qt.RightDockWidgetArea
        
    @staticmethod
    def toolTip():
        return "Graph overview minimap - click and drag to navigate"
        
    @staticmethod
    def name():
        return "Minimap"
