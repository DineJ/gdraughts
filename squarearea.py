from gi.repository import Gtk, Gdk, cairo, Pango, PangoCairo
from gi.repository import GObject
import math

#draw each square of the checker
class SquareArea(Gtk.DrawingArea): 
	def __init__ (self, name=[], color=1.0, square=20, square_type=0): #,  pawn_color=0.0):
		Gtk.DrawingArea.__init__(self)
		self.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
		self.set_size_request(square, square)
		if name:
			self.name = name
		self.color = color
		#pawn_color = pawn_color
		self.square_type = square_type
		self.hexpand = True
		self.vexpand = True
		self.set_halign = Gtk.Align.FILL
		self.set_valign = Gtk.Align.FILL
		self.connect('draw', self.do_draw_cb)


	#draw a square
	def do_draw_cb(self, widget, cr): 
		height = widget.get_allocated_height()
		width = widget.get_allocated_width()
		cr.rectangle(0, 0, width, height)
		cr.set_source_rgba(self.color, self.color, self.color, 1.0)
		cr.fill()
		if self.square_type == 1 or self.square_type == 2:
			self.draw_pawn(cr, width, height)
		elif self.square_type == 4 or self.square_type == 5:
			self.draw_queen(cr, width, height)

	#draw each pawn
	def draw_pawn(self, cr, width, height):
		pawn_color = 0.0
		cr.save()
		cr.translate(width / 2, height / 2)
		radius = width / 2 - 10
		cr.arc(0, 0, radius, 0.0, 2.0 * math.pi)
		if self.square_type == 1:
			pawn_color = 1.0
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
		cr.save()
		cr.translate(width / 2, height / 2)
		radius = width / 2 - 5
		cr.arc(0, 0, radius, 0.0, 2.0 * math.pi)
		if self.square_type == 4:
			pawn_color = 1.0
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

	#resize pawn 
	def resize_pawn(self, taille): 
		self.set_size_request(taille, taille)
		self.queue_draw()
