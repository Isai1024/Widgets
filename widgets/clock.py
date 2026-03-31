from datetime import datetime
from base_widget import BaseWidget
from PyQt6.QtCore import Qt


class Widget(BaseWidget):

    def __init__(self, overlay, x, y):
        super().__init__(overlay, "clock", x, y)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def update_widget(self):
        self.setText(datetime.now().strftime("%I:%M:%S"))
        self.adjustSize()