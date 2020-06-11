import copy
import time
import random
import gettext

#lang_translations = gettext.translation('checkers', localedir='locales', languages=['fr'])
#lang_translations.install()
# define _ shortcut for translations

def minimax(node, depth_ab, alpha, beta, maximizing, depth=5):
    # if depth_ab == depth - 1:
    #     time.sleep(0.01)
    # def minimax(node, depth, maximizing):
    if depth_ab == 0:  # or game OVER
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
            # calc = minimax(child, depth-1, False)
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
            # calc = minimax(child, depth-1, True)
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
        # print(self.Backend.calculate())
        self.value = self.Backend.calculate()
        # sprint(self.value)

    def add_child(self, obj):
        self.children.append(obj)

    def get_value(self):
        return self.value

    def __str__(self, level=0):
        return str(self.Backend) + " | " + str(self.value)

    # def __cmp__(self, other):
    #     input("OPAA")
    #     return cmp(self.value, other.value)

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
    def __init__(self, new_matrix=None, last_jmp=None, game_param=None):
        self.p_max=10
        self.status = ("NEW GAME")
        self.depth = 5
        self.variable_depth = True
        self.force_jump = False
        self.pc_first = False
        self.v1 = "○"
        self.v2 = "⬤"
        self.v3 = "░"
        self.v4 = "□"
        self.v5 = "⬛"
        self.v6 = "－"

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

        if game_param:
            self.force_jump = game_param[0]
            self.pc_first = game_param[1]
            self.variable_depth = game_param[2]
            if self.variable_depth != 5:
                self.variable_depth = False
            if game_param[3]:
                self.matrix = copy.deepcopy(game_param[3])

        self.minimax_heuristic = None

    def get_matrix(self):
        return self.matrix

    def calculate(self):
        value = 0
        for enum_i, i in enumerate(self.matrix):
            for enum_j, j in enumerate(i):
                if j == 0:
                    continue
                if j == 1: value -= 5 + 7 - enum_i + abs(enum_j - 4) + abs(enum_i - 4)
                if j == 2: value += 5 + enum_i + abs(enum_j - 4) + abs(enum_i - 4)
                if j == 4: value -= 14 + abs(enum_j - 4) + abs(enum_i - 4)
                if j == 5: value += 14 + abs(enum_j - 4) + abs(enum_i - 4)

        return value

    def count_figures(self):
        value = 0
        for enum_i, i in enumerate(self.matrix):
            for enum_j, j in enumerate(i):
                if j == 1: value -= 1
                if j == 2: value += 1
                if j == 4: value -= 2
                if j == 5: value += 2

        return value

    def possible_moves(self, param):  # param = 1 - PLAYER, param = 2 - PC
        moves = []
        force_moves = []
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == 0 or self.matrix[i][j] % 3 != param:
                    continue
                #print(i,j)
                vertical = 1 if param == 2 else -1  # ako je param = 1, to su PC figure koje idu dole
                enemy = 1 if param == 2 else 2
                cell = self.matrix[i][j]
                if j - 1 != -1 and i + vertical != -1 and i + vertical != self.p_max and \
                        self.matrix[i + vertical][j - 1] % 3 != param:
                    if j - 2 > -1 and self.p_max > i + vertical * 2 > -1 and self.matrix[i + vertical][j - 1] % 3 == enemy and \
                            self.matrix[i + vertical * 2][j - 2] % 3 == 0:
                        #print("EAT " + str(i) + ", " + str(j) + " => " + str(i + vertical*2) + ", " + str(j - 2))
                        moves.append([[i, j], [i + vertical * 2, j - 2]])
                        force_moves.append([[i, j], [i + vertical * 2, j - 2]])
                    elif self.matrix[i + vertical][j - 1] % 3 == 0:
                        #print(str(i) + ", " + str(j) + " => " + str(i+vertical) + ", " + str(j-1))
                        moves.append([[i, j], [i + vertical, j - 1]])
                if j + 1 != self.p_max and i + vertical != -1 and i + vertical != self.p_max and \
                        self.matrix[i + vertical][j + 1] % 3 != param:
                    if j + 2 < self.p_max and self.p_max > i + vertical * 2 > -1 and self.matrix[i + vertical][j + 1] % 3 == enemy and \
                            self.matrix[i + vertical * 2][j + 2] % 3 == 0:
                        #print("EAT " + str(i) + ", " + str(j) + " => " + str(i + vertical*2) + ", " + str(j + 2))
                        moves.append([[i, j], [i + vertical * 2, j + 2]])
                        force_moves.append([[i, j], [i + vertical * 2, j + 2]])
                    elif self.matrix[i + vertical][j + 1] % 3 == 0:
                        #print(str(i) + ", " + str(j) + " => " + str(i + vertical) + ", " + str(j + 1) + "*")
                        moves.append([[i, j], [i + vertical, j + 1]])
                if cell > 3:
                    if j - 1 != -1 and i - vertical != -1 and i - vertical != self.p_max and \
                            self.matrix[i - vertical][j - 1] % 3 != param:
                        if j - 2 > -1 and self.p_max > i - vertical * 2 > -1 and \
                                self.matrix[i - vertical][j - 1] % 3 == enemy and \
                                self.matrix[i - vertical * 2][j - 2] % 3 == 0:
                            #print("EAT " + str(i) + ", " + str(j) + " => " + str(i + vertical*2) + ", " + str(j - 2))
                            moves.append([[i, j], [i - vertical * 2, j - 2]])
                            force_moves.append([[i, j], [i - vertical * 2, j - 2]])
                        elif self.matrix[i - vertical][j - 1] % 3 == 0:
                            #print(str(i) + ", " + str(j) + " => " + str(i-vertical) + ", " + str(j-1))
                            moves.append([[i, j], [i - vertical, j - 1]])
                    if j + 1 != self.p_max and i - vertical != -1 and i - vertical != self.p_max and \
                            self.matrix[i - vertical][j + 1] % 3 != param:
                        if j + 2 < self.p_max and self.p_max > i - vertical * 2 > -1 and \
                                self.matrix[i - vertical][j + 1] % 3 == enemy and \
                                self.matrix[i - vertical * 2][j + 2] % 3 == 0:
                            #print("EAT " + str(i) + ", " + str(j) + " => " + str(i + vertical*2) + ", " + str(j + 2))
                            moves.append([[i, j], [i - vertical * 2, j + 2]])
                            force_moves.append([[i, j], [i - vertical * 2, j + 2]])
                        elif self.matrix[i - vertical][j + 1] % 3 == 0:
                            #print(str(i) + ", " + str(j) + " => " + str(i + vertical) + ", " + str(j + 1) + "*")
                            moves.append([[i, j], [i - vertical, j + 1]])
        if self.force_jump and force_moves:
            return force_moves
        else:
            return moves


    def pl_before_firstclick(self, explicit=None):
        self.all_moves = self.possible_moves(1)
        self.cells = []
        self.ready_moves = []
        if not explicit:
            for self.cell in self.all_moves:
                if self.cell[0] not in self.cells:
                    self.cells.append(self.cell[0])
            print_moves(self.cells)

    def pl_after_firstclick(self, case=None, explicit=None):
        if not explicit:
            cell_num = -1
            #print('pl_after_firstclick(1)')
            #print("cells1 : ", self.cells)
            #print("case1 : ", case)
            self.pl_before_firstclick()
            for i, move in enumerate(self.cells):
                #print('Boucle after  [%d, %d] => [%d, %d] ' % (case[0], case[1], move[0], move[1]))
                if case[0] == move[0] and case[1] == move[1]:
                    cell_num = int(i)
            #print('pl_after_firstclick(2)')
            if cell_num == -1:
                return 0
            #print('pl_after_firstclick(2)')
            position = self.cells[cell_num]
            #print(position, "position")
            #print("all_moves :", self.all_moves)
            for moves in self.all_moves:
                if moves[0] == [self.cells[cell_num][0], self.cells[cell_num][1]]:
                    self.ready_moves.append(moves[1])
        else:
            #print("cells3 : ", self.cells)
            for pmoves in explicit:
                self.ready_moves.append(pmoves[1])
            position = explicit[0][0]
            #print('POSITION[', position[0], '][', position[1], ']')
        return 1

    def pl_after_secondclick(self, old_case=None, case=None):
        coordonate = -1
        #print('pl_after_secondclick(1)')
        for i, move in enumerate(self.ready_moves):
            #print('Boucle before [%d, %d] => [%d, %d] ' % (old_case[0], old_case[1], move[0], move[1]))
            if case[0] == move[0] and case[1] == move[1]:
                coordonate = int(i)
        #print('pl_after_secondclick(2)')
        if coordonate == -1:
            return 0
        #print('pl_after_secondclick(3)')
        #print(' [%d, %d] => [%d, %d] ' % (old_case[0], old_case[1], case[0], case[1]))
        #position = self.ready_moves[coordonate]
        if self.move(old_case, case) == 2:
            next_hop = self.eatable(1, case[0], case[1])
            self.print()
            # self.pl_move(1, next_hop)
        return 1


    def eatable(self, param, i, j):
        moves = [[[i, j], [i, j]]]
        vertical = 1 if param == 2 else -1
        enemy = 1 if param == 2 else 2
        cell = self.matrix[i][j]
        # print(self.matrix)

        if j - 1 != -1 and i + vertical != -1 and i + vertical != self.p_max and self.matrix[i + vertical][j - 1] % 3 == enemy:
            if j - 2 > -1 and self.p_max > i + vertical * 2 > -1 and self.matrix[i + vertical * 2][j - 2] % 3 == 0:
                # print("EAT " + str(i) + ", " + str(j) + " => " + str(i + vertical * 2) + ", " + str(j - 2))
                moves.append([[i, j], [i + vertical * 2, j - 2]])
                # moves.extend(self.eatable(param, i+2, j-2))
        if j + 1 != self.p_max and i + vertical != -1 and i + vertical != self.p_max and self.matrix[i + vertical][j + 1] % 3 == enemy:
            if j + 2 < self.p_max and self.p_max > i + vertical * 2 > -1 and self.matrix[i + vertical * 2][j + 2] % 3 == 0:
                # print("EAT " + str(i) + ", " + str(j) + " => " + str(i + vertical * 2) + ", " + str(j + 2))
                moves.append([[i, j], [i + vertical * 2, j + 2]])
                # moves.extend(self.eatable(param, i + 2, j + 2))

        if cell > 3:
            if j - 1 != -1 and i - vertical != -1 and i - vertical != self.p_max and \
                    self.matrix[i - vertical][j - 1] % 3 == enemy:
                if j - 2 > -1 and self.p_max > i - vertical * 2 > -1 and self.matrix[i - vertical * 2][j - 2] % 3 == 0:
                    # print("EAT " + str(i) + ", " + str(j) + " => " + str(i + vertical * 2) + ", " + str(j - 2))
                    moves.append([[i, j], [i - vertical * 2, j - 2]])
                    # moves.extend(self.eatable(param, i+2, j-2))
            if j + 1 != self.p_max and i - vertical != -1 and i - vertical != self.p_max and \
                    self.matrix[i - vertical][j + 1] % 3 == enemy:

                if j + 2 < self.p_max and self.p_max > i - vertical * 2 > -1 and self.matrix[i - vertical * 2][j + 2] % 3 == 0:
                    # print("EAT " + str(i) + ", " + str(j) + " => " + str(i + vertical * 2) + ", " + str(j + 2))
                    moves.append([[i, j], [i - vertical * 2, j + 2]])
                    # moves.extend(self.eatable(param, i + 2, j + 2))
        return moves

    def move(self, old, new, param=1, first_layer_depth=True):
        cell = self.matrix[old[0]][old[1]]
        self.matrix[old[0]][old[1]] = 3
        if (new[0] == (self.p_max - 1) or new[0] == 0) and cell < 3:
            self.matrix[new[0]][new[1]] = cell + 3
        else:
            self.matrix[new[0]][new[1]] = cell
        if abs(old[0] - new[0]) == 2:
            # self.lastjump += str(chr(old[0] + 65)) + str(old[1] + 1) + " --> " + str(chr(new[0] + 65)) + str(
            #     new[1] + 1) + " (" + str(chr(int((old[0] + new[0]) / 2) + 65)) + str(
            #     int((old[1] + new[1]) / 2) + 1) + ")" + "\n"

            # A2 -> C4 (B3) is [01, 23, 12]
            # A == 0; B == 1...
            if first_layer_depth:
                self.lastjump.append(old[0] * 1000 + old[1] * 100 + new[0] * 10 + new[1])

            self.matrix[int((old[0] + new[0]) / 2)][int((old[1] + new[1]) / 2)] = 6
            eatable_cells = self.eatable(param, new[0], new[1])
            if len(eatable_cells) > 1:
                if param == 1:
                    # print("Ima jos da se jede PLAYER")
                    return 2
                else:
                    # print("Ima jos da se jede PC")
                    return 3
            return 4  # Pojeo
        # self.lastjump += str(chr(old[0] + 65)) + str(old[1] + 1) + " --> " + str(chr(new[0] + 65)) + str(
        #     new[1] + 1) + "\n"
        if first_layer_depth:
            self.lastjump.append(old[0] * 1000 + old[1] * 100 + new[0] * 10 + new[1])

        return 1  # Samo MOVE

    def pc_move(self, stack):
        root = Node(0, self)
        time1 = time.time()
        self.minimax_heuristic = minimax(root, self.depth, Node(-1000), Node(1000), True, self.depth)
        think = time.time() - time1
        print(("Time (sec):"), think)
        stack.push(think)

        if not root.children:
            return 0

        self.matrix = copy.deepcopy(max(root.children).Backend.matrix)
        self.lastjump = copy.deepcopy(max(root.children).Backend.lastjump)
        return 1

    def clear_table_trails(self):
        for enum_i, i in enumerate(self.matrix):
            for enum_j, j in enumerate(i):
                if self.matrix[enum_i][enum_j] == 3 or self.matrix[enum_i][enum_j] == 6:
                    self.matrix[enum_i][enum_j] = 0

    def print(self, highlighted=0, moves=[], clear_trails=False):
        print(("HV Value:"), self.calculate())
        print(("Turn:"), self.turn)

        cells = []
        order = 0
        if highlighted == 1:
            all_moves = self.possible_moves(1)
            for cell in all_moves:
                if cell[0] not in cells:
                    cells.append(cell[0])
            if not cells:
                return None

        if self.p_max == 8 :
            print("     1      2      3      4      5      6       7       8")
        elif self.p_max == 10 :
            print("     1      2      3      4      5      6       7       8      9     10")

        print("  |" + "－－－|" * self.p_max)
        for enum_i, i in enumerate(self.matrix):
            print(str(chr(enum_i + 65)), end=" |")
            for enum_j, j in enumerate(i):
                if j == 0: j = " "
                if j == 1: j = self.v1
                if j == 2: j = self.v2
                if j == 3: j = self.v3
                if j == 4: j = self.v4
                if j == 5: j = self.v5
                if j == 6: j = self.v6

                num = " "
                try:
                    if highlighted == 1 and cells[0][0] == enum_i and cells[0][1] == enum_j:
                        order += 1
                        num = order
                        cells.pop(0)

                    if highlighted == 2:
                        # print(moves)
                        num = moves.index([enum_i, enum_j]) + 1
                        if num == 0:
                            num = " "
                except ValueError:
                    pass
                except IndexError:
                    pass

                #print(" " + str(num) + str(j), end="   |")
                # print("  " + num + str(j), end="    ❙")
                if clear_trails and (self.matrix[enum_i][enum_j] == 3 or self.matrix[enum_i][enum_j] == 6):
                    self.matrix[enum_i][enum_j] = 0
            print("\n  |" + "－－－|" * self.p_max)
        # if highlighted != 5:
        # print(self.lastjump)
        # last_jump_to_str(self.lastjump)

    def play_game(self):
        self.turn = 0
        stack = Stack([4, 3, 3])

        # Si pc commence le jeu
        if self.pc_first:
            # Choix possible de pion qui peuvent être déplacer
            pc_moves = self.possible_moves(2)
            # Choix aleatoir du pion déplacée
            rand_move = random.choice(pc_moves)
            # Démplacement de la pièces>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<>><<<<<<<<<
            self.move(rand_move[0], rand_move[1], 2)
        while True:
            if self.variable_depth and (stack.three_sum() > 11 or stack.peek() > 4.5):
                self.depth -= 1
                stack.set([4, 4, 4])
                print(("Depth reduced to"), self.depth)
            elif self.variable_depth and (stack.three_sum() < 2):
                self.depth += 1
                stack.set([4, 4, 4])
                print(("Increasing the depth"), self.depth)
            self.turn += 1
            self.print(1)
            self.lastjump[:] = []
            # Si la partie à plus de 80 coup (la partie est finie).
            if self.turn > 80:
                # Compte le nombre de piece de differrence entre le
                # pc et le joueur
                # resultat positif le pc à l'avantage
                # resultat negatif le joueur à l'avantage
                # resultat à zero égalité 
                count = self.count_figures()
                if count > 0:
                    self.status = ("The computer has an advantage")
                    self.finish_message(4)
                    return 0
                elif count < 0:
                    self.status = ("The player has an advantage")
                    self.finish_message(3)
                    return 1
                else:
                    self.status = ("Draw")
                    self.finish_message(0)
                    return 3

            # Le joueur jour
            play = self.pl_move()
            # print("checkers.py Player zavrsio")
            # Jeu terminé ?
            if not play:
                self.status = ("The computer won")
                self.finish_message(2)
                return 0
            self.print(clear_trails=True)
            self.turn += 1
            self.print(clear_trails=False)
            print("==PC==")
            self.lastjump[:] = []
            # Le PC joue
            play = self.pc_move(stack)
            time.sleep(0.1)
            # Jeu terminé ?
            if not play:
                self.status = ("You've won!")
                self.finish_message(1)
                return 1

    def pl_move(self, param=1, explicit=None):
        #if self.player_signal:  # If GUI exist call another function that does not require input from keyBackend
        #    return self.pl_gui_move(explicit)

        # self.pc_move(None, 1)
        all_moves = self.possible_moves(param)
        cells = []
        ready_moves = []
        if not explicit:
            for cell in all_moves:
                if cell[0] not in cells:
                    cells.append(cell[0])
            if not cells:
                return None

            # print(cells)
            print_moves(cells)
            while True:
                cell_num = input(("Enter the square number:"))

                # print("--- Poziv pauze ---")
                # self.player_signal.wait_for_move()

                if cell_num.isnumeric():
                    cell_num = int(cell_num) - 1
                    if 0 <= cell_num < len(cells):
                        break
            position = cells[cell_num]
            for moves in all_moves:
                if moves[0] == [cells[cell_num][0], cells[cell_num][1]]:
                    ready_moves.append(moves[1])
        else:
            for pmoves in explicit:
                ready_moves.append(pmoves[1])
            position = explicit[0][0]
        # print(ready_moves)
        self.print(2, copy.deepcopy(ready_moves))
        print_moves(ready_moves)

        while True:
            coordonate = input(("Enter the shot sequence number"))
            if coordonate.isnumeric():
                coordonate = int(coordonate) - 1
                if 0 <= int(coordonate) < len(ready_moves):
                    break
        if self.move(position, ready_moves[int(coordonate)]) == 2:
            next_hop = self.eatable(1, ready_moves[int(coordonate)][0], ready_moves[int(coordonate)][1])
            self.print()
            self.pl_move(1, next_hop)
        return 1

    def finish_message(self, s):
        print('finish_message:', s)


