#!/usr/bin/env python3
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
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
from checker import Checker
from backend import Backend, Node, Stack
import random
import gettext

## Localization.
# if getattr(sys, 'frozen', False):
#     APP_DIR = os.path.dirname(dirname(sys.executable))
# else:
#     APP_DIR     = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# LOCALDIR      = os.path.join(APP_DIR, 'locale')

# DOMAIN = 'gdraughts'
gettext.install('gdraughts', '/usr/share/locale/')


#create application
class Draughts(Gtk.Window):

	#managing of the main window
	def __init__ (self, pc_first=False, country=3, matrix_classic=True, state=8, square_color=0, square_size=0, tool_height=0, checker=None, open_dialog=0, rear_socket=True, forced_move=True, eatqueen=True, depth=5, queen=False, promotion_eat=False): # country : 0 = France(fr), 1 = Spain(sp), 2 = England(eng), 3 = Netherlands(ne), 4 = Italy(ita)
		Gtk.Window.__init__(self)
		self.state = state
		self.square_color = square_color
		self.square_size = square_size
		self.tool_height = tool_height
		self.checker = checker
		self.open_dialog = open_dialog
		self.turn = 1
		self.pc_first = pc_first
		self.matrix_classic = matrix_classic
		self.country = country
		self.rear_socket = rear_socket
		self.forced_move = forced_move
		self.eatqueen = eatqueen
		self.depth = depth
		self.queen = queen
		self.promotion_eat = promotion_eat

		self.set_border_width(10)
		self.connect('delete-event', Gtk.main_quit)
		self.connect("check_resize", self.on_resize)
		self.set_default_size(640,480)


		application = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
		game_area = Gtk.Box()
		self.checker_game = Gtk.Box()
		game_area.set_homogeneous(False)
		application.set_homogeneous(False)

		self.box_rows = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
		self.box_rows.set_homogeneous(False)

		self.head_label = Gtk.Label()
		self.head_label.set_markup('<span weight="bold">%s</span>' % _("Historical"))
		self.box_rows.pack_start(self.head_label, False, True, 0)

		self.scrolled_window = Gtk.ScrolledWindow()
		self.scrolled_window.set_border_width(10)
		self.scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)
		self.box_rows.pack_start(self.scrolled_window, True, True, 0)

		self.hit_history = Gtk.ListBox()
		self.hit_history.set_selection_mode(Gtk.SelectionMode.NONE)
		self.hit_history.set_size_request(200, -1)
		self.scrolled_window.add(self.hit_history)

		img = Gtk.Image.new_from_icon_name('application-exit', 0)
		quit_button = Gtk.ToolButton.new(img)
		img = Gtk.Image.new_from_icon_name('document-new', 0)
		play_button = Gtk.ToolButton.new(img)
		img = Gtk.Image.new_from_icon_name('preferences-system', 0)
		custom_button = Gtk.ToolButton.new(img)

		quit_button.set_label(_("Close"))
		play_button.set_label(_("New game"))
		custom_button.set_label(_("Settings"))
		quit_button.set_is_important(True)
		play_button.set_is_important(True)
		custom_button.set_is_important(True)


		self.informations_bar = Gtk.Label()
		self.informations_bar.set_markup(('<span foreground="#ff710d" size="large" >%s</span>' %_("Start the game")))
		self.informations_bar.set_size_request(-1, 30)

		r_chercker8 = Gtk.RadioButton.new()
		r_chercker10 = Gtk.RadioButton.new()


		tool_bar = Gtk.Toolbar()
		tool_bar.insert(quit_button, 0)
		tool_bar.insert(play_button, 1)
		tool_bar.insert(custom_button, 2)
		quit_button.show()
		play_button.show()
		custom_button.show()


		quit_button.connect('clicked', Gtk.main_quit)
		play_button.connect('clicked', self.dialog)
		custom_button.connect('clicked', self.custom_dialog)

		application.pack_start(tool_bar, False, True, 0)
		application.pack_start(self.informations_bar, False, False, 0)
		application.pack_start(game_area, True, True, 0)
		game_area.pack_start(self.checker_game, True, True, 0)
		game_area.pack_start(self.box_rows, False, True, 0)
		self.add(application)

	#modify the information label
	def set_informations(self, label):
		self.informations_bar.set_markup(("<span foreground='#ff710d' size='large' >%s</span>" % label))

	#show the application
	def play(self):
		self.show_all()
		self.backend = Backend(self.checker.matrix, self)
		self.backend.fin = False
		self.backend.pl_before_firstclick()

	#designates who plays first
	def who_play(self):
		frame_begin = Gtk.Frame.new(_("Who plays first?"))

		self.r_player = Gtk.RadioButton.new_with_label_from_widget(None, _("Player"))
		self.custom_margin(self.r_player, 5, 10, 5, 10)
		self.r_computer = Gtk.RadioButton.new_from_widget(self.r_player)
		self.custom_margin(self.r_computer, 5, 10, 5, 10)
		self.r_computer.set_label(_("Computer"))


		grid_begin = Gtk.Grid.new()
		grid_begin.set_column_homogeneous(True)
		grid_begin.set_row_homogeneous(True)

		frame_begin.add(grid_begin)

		grid_begin.attach(self.r_player, 0, 0, 1, 1)
		grid_begin.attach(self.r_computer, 1, 0, 1, 1)

		if self.pc_first:
			self.r_computer.set_active(True)
		else:
			self.r_player.set_active(True)

		return frame_begin

	#indicates difficulty levels
	def level_of_difficulty(self):
		frame_difficulties =  Gtk.Frame.new(_("What difficulties do you want?"))

		self.t_easy = Gtk.ToggleButton.new_with_label(_("Easy"))
		self.custom_margin(self.t_easy, 5, 5, 0, 5)
		self.t_medium = Gtk.ToggleButton.new_with_label(_("Medium"))
		self.custom_margin(self.t_medium, 0, 5, 0, 5)
		self.t_hard = Gtk.ToggleButton.new_with_label(_("Hard"))
		self.custom_margin(self.t_hard, 0, 5, 5, 5)

		grid_difficulties = Gtk.Grid.new()
		grid_difficulties.set_column_homogeneous(True)
		grid_difficulties.set_row_homogeneous(True)

		frame_difficulties.add(grid_difficulties)

		grid_difficulties.attach(self.t_easy, 0, 0, 1, 1)
		grid_difficulties.attach(self.t_medium, 1, 0, 1, 1)
		grid_difficulties.attach(self.t_hard, 2, 0, 1, 1)

		self.t_easy.connect('clicked', self.output_state1)
		self.t_medium.connect('clicked', self.output_state2)
		self.t_hard.connect('clicked', self.output_state3)

		if self.depth == 3:
			self.t_easy.set_active(True)
		elif self.depth == 4:
			self.t_medium.set_active(True)
		else:
			self.t_hard.set_active(True)

		return frame_difficulties

	#calibrate the difficulty for min max
	def output_state1(self,button):
		if self.t_easy.get_active():
			self.t_medium.set_active(False)
			self.t_hard.set_active(False)
		self.depth = 3

	#calibrate the difficulty for min max
	def output_state2(self,button):
		if self.t_medium.get_active():
			self.t_easy.set_active(False)
			self.t_hard.set_active(False)
		self.depth = 4

	#calibrate the difficulty for min max
	def output_state3(self,button):
		if self.t_hard.get_active():
			self.t_easy.set_active(False)
			self.t_medium.set_active(False)
		self.depth = 5


	#resize checker after each interraction with main window
	def on_resize(self,widget):
		checker_width = self.checker_game.get_allocation().width
		checker_height = self.checker_game.get_allocation().height

		if checker_width > checker_height:
			self.square_size = checker_height/self.state
		else:
			self.square_size = checker_width/self.state

		if self.checker == None:
			self.checker = Checker(self, self.square_size, self.state, self.square_color)
			self.checker_game.set_center_widget(self.checker)
			self.checker_game.show_all()
			#self.backend = Backend(self.checker.matrix)
		else:
			self.checker.resize_checker(self.square_size)

	#gives margins in dialog boxes
	def custom_margin(self, widget, l, t, r, b):
		widget.set_margin_top(t)
		widget.set_margin_bottom(b)
		widget.set_margin_start(l)
		widget.set_margin_end(r)

	#create a new dialog boxe
	def custom_dialog(self,button):
		#Dialog
		self.open_dialog = 1
		custom_dialog_box = Gtk.Dialog.new()
		custom_dialog_box.set_border_width(10)
		custom_dialog_box.connect('delete-event', Gtk.main_quit)
		custom_dialog_box.show_all()
		custom_dialog_box.add_button(Gtk.STOCK_APPLY, Gtk.ResponseType.APPLY)
		custom_dialog_box.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
		self.turn = 1

		#Hit History
		for element in self.hit_history.get_children():
			self.hit_history.remove(element)

		#Frame
		frame_matrice = Gtk.Frame.new(_("How many square do you want per ligne?"))
		frame_color = Gtk.Frame.new(_("What color do you want in the square at the bottom right?"))
		frame_color1 = Gtk.Frame.new(_("Do you want your pawn to be on the bottom right?"))
		frame_forced_move = Gtk.Frame.new(_("Do you want to force them to eat?"))
		frame_eatbehind = Gtk.Frame.new(_("Do you want to add being able to eat back?"))
		frame_eatqueen = Gtk.Frame.new(_("Do you want pawns can eat a queen?"))
		frame_queen = Gtk.Frame.new(_("Do you want the queens to be able to move one square at a time?"))
		frame_promotion_eat = Gtk.Frame.new(_("Do you want the pawns to become queens during a roundup?"))

		#RadioButton
		r_chercker8 = Gtk.RadioButton.new_with_label_from_widget(None, _("8 square"))
		self.custom_margin(r_chercker8, 5, 10, 5, 10)
		r_chercker10 = Gtk.RadioButton.new_from_widget(r_chercker8)
		self.custom_margin(r_chercker10, 5, 10, 5, 10)
		r_chercker10.set_label(_("10 square"))

		r_color_w = Gtk.RadioButton.new_with_label_from_widget(None, _("White"))
		self.custom_margin(r_color_w, 5, 10, 5, 10)
		r_color_b = Gtk.RadioButton.new_from_widget(r_color_w)
		self.custom_margin(r_color_b, 5, 10, 5, 10)
		r_color_b.set_label(_("Black"))

		r_color1_b = Gtk.RadioButton.new_with_label_from_widget(None, _("No"))
		self.custom_margin(r_color1_b, 5, 10, 5, 10)
		r_color1_w = Gtk.RadioButton.new_from_widget(r_color1_b)
		self.custom_margin(r_color1_w, 5, 10, 5, 10)
		r_color1_w.set_label(_("Yes"))

		r_forced_move_y = Gtk.RadioButton.new_with_label_from_widget(None, _("Yes"))
		self.custom_margin(r_forced_move_y, 5, 10, 5, 10)
		r_forced_move_n = Gtk.RadioButton.new_from_widget(r_forced_move_y)
		self.custom_margin(r_forced_move_n, 5, 10, 5, 10)
		r_forced_move_n.set_label(_("No"))

		r_eatbehind_y = Gtk.RadioButton.new_with_label_from_widget(None,_("Yes"))
		self.custom_margin(r_eatbehind_y, 5, 10, 5, 10)
		r_eatbehind_n = Gtk.RadioButton.new_from_widget(r_eatbehind_y)
		self.custom_margin(r_eatbehind_n, 5, 10, 5, 10)
		r_eatbehind_n.set_label(_("No"))

		r_eatqueen_y = Gtk.RadioButton.new_with_label_from_widget(None, _("Yes"))
		self.custom_margin(r_eatqueen_y, 5, 10, 5, 10)
		r_eatqueen_n = Gtk.RadioButton.new_from_widget(r_eatqueen_y)
		self.custom_margin(r_eatqueen_n, 5, 10, 5, 10)
		r_eatqueen_n.set_label(_("No"))

		r_queen_y = Gtk.RadioButton.new_with_label_from_widget(None, _("Yes"))
		self.custom_margin(r_queen_y, 5, 10, 5, 10)
		r_queen_n = Gtk.RadioButton.new_from_widget(r_queen_y)
		r_queen_n.set_label(_("No"))

		r_promotion_eat_y = Gtk.RadioButton.new_with_label_from_widget(None, _("Yes"))
		self.custom_margin(r_queen_y, 5, 10, 5, 10)
		r_promotion_eat_n = Gtk.RadioButton.new_from_widget(r_promotion_eat_y)
		r_promotion_eat_n.set_label(_("No"))

		#Dialog
		box_dialog = custom_dialog_box.get_content_area()
		box_dialog.pack_start(self.level_of_difficulty(), True, True, 3)
		box_dialog.pack_start(self.who_play(), True, True, 3)
		box_dialog.pack_start(frame_matrice, True, True, 3)
		box_dialog.pack_start(frame_color, True, True, 3)
		box_dialog.pack_start(frame_color1, True, True, 3)
		box_dialog.pack_start(frame_forced_move, True, True, 3)
		box_dialog.pack_start(frame_eatbehind, True, True, 3)
		box_dialog.pack_start(frame_eatqueen, True, True, 3)
		box_dialog.pack_start(frame_queen, True, True, 3)
		box_dialog.pack_start(frame_promotion_eat, True, True, 3)

		#Grid
		grid_matrice = Gtk.Grid.new()
		grid_matrice.set_column_homogeneous(True)
		grid_matrice.set_row_homogeneous(True)

		grid_color = Gtk.Grid.new()
		grid_color.set_column_homogeneous(True)
		grid_color.set_row_homogeneous(True)

		grid_color1 = Gtk.Grid.new()
		grid_color1.set_column_homogeneous(True)
		grid_color1.set_row_homogeneous(True)

		grid_forced_move = Gtk.Grid.new()
		grid_forced_move.set_column_homogeneous(True)
		grid_forced_move.set_row_homogeneous(True)

		grid_eatbehind = Gtk.Grid.new()
		grid_eatbehind.set_column_homogeneous(True)
		grid_eatbehind.set_row_homogeneous(True)

		grid_eatqueen = Gtk.Grid.new()
		grid_eatqueen.set_column_homogeneous(True)
		grid_eatqueen.set_row_homogeneous(True)

		grid_queen = Gtk.Grid.new()
		grid_queen.set_column_homogeneous(True)
		grid_queen.set_row_homogeneous(True)

		grid_promotion_eat = Gtk.Grid.new()
		grid_promotion_eat.set_column_homogeneous(True)
		grid_promotion_eat.set_row_homogeneous(True)

		#Frame
		frame_matrice.add(grid_matrice)
		frame_color.add(grid_color)
		frame_color1.add(grid_color1)
		frame_forced_move.add(grid_forced_move)
		frame_eatbehind.add(grid_eatbehind)
		frame_eatqueen.add(grid_eatqueen)
		frame_queen.add(grid_queen)
		frame_promotion_eat.add(grid_promotion_eat)

		#Grid
		grid_matrice.attach(r_chercker8, 0, 0, 1, 1)
		grid_matrice.attach(r_chercker10, 1, 0, 1, 1)

		grid_color.attach(r_color_w, 0, 0, 1, 1)
		grid_color.attach(r_color_b, 1, 0, 1, 1)

		grid_color1.attach(r_color1_w, 0, 0, 1, 1)
		grid_color1.attach(r_color1_b, 1, 0, 1, 1)

		grid_forced_move.attach(r_forced_move_y, 0, 0, 1, 1)
		grid_forced_move.attach(r_forced_move_n, 1, 0, 1, 1)

		grid_eatbehind.attach(r_eatbehind_y, 0, 0, 1, 1)
		grid_eatbehind.attach(r_eatbehind_n, 1, 0, 1, 1)

		grid_eatqueen.attach(r_eatqueen_y, 0, 0, 1, 1)
		grid_eatqueen.attach(r_eatqueen_n, 1, 0, 1, 1)

		grid_queen.attach(r_queen_y, 0, 0, 1, 1)
		grid_queen.attach(r_queen_n, 1, 0, 1, 1)

		grid_promotion_eat.attach(r_promotion_eat_y, 0, 0, 1, 1)
		grid_promotion_eat.attach(r_promotion_eat_n, 1, 0, 1, 1)

		if self.state == 8:
			r_chercker8.set_active(True)
		else:
			r_chercker10.set_active(True)

		if self.matrix_classic:
			r_color1_b.set_active(True)
		else:
			r_color1_w.set_active(True)

		if self.square_color == 0:
			r_color_w.set_active(True)
		else:
			r_color_b.set_active(True)

		if self.forced_move:
			r_forced_move_y.set_active(True)
		else:
			r_forced_move_n.set_active(True)

		if self.rear_socket:
			r_eatbehind_y.set_active(True)
		else:
			r_eatbehind_n.set_active(True)

		if self.eatqueen:
			r_eatqueen_y.set_active(True)
		else:
			r_eatqueen_n.set_active(True)

		if self.queen:
			r_queen_y.set_active(True)
		else:
			r_queen_n.set_active(True)

		if self.promotion_eat:
			r_promotion_eat_y.set_active(True)
		else:
			r_promotion_eat_n.set_active(True)

		custom_dialog_box.show_all()
		custom_dialog_box.set_transient_for(self)
		custom_dialog_box.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
		self.answer = custom_dialog_box.run()

		if self.answer == Gtk.ResponseType.APPLY:
			if self.r_player.get_active():
				self.pc_first = False
			else:
				self.pc_first = True

			if r_chercker8.get_active():
				self.state = 8 
			else:
				self.state = 10

			if r_color_w.get_active():
				self.square_color = 0
			else:
				self.square_color = 1

			if r_color1_w.get_active():
				self.matrix_classic = False
			else:
				self.matrix_classic = True

			if r_forced_move_y.get_active():
				self.forced_move = True
			else:
				self.forced_move = False

			if r_eatbehind_y.get_active():
				self.rear_socket = True
			else:
				self.rear_socket = False

			if r_eatqueen_y.get_active():
				self.eatqueen = True
			else:
				self.eatqueen = False

			if r_queen_y.get_active():
				self.queen = True
			else:
				self.queen = False

			if r_promotion_eat_y.get_active():
				self.promotion_eat = True
			else:
				self.promotion_eat = False

			self.checker_game.remove(self.checker)
			self.checker = Checker(self, self.square_size, self.state, self.square_color)
			self.checker_game.set_center_widget(self.checker)
			self.checker_game.show_all()
			self.backend = Backend(self.checker.matrix, self, self.rear_socket, self.forced_move, self.eatqueen, self.depth, self.queen, self.promotion_eat)
			custom_dialog_box.destroy()
			if self.pc_first:
				self.checker.play_on_timeout(self.checker.stack)
			self.checker.matrix = self.backend.get_matrix()
			self.checker.resize_checker(self.checker.square_size)
			self.backend.pl_before_firstclick()
		elif self.answer == Gtk.ResponseType.CANCEL:
			custom_dialog_box.destroy()
		open_dialog = 0



	#create a dialog window with 5 choice, each choice gives the rules of the different countries
	def dialog(self,button):
		#Dialog
		self.open_dialog = 1
		dialog_box = Gtk.Dialog.new()
		dialog_box.set_border_width(10)
		dialog_box.connect('delete-event', Gtk.main_quit)
		dialog_box.show_all()
		dialog_box.add_button(Gtk.STOCK_APPLY, Gtk.ResponseType.APPLY)
		dialog_box.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
		self.turn = 1

		#Hit History
		for element in self.hit_history.get_children():
			self.hit_history.remove(element)

		#Frame
		frame_country = Gtk.Frame.new(_("What rules do you want to play with?"))

		#Radio Button
		flag = GdkPixbuf.Pixbuf()
		pixbuf = flag.new_from_file_at_size("/usr/share/gdraughts/images/netherlands.jpg", 30, 30)
		image = Gtk.Image.new_from_pixbuf(pixbuf)
		r_ne = Gtk.RadioButton.new_with_label_from_widget(None, _("Netherlands"))
		r_ne.set_image(image)
		r_ne.set_always_show_image(True)
		self.custom_margin(r_ne, 5, 10, 5, 5)

		pixbuf = flag.new_from_file_at_scale("/usr/share/gdraughts/images/italy.jpg", 30, 30, True)
		image = Gtk.Image.new_from_pixbuf(pixbuf)
		r_ita = Gtk.RadioButton.new_from_widget(r_ne)
		r_ita.set_image(image)
		r_ita.set_label(_("Italy"))
		r_ita.set_always_show_image(True)
		self.custom_margin(r_ita, 5, 5, 5, 5)

		pixbuf = flag.new_from_file_at_scale("/usr/share/gdraughts/images/spain.jpg", 30, 30, True)
		image = Gtk.Image.new_from_pixbuf(pixbuf)
		r_sp = Gtk.RadioButton.new_from_widget(r_ne)
		r_sp.set_label(_("Spain"))
		r_sp.set_image(image)
		r_sp.set_always_show_image(True)
		self.custom_margin(r_sp, 5, 5, 5, 10)

		pixbuf = flag.new_from_file_at_scale("/usr/share/gdraughts/images/uk.jpg", 30, 30, True)
		image = Gtk.Image.new_from_pixbuf(pixbuf)
		r_eng = Gtk.RadioButton.new_from_widget(r_ne)
		r_eng.set_label(_("England"))
		r_eng.set_image(image)
		r_eng.set_always_show_image(True)
		self.custom_margin(r_eng, 5, 5, 5, 5)

		r_fr = Gtk.RadioButton.new_from_widget(r_ne)
		pixbuf = flag.new_from_file_at_scale("/usr/share/gdraughts/images/france.jpg", 30, 30, True)
		image = Gtk.Image.new_from_pixbuf(pixbuf)
		r_fr.set_label(_("France"))
		r_fr.set_image(image)
		r_fr.set_always_show_image(True)
		self.custom_margin(r_fr, 5, 10, 5, 5)

		#Dialog
		box_dialog = dialog_box.get_content_area()
		box_dialog.pack_start(self.level_of_difficulty(), True, True, 4)
		box_dialog.pack_start(self.who_play(), True, True, 4)
		box_dialog.pack_start(frame_country, True, True, 4)

		#Grid
		grid_country = Gtk.Grid()
		grid_country.set_column_spacing(10)
		grid_country.set_row_spacing(10)

		#Frame
		frame_country.add(grid_country)
		
		#Box
		grid_country.set_row_spacing(10)
		grid_country.attach(r_ne, 0, 0, 1, 1)
		grid_country.attach(r_fr, 1, 0, 1, 1)
		grid_country.attach(r_eng, 0, 1, 1, 1)
		grid_country.attach(r_ita, 1, 1, 1, 1)
		grid_country.attach(r_sp, 0, 2, 1, 1)


		if self.country == 0:
			r_fr.set_active(True)
		elif self.country == 1:
			r_sp.set_active(True)
		elif self.country == 2:
			r_eng.set_active(True)
		elif self.country == 3:
			r_ne.set_active(True)
		elif self.country == 4:
			r_ita.set_active(True)

		dialog_box.show_all()
		dialog_box.set_transient_for(self)
		dialog_box.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
		self.answer = dialog_box.run()

		if self.answer == Gtk.ResponseType.APPLY:
			if self.r_player.get_active():
				self.pc_first = False
			else:
				self.pc_first = True

			if r_fr.get_active():
				self.country = 0
				self.state = 10
				self.square_color = 0
				self.eatqueen = True
				self.rear_socket = True
				self.forced_move = True
				self.matrix_classic = True
				self.queen = False
				self.promotion_eat = False
				r_fr.set_active(True)

			elif r_sp.get_active():
				self.country = 1
				self.state = 8
				self.square_color = 0
				self.eatqueen = True
				self.rear_socket = False
				self.forced_move = True
				self.matrix_classic = False
				self.queen = False
				self.promotion_eat = False
				r_sp.set_active(True)

			elif r_eng.get_active():
				self.country = 2
				self.state = 8
				self.square_color = 0
				self.eatqueen = True
				self.rear_socket = False
				self.matrix_classic = True
				self.forced_move = True
				self.queen = False
				self.promotion_eat = False
				r_eng.set_active(True)

			elif r_ne.get_active():
				self.country = 3
				self.state = 10
				self.square_color = 0
				self.eatqueen = True
				self.rear_socket = True
				self.forced_move = True
				self.matrix_classic = True
				self.queen = False
				self.promotion_eat = False
				r_ne.set_active(True)

			elif r_ita.get_active():
				self.country = 4
				self.state = 8
				self.square_color = 1
				self.eatqueen = False
				self.rear_socket = False
				self.forced_move = True
				self.matrix_classic = False
				self.queen = True
				self.promotion_eat = True
				r_ita.set_active(True)

			self.checker_game.remove(self.checker)
			self.checker = Checker(self, self.square_size, self.state, self.square_color)
			self.checker_game.set_center_widget(self.checker)
			self.checker_game.show_all()
			self.backend = Backend(self.checker.matrix, self, self.rear_socket, self.forced_move, self.eatqueen, self.depth, self.queen, self.promotion_eat)
			dialog_box.destroy()
			if self.pc_first:
				self.checker.play_on_timeout(self.checker.stack)
			self.checker.matrix = self.backend.get_matrix()
			self.checker.resize_checker(self.checker.square_size)
			self.backend.pl_before_firstclick()
		elif self.answer == Gtk.ResponseType.CANCEL:
			dialog_box.destroy()
		open_dialog = 0


draughts = Draughts()
draughts.play()
Gtk.main()
