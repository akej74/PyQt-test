import sys
from PyQt5 import QtCore, QtGui, QtWidgets

from design import Ui_MainWindow

class MyWindow(Ui_MainWindow):
    def __init__(self):
        super().__init__()


if __name__ == "__main__":

    # Create the main QT application
    app = QtWidgets.QApplication(sys.argv)

    # Create the main window
    MainWindow = QtWidgets.QMainWindow()

    ui = MyWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    # Exit QT application
    sys.exit(app.exec_())

