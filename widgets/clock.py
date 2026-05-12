from datetime import datetime
import locale
from base_widget import BaseWidget
from PyQt6.QtCore import Qt

import python_weather
import asyncio

class Widget(BaseWidget):

    __posX = 200
    __posY = 100

    __enabled = True
    __draggable = False

    __location = "Ciudad Victoria, MX"
    __Temp = 0
    __Desc = ""

    def __init__(self, overlay, x = __posX, y = __posY):
        x = int(overlay.width() // 2) - self.__posX # centrar horizontalmente
        super().__init__(overlay, "clock", x, y)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        weather = asyncio.run(self.get_weather())
        

    def update_widget(self):

        now = datetime.now()
        
        fecha = now.strftime("%A, %B %d, %Y")
        hora = now.strftime("%I:%M %p")
        
        estilo_html = f"""
            <div style="color: rgba(255, 255, 255, 0.9); font-family: 'Segoe UI Variable Display', 'Segoe UI', sans-serif;">
                <div style="font-size: 18pt; margin-bottom: -10px;">{fecha}</div>
                <div style="font-size: 80pt; font-weight: 500; letter-spacing: -2px;">{hora}</div>
                <div style="font-size: 14pt; opacity: 0.8;">{self.__Temp}°, {self.__Desc}</div>
            </div>
        """
        
        self.setText(estilo_html)
        self.adjustSize()

    async def get_weather(self):
        async with python_weather.Client(unit=python_weather.METRIC) as client:
            weather = await client.get(self.__location)
            self.__Temp = weather.temperature
            self.__Desc = weather.description + " " + weather.kind.emoji
            return weather
    
    def widget_pos(self):
        return {"x": self.x(), "y": self.y()}
    
    def is_draggable(self):
        return self.__draggable
    
    def is_enabled(self):
        return self.__enabled