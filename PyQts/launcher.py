#!/usr/bin/env python

# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QVariant', 2)

from PyQt4 import QtCore, QtGui

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        #TODO define class instance variables here

        #TODO use QtDeclarative
        #view->setSource(QUrl("qrc:/res/virtual_joystick.qml"));

        #TODO sigal & slot binding of joystick_moved()

    #TODO callback/slot
    def joystick_moved(x,y):
    	print 'joystick_moved() slot called'

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())