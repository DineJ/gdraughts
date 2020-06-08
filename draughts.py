from gi.repository import Gtk
from checker import Checker
from backend import Backend, Node, Stack
import random


#create application
class Draughts(Gtk.Window): 

	#managing of the main window
	def __init__ (self, state = 8, square_color = 0, square_size = 0, tool_height = 0, checker = None, open_dialog = 0):  
		Gtk.Window.__init__(self)
		self.state = state
		self.square_color = square_color
		self.square_size = square_size
		self.tool_height = tool_height
		self.checker = checker
		self.open_dialog = open_dialog


		self.set_border_width(10)
		self.connect('delete-event', Gtk.main_quit)
		self.connect("check_resize", self.on_resize)
		self.set_default_size(640,480)


		application = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
		game_area = Gtk.Box()
		self.checker_game = Gtk.Box()
		box_color = Gtk.Label()
		box_color.set_markup('<span weight="bold">Historique</span>')
		game_area.set_homogeneous(False)
		application.set_homogeneous(False)


		hit_history = Gtk.ListBox()
		hit_history.insert(box_color, 0)
		hit_history.set_size_request(200, -1)


		img = Gtk.Image.new_from_icon_name('document-exit', 0)
		quit_button = Gtk.ToolButton.new(img)
		img = Gtk.Image.new_from_icon_name('document-new', 0)
		play_button = Gtk.ToolButton.new(img)

		quit_button.set_label("Quitter")
		play_button.set_label("Nouvelle partie")
		quit_button.set_is_important(True)
		play_button.set_is_important(True)


		r_chercker8 = Gtk.RadioButton.new()
		r_chercker10 = Gtk.RadioButton.new()


		tool_bar = Gtk.Toolbar()
		tool_bar.insert(quit_button, 0)
		tool_bar.insert(play_button, 1)
		quit_button.show()
		play_button.show()


		quit_button.connect('clicked', Gtk.main_quit)
		play_button.connect('clicked', self.dialog)


		application.pack_start(tool_bar, False, True, 0)
		application.pack_start(game_area, True, True, 0)
		game_area.pack_start(self.checker_game, True, True, 0)
		game_area.pack_start(hit_history, False, True, 0)

		self.add(application)

	#show the application
	def play(self): 
		self.show_all()

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

		elif self.open_dialog == 0:
			self.checker.resize_checker(self.square_size)

	#create a dialog window with 4 choice, 2 for color of square and 2 about size of checker
	def dialog(self,button): 
		self.open_dialog = 1
		#Dialog
		dialog_box = Gtk.Dialog.new()
		dialog_box.set_border_width(10)
		dialog_box.connect('delete-event', Gtk.main_quit)
		dialog_box.show_all()
		dialog_box.add_button(Gtk.STOCK_APPLY, Gtk.ResponseType.APPLY)
		dialog_box.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)


		#Frame
		frame_matrice = Gtk.Frame.new("Choix du nombre de cases")
		frame_color = Gtk.Frame.new("Cases en bas a droite")

		#Radio Button
		r_chercker8 = Gtk.RadioButton.new_with_label_from_widget(None, "8 cases")
		r_chercker10 = Gtk.RadioButton.new_from_widget(r_chercker8)
		r_chercker10.set_label("10 cases")
		r_color_w = Gtk.RadioButton.new_with_label_from_widget(None, "Blanc")
		r_color_b = Gtk.RadioButton.new_from_widget(r_color_w)
		r_color_b.set_label("Noirs")



		#Dialog
		box_dialog = dialog_box.get_content_area()
		box_dialog.pack_start(frame_matrice, True, True, 0)
		box_dialog.pack_start(frame_color, True, True, 0)

		#Box
		box_matrice = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		box_color = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

		#Frame
		frame_matrice.add(box_matrice)
		frame_color.add(box_color)

		#Box
		box_matrice.pack_start(r_chercker8, True, True, 0)
		box_matrice.pack_start(r_chercker10, True, True, 0)
		box_color.pack_start(r_color_w, True, True, 0)
		box_color.pack_start(r_color_b, True, True, 0)


		if self.state == 8:
			r_chercker8.set_active(True)
		else:
			r_chercker10.set_active(True)

		if self.square_color == 0:
			r_color_w.set_active(True)
		else:
			r_color_b.set_active(True)

		dialog_box.show_all()

		answer = dialog_box.run()
		if answer == Gtk.ResponseType.APPLY:
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
			self.checker_game.remove(self.checker)
			self.checker = Checker(self, self.square_size, self.state, self.square_color)
			self.checker_game.set_center_widget(self.checker)
			self.checker_game.show_all()
			self.backend = Backend(self.checker.matrix)
			#self.checker.queue_draw()
			dialog_box.destroy()
			#pl_moves = self.backend.possible_moves(1)
			pc_moves = self.backend.possible_moves(2)
			# Choix aleatoire du pion déplacée
			rand_move = random.choice(pc_moves)
			# Déplacement de la pièces>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<>><<<<<<<<<
			#self.backend.move(checker.square.name[0],checker.square.name[1],1)
			self.backend.move(rand_move[0], rand_move[1], 2)
			#pl_before_firstclick()
			self.checker.matrix = self.backend.get_matrix()
			self.checker.resize_checker(self.checker.square_size)
			#self.pl_move()
		elif answer == Gtk.ResponseType.CANCEL:
			dialog_box.destroy()
		open_dialog = 0


#test = Board(self.checker.matrix)
draughts = Draughts()
draughts.play()
#test.play()
Gtk.main()
