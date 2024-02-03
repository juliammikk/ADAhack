import sys

from PyQt6 import uic
from functools import partial
from PyQt6.QtCore import QUrl, QRect, Qt, QCoreApplication
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow, QLabel, QLineEdit
from PyQt6.QtWidgets import (QWidget, QToolTip,
    QPushButton, QApplication)
from PyQt6.QtGui import QFont
from unidecode import unidecode
from PyQt6.uic.properties import QtWidgets, QtCore
from ipywidgets.widgets import widget
from PyQt6.QtCore import QUrl, QTimer


from llm_backend import Interface


class SoundPlayer(QWidget):
    def __init__(self):
        super().__init__()

        filename = "voice.mp3"
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
        
 
        self.layout = QVBoxLayout(self.centralwidget)
        self.play_button = QPushButton('Play', self.centralwidget)
        self.input = QLineEdit(self.centralwidget)
        self.label = QLabel(self.centralwidget)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.play_button)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.CPSBTN)
        self.LANG = 'it'
        self.CONTEXT = 'bakery.'
        self.LM = Interface(self.LANG)

        MainWindow.setCentralWidget(self.centralwidget)

    def handle_input(self):
        text = self.input.text()
        self.input.clear()
        response_eng, response_ita = self.LM.get_response(self.CONTEXT, text, self.LANG)
    
        filename = "voice.mp3"
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QUrl.fromLocalFile(filename))
        self.audio_output.setVolume(50)

        self.play_button.clicked.connect(self.player.play)
    

        self.label.setText(response_ita)

    def check_word(self, reference: str, input: str) -> (bool):
        norm_input = unidecode(input.lower())
        return norm_input == reference

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.welcome = Welcome_window()
        self.bakery = Bakery_Window()
        self.startWelcome()



    def startBakery(self):
        self.bakery.setupUI(self)
        self.bakery.CPSBTN.clicked.connect(self.startWelcome)
        self.bakery.input.returnPressed.connect(self.bakery.handle_input)


        self.show()

    def startWelcome(self):
        self.welcome.setupUI(self)
        self.welcome.ToolsBTN.clicked.connect(self.startBakery)
        self.show()



def handle_input(input, label, LM, CONTEXT, LANG, button):
    global history
    
    text = input.text()
    input.clear()
    print("step 1")
    response_eng, response_ita = LM.get_response(CONTEXT, text, LANG)
    filename = "voice.mp3"
    player = QMediaPlayer()
    audio_output = QAudioOutput()
    player.setAudioOutput(audio_output)
    player.setSource(QUrl.fromLocalFile(filename))
    audio_output.setVolume(50)
    button.clicked.connect(player.play)

    history = history + f"You: {text}\n" + f"Baker: {response_ita}\n{response_eng}\n"



    label.setText(history)
    #label.setText(f"Baker: {response_ita}\n{response_eng}")

class FlashingLineEditManager:
    def __init__(self, line_edit, validation_rule):
        self.line_edit = line_edit
        self.validation_rule = validation_rule
        self.timer = QTimer()
        self.original_stylesheet = self.line_edit.styleSheet()
        self.flashing_stylesheet = "background-color: red;"
        self.correct_stylesheet = "background-color: green;"
        self.timer.timeout.connect(self._toggle_flash)

    def _toggle_flash(self):
        if self.line_edit.styleSheet() != self.flashing_stylesheet:
            self.line_edit.setStyleSheet(self.flashing_stylesheet)
        else:
            self.line_edit.setStyleSheet(self.original_stylesheet)

    def validate_and_flash(self):
        if not self.validation_rule(self.line_edit.text()):
            # Clear the text of the line edit before starting the flash
            self.line_edit.clear()  # This line clears the text
            if not self.timer.isActive():
                self.timer.start(500)  # Start flashing with 500ms interval
        else:
            if self.timer.isActive():
                self.timer.stop()
            # Apply the correct stylesheet instead of resetting to the original
            self.line_edit.setStyleSheet(self.correct_stylesheet)

    def stop_flashing(self):
        if self.timer.isActive():
            self.timer.stop()
        self.line_edit.setStyleSheet(self.original_stylesheet)


global history
history = ''
def main():


    ##main loop here
    app = QApplication(sys.argv)

    LANG = 'it'
    CONTEXT = 'bakery.'
    LM = Interface(LANG)
    #w = MainWindow()
    window = uic.loadUi("base.ui")

    
    window.background.setStyleSheet("background-image: url(background.png)")

    line_edit_word_1 = window.findChild(QLineEdit, "word1textField")
    validation_rule_word_1 = lambda text: text.lower() == 'pane'
    flashing_manager_word_1 = FlashingLineEditManager(line_edit_word_1, validation_rule_word_1)
    line_edit_word_1.returnPressed.connect(flashing_manager_word_1.validate_and_flash)

    line_edit_word_2 = window.findChild(QLineEdit, "word2textField")
    validation_rule_word_2 = lambda text: text.lower() == 'soldi'
    flashing_manager_word_2 = FlashingLineEditManager(line_edit_word_2, validation_rule_word_2)
    line_edit_word_2.returnPressed.connect(flashing_manager_word_2.validate_and_flash)

    line_edit_word_3 = window.findChild(QLineEdit, "word3textField")
    validation_rule_word_3 = lambda text: text.lower() == 'fresca'
    flashing_manager_word_3 = FlashingLineEditManager(line_edit_word_3, validation_rule_word_3)
    line_edit_word_3.returnPressed.connect(flashing_manager_word_3.validate_and_flash)

    line_edit_word_4 = window.findChild(QLineEdit, "word4textField")
    validation_rule_word_4 = lambda text: text.lower() == 'dolce'
    flashing_manager_word_4 = FlashingLineEditManager(line_edit_word_4, validation_rule_word_4)
    line_edit_word_4.returnPressed.connect(flashing_manager_word_4.validate_and_flash)

    line_edit_word_5 = window.findChild(QLineEdit, "word5textField")
    validation_rule_word_5 = lambda text: text.lower() == 'farina'
    flashing_manager_word_5 = FlashingLineEditManager(line_edit_word_5, validation_rule_word_5)
    line_edit_word_5.returnPressed.connect(flashing_manager_word_5.validate_and_flash)


    window.userInput.returnPressed.connect(partial(handle_input, window.userInput, window.outputText, LM, CONTEXT, LANG, window.playSound))



    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()