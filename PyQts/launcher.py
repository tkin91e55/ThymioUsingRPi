#!/usr/bin/env python

# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QVariant', 2)

import math
from PyQt4 import QtCore, QtGui, QtDeclarative
from model import ThymioController

class ThymioImplQObj(QtCore.QObject):

    def __init__(self):
        super(ThymioImplQObj, self).__init__()

        self.thymioCltr = ThymioController("/home/tkingless/Development/Github/ThymioOfficeAssistant/PyQts/tmpl.aesl")
        self.cur_leftSpd = 0
        self.cur_rightSpd = 0
        self.turnleft = 0
        self.turnright = 0

        self.thymioCltr.start()

    #@QtCore.pyqtSlot(float,float)
    def on_joystick_moved(self,x,y):
    	#print 'joystick_moved() x: {0}, y:{1}'.format(x,y)
        [leftSpd, rightSpd] = self.transformToMotorsSpd(x,y)

        if math.fabs(self.cur_leftSpd - leftSpd) >= 50 :
            self.thymioCltr.SetVar("motor.left.target",[leftSpd])
            self.cur_leftSpd = leftSpd

        if math.fabs(self.cur_rightSpd - rightSpd) >= 50:
            self.thymioCltr.SetVar("motor.right.target",[rightSpd])
            self.cur_rightSpd = rightSpd
        
        if leftSpd > 200:
            if self.turnright == 0:
                self.thymioCltr.SetVar("turnright",[1])
                self.turnright = 1
        else:
            if self.turnright == 1:
                self.thymioCltr.SetVar("turnright",[0])
                self.turnright = 0

        if rightSpd > 200:
            if self.turnleft == 0:
                self.thymioCltr.SetVar("turnleft",[1])
                self.turnleft = 1
        else:
            if self.turnleft == 1:
                self.thymioCltr.SetVar("turnleft",[0])
                self.turnleft = 0

    def transformToMotorsSpd(self,x,y):
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
    #canvas.setSource(QtCore.QUrl.fromLocalFile('virtual_joystick.qml')) 
    canvas.setSource(QtCore.QUrl('virtual_joystick.qml')) 

    #http://pyqt.sourceforge.net/Docs/PyQt4/qml.html
    #also reverse way can be done, this is cleaner for separation
    rootObject = canvas.rootObject()
    rootObject.joystick_moved.connect(mainModel.on_joystick_moved)

    canvas.setGeometry(QtCore.QRect(100, 100, 450, 450)) #TODO get the property from qml, the root.width & root.height
    canvas.show()

    sys.exit(app.exec_())