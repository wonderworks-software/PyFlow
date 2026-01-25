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

"""
Minimap Overlay Widget - GTA5-style overlay minimap for PyFlow canvas.
Displays a small, semi-transparent overview in the bottom-right corner.
"""

from qtpy import QtCore
from qtpy import QtGui
from qtpy.QtWidgets import *


class MinimapOverlay(QWidget):
    """A compact overlay minimap widget positioned in the corner of the canvas.
    
    Similar to GTA 5's minimap - small, semi-transparent, and always visible
    in the corner without taking up dock space.
    """
    
    # Minimap size
    MINIMAP_WIDTH = 180
    MINIMAP_HEIGHT = 120
    MARGIN = 10
    CORNER_RADIUS = 8
    
    def __init__(self, canvas, parent=None):
        super(MinimapOverlay, self).__init__(parent)
        self._canvas = canvas
        self._isDragging = False
        self._isHovered = False
        self._opacity = 0.7
        self._hoverOpacity = 0.95
        
        # Fixed size for the minimap
        self.setFixedSize(self.MINIMAP_WIDTH, self.MINIMAP_HEIGHT)
        
        # Make it stay on top and be transparent to non-interactive areas
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        
        # Update timer
        self._updateTimer = QtCore.QTimer(self)
        self._updateTimer.timeout.connect(self.update)
        self._updateTimer.start(50)  # 20 FPS refresh
        
        # Cache for node bounds
        self._cachedBounds = QtCore.QRectF()
        self._lastNodeCount = 0
        
    def setCanvas(self, canvas):
        """Set the source canvas to mirror."""
        self._canvas = canvas
        
    def _getNodeBounds(self):
        """Calculate the bounding rectangle of all visible nodes."""
        if self._canvas is None:
            return QtCore.QRectF()
            
        try:
            nodes = self._canvas.nodes
        except:
            return QtCore.QRectF()
            
        if not nodes:
            return QtCore.QRectF()
        
        # Check if we need to recalculate
        visibleNodes = [n for n in nodes.values() if n.isVisible()]
        if len(visibleNodes) == 0:
            return QtCore.QRectF()
            
        bounds = QtCore.QRectF()
        for node in visibleNodes:
            rect = node.sceneBoundingRect()
            if bounds.isNull():
                bounds = rect
            else:
                bounds = bounds.united(rect)
        
        # Add padding
        padding = 50
        bounds.adjust(-padding, -padding, padding, padding)
        
        return bounds
        
    def _getViewportRect(self):
        """Get the current viewport rectangle in scene coordinates."""
        if self._canvas is None:
            return QtCore.QRectF()
        try:
            viewRect = self._canvas.viewport().rect()
            topLeft = self._canvas.mapToScene(viewRect.topLeft())
            bottomRight = self._canvas.mapToScene(viewRect.bottomRight())
            return QtCore.QRectF(topLeft, bottomRight)
        except:
            return QtCore.QRectF()
            
    def _sceneToMinimap(self, sceneRect, bounds):
        """Convert scene coordinates to minimap coordinates."""
        if bounds.isNull() or bounds.width() == 0 or bounds.height() == 0:
            return QtCore.QRectF()
            
        # Available drawing area (with padding for border)
        drawArea = QtCore.QRectF(4, 4, self.width() - 8, self.height() - 8)
        
        # Calculate scale to fit bounds in draw area
        scaleX = drawArea.width() / bounds.width()
        scaleY = drawArea.height() / bounds.height()
        scale = min(scaleX, scaleY)
        
        # Center the content
        scaledWidth = bounds.width() * scale
        scaledHeight = bounds.height() * scale
        offsetX = drawArea.x() + (drawArea.width() - scaledWidth) / 2
        offsetY = drawArea.y() + (drawArea.height() - scaledHeight) / 2
        
        # Transform the rectangle
        x = offsetX + (sceneRect.x() - bounds.x()) * scale
        y = offsetY + (sceneRect.y() - bounds.y()) * scale
        w = sceneRect.width() * scale
        h = sceneRect.height() * scale
        
        return QtCore.QRectF(x, y, w, h)
        
    def _minimapToScene(self, minimapPos, bounds):
        """Convert minimap coordinates to scene coordinates."""
        if bounds.isNull() or bounds.width() == 0 or bounds.height() == 0:
            return QtCore.QPointF()
            
        # Available drawing area
        drawArea = QtCore.QRectF(4, 4, self.width() - 8, self.height() - 8)
        
        # Calculate scale
        scaleX = drawArea.width() / bounds.width()
        scaleY = drawArea.height() / bounds.height()
        scale = min(scaleX, scaleY)
        
        # Center offset
        scaledWidth = bounds.width() * scale
        scaledHeight = bounds.height() * scale
        offsetX = drawArea.x() + (drawArea.width() - scaledWidth) / 2
        offsetY = drawArea.y() + (drawArea.height() - scaledHeight) / 2
        
        # Inverse transform
        sceneX = bounds.x() + (minimapPos.x() - offsetX) / scale
        sceneY = bounds.y() + (minimapPos.y() - offsetY) / scale
        
        return QtCore.QPointF(sceneX, sceneY)
        
    def paintEvent(self, event):
        """Paint the minimap overlay."""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        
        # Set opacity based on hover state
        opacity = self._hoverOpacity if self._isHovered else self._opacity
        painter.setOpacity(opacity)
        
        # Draw rounded background
        bgPath = QtGui.QPainterPath()
        bgPath.addRoundedRect(QtCore.QRectF(0, 0, self.width(), self.height()), 
                              self.CORNER_RADIUS, self.CORNER_RADIUS)
        painter.fillPath(bgPath, QtGui.QColor(20, 20, 25, 230))
        
        # Draw border
        painter.setPen(QtGui.QPen(QtGui.QColor(60, 60, 70), 1))
        painter.drawPath(bgPath)
        
        if self._canvas is None:
            painter.end()
            return
            
        # Get bounds including viewport
        nodeBounds = self._getNodeBounds()
        viewportRect = self._getViewportRect()
        
        # Combine node bounds with viewport to ensure viewport is always visible
        if nodeBounds.isNull():
            bounds = viewportRect
        elif viewportRect.isNull():
            bounds = nodeBounds
        else:
            bounds = nodeBounds.united(viewportRect)
            
        if bounds.isNull():
            painter.end()
            return
            
        # Draw nodes
        try:
            nodes = self._canvas.nodes
            for uid, node in nodes.items():
                if not node.isVisible():
                    continue
                    
                nodeRect = node.sceneBoundingRect()
                minimapRect = self._sceneToMinimap(nodeRect, bounds)
                
                if minimapRect.isNull():
                    continue
                
                # Ensure minimum size for visibility
                if minimapRect.width() < 3:
                    minimapRect.setWidth(3)
                if minimapRect.height() < 2:
                    minimapRect.setHeight(2)
                
                # Color based on node state
                if node.isSelected():
                    color = QtGui.QColor(255, 180, 80)
                    borderColor = QtGui.QColor(255, 200, 120)
                elif hasattr(node, 'isCommentNode') and node.isCommentNode:
                    color = QtGui.QColor(60, 60, 60, 150)
                    borderColor = QtGui.QColor(80, 80, 80)
                else:
                    color = QtGui.QColor(70, 130, 180)
                    borderColor = QtGui.QColor(100, 160, 210)
                
                painter.fillRect(minimapRect, color)
                painter.setPen(QtGui.QPen(borderColor, 0.5))
                painter.drawRect(minimapRect)
        except:
            pass
            
        # Draw viewport rectangle
        if not viewportRect.isNull():
            vpMinimap = self._sceneToMinimap(viewportRect, bounds)
            if not vpMinimap.isNull():
                # Viewport fill
                painter.fillRect(vpMinimap, QtGui.QColor(100, 150, 255, 30))
                # Viewport border
                painter.setPen(QtGui.QPen(QtGui.QColor(100, 150, 255), 2))
                painter.drawRect(vpMinimap)
        
        painter.end()
        
    def _navigateToPoint(self, minimapPos):
        """Navigate the canvas to center on the clicked minimap position."""
        if self._canvas is None:
            return
            
        # Get current bounds
        nodeBounds = self._getNodeBounds()
        viewportRect = self._getViewportRect()
        
        if nodeBounds.isNull():
            bounds = viewportRect
        elif viewportRect.isNull():
            bounds = nodeBounds
        else:
            bounds = nodeBounds.united(viewportRect)
            
        if bounds.isNull():
            return
            
        # Convert minimap position to scene position
        scenePos = self._minimapToScene(minimapPos, bounds)
        
        # Navigate canvas to this position
        try:
            currentCenter = viewportRect.center()
            delta = currentCenter - scenePos
            scale = self._canvas.currentViewScale()
            self._canvas.pan(delta * scale)
        except:
            pass
            
    def enterEvent(self, event):
        """Handle mouse enter - increase opacity."""
        self._isHovered = True
        self.update()
        super(MinimapOverlay, self).enterEvent(event)
        
    def leaveEvent(self, event):
        """Handle mouse leave - decrease opacity."""
        self._isHovered = False
        self._isDragging = False
        self.update()
        super(MinimapOverlay, self).leaveEvent(event)
        
    def mousePressEvent(self, event):
        """Handle mouse press for navigation."""
        if event.button() == QtCore.Qt.LeftButton:
            self._isDragging = True
            self._navigateToPoint(event.pos())
        super(MinimapOverlay, self).mousePressEvent(event)
        
    def mouseMoveEvent(self, event):
        """Handle mouse drag for continuous navigation."""
        if self._isDragging:
            self._navigateToPoint(event.pos())
        super(MinimapOverlay, self).mouseMoveEvent(event)
        
    def mouseReleaseEvent(self, event):
        """Handle mouse release."""
        if event.button() == QtCore.Qt.LeftButton:
            self._isDragging = False
        super(MinimapOverlay, self).mouseReleaseEvent(event)
        
    def wheelEvent(self, event):
        """Forward wheel events to canvas for zooming."""
        if self._canvas:
            self._canvas.wheelEvent(event)
