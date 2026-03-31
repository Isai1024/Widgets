from datetime import datetime
from base_widget import BaseWidget
from PyQt6.QtCore import Qt


class Widget(BaseWidget):

    def __init__(self, overlay, x, y):
        super().__init__(overlay, "clock", x, y)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def update_widget(self):
        now = datetime.now()
        
        fecha = now.strftime("%A, %b %d")
        hora = now.strftime("%H:%M") 
        
        estilo_html = f"""
            <div style="color: rgba(255, 255, 255, 0.9); font-family: 'Segoe UI Variable Display', 'Segoe UI', sans-serif;">
                <div style="font-size: 18pt; margin-bottom: -10px;">{fecha}</div>
                <div style="font-size: 80pt; font-weight: 500; letter-spacing: -2px;">{hora}</div>
                <div style="font-size: 14pt; opacity: 0.8;">26°, Partly Cloudy</div>
            </div>
        """
        
        self.setText(estilo_html)
        self.adjustSize()