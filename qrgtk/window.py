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

from gi.repository import Gtk, GLib, GdkPixbuf, Gdk

from qrgtk.textentry import TextEntry

#
# Main Window		
#
class Window(Gtk.Window):
	def __init__(self, app):
		Gtk.Window.__init__(self,
			title="QR Encode",
			type=Gtk.WindowType.TOPLEVEL,
			application=app)
		self.set_border_width(0)
		self.set_size_request(500, 550)
		self.set_default_icon_name("qrencode-gtk")

		self.entry = TextEntry(self)
		self.entry.set_size_request(320,20)
		
		# TODO: options menu for saving pixbuf to file using
		# TODO: pixbuf.savev(filename, type_, option_keys, option_values)
		#options = Gtk.Button.new_from_icon_name("emblem-system-symbolic",1)
		#options = Gtk.MenuButton()
		#options.set_image("emblem-system-symbolic")
		
		header = Gtk.HeaderBar(show_close_button=True, custom_title=self.entry)
		#header.pack_start(options)
		self.set_titlebar(header)
		
		self.image_widget = Gtk.Image()
		self.image_widget.modify_bg(Gtk.StateType.NORMAL,
			Gdk.Color.from_floats(1, 1, 1))
		self.box = Gtk.ScrolledWindow()
		self.box.set_policy(1, 1)
		self.box.add_with_viewport(self.image_widget)
		self.add(self.box)
		
		self.set_events(Gdk.EventMask.STRUCTURE_MASK)
		self.connect("configure-event", self.handle_resize_request);
		
		self.entry.grab_focus()
		
		self.resize_ready = True
	
	def request_image(self,string):
		if self.encoder.lock.acquire(False):
			self.encoder.string = string
			self.encoder.doencode.set()
			self.encoder.lock.release()
		
	def update_image(self,pixbuf):
	
		#Gdk.threads_enter()
		self.image_widget.clear()
		self.image_widget.set_from_pixbuf(pixbuf)
		#Gdk.threads_leave()
		return False
		
	def handle_resize_request(self, action, parameter):
		
		# change entry bar size
		size = self.get_allocated_width()
		if size > 1000:
			self.entry.set_size_request(750,20)
		elif size < 900:
			self.entry.set_size_request(320,20)
		
		# change image size
		if self.resize_ready == True:
			self.resize_ready = False
			GLib.timeout_add(1000, self.do_resize_image, parameter)
	
	def do_resize_image(self,parameter):		
		#Gdk.threads_enter()
		pixbuf = self.image_widget.get_pixbuf()
		#Gdk.threads_leave()
		if pixbuf != None:
			size = self.get_width_height()
			pixbuf = pixbuf.scale_simple(size,size,
				GdkPixbuf.InterpType.NEAREST)
		if pixbuf != None:
			#Gdk.threads_enter()
			self.image_widget.set_from_pixbuf(pixbuf)
			#Gdk.threads_leave()
		self.resize_ready = True
		return False
		
	def get_width_height(self):
		Gdk.threads_enter()
		size = max(
			min(
				self.box.get_allocated_width(),
				self.box.get_allocated_height()	) - 100,
			100 )
		Gdk.threads_leave()
		return size

