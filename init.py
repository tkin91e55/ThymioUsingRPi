import dbus
import dbus.mainloop.glib
import glib
import gobject
import sys
#src and ref from: https://www.thymio.org/en:asebamedulla

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

def main():
	# check command-line arguments
	if len(sys.argv) != 2:
		print('This is trying to automate the behavior of'
			' Thymio with asel script, \npls provide an sub argument for'
			' \"python %s\"' % sys.argv[0])
		return
	
	# create and run controller
	thymioController = ThymioController(sys.argv[1])
	thymioController.run()


if __name__ == '__main__':
	main()