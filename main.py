import sys

from PyQt6.QtCore import QUrl, QRect, Qt, QCoreApplication
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow, QLabel
from PyQt6.QtWidgets import (QWidget, QToolTip,
    QPushButton, QApplication)
from PyQt6.QtGui import QFont
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

        self.play_button.clicked.connect(self.player.play)


        MainWindow.setCentralWidget(self.centralwidget)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.uiWindow = Welcome_window()
        self.uiToolTab = Bakery_Window()
        self.startUIWindow()

    def startUIToolTab(self):
        self.uiToolTab.setupUI(self)
        self.uiToolTab.CPSBTN.clicked.connect(self.startUIWindow)
        self.show()

    def startUIWindow(self):
        self.uiWindow.setupUI(self)
        self.uiWindow.ToolsBTN.clicked.connect(self.startUIToolTab)
        self.show()



def main():


    ##main loop here
    app = QApplication(sys.argv)

    w = MainWindow()





    sys.exit(app.exec())


if __name__ == '__main__':
    main()