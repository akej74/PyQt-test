import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from DiceSimulatorUI import Ui_MainWindow
from random import randint
import time

class DiceThread(QtCore.QThread):
    dice_throw_signal = QtCore.pyqtSignal(int)

    def __init__(self, dices, throws_per_second):
        super().__init__()
        self.dices = dices
        self.throws_per_second = throws_per_second

    def __del__(self):
        self.wait()

    def run(self):
        print("Run method!")
        print(self.dices)
        print(self.throws_per_second)
        self.dice_throw_signal.emit(dicethrow(self.dices))


def dicethrow(dices):

    #for t in range(5):
    dice_sum = 0
    for d in range(dices):
        current_dice = dice()
        dice_sum += current_dice

    #time.sleep(0.5)
    return dice_sum

def dice():
    return randint(1, 6)


class DiceSimulator(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set the default value of the spinbox to 1
        self.ui.spinBoxDices.setValue(1)

        # Connect the "button start click" to the "button_start_clicked" method
        self.ui.buttonStart.clicked.connect(self.button_start_clicked)


    def button_start_clicked(self):
        thread = DiceThread(self.ui.spinBoxDices.value(), self.ui.spinBoxThrows.value())
        thread.dice_throw_signal.connect(self.ui.lcdNumberDiceOutcome.display)
        thread.start()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    win = DiceSimulator()
    win.show()

    sys.exit(app.exec_())
