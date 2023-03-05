import sys
import time
from random import randint

from PyQt6 import QtCore, QtWidgets

from DiceSimulatorUI import Ui_MainWindow


class DiceSimulator(QtWidgets.QMainWindow):
    """Main class to create the UI, based on QT QMainWindow. The UI elements are defined in DiceSimulatoruUI.py,
     which is created with pyuic5 from a QT Designer .ui file.
     Never modify the DiceSimulatorUI.py manually, it is generated from QT Designer.
    """
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Create QSettings object for storing configuration data in the OS native repository
        # (Registry for Windows, ini-file for Linux)
        self.settings = QtCore.QSettings('DiceSimulator', 'myApp')

        # Update UI with stored config
        self.read_config()

        # Create a thread for running the dice simulation
        self.thread = DiceThread()

        # Disable "Stop" button (only "Start" should be enabled when dice simulation is stopped
        self.ui.buttonStop.setEnabled(False)

        # Connect button signals to slots
        self.ui.buttonStart.clicked.connect(self.button_start_clicked)
        self.ui.buttonStop.clicked.connect(self.button_stop_clicked)

        # Connect the signal from the dice simulation thread to the LCD display
        self.thread.dice_throw_signal.connect(self.ui.lcdNumberDiceOutcome.display)

        # Connect the "Throws per second" signal to the other LDC
        self.thread.actual_throws_per_second_signal.connect(self.ui.lcdNumberActualThrows.display)

    def read_config(self):
        """Reads configuration from the OS repository (Registry in Windows, ini-file in Linux).
        Reads last used settings for the spinboxes, use default values first time.
        type=int defines the data type (should work in a Linux environment that uses ini-files)
        """
        self.ui.spinBoxDices.setValue(self.settings.value("dices", 5, type=int))
        self.ui.spinBoxThrows.setValue(self.settings.value("throws", 10, type=int))

    def write_config(self):
        """ Writes the config settings to the OS repository"""
        # Write current spinbox values to config file
        self.settings.setValue("dices", self.ui.spinBoxDices.value())
        self.settings.setValue("throws", self.ui.spinBoxThrows.value())

    def closeEvent(self, e):
        """Override the closeEvent method to save config data before exiting"""
        self.write_config()
        e.accept()

    def button_start_clicked(self):
        """1. Disables GUI elements before the thread is started, to prevent more than
        one thread to be started at the same time.
        2. Configures the thread object with the current values from the GUI spin boxes.
        3. Starts the thread.
        """

        self.ui.spinBoxDices.setEnabled(False)
        self.ui.spinBoxThrows.setEnabled(False)
        self.ui.buttonStart.setEnabled(False)
        self.ui.buttonStop.setEnabled(True)

        self.thread.set_parameters(self.ui.spinBoxDices.value(), self.ui.spinBoxThrows.value())

        self.thread.start()

    def button_stop_clicked(self):
        """Stops the running thread and resets the GUI"""
        print("Stop!")

        self.thread.stop()
        self.ui.buttonStart.setEnabled(True)
        self.ui.buttonStop.setEnabled(False)
        self.ui.spinBoxDices.setEnabled(True)
        self.ui.spinBoxThrows.setEnabled(True)


class DiceThread(QtCore.QThread):
    """QThread class to define the dice calculation and signals to be emitted from the running thread."""

    # Signal with current dice sum after a throw
    dice_throw_signal = QtCore.pyqtSignal(int)

    # Signal with current "dice throws per second" value
    actual_throws_per_second_signal = QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()

        # "keep_running" controls the while loop in the running thread
        self.keep_running = True

    def __del__(self):
        self.wait()

    def set_parameters(self, dices, throws_per_second):
        """Sets the number of dices and throws per second used in the run method"""
        self.dices = dices
        self.throws_per_second = throws_per_second

    def stop(self):
        """ Stops the while loop in the running thread """
        self.keep_running = False

    def run(self):
        """Define the dice simulation process to be run in the thread, emitting signals
        with current values from the simulation. The while loop is stopped gracefully by calling the stop method"""
        # Debug messages
        print("Run method!")
        print(self.dices)
        print(self.throws_per_second)

        # keep_running should be True before starting the while loop
        self.keep_running = True

        # Run a loop to call "dicethrow" x times every second
        while self.keep_running:
            try:
                # Start time
                t0 = time.time()

                # Wait according to "throws per second"
                time.sleep(1/self.throws_per_second)

                # Calculate the sum of throwing "dices" and emit this value so it can update the main UI application
                self.dice_throw_signal.emit(dicethrow(self.dices))

                # End time and calculation of actual "throws per second" value
                # TODO: Make an average of many throws instead of measuring each throw
                t1 = time.time()
                self.actual_throws_per_second_signal.emit(1/(t1 - t0))

            # Exception handling to catch and print out any exceptions that may occur in the running thread
            except:
                (type, value, traceback) = sys.exc_info()
                sys.excepthook(type, value, traceback)


def dicethrow(dices):
    """Calculate the sum om throwing x dices"""
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

    sys.exit(app.exec())
