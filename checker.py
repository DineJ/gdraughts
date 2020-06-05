from gi.repository import Gtk, Gdk, cairo, Pango, PangoCairo
from squarearea import SquareArea

#create the checker game
class Checker(Gtk.Grid): 
    def __init__ (self, square_size = 1, matrix_size = 10, color = 0):
        Gtk.Grid.__init__(self)
        self.old_square = None
        self.color = color
        self.square_size = square_size
        self.matrix_size = matrix_size

        self.matrix8 = [[0, 2, 0, 2, 0, 2, 0, 2],
                        [2, 0, 2, 0, 2, 0, 2, 0],
                        [0, 2, 0, 2, 0, 2, 0, 2],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [1, 0, 1, 0, 1, 0, 1, 0],
                        [0, 1, 0, 1, 0, 1, 0, 1],
                        [1, 0, 1, 0, 1, 0, 1, 0]]

        self.matrix10 =[[0, 2, 0, 2, 0, 2, 0, 2, 0, 2],
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
            self.matrix = self.matrix8
        else:
            self.matrix = self.matrix10
        self.create_tableau()

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
                pawn_color = 0
                type_pawn = 0
                test = self.matrix[y][x]

                if test == 1:
                    pawn_color = 1
                    type_pawn = 1
                elif test == 2:
                    pawn_color = 0
                    type_pawn = 1
                name =  [y,x]
                if color %2 == 0:
                    square_b = SquareArea(name,0.0, self.square_size, test)#type_pawn, pawn_color)
                    square_b.connect('button-press-event', self.do_release_mouse, square_b)

                    #self.connect('drag_data_received', self.drag_drop(self.old_square, square_b))
                    #self.drag_dest_set(0, [], 0)
                    
                    self.attach(square_b, x, y, 1, 1)
                    square_b.queue_draw()
                    x += 1
                    color += 1
                else:
                    square_w = SquareArea(name,1.0, self.square_size, test)#type_pawn, pawn_color)
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
                print("y= ", y, "x= ", x)
                checker_square.resize_pawn(self.square_size)
                x += 1
            y += 1

    #move a pawn
    def do_release_mouse(self, widget, event, square): 
        if self.old_square == None:
            if square.square_type != 0:
                self.old_square = square
                #print("square non vide")
            print ("Mouse clicked... at (%s)" % (square.name))
        else:
            print("je fais l'echange %s %s" % (self.old_square.name, square.name))
            if square.color == self.old_square.color:
                self.echange_square(self.old_square, square)
                #self.drag_drop(self.old_square, square)
                self.old_square = None
                #print("square meme color")

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
