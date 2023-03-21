# By Sebastian Raaphorst, 2023.

import sys
import random
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QColor, QBrush, QPainter
from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsRectItem


class Ball(QGraphicsEllipseItem):
    def __init__(self, index, width, height, min_r, max_r, velocity):
        self.index = index

        self.r = random.randint(min_r, max_r)
        self.start_x = random.randint(self.r, width - self.r)
        self.start_y = random.randint(self.r, height - self.r)
        super().__init__(self.start_x, self.start_y, self.r, self.r)

        self.vx = random.uniform(-velocity, velocity)
        self.vy = random.uniform(-velocity, velocity)

        color = QColor(random.randint(0, 0xffffff))
        self.setBrush(QBrush(color))

    @property
    def adj_x(self):
        return self.x() + self.start_x

    @property
    def adj_y(self):
        return self.y() + self.start_y

    def move(self):
        self.setX(self.x() + self.vx)
        self.setY(self.y() + self.vy)

    def __str__(self):
        return f'Ball id={self.index}, pos=({int(self.x())},{int(self.y())}), adj_pos=({int(self.adj_x())},{int(self.adj_y())}), velocity=({self.vx},{self.vy})'


class Scene(QGraphicsScene):
    def __init__(self, width, height):
        super().__init__(0, 0, width, height)
        self.balls = []
        self.timer = QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.tick)
        self.timer.start()

    def add_ball(self, ball):
        self.addItem(ball)
        self.balls.append(ball)

    def tick(self):
        for ball in self.balls:
            ball.move()

            if ball.adj_x <= self.sceneRect().left():
                ball.vx = -ball.vx
            if ball.adj_x + ball.boundingRect().width() >= self.sceneRect().right():
                ball.vx = -ball.vx
            if ball.adj_y <= self.sceneRect().top():
                ball.vy = -ball.vy
            if ball.adj_y + ball.boundingRect().height() >= self.sceneRect().bottom():
                ball.vy = -ball.vy


class View(QGraphicsView):
    _width = 1200
    _height = 800
    _radius_min = 20
    _radius_max = 40
    _velocity = 5
    _num_balls = 50

    def __init__(self):
        super().__init__()
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        scene = Scene(View._width, View._height)
        self.setScene(scene)

        for idx in range(View._num_balls):
            ball = Ball(idx, View._width, View._height, View._radius_min, View._radius_max, View._velocity)
            scene.add_ball(ball)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = View()
    view.show()
    sys.exit(app.exec())
