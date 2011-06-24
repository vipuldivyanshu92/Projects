import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from MyApp import Ui_MainWindow

# We start a new class here
# derived from QMainWindow

class TestApp(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect the pushButton to a message method.
        self.connect(self.ui.pushButton, QtCore.SIGNAL("clicked()"), self.message)

    def message(self):
        print dir(self.ui.listView)
        

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = TestApp()
    window.show()
    sys.exit(app.exec_())
