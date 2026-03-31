import psutil
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QListWidget, QLineEdit, QPushButton, QVBoxLayout
from base_widget import BaseWidget
from PyQt6.QtCore import Qt


class Widget(BaseWidget):

    def __init__(self, overlay, x, y):
        super().__init__(overlay, "tasks", x, y)
        
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
        """)

        self.resize(250, 350)

        self.list = QListWidget()
        self.input = QLineEdit()
        self.txt = QLabel("Tareas")
        self.input.setPlaceholderText("Agregar tarea...")
        self.button = QPushButton("+")

        layout_V = QVBoxLayout()
        layout_H = QHBoxLayout()

        layout_H.addWidget(self.input)
        layout_H.addWidget(self.button)

        layout_V.addWidget(self.txt)
        layout_V.addWidget(self.list)
        layout_V.addLayout(layout_H)

        self.setLayout(layout_V)

        self.button.clicked.connect(self.add_task)
        self.input.returnPressed.connect(self.add_task)
        
        
    def update_widget(self):
        pass

    def add_task(self):
        task = self.input.text().strip()
        if task:
            self.list.addItem(task)
            self.input.clear()
            self.input.setFocus()