def generate(node, param, depth_ab, depth):
    table = node.Backend
    for move in table.possible_moves(param):
        next_hop_add(node, table, move, param, depth_ab, depth)


def next_hop_add(node, table, move, param, depth_ab, depth):
    first_layer_depth = True if depth_ab == depth else False
    # first_layer_depth = True

    temp_new_table = Backend(copy.deepcopy(table.matrix))
    if first_layer_depth:
        temp_new_table.lastjump = copy.deepcopy(table.lastjump)
    if temp_new_table.move(move[0], move[1], param, first_layer_depth=first_layer_depth) > 1:
        next_hop = temp_new_table.eatable(param, move[1][0], move[1][1])
        if len(next_hop) > 1:
            for n_move in next_hop[1:]:
                next_hop_add(node, temp_new_table, n_move, param, depth_ab, depth)

    # new_table = Backend([1,23])
    new_table = Backend(copy.deepcopy(table.matrix))
    if first_layer_depth:
        new_table.lastjump = copy.deepcopy(table.lastjump)
    new_table.move(move[0], move[1], param, first_layer_depth=first_layer_depth)
    node.add_child(Node(None, new_table))
    return


def accurate_calculate(matrix):
    value = 0
    for enum_i, i in enumerate(matrix):
        for enum_j, j in enumerate(i):
            horizontal = abs(enum_j - 3) if enum_j < 4 else abs(enum_j - 4)
            vertical = abs(enum_i - 3) if enum_i < 4 else abs(enum_i - 4)
            if j == 1: value -= 5 + 7 - enum_i + horizontal + vertical
            if j == 2: value += 5 + enum_i + horizontal + vertical
            if j == 4: value -= 14 + horizontal + vertical
            if j == 5: value += 14 + horizontal + vertical

    return value


