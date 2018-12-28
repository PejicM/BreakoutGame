import sys
import os.path

from PyQt5.QtWidgets import (QApplication,
                            QPushButton,
                            QVBoxLayout,
                            QStackedLayout,
                            QWidget,
                            QDesktopWidget,
                            QMessageBox)
from PyQt5.QtCore import QUrl, QSize
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtGui import QPainter, QImage, QBrush, QPalette, QFont, QColor
from PyQt5.QtCore import Qt, QRectF, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist

from common import BallState, Size
from game import GameOnePlayer, GameTwoPlayers

from key_notifier import KeyNotifier


class Window(QWidget):
    def __init__(self):
        super().__init__()


class WindowOnePlayer(Window):
    def __init__(self):
        super().__init__()

        self.screen = QDesktopWidget().screenGeometry()
        self.setFixedSize(self.screen.width(), self.screen.height() - 70)
        self.move(0, 0)

        self.game_mode = 1              # indikator da li se igra sa jednim ili dva igraca

        self.started = False
        self.paused = False

        self.left1 = False
        self.right1 = False
        self.left2 = False
        self.right2 = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.setWindowTitle('Breakout')

        self.main_menu = QWidget(self)
        self.game_widget = QWidget(self)
        self.game_widget.setMouseTracking(True)
        self.mouse_x = None

        self.key_notifier = KeyNotifier()
        self.key_notifier.key_signal.connect(self.__update_position__)
        self.key_notifier.start()

        o_image = QImage(os.path.join('images', 'space.jpg'))
        s_image = o_image.scaled(QSize(self.screen.width(), self.screen.height()))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(10, QBrush(s_image))  # 10 = Windowrole
        self.setPalette(palette)

        self.game = 0
        self.painter = QPainter()

        self.stacked = QStackedLayout(self)
        self.stacked.addWidget(self.game_widget)
        self.set_main_menu()
        self.stacked.setCurrentWidget(self.main_menu)

        self.showFullScreen()

    def start1(self):
        self.game = GameOnePlayer(Size(self.width(), self.height()))
        self.left1 = self.right1 = False
        self.change_current_widget(self.game_widget)
        self.started = True
        self.timer.start(12)

    def start2(self):
        self.game = GameTwoPlayers(Size(self.width(), self.height()))
        self.left1 = self.right1 = False
        self.left2 = self.right2 = False
        self.change_current_widget(self.game_widget)
        self.started = True
        self.timer.start(12)

    def restart(self):
        if self.game_mode == 1:
            reply = QMessageBox.question(self, 'Restart', 'Your score: %s. Do you want to restart?' % self.game.player.score,
                                     QMessageBox.Yes | QMessageBox.No)
        else:
            reply = QMessageBox.question(self, 'Restart',
                                         'Player 1 score: %s.' % self.game.player1.score,
                                         'Player 2 score: %s.' % self.game.player2.score,
                                         QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.start1()
        else:
            self.change_current_widget(self.main_menu)

    def change_current_widget(self, widget):
        self.stacked.setCurrentWidget(widget)
        self.update()

    def tick(self):
        if self.game.game_over:
            self.restart()
            self.timer.stop()
        if self.game.won:
            self.notify_win()
            self.timer.stop()

        if self.game_mode == 1:
            turn_rate = 1 if self.right1 else -1 if self.left1 else 0
            self.game.tick(turn_rate)
        else:
            turn_rate1 = 1 if self.right1 else -1 if self.left1 else 0
            turn_rate2 = 1 if self.right2 else -1 if self.left2 else 0
            self.game.tick(turn_rate1, turn_rate2)

        self.repaint()

    def notify_win(self):
        if self.game_mode == 1:
            QMessageBox.information(self, 'Win', 'You win. Your score: %s'
                                    % self.game.player.score)
        else:
            QMessageBox.information(self, 'Win', 'You win. Player 1 score: %s' % self.game.player1.score,
                                    'Player 2 score: %s' % self.game.player2.score)
        self.started = False
        self.change_current_widget(self.main_menu)

    def quit(self):
        APP.quit()

    def set_main_menu(self):
        v_box = QVBoxLayout(self.main_menu)
        self.add_button('One Player Game', self.start1, v_box)
        self.add_button('Two Player Game', self.start2, v_box)
        self.add_button('Quit', self.quit, v_box)

        v_box.setAlignment(Qt.AlignCenter)
        self.stacked.addWidget(self.main_menu)

    #def mousePressEvent(self, event):
        #self.game.release_ball()

    def keyPressEvent(self, event):
        """
            SPACE -> release ball
            ESC   -> pause
            P     -> pause/continue
            Q     -> quit
            One player game -> moving on arrows
            Two player game -> moving on ASDW and arrows
        """
        key = event.key()
        self.key_notifier.add_key(event.key())
        if self.game_mode == 1:
            self.left1 = key == Qt.Key_Left
            self.right1 = key == Qt.Key_Right
        else:
            self.left1 = key == Qt.Key_A
            self.right1 = key == Qt.Key_D
            self.left2 = key == Qt.Key_Left
            self.right2 = key == Qt.Key_Right

        if key == Qt.Key_Space:
            self.game.release_ball()

        if key == Qt.Key_Escape:
            self.timer.stop()
            self.started = False
            self.change_current_widget(self.main_menu)

        if key == Qt.Key_P:
            self.paused = not self.paused
            if self.paused:
                self.timer.stop()
            else:
                self.timer.start()

        if key == Qt.Key_Q:
            self.quit()

    def keyReleaseEvent(self, event):
        key = event.key()
        self.key_notifier.rem_key(event.key())
        if self.game_mode == 1:
            if key == Qt.Key_Left:
                self.left1 = False
            elif key == Qt.Key_Right:
                self.right1 = False
        else:
            if key == Qt.Key_A:
                self.left1 = False
            elif key == Qt.Key_D:
                self.right1 = False
            elif key == Qt.Key_Left:
                self.left2 = False
            elif key == Qt.Key_Right:
                self.right2 = False

    def __update_position__(self, key):
        if key == Qt.Key_Right:
            self.game.paddle2.move(1)
            self.game.normalize_paddle_location()
        elif key == Qt.Key_Left:
            self.game.paddle2.move(-1)
            self.game.normalize_paddle_location()

        if key == Qt.Key_D:
            self.game.paddle1.move(1)
            self.game.normalize_paddle_location()
        elif key == Qt.Key_A:
            self.game.paddle1.move(-1)
            self.game.normalize_paddle_location()

    def paintEvent(self, event):
        self.painter.begin(self)
        self.draw()
        self.painter.end()

    def draw(self):
        """ Function draws all the objects inside game window
        DODATI NEKI LOGO"""
        self.painter.setRenderHint(self.painter.Antialiasing)
        self.painter.setFont(QFont('Times New Roman', 20))
        self.painter.setPen(QColor('silver'))

        if not self.started:
            # neki logo
            return

        game = self.game

        life_img = QImage(os.path.join('images', 'lifebonus.png')).scaled(
            QSize(30, 30))  # resize Image to widgets size
        draw_x = 60
        draw_y = 30

        if self.game.__class__ == GameOnePlayer:
            self.game_mode = 1
            self.painter.drawText(0, 20, 'Player score: %s' % str(self.game.player.score))

            for _ in range(self.game.player.lives):
                self.painter.drawImage(draw_x, draw_y, life_img)
                draw_x -= life_img.width()
        else:
            self.game_mode = 2
            self.painter.drawText(0, 20, 'Player 1 score: %s' % str(self.game.player1.score))
            self.painter.drawText(self.screen.width() - 220, 20, 'Player 2 score: %s' % str(self.game.player2.score))

            for _ in range(self.game.player1.lives):
                self.painter.drawImage(draw_x, draw_y, life_img)
                draw_x -= life_img.width()

            draw_x = self.screen.width() - 220 + 57
            for _ in range(self.game.player2.lives):
                self.painter.drawImage(draw_x, draw_y, life_img)
                draw_x -= life_img.width()

        self.painter.drawLine(game.frame.left, game.border_line, game.frame.right, game.border_line)

        if self.game.game_over:
            return

        self.draw_game_objects()

    def draw_game_objects(self):
        """Function draw all the objects in the game"""
        for obj in self.game.get_objects():
            self.painter.drawImage(QRectF(*obj.location, obj.frame.width, obj.frame.height),
                                   QImage(obj.get_image()))

    @staticmethod
    def add_button(text, callback, layout, alignment=Qt.AlignCenter):
        button = QPushButton(text)
        button.setFixedSize(400, 50)
        button.pressed.connect(callback)
        button.setStyleSheet(
            'QPushButton {'
            'font-size: 20px;'
            'background-color: transparent;'
            'color: rgb(0, 0, 0);'
            '}'
            'QPushButton:focus {'
            'opacity: 0.5;'
            'background-color: rgba(179, 179, 255,0.3);'
            '}')
        button.setAutoDefault(True)
        layout.addWidget(button, alignment=alignment)
        return button


if __name__ == '__main__':
    APP = QApplication(sys.argv)
    WINDOW = WindowOnePlayer()
    APP.setOverrideCursor(Qt.BlankCursor)
    APP.exec_()
