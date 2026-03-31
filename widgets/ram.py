import psutil
from base_widget import BaseWidget
from PyQt6.QtCore import Qt


class Widget(BaseWidget):

    def __init__(self, overlay, x, y):
        super().__init__(overlay, "ram", x, y)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def update_widget(self):
        self.setText(f"RAM: {psutil.virtual_memory().percent}%")
        self.adjustSize()