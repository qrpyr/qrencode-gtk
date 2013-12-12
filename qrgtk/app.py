# This file is part of qrencode-gtk
#
# Copyright (C) 2013 random <random237849@gmx.at>
# 
# qrencode-gtk is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# qrencode-gtk is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk, Gio, GLib, Gdk

from qrgtk.window import Window
from qrgtk.encoder import Encoder

#
# Application
#
class Application(Gtk.Application):
	def __init__(self):
		Gtk.Application.__init__(self,
			application_id="app.qrencode-gtk",
			flags=Gio.ApplicationFlags.FLAGS_NONE)
		
		GLib.set_application_name("QR code") # ?
		
		Gdk.threads_init()
        	
		self.connect("shutdown", self.handle_action_quit, None)
        	
	def do_activate(self):
	
		self.window = Window(self)
		self.add_window(self.window)

		self.encoder = Encoder()
		
		self.window.encoder = self.encoder
		self.encoder.window = self.window
		
		self.window.show_all()
		self.encoder.start()

	def do_startup(self):
		Gtk.Application.do_startup(self)

		# TODO: Menu?
		"""
		menu = Gio.Menu()
		menu.append("About", "app.about")
		menu.append("Quit", "app.quit")
		self.set_app_menu(menu)

		action_about = Gio.SimpleAction.new("about", None)
		action_about.connect("activate", self.handle_action_about)
		self.add_action(action_about)

		action_quit = Gio.SimpleAction.new("quit", None)
		action_quit.connect("activate", self.handle_action_quit)
		self.add_action(action_quit)
		"""
	
	def handle_action_quit(self, action, parameter):		
		if self.encoder.lock.acquire(True, 0.5):
			self.encoder.running = False
			self.encoder.doencode.set()
			self.encoder.lock.release()
			self.encoder.join()
		self.window.close()
		self.quit()

	"""
	def handle_action_about(self, action, parameter):
		aboutdialog = Gtk.AboutDialog()
		authors = [""]
		documenters = [""]
		aboutdialog.set_program_name("QR Something")
		aboutdialog.set_copyright("Copyright ")
		aboutdialog.set_authors(["Authors"])
		aboutdialog.set_documenters(["Documents"])
		aboutdialog.set_website("")
		aboutdialog.set_website_label("")
		aboutdialog.set_title("")
		aboutdialog.connect("response", self.on_close_about)
		aboutdialog.show()

	def on_close_about(self, action, parameter):
		action.destroy()
	"""

