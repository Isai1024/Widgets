import sys
import os
import importlib
import json
from PyQt6.QtWidgets import QApplication, QWidget, QMenu, QSystemTrayIcon
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtGui import QGuiApplication

from utils import load_config, save_config

from config_widgets import Edit_Widget

FOLDER = "widgets"

class Overlay(QWidget):
    def __init__(self):
        super().__init__()
        self.widgets_list = [] 
        self.available_plugins = {}
        self.config = load_config()
        self.editing_mode = False 

        self.screen = QApplication.primaryScreen().geometry()
        self.setGeometry(self.screen)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.Tool | 
            Qt.WindowType.WindowStaysOnBottomHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.load_plugins()
        self.setup_tray()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_widgets)
        self.timer.start(1000)

    def setup_tray(self):
        """Configura el icono al lado del reloj de Windows"""
        self.tray_icon = QSystemTrayIcon(self)
        
        self.tray_icon.setIcon(QIcon("img/icon.png") or QIcon.fromTheme("applications-system")) 
        
        self.tray_menu = QMenu()
        self.refresh_tray_menu()
        
        # Detectar clic derecho
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()
        
        # Detectar clic izquierdo
        self.tray_icon.activated.connect(self.on_tray_activated)
        self.tray_icon.show()

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.show_quick_settings()

    def show_quick_settings(self):
        """Menú que aparece al dar clic izquierdo"""
        menu = QMenu()

        menu.addAction("Control de Widgets").setEnabled(False)
        menu.addSeparator()

        label = "Edición de widgets"
        action = menu.addAction(label)
        action.triggered.connect(self.toggle_editing)
        
        menu.addSeparator()
        
        from PyQt6.QtGui import QCursor
        menu.exec(QCursor.pos())

    def toggle_editing(self):
        self.editing_mode = not self.editing_mode

        widget = Edit_Widget(self, 500, 200)
        widget.setParent(self)
        widget.setWindowFlags(Qt.WindowType.Widget)
        widget.move(500, 200)
        widget.setVisible(True)

    def refresh_tray_menu(self):
        """Actualiza la lista de widgets en el menú del icono"""
        self.tray_menu.clear()
        
        header = self.tray_menu.addAction("Configuración Rápida")
        header.setEnabled(False)
        self.tray_menu.addSeparator()

        for name, widget in self.available_plugins.items():
            if name == "EDIT": continue
            action = QAction(name, self)
            action.setIcon(QIcon(self.config.get(name, {}).get("img", "img/default.png")))
            action.setCheckable(True)
            action.setChecked(self.config.get(name, {}).get("enabled", True))
            action.triggered.connect(lambda checked, n=name: self.toggle_widget(n, checked))
            self.tray_menu.addAction(action)

        self.tray_menu.addSeparator()
        
        quit_action = self.tray_menu.addAction("Cerrar Todo")
        quit_action.triggered.connect(QApplication.instance().quit)

    def load_plugins(self):
        if not os.path.exists(FOLDER): return
        y_offset = 100
        __config = self.config.get("config", {})
        
        for file in os.listdir(FOLDER):
            if file.endswith(".py") and file != "__init__.py":
                name = file[:-3]
                try:
                    module = importlib.import_module(f"{FOLDER}.{name}")
                    widget_class = module.Widget

                    if name == "clock" and __config.get("startup", False):
                        plugin = self.config.get(name, {})
                        
                        self.config[name] = {
                            "x": int(self.screen.width() /2) - 100,
                            "y": 100,
                            "img": plugin.get("img", f"img/{name}.png" if not plugin.get("img") else "img/default.png"),
                            "enabled": plugin.get("enabled", True),
                            "dragging": plugin.get("dragging", False)
                        }
                        self.config['config']['startup'] = False
                                     
                    pos = self.config.get(name, {"x": 100, "y": y_offset, "img": f"img/{name}.png", "enabled": True, "dragging": True})
                    y_offset += 50

                    self.config[name] = pos

                    widget = widget_class(self, pos["x"], pos["y"])
                    widget.setParent(self)
                    widget.setWindowFlags(Qt.WindowType.Widget)
                    widget.move(pos["x"], pos["y"])
                    
                    save_config(self.config)   
                    self.widgets_list.append(widget)
                    self.available_plugins[name] = widget
                    widget.setVisible(pos.get("enabled", True))
                except Exception as e:
                    print(f"Error cargando {name}: {e}")

    def toggle_widget(self, name, enabled):
        widget = self.available_plugins[name]
        widget.setVisible(enabled)
        
        if name not in self.config: 
            self.config[name] = {"x": widget.x(), "y": widget.y()}
        
        self.config[name]["enabled"] = enabled
        save_config(self.config)

    def update_widgets(self):
        for widget in self.widgets_list:
            if widget.isVisible() and hasattr(widget, "update_widget"):
                widget.update_widget()

if __name__ == "__main__":
    app = QApplication.instance() or QApplication(sys.argv)
    
    app.setQuitOnLastWindowClosed(False)

    overlay = Overlay()
    overlay.show()
    sys.exit(app.exec())