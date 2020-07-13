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
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, cairo, Pango, PangoCairo, GLib
from squarearea import SquareArea
from backend import Backend, Node, Stack
import random
import time
import gettext

#create the checker game
class Checker(Gtk.Grid):
    def __init__ (self, draughts=None, square_size=1, matrix_size=10, color=0, matrix_coordonate=None):
        Gtk.Grid.__init__(self)
        self.draughts = draughts
        self.old_square = None
        self.color = color
        self.square_size = square_size
        self.matrix_size = matrix_size
        self.matrix_coordonate = matrix_coordonate
        self.replay = False
        self.rafle = False
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

        self.matrix10v2 =  [[2, 0, 2, 0, 2, 0, 2, 0, 2, 0],
                            [0, 2, 0, 2, 0, 2, 0, 2, 0, 2],
                            [2, 0, 2, 0, 2, 0, 2, 0, 2, 0],
                            [0, 2, 0, 2, 0, 2, 0, 2, 0, 2],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]]

        self.matrix8_notation  =       [[0, 1, 0, 2, 0, 3, 0, 4],
                                        [5, 0, 6, 0, 7, 0, 8, 0],
                                        [0, 9, 0, 10, 0, 11, 0,12],
                                        [13, 0, 14, 0, 15, 0, 16, 0],
                                        [0, 17, 0, 18, 0, 19, 0, 20],
                                        [21, 0, 22, 0, 23, 0, 24, 0],
                                        [0, 25, 0, 26, 0, 27, 0, 28],
                                        [29, 0, 30, 0, 31, 0, 32, 0]]

        self.matrix8_notationv2  =     [[0, 32, 0, 31, 0, 30, 0, 29],
                                        [28, 0, 27, 0, 26, 0, 25, 0],
                                        [0, 24, 0, 23, 0, 22, 0, 21],
                                        [20, 0, 19, 0, 18, 0, 17, 0],
                                        [0, 16, 0, 15, 0, 14, 0, 13],
                                        [12, 0, 11, 0, 10, 0, 9, 0],
                                        [0, 8, 0, 7, 0, 6, 0, 5],
                                        [4, 0, 3, 0, 2, 0, 1, 0]]


        self.matrix8v2_notation  =     [[1, 0, 2, 0, 3, 0, 4, 0],
                                        [0, 5, 0, 6, 0, 7, 0, 8],
                                        [9, 0, 10, 0, 11, 0, 12, 0],
                                        [0, 13, 0, 14, 0, 15, 0, 16],
                                        [17, 0, 18, 0, 19, 0, 20, 0],
                                        [0, 21, 0, 22, 0, 23, 0, 24],
                                        [25, 0, 26, 0, 27, 0, 28, 0],
                                        [0, 29, 0, 30, 0, 31, 0, 32]]

        self.matrix8v2_notationv2  =   [[32, 0, 31, 0, 30, 0, 29, 0],
                                        [0, 28, 0, 27, 0, 26, 0, 25],
                                        [24, 0, 23, 0, 22, 0, 21, 0],
                                        [0, 20, 0, 19, 0, 18, 0, 17],
                                        [16, 0, 15, 0, 14, 0, 13, 0],
                                        [0, 12, 0, 11, 0, 10, 0, 9],
                                        [8, 0, 7, 0, 6, 0, 5, 0],
                                        [0, 4, 0, 3, 0, 2, 0, 1]]

        self.matrix10_notation =       [[0, 1, 0, 2, 0, 3, 0, 4, 0, 5],
                                        [6, 0, 7, 0, 8, 0, 9, 0, 10, 0],
                                        [0, 11, 0, 12, 0, 13, 0, 14, 0, 15],
                                        [16, 0, 17, 0, 18, 0, 19, 0, 20, 0],
                                        [0, 21, 0, 22, 0, 23, 0, 24, 0, 25],
                                        [26, 0, 27, 0, 28, 0, 29, 0, 30, 0],
                                        [0, 31, 0, 32, 0, 33, 0, 34, 0, 35],
                                        [36, 0, 37, 0, 38, 0, 39, 0, 40, 0],
                                        [0, 41, 0, 42, 0, 43, 0, 44, 0, 45],
                                        [46, 0, 47, 0, 48, 0, 49, 0, 50, 0]]

        self.matrix10_notationv2   =   [[0, 50, 0, 49, 0, 48, 0, 47, 0, 46],
                                        [45, 0, 44, 0, 43, 0, 42, 0, 41, 0],
                                        [0, 40, 0, 39, 0, 38, 0, 37, 0, 36],
                                        [35, 0, 34, 0, 33, 0, 32, 0, 31, 0],
                                        [0, 30, 0, 29, 0, 28, 0, 27, 0, 26],
                                        [25, 0, 24, 0, 23, 0, 22, 0, 21, 0],
                                        [0, 20, 0, 19, 0, 18, 0, 17, 0, 16],
                                        [15, 0, 14, 0, 13, 0, 12, 0, 11, 0],
                                        [0, 10, 0, 9, 0, 8, 0, 7, 0, 6],
                                        [5, 0, 4, 0, 3, 0, 2, 0, 1, 0]]

        self.matrix10v2_notation =     [[1, 0, 2, 0, 3, 0, 4, 0, 5, 0],
                                        [0, 6, 0, 7, 0, 8, 0, 9, 0, 10],
                                        [11, 0, 12, 0, 13, 0, 14, 0, 15, 0],
                                        [0, 16, 0, 17, 0, 18, 0, 19, 0, 20],
                                        [21, 0, 22, 0, 23, 0, 24, 0, 25, 0],
                                        [0, 26, 0, 27, 0, 28, 0, 29, 0, 30],
                                        [31, 0, 32, 0, 33, 0, 34, 0, 35, 0],
                                        [0, 36, 0, 37, 0, 38, 0, 39, 0, 40],
                                        [41, 0, 42, 0, 43, 0, 44, 0, 45, 0],
                                        [0, 46, 0, 47, 0, 48, 0, 49, 0, 50]]

        self.matrix10v2_notationv2 =   [[50, 0, 49, 0, 48, 0, 47, 0, 46, 0],
                                        [0, 45, 0, 44, 0, 43, 0, 42, 0, 41],
                                        [40, 0, 39, 0, 38, 0, 37, 0, 36, 0],
                                        [0, 35, 0, 34, 0, 33, 0, 32, 0, 31],
                                        [30, 0, 29, 0, 28, 0, 27, 0, 26, 0],
                                        [0, 25, 0, 24, 0, 23, 0, 22, 0, 21],
                                        [20, 0, 19, 0, 18, 0, 17, 0, 16, 0],
                                        [0, 15, 0, 14, 0, 13, 0, 12, 0, 11],
                                        [10, 0, 9, 0, 8, 0, 7, 0, 6, 0],
                                        [0, 5, 0, 4, 0, 3, 0, 2, 0, 1]]

        if matrix_size == 8 :
            if self.draughts.matrix_classic:
                self.matrix = self.matrix8
                if self.draughts.pc_first:
                    self.matrix_coordonate = self.matrix8_notationv2
                else:
                    self.matrix_coordonate = self.matrix8_notation 
            else:
                self.matrix = self.matrix8v2
                if self.draughts.pc_first:
                    self.matrix_coordonate = self.matrix8v2_notationv2
                else:
                    self.matrix_coordonate = self.matrix8v2_notation
        else:
            if self.draughts.matrix_classic:
                self.matrix = self.matrix10
                if self.draughts.pc_first:
                    self.matrix_coordonate = self.matrix10_notationv2
                else:
                    self.matrix_coordonate = self.matrix10_notation
            else:
                self.matrix = self.matrix10v2
                if self.draughts.pc_first:
                    self.matrix_coordonate = self.matrix10v2_notationv2
                else:
                    self.matrix_coodonate = self.matrix10v2_notation
        self.create_tableau()

    #this funtion makes it possible to display the hits of the computer
    def print_pc_hit(self, number):
        counter = 0
        z = number
        while number > 10:
            counter += 1
            number = int(number/10)
        w = int((z - number*10**counter)/10**(counter-1))
        x = int (((z - number*10**counter) - (w*10**(counter-1))) / 10)
        y = int (((z - number*10**counter) - (w*10**(counter-1))) - x*10**(counter-2))
        return number,w,x,y


    #after you choose an option in dialog window, it destroy the last checker and build another one
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

    #all this part is about pc (move,hit,game over)
    def play_on_timeout(self, stack):
        if self.draughts.backend.fin == False:
            self.draughts.set_informations(_("Your turn"))
            self.draughts.backend.pc_move(stack)
            jump = self.draughts.backend.lastjump[:]
            if len(str(jump[0])) == 4 :
                if (self.print_pc_hit(jump[0])[0] - self.print_pc_hit(jump[0])[2] !=1 and self.print_pc_hit(jump[0])[0] - self.print_pc_hit(jump[0])[2] != -1) or (self.print_pc_hit(jump[0])[1] - self.print_pc_hit(jump[0])[3] !=1 and self.print_pc_hit(jump[0])[1] - self.print_pc_hit(jump[0])[3] != -1):
                    row1 = ("%s" % (self.matrix_coordonate[int(str(jump[0])[0])][int(str(jump[0])[1])]))
                    row2 = ("%s" % (self.matrix_coordonate[int(str(jump[0])[2])][int(str(jump[0])[3])]))
                    if self.draughts.pc_first == False:
                        row3 = ('%s %d : (%s) x (%s)' % (_("Hit"),self.draughts.turn,row1,row2))
                    else:
                        row3 = ('%s %d : %s x %s' % (_("Hit"),self.draughts.turn,row1,row2))
                else:
                    row1 = ("%s" % (self.matrix_coordonate[int(str(jump[0])[0])][int(str(jump[0])[1])]))
                    row2 = ("%s" % (self.matrix_coordonate[int(str(jump[0])[2])][int(str(jump[0])[3])]))
                    if self.draughts.pc_first == False:
                        row3 = ('%s %d : (%s) - (%s)' % (_("Hit"),self.draughts.turn,row1,row2))
                    else:
                        row3 = ('%s %d : %s - %s' % (_("Hit"),self.draughts.turn,row1,row2))
            elif len(str(jump[0])) == 3:
                if (self.print_pc_hit(jump[0])[1] - self.print_pc_hit(jump[0])[2] !=1 and self.print_pc_hit(jump[0])[1] - self.print_pc_hit(jump[0])[2] != -1) or (self.print_pc_hit(jump[0])[0] - self.print_pc_hit(jump[0])[3] !=1 and self.print_pc_hit(jump[0])[0] - self.print_pc_hit(jump[0])[3] != -1):
                    row1 = ("%s" % (self.matrix_coordonate[int(str("0"))][int(str(jump[0])[0])]))
                    row2 = ("%s" % (self.matrix_coordonate[int(str(jump[0])[1])][int(str(jump[0])[2])]))
                    if self.draughts.pc_first == False:
                        row3 = ('%s %d : (%s) x (%s)' % (_("Hit"),self.draughts.turn,row1,row2))
                    else:
                        row3 = ('%s %d : %s x %s' % (_("Hit"),self.draughts.turn,row1,row2))
                else:
                    row1 = ("%s" % (self.matrix_coordonate[int(str("0"))][int(str(jump[0])[0])]))
                    row2 = ("%s" % (self.matrix_coordonate[int(str(jump[0])[1])][int(str(jump[0])[2])]))
                    if self.draughts.pc_first == False:
                        row3 = ('%s %d : (%s) - (%s)' % (_("Hit"),self.draughts.turn,row1,row2))
                    else:
                        row3 = ('%s %d : %s - %s' % (_("Hit"),self.draughts.turn,row1,row2))
            self.draughts.row_label2 = Gtk.Label(row3)
            if self.draughts.pc_first == False:
                self.draughts.turn += 1
            self.draughts.row_label2.show_all()
            self.draughts.hit_history.prepend(self.draughts.row_label2)
            jump = []
            self.matrix = self.draughts.backend.get_matrix()
            self.resize_checker(self.draughts.checker.square_size)
            play = self.draughts.backend.possible_moves(1)
            if len(play) == 0:
                self.draughts.hit_history.remove(self.draughts.hit_history.get_children()[0])
                self.draughts.set_informations(_("The computer won"))
                self.draughts.backend.fin = True
                self.draughts.row_endgame = Gtk.Label(" %s+ " % (row3))
                self.draughts.row_endgame.show_all()
                self.draughts.hit_history.prepend(self.draughts.row_endgame)
                return 1


    #all this part is about player (move,hit,game over)
    def do_release_mouse(self, widget, event, square):
        if self.draughts.backend.fin == False:
            if self.old_square == None:
                if self.draughts.backend.pl_after_firstclick(square.name) == 0:
                    return
                if square.square_type != 0:
                    self.old_square = square
            else:
                row3 = None
                if 1 :
                    ret = self.draughts.backend.pl_after_secondclick(self.old_square.name, square.name)
                    if ret == 0:
                        self.old_square = None
                        if self.replay:
                            self.replay = False
                        else:
                            self.draughts.set_informations(_("You made an illegal hit, start your hit again"))
                            return
                        if self.draughts.backend.force_jump:
                            
                            self.draughts.set_informations(_("You are forced to continue eating"))
                            return
                    if ret == 2:
                        self.rafle = True
                        self.square_notation = self.old_square
                        self.matrix = self.draughts.backend.get_matrix()
                        self.resize_checker(self.draughts.checker.square_size)
                        self.old_square = square
                        self.replay = True
                        return
                    play = self.draughts.backend.possible_moves(2)
                    if ret == 4:
                        row1 = ("%d" % (self.matrix_coordonate[int(str(self.old_square.name[0]))][int(str(self.old_square.name[1]))]))
                        row2 = ("%d" % (self.matrix_coordonate[int(str(square.name[0]))][int(str(square.name[1]))])) 
                        if self.rafle:
                            row1 = ("%d" % (self.matrix_coordonate[int(str(self.square_notation.name[0]))][int(str(self.square_notation.name[1]))]))
                            self.rafle = False
                            self.replay = False
                        if self.draughts.pc_first == False:
                            row3 = ('%s %d : %s x %s' % (_("Hit"),self.draughts.turn,row1,row2))
                        else:
                            row3 = ('%s %d : (%s) x (%s)' % (_("Hit"),self.draughts.turn,row1,row2))
                    elif ret == 1:
                        row1 = ("%d" % (self.matrix_coordonate[int(str(self.old_square.name[0]))][int(str(self.old_square.name[1]))]))
                        row2 = ("%d" % (self.matrix_coordonate[int(str(square.name[0]))][int(str(square.name[1]))]))
                        if self.draughts.pc_first == False:
                            row3 = ('%s %d : %s - %s' % (_("Hit") ,self.draughts.turn,row1,row2))
                        else:
                            row3 = ('%s %d : (%s) - (%s)' % (_("Hit"),self.draughts.turn,row1,row2))
                    self.draughts.row_label1 = Gtk.Label(row3)
                    self.draughts.row_label1.show_all()
                    self.draughts.hit_history.prepend(self.draughts.row_label1)
                    self.old_square = None
                    self.matrix = self.draughts.backend.get_matrix()
                    self.resize_checker(self.draughts.checker.square_size)
                    if len(play) == 0:
                        self.draughts.hit_history.remove(self.draughts.hit_history.get_children()[0])
                        self.draughts.set_informations(_("You won"))
                        self.draughts.backend.fin = True
                        self.draughts.row_endgame = Gtk.Label(" %s+ " % (row3))
                        self.draughts.row_endgame.show_all()
                        self.draughts.hit_history.prepend(self.draughts.row_endgame)
                        return 0
                    if self.draughts.pc_first:
                        self.draughts.turn += 1
                    self.draughts.backend.lastjump[:] = []
                    GLib.timeout_add(5.0, self.play_on_timeout, self.stack)
                    self.draughts.set_informations(_("Computer turn"))

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
