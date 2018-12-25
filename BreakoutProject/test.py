import sys
import os.path

from PyQt5.QtWidgets import (QApplication,
                            QPushButton,
                            QVBoxLayout,
                            QStackedLayout,
                            QWidget,
                            QDesktopWidget,
                            QMessageBox)
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtGui import QPainter, QImage, QBrush, QPalette, QFont, QColor
from PyQt5.QtCore import Qt, QRectF, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist

from common import BallState, Size


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.screen = QDesktopWidget().screenGeometry()
        self.setFixedSize(self.screen.width(), self.screen.height() - 70)
        self.move(0, 0)

        self.started = False
        self.paused = False
        self.left = False
        self.right = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.setWindowTitle('Breakout')

        self.main_menu = QWidget(self)
        self.game_widget = QWidget(self)
        self.game_widget.setMouseTracking(True)
        self.game_widget.mouseMoveEvent = self.mouse_move_event
        self.mouse_x = None

        palette = QPalette()
        palette.setBrush(self.backgroundRole(),
                         QBrush(QImage(os.path.join('images', 'space.jpg'))))
        self.setPalette(palette)

        self.stacked = QStackedLayout(self)
        self.stacked.addWidget(self.game_widget)
        self.set_main_menu()
        self.stacked.setCurrentWidget(self.main_menu)

        self.showFullScreen()

    def start(self):
        pass

    def tick(self):
        pass

    def mouse_move_event(self, event):
        pass

    def quit(self):
        reply = QMessageBox.question(self, 'Quit', 'Do you really want to quit the game?', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            APP.quit()

    def set_main_menu(self):
        vbox = QVBoxLayout(self.main_menu)
        self.add_button('Start', self.start, vbox)
        self.add_button('Quit', self.quit, vbox)

        vbox.setAlignment(Qt.AlignCenter)
        self.stacked.addWidget(self.main_menu)

    @staticmethod
    def add_button(text, callback, layout, alignment=Qt.AlignCenter):
        button = QPushButton(text)
        button.setFixedSize(400, 50)
        button.pressed.connect(callback)
        button.setStyleSheet(
            'QPushButton {'
            'font-size: 20px;'
            'color: rgb(255, 215, 0);'
            '}'
            'QPushButton:focus {'
            'background-color: rgb(0, 0, 255, 20);'
            '}')
        button.setAutoDefault(True)
        layout.addWidget(button, alignment=alignment)
        return button


if __name__ == '__main__':
    APP = QApplication(sys.argv)
    WINDOW = Window()
    APP.setOverrideCursor(Qt.BlankCursor)
    APP.exec_()
