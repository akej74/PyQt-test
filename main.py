import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from DiceSimulatorUI import Ui_MainWindow
from random import randint

#class DiceThread(QtCore.QThread):
#    def __init__(self):
#        super.__init__()
#
#    def __del__(self):
#        self.wait()
#
#    def run(self):
#        pass

class Communicate(QtCore.QObject):
    # Signal to send the value of a dice throw
    dice_throw_signal = QtCore.pyqtSignal(int)

class DiceSimulator(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.c = Communicate()

        # Connect the dice_throw_signal to the LDC display
        self.c.dice_throw_signal.connect(self.ui.lcdNumberDiceOutcome.display)

        # Set the default value of the spinbox to 1
        self.ui.spinBoxDices.setValue(1)

        # Connect the "button start click" to the "button_start_clicked" method
        self.ui.buttonStart.clicked.connect(self.button_start_clicked)

    def button_start_clicked(self):
        # Send the value of the spin box "Number of dices" to the "dicethrow" method
        self.dicethrow(self.ui.spinBoxDices.value())

    def dicethrow(self, dices):

        dice_sum = 0

        for d in range(dices):
            current_dice = self.dice()
            dice_sum += current_dice

        # Emit the "dice_throw" signal
        self.c.dice_throw_signal.emit(dice_sum)


    def dice(self):
        return randint(1, 6)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    win = DiceSimulator()
    win.show()

    sys.exit(app.exec_())
