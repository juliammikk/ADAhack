import sys

from PyQt6.QtCore import QUrl, QRect, Qt, QCoreApplication, QPropertyAnimation, QSequentialAnimationGroup, pyqtProperty
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow, QLabel, QLineEdit
from PyQt6.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication)
from PyQt6.QtGui import QFont, QColor
from PyQt6.uic.properties import QtWidgets, QtCore
from ipywidgets.widgets import widget


class SoundPlayer(QWidget):
    def __init__(self):
        super().__init__()

        filename = "temp2.mp3"
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QUrl.fromLocalFile(filename))
        self.audio_output.setVolume(50)
        # player.play()

        self.play_button = QPushButton('Play')

        layout = QVBoxLayout()
        layout.addWidget(self.play_button)
        self.setLayout(layout)

        self.play_button.clicked.connect(self.player.play)


    def play_sound(self):
        self.player.play()


class FlashingLineEdit(QLineEdit):
    def __init__(self, parent=None, validation_rule=None):
        super().__init__(parent)
        self.validation_rule = validation_rule  # Custom validation rule passed as a lambda function
        self.original_palette = self.palette()
        self.setup_animation()
        self.textChanged.connect(self.validate_input)  # Connect textChanged signal to validation slot

    def setup_animation(self):
        self.animation_group = QSequentialAnimationGroup(self)

        # Flash in
        self.flash_in = QPropertyAnimation(self, b"flashColor")
        self.flash_in.setDuration(250)
        self.flash_in.setStartValue(QColor("white"))
        self.flash_in.setEndValue(QColor("red"))

        # Flash out
        self.flash_out = QPropertyAnimation(self, b"flashColor")
        self.flash_out.setDuration(250)
        self.flash_out.setStartValue(QColor("red"))
        self.flash_out.setEndValue(QColor("white"))

        self.animation_group.addAnimation(self.flash_in)
        self.animation_group.addAnimation(self.flash_out)
        self.animation_group.setLoopCount(3)

    @pyqtProperty(QColor)
    def flashColor(self):
        return self.palette().color(self.backgroundRole())

    @flashColor.setter
    def flashColor(self, color):
        palette = self.palette()
        palette.setColor(self.backgroundRole(), color)
        self.setPalette(palette)

    def start_flashing(self):
        if not self.animation_group.state() == QPropertyAnimation.State.Running:
            self.animation_group.start()

    def validate_input(self):
        if self.validation_rule and not self.validation_rule(self.text()):
            self.start_flashing()
        else:
            self.animation_group.stop()  # Stop flashing if input is valid
            self.setPalette(self.original_palette)  # Reset to original palette


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def center(self):

        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):

        self.resize(350, 250)
        self.center()

        self.setWindowTitle('Center')


        QToolTip.setFont(QFont('SansSerif', 10))

        self.setToolTip('This is a <b>QWidget</b> widget')

        btn = QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(50, 50)

        self.show()



#####
class Welcome_window(object):
    def setupUI(self, MainWindow):
        MainWindow.setGeometry(50, 50, 400, 450)
        MainWindow.setFixedSize(400, 450)
        MainWindow.setWindowTitle("UIWindow")
        self.centralwidget = QWidget(MainWindow)
        # mainwindow.setWindowIcon(QtGui.QIcon('PhotoIcon.png'))
        self.ToolsBTN = QPushButton('Bakery', self.centralwidget)
        self.ToolsBTN.move(50, 350)
        self.label = QLabel(self.centralwidget)
        self.label.setText("Welcome to Italy! \n Where do you want to go?")


        MainWindow.setCentralWidget(self.centralwidget)


class Bakery_Window(object):
    def setupUI(self, MainWindow):
        MainWindow.setGeometry(50, 50, 400, 450)
        MainWindow.setFixedSize(400, 450)
        MainWindow.setWindowTitle("UIToolTab")
        self.centralwidget = QWidget(MainWindow)
        self.CPSBTN = QPushButton("Back to welcome", self.centralwidget)
        self.CPSBTN.move(100, 350)

        filename = "temp2.mp3"
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QUrl.fromLocalFile(filename))
        self.audio_output.setVolume(50)
        # player.play()

        self.play_button = QPushButton('Play', self.centralwidget)
        validation_rule = lambda text: text.strip() == "aaaaa"
        self.input = FlashingLineEdit(self.centralwidget, validation_rule=validation_rule)

        MainWindow.setCentralWidget(self.centralwidget)

    def handle_input(self):
        text_input = self.input.text()
        self.input.clear()
        print(text_input)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.welcome = Welcome_window()
        self.bakery = Bakery_Window()
        self.startWelcome()

    def startBakery(self):
        self.bakery.setupUI(self)
        self.bakery.CPSBTN.clicked.connect(self.startWelcome)
        self.bakery.play_button.clicked.connect(self.bakery.player.play)
        self.bakery.input.returnPressed.connect(self.bakery.handle_input)

        self.show()

    def startWelcome(self):
        self.welcome.setupUI(self)
        self.welcome.ToolsBTN.clicked.connect(self.startBakery)
        self.show()



def main():


    ##main loop here
    app = QApplication(sys.argv)
    w = MainWindow()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
