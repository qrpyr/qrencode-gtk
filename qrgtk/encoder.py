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

from gi.repository import GLib, GdkPixbuf
import ctypes
import threading
from bitarray import bitarray

# 
# QRcode data object as defined by libqrencode
# 
class QRcode(ctypes.Structure):
	_fields_ = [
		("version", ctypes.c_int),
		("width", ctypes.c_int),
		("data", ctypes.POINTER(ctypes.c_ubyte))]

# 
# Encoder thread, encodes string as QR-code in GdkPixbuf buffer
# 
class Encoder(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		
		self.lock = threading.Lock()
		self.doencode = threading.Event()

		self.window = None
		self.running = True
		self.string = ""

		self.libqrencode = ctypes.CDLL("libqrencode.so")
		self.libqrencode.QRcode_encodeString.argtypes = [
			ctypes.c_char_p,
			ctypes.c_int,
			ctypes.c_int,
			ctypes.c_int,
			ctypes.c_int]
		self.libqrencode.QRcode_encodeString.restype = ctypes.POINTER(QRcode)
		self.libqrencode.QRcode_free.argtypes = [ctypes.POINTER(QRcode)]

	def run(self):		
		
		self.doencode.wait()
		self.lock.acquire()
		self.doencode.clear()
		
		while(self.running):
			
			# TODO: additional test: string length < MAX_STR_LEN
			qrcode_object = self.libqrencode.QRcode_encodeString(
				self.string.encode(), 0, 0, 2, 1)
			
			data = qrcode_object.contents.data
			width = qrcode_object.contents.width

			image_header = "P4 "+str(width)+" "+str(width)+" "
			# TODO: get rid of bitarray
			image_data = bitarray(width, endian='big') # line buffer
			
			pixbufloader = GdkPixbuf.PixbufLoader.new_with_type("pnm")
			pixbufloader.write(image_header.encode())

			for row in range(width):
				for col in range(width):
					# information is stored in LSB
					if ( data[row*width + col] & 0x01 ):
						image_data[col] = True
					else:
						image_data[col] = False
				pixbufloader.write(image_data.tobytes())

			pixbufloader.close()
			
			self.libqrencode.QRcode_free(qrcode_object)
			
			pixbuf = pixbufloader.get_pixbuf()
			
			# TODO: pixbufloader.unref() ?				
			
			size = self.window.get_width_height()
			pixbuf = pixbuf.scale_simple(size, size,
				GdkPixbuf.InterpType.NEAREST)

			#Gdk.threads_enter()
			GLib.idle_add(self.window.update_image,pixbuf)
			pixbuf = None
			#Gdk.threads_leave()
			
			self.lock.release()

			self.doencode.wait()
			self.lock.acquire()
			self.doencode.clear()

