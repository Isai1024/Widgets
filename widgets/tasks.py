from PyQt6.QtWidgets import QHBoxLayout, QMenu, QLabel, QListWidget, QLineEdit, QPushButton, QVBoxLayout
from base_widget import BaseWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from utils import load_config, save_config
import time

TASK_DATA = "data/tasks.json"

class Widget(BaseWidget):

    def __init__(self, overlay, x, y):
        super().__init__(overlay, "tasks", x, y)
        
        self.tasks = load_config(TASK_DATA)

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

        self.list.mousePressEvent = self.handle_list_click
        self.button.clicked.connect(self.add_task)
        self.input.returnPressed.connect(self.add_task)
        self.load_tasks()

    def update_widget(self):
        pass

    def handle_list_click(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            item = self.list.itemAt(event.pos())
            if item:
                menu = QMenu()
                menu.addAction("Opciones").setEnabled(False)
                menu.addSeparator()

                action = menu.addAction("Eliminar")
                action.setIcon(QIcon("img/delete.png") or QIcon.fromTheme("edit-delete"))
                action.triggered.connect(lambda: self.remove_task(item))

                from PyQt6.QtGui import QCursor
                menu.exec(QCursor.pos())

    def load_tasks(self):
        self.list.clear()
        for task in self.tasks.keys():
            self.list.addItem(task)

    def add_task(self):
        task = self.input.text().strip()
        if task:
            self.list.addItem(task)
            self.input.clear()
            self.input.setFocus()

            self.tasks[task] = {
                "timestamp": int(time.time())
            }

            save_config(self.tasks, TASK_DATA)

    def remove_task(self, item):
        self.list.takeItem(self.list.row(item))
        del self.tasks[item.text()]
        save_config(self.tasks, TASK_DATA)