def print_moves(moves):
    #for i, move in enumerate(moves):
        # print(chr(move[0]+65))
        #print(str(i + 1) + ") " + str(chr(move[0] + 65)) + str(move[1] + 1), end="   |  ")
    #print()

    #for i, move in enumerate(moves):
        #print(str(i + 1) + ") " + str(move[0]) + str(move[1]), end="   |  ")
    print()

def player_move():
    pass


def f_jump(Backend):
    opt1 = "X"
    opt2 = "X"
    while True:
        print("\n" * 15)
        print("\n", Backend.status, "\n")
        print("1)", "[" + opt1 + "]", _("Compulsory take"))
        print("2)", "[" + opt2 + "]", _("The computer plays first"))
        print("9)", _("Quit"))
        print(_("\tENTER to confirm\n"))
        user_input = input(_("Select an option: "))
        if user_input == "":
            break
        if user_input.isnumeric():
            if int(user_input) == 1:
                opt1 = "O" if opt1 == "X" else "X"
                print(opt1)
            if int(user_input) == 2:
                opt2 = "O" if opt2 == "X" else "X"
            if int(user_input) == 9:
                exit()

    Backend.force_jump = True if opt1 == "O" else False
    Backend.pc_first = True if opt2 == "O" else False


def config_print(Backend):
    str1=("%s○): " % _("First player's piece (default = "))
    Backend.v1 = input(str1)
    str2=("%s⬤): " % _("First player's queen (default = "))
    Backend.v4 = input(str2)
    str3=("%s⬛): " % _("Second player's piece (default = "))
    Backend.v2 = input(str3)
    str4=("%s□): " % _("Queen of the second player (default = "))
    Backend.v5 = input(str4)
    str5=("%s)░: " % _("Previous position square (defaul = "))
    Backend.v3 = input(str5)
    str6=("%s－): " % _("Case of the eaten piece (default = "))
    Backend.v6 = input(str6)

    Backend.v1 = "○" if Backend.v1 == "" else Backend.v1
    Backend.v2 = "⬤" if Backend.v2 == "" else Backend.v2
    Backend.v3 = "░" if Backend.v3 == "" else Backend.v3
    Backend.v4 = "□" if Backend.v4 == "" else Backend.v4
    Backend.v5 = "⬛" if Backend.v5 == "" else Backend.v5
    Backend.v6 = "－" if Backend.v6 == "" else Backend.v6


