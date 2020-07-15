"""Copyright (C) 2020 Jridi Dine (dinejridi@gmail.com)

This checkers game is a free; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation; either version 3 of the License, or (at your
option) any later version.

This checkers game is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
for more details.

You should have received a copy of the GNU General Public License
along with this checkers game ; see the file LICENSE.  If not, write to the Free
Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA."""


import gi
gi.require_version('PangoCairo', '1.0')
from gi.repository import Gtk, Gdk, cairo, Pango, PangoCairo
from gi.repository import GObject
import math
import gettext


#draw each square of the checker
class SquareArea(Gtk.DrawingArea): 
	def __init__ (self, name=[], color=1.0, square=20, square_type=0, pc_first = False):
		Gtk.DrawingArea.__init__(self)
		self.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
		self.set_size_request(square, square)
		if name:
			self.name = name
		self.pc_first = pc_first
		self.color = color
		self.square_type = square_type
		self.hexpand = True
		self.vexpand = True
		self.set_halign = Gtk.Align.FILL
		self.set_valign = Gtk.Align.FILL
		self.selected = False
		self.connect('draw', self.do_draw_cb)


	#draw a square
	def do_draw_cb(self, widget, cr):
		height = widget.get_allocated_height()
		width = widget.get_allocated_width()
		cr.rectangle(0, 0, width, height)
		if self.selected:
			cr.set_source_rgba(1.0, 0.0, 0.0, 1.0)
		else:
			cr.set_source_rgba(self.color, self.color, self.color, 1.0)
		cr.fill()
		if self.square_type == 1 or self.square_type == 2:
			self.draw_pawn(cr, width, height)
		elif self.square_type == 4 or self.square_type == 5:
			self.draw_queen(cr, width, height)

	#draw each pawn
	def draw_pawn(self, cr, width, height):
		pawn_color = 0.0
		if self.pc_first:
			pawn_color = 1.0
		cr.save()
		cr.translate(width / 2, height / 2)
		radius = width / 2 - 10
		cr.arc(0, 0, radius, 0.0, 2.0 * math.pi)
		if self.square_type == 1:
			pawn_color = 1.0
			if self.pc_first:
				pawn_color = 0.0
		cr.set_source_rgb(pawn_color, pawn_color, pawn_color)
		cr.fill()
		cr.arc(0, 0, radius, 0.0, 2.0 * math.pi)
		cr.set_source_rgb(1 - self.color, 1 - self.color, 1 - self.color)
		cr.set_line_width(5)
		cr.stroke()
		cr.restore()

	#draw each queen
	def draw_queen(self, cr, width, height):
		pawn_color = 0.0
		if self.pc_first:
			pawn_color = 1.0
		cr.save()
		cr.translate(width / 2, height / 2)
		radius = width / 2 - 5
		cr.arc(0, 0, radius, 0.0, 2.0 * math.pi)
		if self.square_type == 4:
			pawn_color = 1.0
			if self.pc_first:
				pawn_color = 0.0
		cr.set_source_rgb(pawn_color, pawn_color, pawn_color)
		cr.fill()
		cr.arc(0, 0, radius, 0.0, 2.0 * math.pi)
		cr.set_source_rgb(1 - pawn_color, 1 - pawn_color, 1 - pawn_color)
		cr.set_line_width(6)
		cr.stroke()
		cr.arc(0, 0, radius * 0.7, 0.0, 2.0 * math.pi)
		cr.set_source_rgb(1 - pawn_color, 1 - pawn_color, 1 - pawn_color)
		cr.set_line_width(6)
		cr.stroke()
		cr.restore()

	def square_selected(self, size, selected):
		self.selected = selected
		self.set_size_request(size, size)
		self.queue_draw()

	#resize pawn 
	def resize_pawn(self, size): 
		self.set_size_request(size, size)
		self.queue_draw()
