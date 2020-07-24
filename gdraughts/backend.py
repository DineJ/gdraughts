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
along with this checkers game ; see the file LICENSE. If not, write to the Free
Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA."""


import copy
import time
import random
import gettext
from squarearea import SquareArea
#lang_translations = gettext.translation('checkers', localedir='locales', languages=['fr'])
#lang_translations.install()
# define _ shortcut for translations

def minimax(node, depth_ab, alpha, beta, maximizing, depth=5):
    if depth_ab == 0:
        node.calc()
        return node

    if maximizing:
        max_value = -999
        generate(node, 2, depth_ab, depth)
        if not node.children:
            node.value = -900
            return Node(-900)
        for child in node.children:
            calc = minimax(child, depth_ab - 1, alpha, beta, False, depth)
            max_value = max(max_value, calc)
            alpha = max(calc, alpha)
            if beta <= alpha:
                break
        node.value = max_value.value
        return max_value
    else:
        min_value = 999
        generate(node, 1, depth_ab, depth)
        if not node.children:
            node.value = 900
            return Node(900)
        for child in node.children:
            calc = minimax(child, depth_ab - 1, alpha, beta, True, depth)
            min_value = min(min_value, calc)
            beta = min(calc, beta)
            if beta <= alpha:
                break
        node.value = min_value.value
        return min_value


class Node(object):
    def __init__(self, value=None, Backend=None):
        self.Backend = Backend
        self.value = value
        self.children = []

    def calc(self):
        self.value = self.Backend.calculate()

    def add_child(self, obj):
        self.children.append(obj)

    def get_value(self):
        return self.value

    def __str__(self, level=0):
        return str(self.Backend) + " | " + str(self.value)

    def __lt__(self, other):
        if isinstance(other, Node):
            other = other.value
        return self.value < other if True else False

    def __le__(self, other):
        if isinstance(other, Node):
            other = other.value
        return self.value <= other if True else False

    def __gt__(self, other):
        if isinstance(other, Node):
            other = other.value
        return self.value > other if True else False

    def __ge__(self, other):
        if isinstance(other, Node):
            other = other.value
        return self.value >= other if True else False

    def treeview(self, level=0):
        ret = "\t" * level + repr(self.value) + "\n"
        for child in self.children:
            ret += child.treeview(level + 1)
        return ret


class Stack:
    def __init__(self, items=[]):
        if items:
            self.items = items
        else:
            self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)

    def set(self, elements=[]):
        self.items = elements

    def three_sum(self):
        return self.items[-1] + self.items[-2] + self.items[-3]


class Backend(object):
    def __init__(self, new_matrix=None, draughts=None, rear_socket=True, force_jump=False, eat_queen=True, depth=5, pawn_queen=True, promotion_eat=True, last_jmp=None):
        self.p_max=10
        self.status = ("NEW GAME")
        self.depth = depth
        self.variable_depth = True
        self.fin = False
        self.force_jump = force_jump # force the pawns to eat
        self.rear_socket = rear_socket   # allow pawns to eat back
        self.eat_queen = eat_queen   # allow queens to be eaten by pawns
        self.pawn_queen = pawn_queen
        self.draughts = draughts
        self.promotion_eat = promotion_eat
        self.green = False
        if not new_matrix:
            if self.p_max==10 :
                self.matrix = [[0, 2, 0, 2, 0, 2, 0, 2, 0, 2],
                               [2, 0, 2, 0, 2, 0, 2, 0, 2, 0],
                               [0, 2, 0, 2, 0, 2, 0, 2, 0, 2],
                               [2, 0, 2, 0, 2, 0, 2, 0, 2, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                               [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                               [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                               [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]]

            elif self.p_max==8 :
                self.matrix = [[0, 2, 0, 2, 0, 2, 0, 2],
                               [2, 0, 2, 0, 2, 0, 2, 0],
                               [0, 2, 0, 2, 0, 2, 0, 2],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [1, 0, 1, 0, 1, 0, 1, 0],
                               [0, 1, 0, 1, 0, 1, 0, 1],
                               [1, 0, 1, 0, 1, 0, 1, 0]]

        else:
            self.matrix = new_matrix
            self.p_max = len(self.matrix)
        if last_jmp:
            self.lastjump = last_jmp
        else:
            self.lastjump = []
        if self.variable_depth != 5:
            self.variable_depth = False
        self.minimax_heuristic = None

    def get_matrix(self):
        return self.matrix

    def calculate(self):
        value = 0
        for enum_i, i in enumerate(self.matrix):
            for enum_j, j in enumerate(i):
                if j == 0:
                    continue
                matrix_size = len(self.matrix) - 1
                matrix_sizex2 = matrix_size * 2
                if j == 1: value -= 5 + matrix_size - enum_i + abs(enum_j - 4) + abs(enum_i - 4)
                if j == 2: value += 5 + enum_i + abs(enum_j - 4) + abs(enum_i - 4)
                if j == 4: value -= matrix_sizex2 + abs(enum_j - 4) + abs(enum_i - 4)
                if j == 5: value += matrix_sizex2 + abs(enum_j - 4) + abs(enum_i - 4)

        return value

    #defines the movements of the pawn
    def possible_moves_square(self, param, enemy, j, i, jo, io, moves=True):
        cell = self.matrix[i][j]
        if -1 < j + jo < len(self.matrix) and -1 < i + io < len(self.matrix) and \
                self.matrix[i + io][j + jo] % 3 != param:
            if -1 < j + jo * 2 < len(self.matrix) and -1 < i + io * 2 < len(self.matrix) and \
                      self.matrix[i + io][j + jo] % 3 == enemy and \
                      self.matrix[i + io * 2][j + jo * 2] % 3 == 0 and \
                      (self.eat_queen == True or cell > 3 or \
                       self.matrix[i + io][j + jo] < 4):
                #print("EAT " + str(i) + ", " + str(j) + " => " + str(i + vertical*2) + ", " + str(j - 2))
                self.p_moves.append([[i, j], [i + io * 2, j + jo * 2]])
                self.p_force_moves.append([[i, j], [i + io * 2, j + jo * 2]])
                if self.draughts != None and self.force_jump and param == 1:
                    self.green = True
                    self.draughts.set_informations(_("You must eat"))
            elif moves and self.matrix[i + io][j + jo] % 3 == 0:
                #print(str(i) + ", " + str(j) + " => " + str(i-vertical) + ", " + str(j-1))
                self.p_moves.append([[i, j], [i + io, j + jo]]) 

    #defines the movements of the queen
    def possible_moves_queen(self, param, enemy, j, i, jo, io):  # param = 1 - PLAYER, param = 2 - PCoffset = 1
        eat = False
        offset = 1
        offset_max = self.p_max
        while offset < offset_max:
            if -1 < j + (jo * offset) < len(self.matrix) and \
               -1 < i + (io * offset) < len(self.matrix) and \
               self.matrix[i + (io * offset)][j + (jo * offset)] % 3 == param:
                    break
            if -1 < j + jo * offset < len(self.matrix) and \
               -1 < i + io * offset < len(self.matrix) and \
               self.matrix[i + io * offset][j + jo * offset] % 3 != param:
                    if -1 < j + jo * (offset + 1) < len(self.matrix) and \
                       -1 < i + io * (offset + 1) < len(self.matrix) and \
                       self.matrix[i + io * offset][j + jo * offset] % 3 == enemy and \
                       self.matrix[i + io * (offset + 1)][j + jo * (offset + 1)] % 3 == param:
                            break
                    elif -1 < j + jo * (offset + 1) < len(self.matrix) and \
                         -1 < i + io * (offset + 1) < len(self.matrix) and \
                         self.matrix[i + io * offset][j + jo * offset] % 3 == enemy and \
                         self.matrix[i + io * (offset + 1)][j + jo * (offset + 1)] % 3 == enemy:
                            break
                    elif -1 < j + jo * (offset + 1) < len(self.matrix) and \
                         -1 < i + io * (offset + 1) < len(self.matrix) and \
                         self.matrix[i + io * offset][j + jo * offset] % 3 == enemy and \
                         self.matrix[i + io * (offset + 1)][j + jo * (offset + 1)] % 3 == 0:
                            #print("EAT " + str(i) + ", " + str(j) + " => " + str(i + vertical*2) + ", " + str(j - 2))
                            self.p_moves.append([[i, j], [i + io * (offset + 1), j + jo * (offset + 1)]])
                            self.p_force_moves.append([[i, j], [i + io * (offset + 1), j + jo * (offset + 1)]])
                            if self.draughts != None and self.force_jump and param == 1:
                                self.green = True
                                self.draughts.set_informations(_("You must eat"))
                            eat = True
                    elif self.matrix[i + io * offset][j + jo * offset] % 3 == 0:
                        #print(str(i) + ", " + str(j) + " => " + str(i-vertical) + ", " + str(j-1))
                        self.p_moves.append([[i, j], [i + io * offset, j + jo * offset]])
                        if eat == True:
                            self.p_force_moves.append([[i, j], [i + io * offset, j + jo * offset]])
            offset += 1

    #defines the movements
    def possible_moves(self, param):  # param = 1 - PLAYER, param = 2 - PC
        self.p_moves = []
        self.p_force_moves = []
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == 0 or self.matrix[i][j] % 3 != param:
                    continue
                vertical = 1 if param == 2 else -1
                enemy = 1 if param == 2 else 2
                cell = self.matrix[i][j]
                if cell == 1 or cell == 2 or self.pawn_queen:
                    self.possible_moves_square(param, enemy, j, i, -1, vertical)
                    self.possible_moves_square(param, enemy, j, i, 1, vertical)
                    if self.rear_socket or cell == 4 or cell == 5:
                        self.possible_moves_square(param, enemy, j, i, -1, vertical * -1, False)
                        self.possible_moves_square(param, enemy, j, i, 1, vertical * -1, False)
                elif (cell == 4 or cell == 5) and not self.pawn_queen:
                    self.possible_moves_queen(param, enemy, j, i, 1, 1)
                    self.possible_moves_queen(param, enemy, j, i, -1, 1)
                    self.possible_moves_queen(param, enemy, j, i, 1, -1)
                    self.possible_moves_queen(param, enemy, j, i, -1, -1)
        if self.force_jump and self.p_force_moves:
            return self.p_force_moves
        else:
            return self.p_moves

    #define player movement
    def pl_before_firstclick(self, explicit=None):
        self.all_moves = self.possible_moves(1)
        self.cells = []
        self.ready_moves = []
        if not explicit:
            for self.cell in self.all_moves:
                if self.cell[0] not in self.cells:
                    self.cells.append(self.cell[0])
    #define player movement
    def pl_after_firstclick(self, case=None, explicit=None):
        self.pl_before_firstclick()
        if not explicit:
            cell_num = -1
            for i, move in enumerate(self.cells):
                if case[0] == move[0] and case[1] == move[1]:
                    cell_num = int(i)
            if cell_num == -1:
                return 0
            for moves in self.all_moves:
                if moves[0] == [self.cells[cell_num][0], self.cells[cell_num][1]]:
                    self.ready_moves.append(moves[1])
        else:
            self.ready_moves.append(explicit)
        return 1

    #define player movement
    def pl_after_secondclick(self, old_case=None, case=None):
        coordonate = -1
        for i, move in enumerate(self.ready_moves):
            if case[0] == move[0] and case[1] == move[1]:
                coordonate = int(i)
        if coordonate == -1:
            return 0
        ret = self.move(old_case, case)
        if ret == 2:
            next_hop = self.eatable(1, case[0], case[1])
            if next_hop:
                self.pl_after_firstclick(case)
                return 2
        elif ret == 4:
            return 4
        elif ret == 5:
            return 5
        return 1

    # defines the movements to eat of the pawn
    def eatable_square(self, param, enemy, j, i, jo, io):
        if -1 < j + jo < len(self.matrix) and -1 < i + io < len(self.matrix) and \
                self.matrix[i + io][j + jo] % 3 != param:
            if -1 < j + jo * 2 < len(self.matrix) and -1  < i + io * 2 < len(self.matrix) and \
                      self.matrix[i + io][j + jo] % 3 == enemy and \
                      self.matrix[i + io * 2][j + jo * 2] % 3 == 0 and \
                      (self.eat_queen == True or \
                       self.matrix[i + io][j + jo] < 4):
                self.eat_moves.append([[i, j], [i + io * 2, j + jo * 2]])

    # defines the movements to eat of the queen
    def eatable_queen(self, param, enemy, j, i, jo, io):
        eat = False
        offset = 1
        while offset < self.p_max - 1  :
            if -1 < j + jo * offset < len(self.matrix) and -1 < i + io * offset < len(self.matrix) and \
                    self.matrix[i + io * offset][j + jo * offset] % 3 != param:
                if -1 < j + (jo * (offset + 1)) < len(self.matrix) -1 < i + (io * (offset + 1)) < len(self.matrix) and \
                        self.matrix[i + (io * offset)][j + (jo * offset)] % 3 != enemy:
                    break
                elif -1 < j + jo * (offset + 1) < len(self.matrix) and -1 < i + io * (offset + 1) < len(self.matrix) and \
                        self.matrix[i + io * offset][j + jo * offset] % 3 == enemy and \
                        self.matrix[i + io * (offset + 1)][j + jo * (offset + 1)] % 3 == enemy:
                    break
                elif -1 < j + jo * (offset + 1) < len(self.matrix) and -1 < i + io * (offset + 1) < len(self.matrix) and \
                          self.matrix[i + io * offset][j + jo * offset] % 3 == enemy and \
                          self.matrix[i + io * (offset + 1)][j + jo * (offset + 1)] % 3 == 0:
                    self.eat_moves.append([[i, j], [i + io * (offset + 1), j + jo * (offset + 1)]])
                    eat = True
                elif self.matrix[i + io * offset][j + jo * offset] % 3 == 0:
                    if eat == True:
                        self.eat_moves.append([[i, j], [i + io * offset, j + jo * offset]])
            offset += 1 

    # defines who is edible
    def eatable(self, param, i, j):
        self.eat_moves = [[[i, j], [i, j]]]
        vertical = 1 if param == 2 else -1
        enemy = 1 if param == 2 else 2
        cell = self.matrix[i][j]

        if cell == 1 or cell == 2 or self.pawn_queen:
            self.eatable_square(param, enemy, j, i, -1, vertical)
            self.eatable_square(param, enemy, j, i, 1, vertical)
            if self.rear_socket or cell == 4 or cell == 5:
                self.eatable_square(param, enemy, j, i, -1, vertical * -1)
                self.eatable_square(param, enemy, j, i, 1, vertical * -1)
        elif (cell == 4 or cell == 5) and not self.pawn_queen:
            self.eatable_queen(param, enemy, j, i, -1, vertical * -1)
            self.eatable_queen(param, enemy, j, i, -1, vertical)
            self.eatable_queen(param, enemy, j, i, 1, vertical * -1)
            self.eatable_queen(param, enemy, j, i, 1, vertical)
        return self.eat_moves

    ## defines the movements
    def move(self, old, new, param=1, first_layer_depth=True):
        promotion = False
        one = 0
        two = 0
        cell = self.matrix[old[0]][old[1]]
        self.matrix[old[0]][old[1]] = 0
        if (new[0] == (self.p_max - 1) or new[0] == 0) and cell < 3 and \
                (param == 1 and old[0] > new[0] or \
                param == 2 and old[0] < new[0]):
            if self.promotion_eat:
                self.matrix[new[0]][new[1]] = cell + 3
            else:
                promotion = True
                self.matrix[new[0]][new[1]] = cell
                one = new[0]
                two = new[1]
        else:
            self.matrix[new[0]][new[1]] = cell
        if abs(old[0] - new[0]) >= 2:
            if first_layer_depth:
                self.lastjump.append(old[0] * 1000 + old[1] * 100 + new[0] * 10 + new[1])
            x = 1
            y = 1
            enemy = 1 if param == 2 else 2
            offset = 1
            eat1 = False
            p_max = self.p_max
            if old[0] > new[0]:
                x = -1
                p_max = old[0] - new[0]
            else:
                p_max = new[0] - old[0]
            if old[1] > new[1]:
                y = -1
            while offset < p_max:
                if old[0] + (x * offset) != new[0] and old[1] + (y * offset) !=  new[1] and \
                        self.matrix[old[0] + (x * offset)][old[1] + (y * offset)] % 3 == enemy:
                     self.matrix[old[0] + (x * offset)][old[1] + (y * offset)] = 0
                     eat1 = True
                offset += 1
            if eat1:
                eatable_cells = self.eatable(param, new[0], new[1])
                if len(eatable_cells) > 1:
                    if param == 1:
                        return 2
                    else:
                        return 3
                elif promotion:
                    self.matrix[one][two] =  cell + 3
                    return 5
                return 4
        elif first_layer_depth:
            self.lastjump.append(old[0] * 1000 + old[1] * 100 + new[0] * 10 + new[1])
        if promotion:
            self.matrix[one][two] =  cell + 3
        return 1

    # defines pc movements
    def pc_move(self, stack):
        if self.fin == False:
            root = Node(0, self)
            time1 = time.time()
            self.minimax_heuristic = minimax(root, self.depth, Node(-1000), Node(1000), True, self.depth)
            think = time.time() - time1
            stack.push(think)

            if not root.children:
                return 0

            self.matrix = copy.deepcopy(max(root.children).Backend.matrix)
            self.lastjump = copy.deepcopy(max(root.children).Backend.lastjump)
            return 1

def generate(node, param, depth_ab, depth):
    table = node.Backend
    for move in table.possible_moves(param):
        next_hop_add(node, table, move, param, depth_ab, depth)


def next_hop_add(node, table, move, param, depth_ab, depth):
    first_layer_depth = True if depth_ab == depth else False
    temp_new_table = Backend(copy.deepcopy(table.matrix), None, table.rear_socket, table.force_jump, table.eat_queen, table.depth, table.pawn_queen, table.promotion_eat)
    if first_layer_depth:
        temp_new_table.lastjump = copy.deepcopy(table.lastjump)
    ret = temp_new_table.move(move[0], move[1], param, first_layer_depth=first_layer_depth)
    if ret > 1 and ret < 5:
        next_hop = temp_new_table.eatable(param, move[1][0], move[1][1])
        if len(next_hop) > 1:
            for n_move in next_hop[1:]:
                next_hop_add(node, temp_new_table, n_move, param, depth_ab, depth)

    new_table = Backend(copy.deepcopy(table.matrix), None, table.rear_socket, table.force_jump, table.eat_queen, table.depth, table.pawn_queen, table.promotion_eat)
    if first_layer_depth:
        new_table.lastjump = copy.deepcopy(table.lastjump)
    new_table.move(move[0], move[1], param, first_layer_depth=first_layer_depth)
    node.add_child(Node(None, new_table))
    return
