import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from DiceSimulatorUI import Ui_MainWindow
from random import randint

class DiceThread(QtCore.QThread):
    def __init__(self):
        super.__init__()

    def __del__(self):
        self.wait()

    def run(self):


class DiceSimulator(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.buttonStart.clicked.connect(self.button_start_clicked)

    def button_start_clicked(self):
        self.ui.lcdNumberDiceOutcome.display(dicethrow(self.ui.spinBoxDices.value()))


def dicethrow(dices):
    dice_sum = 0

    for d in range(dices):
        current_dice = dice()
        dice_sum += current_dice

    return dice_sum

def dice():
    return randint(1, 6)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    win = DiceSimulator()
    win.show()

    sys.exit(app.exec_())
