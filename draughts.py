"""Copyright (C) 2020 Jridi Dine

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


from gi.repository import Gtk
from checker import Checker
from backend import Backend, Node, Stack
import random


#create application
class Draughts(Gtk.Window):

	#managing of the main window
	def __init__ (self, pc_first=False, country=3, matrix_classic=True, state=8, square_color=0, square_size=0, tool_height=0, checker=None, open_dialog=0, rear_socket=True): # country : 0 = France(fr), 1 = Spain(sp), 2 = England(eng), 3 = Netherlands(ne), 4 = Italy(ita)
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
		self.head_label.set_markup('<span weight="bold">Historique</span>')
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

		quit_button.set_label("Quitter")
		play_button.set_label("Nouvelle partie")
		custom_button.set_label("Parametres")
		quit_button.set_is_important(True)
		play_button.set_is_important(True)
		custom_button.set_is_important(True)


		self.informations_bar = Gtk.Label()
		self.informations_bar.set_markup("<span foreground='#ff710d' size='large' >Commencez une nouvelle partie</span>")
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

	#show the application
	def play(self):
		self.show_all()
		self.backend = Backend(self.checker.matrix)
		self.backend.fin = False
		self.backend.rear_socket = False
		self.backend.pl_before_firstclick()

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

		frame_begin = Gtk.Frame.new("Qui joue en premier ?")
		frame_matrice = Gtk.Frame.new("Combien de cases voulez-vous par ligne?")
		frame_color = Gtk.Frame.new("Quelle couleur voulez-vous dans la case en bas à droite ?")
		frame_color1 = Gtk.Frame.new("Voulez-vous que votre pion soit en bas à droite?")

		r_player = Gtk.RadioButton.new_with_label_from_widget(None, "Joueur")
		r_computer = Gtk.RadioButton.new_from_widget(r_player)
		r_computer.set_label("Ordinateur")
		r_chercker8 = Gtk.RadioButton.new_with_label_from_widget(None, "8 cases")
		r_chercker10 = Gtk.RadioButton.new_from_widget(r_chercker8)
		r_chercker10.set_label("10 cases")
		r_color_w = Gtk.RadioButton.new_with_label_from_widget(None, "Blanches")
		r_color_b = Gtk.RadioButton.new_from_widget(r_color_w)
		r_color_b.set_label("Noires")
		r_color1_b = Gtk.RadioButton.new_with_label_from_widget(None, "Non")
		r_color1_w = Gtk.RadioButton.new_from_widget(r_color1_b)
		r_color1_w.set_label("Oui")

		#Dialog
		box_dialog = custom_dialog_box.get_content_area()
		box_dialog.pack_start(frame_begin, True, True, 0)
		box_dialog.pack_start(frame_matrice, True, True, 0)
		box_dialog.pack_start(frame_color, True, True, 0)
		box_dialog.pack_start(frame_color1, True, True, 0)


		#Box
		box_begin = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		box_matrice = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.box_color = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.box_color1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

		frame_begin.add(box_begin)
		frame_matrice.add(box_matrice)
		frame_color.add(self.box_color)
		frame_color1.add(self.box_color1)

		#Box
		box_begin.pack_start(r_player, True, True, 0)
		box_begin.pack_start(r_computer, True, True, 0)

		box_matrice.pack_start(r_chercker8, True, True, 0)
		box_matrice.pack_start(r_chercker10, True, True, 0)

		self.box_color.pack_start(r_color_w, True, True, 0)
		self.box_color.pack_start(r_color_b, True, True, 0)

		self.box_color1.pack_start(r_color1_w, True, True, 0)
		self.box_color1.pack_start(r_color1_b, True, True, 0)

		if self.pc_first:
			r_computer.set_active(True)
		else:
			r_player.set_active(True)

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

		custom_dialog_box.show_all()
		answer = custom_dialog_box.run()

		if answer == Gtk.ResponseType.APPLY:
			if r_player.get_active():
				self.pc_first = False
				r_player.set_active(True)
			else:
				self.pc_first = True
				r_computer.set_active(True)

			if r_chercker8.get_active():
				self.state = 8 
				r_chercker8.set_active(True)
			else:
				self.state = 10
				r_chercker10.set_active(True)

			if r_color_w.get_active():
				self.square_color = 0
			else:
				self.square_color = 1
				self.matrix_classic = False

			if r_color1_w.get_active():
				self.matrix_classic = False
				r_color1_w.set_active(True)
			else:
				self.matrix_classic = True
				r_color1_b.set_active(True)

			self.checker_game.remove(self.checker)
			self.checker = Checker(self, self.square_size, self.state, self.square_color)
			self.checker_game.set_center_widget(self.checker)
			self.checker_game.show_all()
			self.backend = Backend(self.checker.matrix, self.rear_socket)
			#self.checker.queue_draw()
			custom_dialog_box.destroy()
			#pl_moves = self.backend.possible_moves(1)
			if self.pc_first:
				self.checker.play_on_timeout(self.checker.stack)
			self.checker.matrix = self.backend.get_matrix()
			self.checker.resize_checker(self.checker.square_size)
			self.backend.pl_before_firstclick()
			#self.backend.move(self.checker.square.name[0], self.checker.square.name[1],1)
			#self.pl_move()
		elif answer == Gtk.ResponseType.CANCEL:
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
		frame_country = Gtk.Frame.new("Avec quelles règles voulez-vous jouer?")

		#Radio Button
		r_ne = Gtk.RadioButton.new_with_label_from_widget(None, "Netherlands")
		r_ita = Gtk.RadioButton.new_from_widget(r_ne)
		r_ita.set_label("Italy")
		r_sp = Gtk.RadioButton.new_from_widget(r_ne)
		r_sp.set_label("Spain")
		r_eng = Gtk.RadioButton.new_from_widget(r_ne)
		r_eng.set_label("England")
		r_fr = Gtk.RadioButton.new_from_widget(r_ne)
		r_fr.set_label("France")

		#Dialog
		box_dialog = dialog_box.get_content_area()
		box_dialog.pack_start(frame_country, True, True, 0)

		#Box
		box_country = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

		#Frame
		frame_country.add(box_country)

		#Box
		box_country.pack_start(r_ne, True, True, 0)
		box_country.pack_start(r_fr, True, True, 0)
		box_country.pack_start(r_eng, True, True, 0)
		box_country.pack_start(r_ita, True, True, 0)
		box_country.pack_start(r_sp, True, True, 0)


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
		answer = dialog_box.run()

		if answer == Gtk.ResponseType.APPLY:

			if r_fr.get_active():
				self.country = 0
				self.state = 10
				self.rear_socket = True
				self.matrix_classic = True
				r_fr.set_active(True)

			elif r_sp.get_active():
				self.country = 1
				self.state = 8
				self.square_color = 0
				self.rear_socket = False
				self.matrix_classic = False
				r_sp.set_active(True)

			elif r_eng.get_active():
				self.country = 2
				self.state = 8
				self.rear_socket = False
				self.matrix_classic = True
				r_eng.set_active(True)

			elif r_ne.get_active():
				self.country = 3
				self.state = 10
				self.rear_socket = True
				self.matrix_classic = True
				r_ne.set_active(True)

			elif r_ita.get_active():
				self.country = 4
				self.state = 8
				self.square_color = 1
				self.rear_socket = False
				self.matrix_classic = False
				r_ita.set_active(True)

			self.checker_game.remove(self.checker)
			self.checker = Checker(self, self.square_size, self.state, self.square_color)
			self.checker_game.set_center_widget(self.checker)
			self.checker_game.show_all()
			self.backend = Backend(self.checker.matrix, self.rear_socket)
			#self.checker.queue_draw()
			dialog_box.destroy()
			#pl_moves = self.backend.possible_moves(1)
			if self.pc_first:
				self.checker.play_on_timeout(self.checker.stack)
			self.checker.matrix = self.backend.get_matrix()
			self.checker.resize_checker(self.checker.square_size)
			self.backend.pl_before_firstclick()
			#self.backend.move(self.checker.square.name[0], self.checker.square.name[1],1)
			#self.pl_move()
		elif answer == Gtk.ResponseType.CANCEL:
			dialog_box.destroy()
		open_dialog = 0


#test = Board(self.checker.matrix)
draughts = Draughts()
draughts.play()
#test.play()
Gtk.main()
