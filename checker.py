from gi.repository import Gtk, Gdk, cairo, Pango, PangoCairo, GLib
from squarearea import SquareArea
from backend import Backend, Node, Stack
import random
import time

#create the checker game
class Checker(Gtk.Grid):
    def __init__ (self, draughts=None, square_size=1, matrix_size=10, color=0):
        Gtk.Grid.__init__(self)
        self.draughts = draughts
        self.old_square = None
        self.color = color
        self.square_size = square_size
        self.matrix_size = matrix_size
        self.stack = Stack([4, 3, 3])

        self.matrix8    =  [[0, 2, 0, 2, 0, 2, 0, 2],
                            [2, 0, 2, 0, 2, 0, 2, 0],
                            [0, 2, 0, 2, 0, 2, 0, 2],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [1, 0, 1, 0, 1, 0, 1, 0],
                            [0, 1, 0, 1, 0, 1, 0, 1],
                            [1, 0, 1, 0, 1, 0, 1, 0]]

        self.matrix8v2  =  [[2, 0, 2, 0, 2, 0, 2, 0],
                            [0, 2, 0, 2, 0, 2, 0, 2],
                            [2, 0, 2, 0, 2, 0, 2, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 1, 0, 1, 0, 1, 0, 1],
                            [1, 0, 1, 0, 1, 0, 1, 0],
                            [0, 1, 0, 1, 0, 1, 0, 1]]

        self.matrix10 =    [[0, 2, 0, 2, 0, 2, 0, 2, 0, 2],
                            [2, 0, 2, 0, 2, 0, 2, 0, 2, 0],
                            [0, 2, 0, 2, 0, 2, 0, 2, 0, 2],
                            [2, 0, 2, 0, 2, 0, 2, 0, 2, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]]

        if matrix_size == 8 :
            if self.draughts.matrix_classic:
                self.matrix = self.matrix8
            else:
                self.matrix = self.matrix8v2
        else:
            self.matrix = self.matrix10
        self.create_tableau()
    
    def print_pc_hit(self, number):
        compteur = 0
        self.z = number
        while number > 10:
            compteur += 1
            number = int(number/10)
        self.w = int((self.z - number*10**compteur)/10**(compteur-1))
        self.x = int (((self.z - number*10**compteur) - (self.w*10**(compteur-1))) / 10)
        self.y = int (((self.z - number*10**compteur) - (self.w*10**(compteur-1))) - self.x*10**(compteur-2))
        return number,self.w,self.x,self.y
        
    #after you choose an option in dialog window, that destroy the last checker and build another one
    def modify_checker(self, matrix_size = 10, color = 0): 
        self.square_size = (self.square_size * self.matrix_size) / matrix_size
        self.hide()
        while True:
            if self.get_child_at(0,1)!= None:
                self.remove_row(1)
            else:
                break
        self.matrix_size = matrix_size

        if matrix_size == 8 :
            self.matrix = self.matrix8
        else:
            self.matrix = self.matrix10

        self.color = color
        self.create_tableau()

    #create checker
    def create_tableau(self): 
        color = self.color
        y = 0
        while y < self.matrix_size:
            x = 0
            color += 1

            while x < self.matrix_size:
                test = self.matrix[y][x]
                name =  [y,x]
                if color %2 == 0:
                    color_pawn = 0.0
                    square_b = SquareArea(name,color_pawn, self.square_size, test, self.draughts.pc_first)
                    square_b.connect('button-press-event', self.do_release_mouse, square_b)

                    #self.connect('drag_data_received', self.drag_drop(self.old_square, square_b))
                    #self.drag_dest_set(0, [], 0)
                    
                    self.attach(square_b, x, y, 1, 1)
                    square_b.queue_draw()
                    x += 1
                    color += 1
                else:
                    color_pawn = 1.0
                    square_w = SquareArea(name,color_pawn, self.square_size, test, self.draughts.pc_first)
                    square_w.connect('button-press-event', self.do_release_mouse, square_w)
                    
                    #self.connect('drag_data_received', self.drag_drop(self.old_square, square_w))
                    #self.drag_dest_set(0, [], 0)

                    self.attach(square_w, x, y, 1, 1)
                    square_w.queue_draw()
                    x += 1
                    color += 1
            y += 1
        self.show_all()

    #draw a checker
    def do_draw_cb(self):
        y = 0
        while y < self.matrix_size:
            x = 0
            while x < self.matrix_size:
                checker_square = self.get_child_at(x, y)
                checker_square.resize_pawn(self.square_size)
                x += 1
            y += 1


    def play_on_timeout(self, stack):
        if self.draughts.backend.fin == False:
            row2 = None
            self.draughts.informations_bar.set_markup("<span foreground='#ff710d' size='large' >A vous de jouer </span>")
            self.draughts.backend.pc_move(stack)
            jump = self.draughts.backend.lastjump[:]
            if len(str(jump[0])) == 4 :
                if (self.print_pc_hit(jump[0])[0] - self.print_pc_hit(jump[0])[2] !=1 and self.print_pc_hit(jump[0])[0] - self.print_pc_hit(jump[0])[2] != -1) or (self.print_pc_hit(jump[0])[1] - self.print_pc_hit(jump[0])[3] !=1 and self.print_pc_hit(jump[0])[1] - self.print_pc_hit(jump[0])[3] != -1):
                    row2 = ("Coup %d : (%s,%s) x (%s,%s)" % (self.draughts.turn, str(jump[0])[0], str(jump[0])[1], str(jump[0])[2], str(jump[0])[3]))
                else:
                    row2 = ("Coup %d : (%s,%s) - (%s,%s)" % (self.draughts.turn, str(jump[0])[0], str(jump[0])[1], str(jump[0])[2], str(jump[0])[3]))
            elif len(str(jump[0])) == 3:
                if (self.print_pc_hit(jump[0])[1] - self.print_pc_hit(jump[0])[2] !=1 and self.print_pc_hit(jump[0])[1] - self.print_pc_hit(jump[0])[2] != -1) or (self.print_pc_hit(jump[0])[0] - self.print_pc_hit(jump[0])[3] !=1 and self.print_pc_hit(jump[0])[0] - self.print_pc_hit(jump[0])[3] != -1):
                    row2 = ("Coup %d : (0,%s) x (%s,%s)" % (self.draughts.turn, str(jump[0])[0], str(jump[0])[1], str(jump[0])[2]))
                else:
                    row2 = ("Coup %d : (0,%s) - (%s,%s)" % (self.draughts.turn, str(jump[0])[0], str(jump[0])[1], str(jump[0])[2]))
            self.draughts.row_label2 = Gtk.Label(row2)
            if self.draughts.pc_first == False:
                self.draughts.turn += 1
            self.draughts.row_label2.show_all()
            self.draughts.hit_history.prepend(self.draughts.row_label2)
            jump = []
            self.draughts.checker.matrix = self.draughts.backend.get_matrix()
            self.draughts.checker.resize_checker(self.draughts.checker.square_size)
            play = self.draughts.backend.possible_moves(1)
            if len(play) == 0:
                 self.draughts.informations_bar.set_markup("<span foreground='#ff710d' size='large' >L'ordinateur a gagne</span>")
                 self.draughts.backend.fin = True
                 return 1


    #move a pawn
    def do_release_mouse(self, widget, event, square):
        if self.old_square == None:
            if self.draughts.backend.pl_after_firstclick(square.name) == 0:
                return
            if square.square_type != 0:
                self.old_square = square
        else:
            if 1 :
                if self.draughts.backend.pl_after_secondclick(self.old_square.name, square.name) == 0:
                    self.old_square = None
                    return
                play = self.draughts.backend.possible_moves(2)
                if play:
                    if (self.old_square.name[0] - square.name[0] != 1 and self.old_square.name[0] - square.name[0] != -1) or (self.old_square.name[1] - square.name[1] != 1 and self.old_square.name[1] - square.name[1] != -1):
                        self.draughts.row_label1 = Gtk.Label("Coup %d : %d,%d x %d,%d" % (self.draughts.turn, self.old_square.name[0], self.old_square.name[1], square.name[0], square.name[1]))
                    else:
                        self.draughts.row_label1 = Gtk.Label("Coup %d : %d,%d - %d,%d" % (self.draughts.turn, self.old_square.name[0], self.old_square.name[1], square.name[0], square.name[1]))
                    self.draughts.row_label1.show_all()
                    self.draughts.hit_history.prepend(self.draughts.row_label1)
                self.old_square = None
                self.draughts.checker.matrix = self.draughts.backend.get_matrix()
                self.draughts.checker.resize_checker(self.draughts.checker.square_size)
                if len(play) == 0:
                    self.draughts.informations_bar.set_markup("<span foreground='#ff710d' size='large' >Tu as gagne</span>")
                    self.draughts.backend.fin = True
                    return 0
                if self.draughts.pc_first:
                    self.draughts.turn += 1
                self.draughts.backend.lastjump[:] = []
                GLib.timeout_add(2.0, self.play_on_timeout, self.stack)
                self.draughts.informations_bar.set_markup("<span foreground='#ff710d' size='large' >A l'ordinateur de jouer </span>")

    #change square
    def echange_square(self, old_square, square): 
        temp = old_square.color
        old_square.color = square.color
        square.color = temp

        temp = old_square.square_type
        old_square.square_type = square.square_type
        square.square_type = temp

        old_square.queue_draw()
        square.queue_draw()


    #resize checker after each interraction
    def resize_checker(self, square_size): 
        self.square_size = square_size
        size = self.matrix_size
        y = 0
        while y < size:
            x = 0
            while x < size:
                checker_square = self.get_child_at(x, y)
                checker_square.square_type = int(self.matrix[y][x])
                checker_square.resize_pawn(square_size)
                x += 1
            y += 1


    #def drag_drop(self, old_square, square):
        #self.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, old_square, Gdk.DragAction.MOVE)
        #self.drag_dest_set(Gdk.DestDefaults.DROP, square, Gdk.DragAction.MOVE)
        #self.SelectionData.get_data()
        #self.TargetEntry()
