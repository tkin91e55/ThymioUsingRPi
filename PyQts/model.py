import dbus
import dbus.mainloop.glib
import glib
import gobject
import sys
#src and ref from: https://www.thymio.org/en:asebamedulla
#API of asebaNetworkObject, medulla: https://github.com/aseba-community/aseba/blob/master/switches/medulla/medulla.cpp

#TODO impl threading
class ThymioController(object):
	def __init__(self, filename):
		#members
		self.asebaNetwork=None
		self.loop=None

		# init the main loop
		dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
		
		# get stub of the Aseba network
		bus = dbus.SessionBus()
		asebaNetworkObject = bus.get_object('ch.epfl.mobots.Aseba', '/')
		self.asebaNetwork = dbus.Interface(asebaNetworkObject,
			dbus_interface='ch.epfl.mobots.AsebaNetwork')
		
		# load the .asel file
		self.asebaNetwork.LoadScripts(filename,
			reply_handler=self.dbusReply,
			error_handler=self.dbusError
		)
	
	#TODO optimize dbus using: http://rocksaying.tw/archives/15534603.html
	def run(self):
		# run event loop
		self.loop = gobject.MainLoop()
		self.loop.run()
	
	def dbusReply(self):
		# correct replay on D-Bus, ignore
		pass

	def dbusError(self, e):
		# there was an error on D-Bus, stop loop
		print('dbus error: %s' % str(e))
		self.loop.quit()

	#convenient funcs:: begin
	# TODO: to be in behavior programming, organize some freqent attr
	defaultNodeName = "thymio-II"

	def TestGlo():
		print defaultNodeName

	def GetVar(self, attrStr):
		return self.asebaNetwork.GetVariable(self.defaultNodeName,attrStr)

	def SetVar(self, attrStr, attrValArray):
		self.asebaNetwork.SetVariable(self.defaultNodeName,attrStr,attrValArray)

	def TrigEvent(self, evt, evtArgs):
		self.asebaNetwork.SendEventName(evt,evtArgs,
			reply_handler=self.dbusReply,
			error_handler=self.dbusError)
	#convenient funcs:: end