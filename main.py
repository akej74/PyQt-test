import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from DiceSimulatorUI import Ui_MainWindow
from random import randint
import time

class DiceThread(QtCore.QThread):
    dice_throw_signal = QtCore.pyqtSignal(int)
    actual_throws_per_second_signal = QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.keep_running = True

    def __del__(self):
        self.wait()

    def set_parameters(self, dices, throws_per_second):
        self.dices = dices
        self.throws_per_second = throws_per_second

    def stop(self):
        self.keep_running = False

    def run(self):
        print("Run method!")
        print(self.dices)
        print(self.throws_per_second)

        # Run a loop to call "dicethrow" x times every second
        while self.keep_running:
            try:
                t0 = time.time()

                time.sleep(1/self.throws_per_second)
                self.dice_throw_signal.emit(dicethrow(self.dices))

                t1 = time.time()
                self.actual_throws_per_second_signal.emit(1/(t1 - t0))
            except:
                (type, value, traceback) = sys.exc_info()
                sys.excepthook(type, value, traceback)

def dicethrow(dices):
    dice_sum = 0
    for d in range(dices):
        current_dice = dice()
        dice_sum += current_dice

    return dice_sum

def dice():
    return randint(1, 6)

class DiceSimulator(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Create the thread
        self.thread = DiceThread()

        # Disable "Stop" button
        self.ui.buttonStop.setEnabled(False)

        # Connect signals to slots
        self.ui.buttonStart.clicked.connect(self.button_start_clicked)
        self.ui.buttonStop.clicked.connect(self.button_stop_clicked)
        self.thread.dice_throw_signal.connect(self.ui.lcdNumberDiceOutcome.display)

        self.thread.actual_throws_per_second_signal.connect(self.ui.lcdNumberActualThrows.display)

    def button_start_clicked(self):

        # Disable "Start" and "SpinBoxes" to prevent more that one thread to be started
        self.ui.spinBoxDices.setEnabled(False)
        self.ui.spinBoxThrows.setEnabled(False)
        self.ui.buttonStart.setEnabled(False)
        self.ui.buttonStop.setEnabled(True)

        # Set current parameters for the thread
        self.thread.set_parameters(self.ui.spinBoxDices.value(), self.ui.spinBoxThrows.value())

        self.thread.start()

    def button_stop_clicked(self):
        print("Stop!")
        #self.thread.terminate()
        self.thread.stop()
        self.ui.buttonStart.setEnabled(True)
        self.ui.buttonStop.setEnabled(False)
        self.ui.spinBoxDices.setEnabled(True)
        self.ui.spinBoxThrows.setEnabled(True)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    win = DiceSimulator()
    win.show()

    sys.exit(app.exec_())
