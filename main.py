import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from design import Ui_MainWindow


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        ui = Ui_MainWindow()
        ui.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    win = MyWindow()
    win.show()

    sys.exit(app.exec_())
