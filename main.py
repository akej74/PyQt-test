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
    print("Current dice sum " + str(dice_sum))
    return dice_sum

def dice():
    return randint(1, 6)


class DiceSimulator(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.thread = DiceThread(self.ui.spinBoxDices.value(), self.ui.spinBoxThrows.value())

        # Set the default value of the spinbox to 1
        self.ui.spinBoxDices.setValue(1)

        # Disable "Stop" button
        self.ui.buttonStop.setEnabled(False)

        # Connect signals to slots
        self.ui.buttonStart.clicked.connect(self.button_start_clicked)
        self.ui.buttonStop.clicked.connect(self.button_stop_clicked)
        self.thread.dice_throw_signal.connect(self.ui.lcdNumberDiceOutcome.display)

    def button_start_clicked(self):

        # Disable "Start" and enable "Stop" button to prevent more that one thread to be started
        self.ui.buttonStart.setEnabled(False)
        self.ui.buttonStop.setEnabled(True)

        #thread = DiceThread(self.ui.spinBoxDices.value(), self.ui.spinBoxThrows.value())

        self.thread.start()

    def button_stop_clicked(self):
        print("Thread terminated!")
        self.thread.terminate()
        self.ui.buttonStart.setEnabled(True)
        self.ui.buttonStop.setEnabled(False)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    win = DiceSimulator()
    win.show()

    sys.exit(app.exec_())
