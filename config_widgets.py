import sys
from PyQt6.QtWidgets import (QApplication, QCheckBox, QLabel, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QPushButton, QListWidget)
from base_widget import BaseWidget
from PyQt6.QtCore import Qt

from utils import load_config, save_config

class Edit_Widget(BaseWidget):
    def __init__(self, overlay, x, y):
        super().__init__(overlay, "EDIT", x, y)

        data = load_config()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

        self.setStyleSheet("""
            QWidget {
                border-radius: 10px;
                background-color: #f0f0f0; /* Gris claro de fondo */
            }
            QListWidget {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 5px;
                color: black;
            }
            QLineEdit {
                border-radius: 10px;
                background-color: white;
                padding: 5px;
                border: 1px solid #0078d7;
                color: black;
            }
            QPushButton {
                background-color: #0078d7;
                color: white;
                border-radius: 10px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #005a9e; /* Color más oscuro al pasar el mouse */
            }
            QLabel {
                color: black;
                font-weight: bold;
                font-size: 10px;
            }
            QCheckBox {
                color: black;
                font-size: 10px;
            }
        """)

        self.resize(330, 200)
        layout = QVBoxLayout()

        title = QLabel("Configuración de Widgets")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        for key, value in data.items():
            if key == "EDIT": continue
            if key == "config": continue

            h_layout = QHBoxLayout()
            label = QLabel(key)

            line_X = QLineEdit(str(value.get("x", "")))

            line_Y = QLineEdit(str(value.get("y", "")))

            Check_Enabled = QCheckBox("Enabled")
            Check_Enabled.setChecked(value.get("enabled", False))
            
            Check_Dragging = QCheckBox("Dragging")
            Check_Dragging.setChecked(value.get("dragging", False))
            
            h_layout.addWidget(label)
            h_layout.addWidget(line_X)
            h_layout.addWidget(line_Y)
            h_layout.addWidget(Check_Enabled)
            h_layout.addWidget(Check_Dragging)

            btn = QPushButton("SAVE")
            btn.clicked.connect(lambda _, k=key, x=line_X, y=line_Y, e=Check_Enabled, d=Check_Dragging: self.save_edit(k, x, y, e, d))
            h_layout.addWidget(btn)

            layout.addLayout(h_layout)

        
        btn_close = QPushButton("Cerrar")
        btn_close.clicked.connect(self.close)
        layout.addWidget(btn_close)

        self.setLayout(layout)
    
    def save_edit(self, key, line_X, line_Y, Check_Enabled, Check_Dragging):
        try:
            config = load_config()
            config[key] = {
                "x": int(line_X.text()),
                "y": int(line_Y.text()),
                "img": config.get(key, {}).get("img", "img/default.png"),
                "enabled": Check_Enabled.isChecked(),
                "dragging": Check_Dragging.isChecked()
            }
            save_config(config)
        except Exception as e:
            print(f"Error saving config from Edit_Widget: {e}")