def last_jump_to_str(last_jump):
    for lj in last_jump:
        b2 = lj % 10
        lj = int(lj / 10)
        b1 = lj % 10
        lj = int(lj / 10)
        a2 = lj % 10
        lj = int(lj / 10)
        a1 = lj % 10

        print(a1, a2, b1, b2)


def last_jump_to_list(last_jump):
    jumps = []
    for lj in last_jump:
        b2 = lj % 10
        lj = int(lj / 10)
        b1 = lj % 10
        lj = int(lj / 10)
        a2 = lj % 10
        lj = int(lj / 10)
        a1 = lj % 10

        jumps.append([[a1, a2], [b1, b2]])
    return jumps


if __name__ == '__main__':

    while True:
        # config_print()
        # f_jump()
        # Creation de la matrice
        matrix = [[0, 2, 0, 2, 0, 2, 0, 2],
                  [2, 0, 2, 0, 2, 0, 2, 0],
                  [0, 2, 0, 2, 0, 2, 0, 2],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [1, 0, 1, 0, 1, 0, 1, 0],
                  [0, 1, 0, 1, 0, 1, 0, 1],
                  [1, 0, 1, 0, 1, 0, 1, 0]]
        # Creation du Damier 
        tabla1 = Backend(matrix)
        # Lancement du jeu
        tabla1.play_game()
