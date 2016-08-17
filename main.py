import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from DiceSimulatorUI import Ui_MainWindow
from random import randint
import time

class DiceThread(QtCore.QThread):
    #dice_throw_signal = QtCore.pyqtSignal(int)

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




class DiceSimulator(QtWidgets.QMainWindow):

    dice_throw_signal = QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect the dice_throw_signal to the LDC display
        self.dice_throw_signal.connect(self.ui.lcdNumberDiceOutcome.display)

        # Set the default value of the spinbox to 1
        self.ui.spinBoxDices.setValue(1)

        # Connect the "button start click" to the "button_start_clicked" method
        self.ui.buttonStart.clicked.connect(self.button_start_clicked)

        self.thread = DiceThread(self.ui.spinBoxDices.value(), self.ui.spinBoxThrows.value())



    def button_start_clicked(self):
        # Send the value of the spin box "Number of dices" to the "dicethrow" method
        #self.dicethrow(self.ui.spinBoxDices.value())
        self.thread.start()



    def dicethrow(self, dices):

        #for t in range(5):
            dice_sum = 0
            for d in range(dices):
                current_dice = self.dice()
                dice_sum += current_dice

            #time.sleep(0.5)

            # Emit the "dice_throw" signal
            self.dice_throw_signal.emit(dice_sum)
            print("Dice throw " + str(t))


    def dice(self):
        return randint(1, 6)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    win = DiceSimulator()
    win.show()

    sys.exit(app.exec_())
