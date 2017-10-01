#!/usr/bin/env python

# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QVariant', 2)

from PyQt4 import QtCore, QtGui, QtDeclarative

class ThymioModel(QtCore.QObject):

    def __init__(self):
        super(ThymioModel, self).__init__()

    #TODO callback/slot
    #@QtCore.pyqtSlot(float,float)
    def on_joystick_moved(self,x,y):
    	print 'joystick_moved() x: {0}, y:{1}'.format(x,y)

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    canvas = QtDeclarative.QDeclarativeView()
    engine = canvas.engine()

    mainModel = ThymioModel()

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