#!/usr/bin/env python

# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QVariant', 2)

from PyQt4 import QtCore, QtGui, QtDeclarative
from model import ThymioController

class ThymioImplQObj(QtCore.QObject):

    def __init__(self):
        super(ThymioImplQObj, self).__init__()

        self.thymioCltr = ThymioController("/home/tkingless/Development/Github/ThymioOfficeAssistant/PyQts/tmpl.aesl")

    #TODO callback/slot
    #@QtCore.pyqtSlot(float,float)
    def on_joystick_moved(self,x,y):
    	#print 'joystick_moved() x: {0}, y:{1}'.format(x,y)
        [leftSpd, rightSpd] = self.transformToMotorsSpd(x,y)
        self.thymioCltr.SetVar("motor.left.target",[leftSpd])
        self.thymioCltr.SetVar("motor.right.target",[rightSpd])

    def transformToMotorsSpd(self,x,y):
        import math
        mag = math.sqrt(x*x+y*y)
        leftMotorSpd = 500 * mag * (y + x)
        rightMotorSpd = 500 * mag * (y - x)
        return [leftMotorSpd,rightMotorSpd]

#TODO make this as Xwin controllable
if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    canvas = QtDeclarative.QDeclarativeView()
    engine = canvas.engine()

    mainModel = ThymioImplQObj()

    engine.rootContext().setContextObject(mainModel)
    canvas.setSource(QtCore.QUrl.fromLocalFile('virtual_joystick.qml')) 

    #http://pyqt.sourceforge.net/Docs/PyQt4/qml.html
    #also reverse way can be done, this is cleaner for separation
    rootObject = canvas.rootObject()
    rootObject.joystick_moved.connect(mainModel.on_joystick_moved)

    """TODO 
    using qrc not working, e.g. 
    "view.setSource(QtCore.QUrl('qrc:/res/virtual_joystick.qml'))"
    How .qrc be used? check document
    """

    canvas.setGeometry(QtCore.QRect(100, 100, 450, 450)) #TODO get the property from qml, the root.width & root.height
    canvas.show()



    sys.exit(app.exec_())