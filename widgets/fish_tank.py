import random

from base_widget import BaseWidget
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget, QVBoxLayout, QColorDialog
from PyQt6.QtCore import QTimer, Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QPixmap, QPainter, QFont, QPen, QTransform
import math, os

FOLDER_IMGS = "./img"

class Fish(QLabel):

    def __init__(self, fish_img, speed, parent, base_y):
        super().__init__(parent)

        self.fish_img = fish_img
        self.vel = speed
        self.base_y = base_y

        self.x = 0
        self.t = random.random() * 10

        # cargar imagen
        self.original_pixmap = QPixmap(fish_img).scaled(
                64, 64, 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
        )

        self.setPixmap(self.original_pixmap)
        self.adjustSize()

        self.update_direction()

    def animate(self):

        # movimiento horizontal
        self.x += self.vel

        parent_width = self.parent().width()

        if self.x <= 0 or self.x >= parent_width - self.width():
            self.vel = -self.vel
            self.update_direction()

        # onda vertical
        self.t += 0.1
        amplitude = 15

        y = self.base_y + amplitude * math.sin(self.t)

        self.move(int(self.x), int(y))
    
    def update_direction(self):

        if self.vel > 0:
            transform = QTransform().scale(-1, 1)
            flipped = self.original_pixmap.transformed(transform)
            self.setPixmap(flipped)
        else:
            self.setPixmap(self.original_pixmap)

class Widget(BaseWidget):

    def __init__(self, overlay, x, y):
        super().__init__(overlay, "fish_tank", x, y)

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.resize(overlay.width(), 600)

        self.fishes = []

        # timer de animación
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)  # ~60 FPS

        button = QPushButton("FISH ➕", self)
        button.setGeometry(self.width() - 100, self.height() - 100, 80, 40)
        button.clicked.connect(lambda: self.draw_fish())

        btn = QPushButton("FISH ➖", self)
        btn.setGeometry(self.width() - 100, self.height() - 150, 80, 40)
        btn.clicked.connect(self.delete_fish)

        self.load_fishes()

    def draw_fish(self):
        id = random.randint(1000, 9999)

        widget = Window(id=id)
        widget.setParent(self)
        widget.setWindowFlags(Qt.WindowType.Widget)

        widget.fish_saved.connect(self.load_fishes)  # conexión

        widget.move(self.width() - 350, 200)
        widget.setVisible(True)

    def add_fish(self, fish_img, speed, base_y):
        fish = Fish(fish_img, speed, self, base_y)
        fish.show()
        self.fishes.append(fish)

    def delete_fish(self):
        if self.fishes:
            fish = self.fishes.pop()
            fish.deleteLater()

    def load_fishes(self, fish_id=None):
        imgs = os.listdir(FOLDER_IMGS)
        only_fish = [img for img in imgs if img.endswith("_fish.png")]

        if fish_id is not None and f"{fish_id}_fish.png" in only_fish:
            path = os.path.join(FOLDER_IMGS, f"{fish_id}_fish.png")
            base_y = random.randint(50, 550)
            speed = random.uniform(1, 4)
            self.add_fish(path, speed, base_y)  
        else:
            for fish in only_fish:
                path = os.path.join(FOLDER_IMGS, fish)
                base_y = random.randint(50, 550)
                speed = random.uniform(1, 4)
                self.add_fish(path, speed, base_y)

    def animate(self):
        for fish in self.fishes:
            fish.animate()

    def update_widget(self):
        pass

class PaintWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.canvas_size = 128
        self.setFixedSize(self.canvas_size, self.canvas_size)

        self.pixmap = QPixmap(self.canvas_size, self.canvas_size)
        self.pixmap.fill(Qt.GlobalColor.transparent)

        self.last_point = QPoint()
        self.drawing = False

        self.pen_color = Qt.GlobalColor.black
        self.pen_size = 3

    def paintEvent(self, event):
        painter = QPainter(self)

        # fondo para ver la transparencia
        painter.fillRect(self.rect(), Qt.GlobalColor.lightGray)

        painter.drawPixmap(0, 0, self.pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.last_point = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if self.drawing:
            painter = QPainter(self.pixmap)

            pen = QPen(
                self.pen_color,
                self.pen_size,
                Qt.PenStyle.SolidLine,
                Qt.PenCapStyle.RoundCap,
                Qt.PenJoinStyle.RoundJoin
            )

            painter.setPen(pen)

            current_point = event.position().toPoint()
            painter.drawLine(self.last_point, current_point)

            self.last_point = current_point
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = False


class Window(QWidget):

    fish_saved = pyqtSignal(int)

    def __init__(self, id=None):
        super().__init__()

        self.setWindowTitle("Mini Paint 128x128")
        self.resize(220, 260)

        self.paint = PaintWidget()
        self.id = id

        btn_color = QPushButton("Color")
        btn_save = QPushButton("Guardar")
        btn_clear = QPushButton("Limpiar")
        btn_cerrar = QPushButton("Cerrar")

        btn_color.clicked.connect(self.choose_color)
        btn_save.clicked.connect(self.save_image)
        btn_clear.clicked.connect(self.clear_canvas)
        btn_cerrar.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(self.paint, alignment=Qt.AlignmentFlag.AlignCenter)

        buttons = QHBoxLayout()

        buttons.addWidget(btn_color)
        buttons.addWidget(btn_save)
        buttons.addWidget(btn_clear)
        buttons.addWidget(btn_cerrar)

        layout.addLayout(buttons)

        self.setLayout(layout)

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.paint.pen_color = color

    def save_image(self):
        path = f"./img/{self.id}_fish.png"
        self.paint.pixmap.save(path)

        self.fish_saved.emit(self.id)
        self.close()

    def clear_canvas(self):
        self.paint.pixmap.fill(Qt.GlobalColor.transparent)
        self.paint.update()