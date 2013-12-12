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

from gi.repository import Gtk, Gio

MAX_STR_LEN = 1500
			
#
# Text Entry Field		
#
class TextEntry(Gtk.Entry):
	def __init__(self,window):
		Gtk.Entry.__init__(self)
		self.set_max_length(MAX_STR_LEN)
		self.set_progress_fraction(0)
		
		icon = Gio.ThemedIcon.new("edit-clear-symbolic")
		self.set_icon_from_gicon(1,icon)
		self.connect("icon-press",self.handle_icon)
		self.connect("activate",self.handle_enter)
		
		self.buffer = self.get_buffer()
		self.buffer.connect("inserted-text",self.handle_input)
		self.buffer.connect("deleted-text",self.handle_delete)
	
		self.window = window
	
	def update_progress_bar(self):
		self.set_progress_fraction(self.buffer.get_length()/MAX_STR_LEN)
	
	def handle_icon(self, action, position, event):
		# clear image when icon is pressed a second time
		if len(self.buffer.get_text()) == 0:
			self.window.image_widget.clear()
		else:
			self.set_text("")
	
	def handle_delete(self, action, count, length):
		self.update_progress_bar()
	
	def handle_input(self, action, count, input_text, input_length):
		self.update_progress_bar()
		# reencode when max length is reached
		if self.buffer.get_length() == MAX_STR_LEN:
			self.window.request_image(self.buffer.get_text())
		# reencode also when text is pasted
		elif input_length > 1:
			self.window.request_image(self.buffer.get_text())

	def handle_enter(self, action):
		# reencode when enter is pressed but not empty
		if self.buffer.get_length() > 0:
			self.window.request_image(self.buffer.get_text())

