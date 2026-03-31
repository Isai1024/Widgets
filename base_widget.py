from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from utils import load_config, save_config

class BaseWidget(QLabel):

    def __init__(self, overlay, name, x, y):
        super().__init__("")

        self.overlay = overlay
        self.name = name
        self.CONFIG = {}

        self.move(x, y)

        self.setFont(QFont("Segoe UI", 20))
        self.setStyleSheet("color:white;")

        self.drag = False

    def mousePressEvent(self, event):
        self.CONFIG = load_config().get(self.name, {})

        isDraggingEnabled = self.CONFIG.get("dragging", False)
        if event.button() == Qt.MouseButton.LeftButton and isDraggingEnabled:
            self.drag = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.drag:
            new_pos = self.mapToParent(event.pos() - self.offset)
            self.move(new_pos)

    def mouseReleaseEvent(self, event):
        self.drag = False

        pos = self.pos()

        if self.name not in self.overlay.config:
            self.overlay.config[self.name] = {}

        self.overlay.config[self.name]["x"] = pos.x()
        self.overlay.config[self.name]["y"] = pos.y()
        self.overlay.config[self.name]["img"] = self.CONFIG.get("img", "img/default.png")
        self.overlay.config[self.name]["enabled"] = self.isVisible()
        self.overlay.config[self.name]["dragging"] = self.CONFIG.get("dragging", False)

        save_config(self.overlay.config)