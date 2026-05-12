import psutil
from base_widget import BaseWidget
from PyQt6.QtCore import Qt


class Widget(BaseWidget):

    __posX = 100
    __posY = 200

    __enabled = False
    __draggable = False

    def __init__(self, overlay, x = __posX, y = __posY):
        super().__init__(overlay, "ram", x, y)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def update_widget(self):
        self.setText(f"RAM: {psutil.virtual_memory().percent}%")
        self.adjustSize()
    
    def widget_pos(self):
        return {"x": self.x(), "y": self.y()}
    
    def is_draggable(self):
        return self.__draggable
    
    def is_enabled(self):
        return self.__enabled