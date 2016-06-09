import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from design import Ui_MainWindow


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self._ui.btnInfo1.clicked.connect(self.btnInfo1Clicked)
        self._ui.btnClear.clicked.connect(self.btnClearClicked)

    def btnInfo1Clicked(self):
        self._ui.textBrowser.setText('Important message')

    def btnClearClicked(self):
        self._ui.textBrowser.setText('')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    win = MyWindow()
    win.show()

    sys.exit(app.exec_())
