class Units:

    def __init__(self, faction, unit_name):
        self.faction = faction
        self.hp = 9
        self.unit_name = unit_name

    def get_faction(self):
        return self.faction

    def get_hp(self):
        return self.hp

    def get_unit_name(self):
        return self.unit_name

    def damage_by(self, damage):
        self.hp = self.hp - damage

    def repair_by(self, recovery):
        self.hp = self.hp + recovery

    def myself(self):
        return f"{self.faction[0]}{self.unit_name[0]}{self.hp}"


class CheckerBoard:

    def __init__(self):

        dA = Units('defender', 'AI')
        dT1 = Units('defender', 'Techs')
        dT2 = Units('defender', 'Techs')
        dF1 = Units('defender', 'Firewalls')
        dF2 = Units('defender', 'Firewalls')
        dP = Units('defender', 'Programs')

        aP1 = Units('attacker', 'Programs')
        aP2 = Units('attacker', 'Programs')
        aF = Units('attacker', 'Firewalls')
        aV1 = Units('attacker', 'Viruses')
        aV2 = Units('attacker', 'Viruses')
        aA = Units('attacker', 'AI')

        self.board = [
            [dA, dT1, dF1, None, None],
            [dT2, dP, None, None, None],
            [dF2, None, None, None, aP1],
            [None, None, None, aF, aV1],
            [None, None, aP2, aV2, aA]
        ]
        # 00 01 02 03 04
        # 10 11 12 13 14
        # 20 21 22 23 24
        # 30 31 32 33 34
        # 40 41 42 43 44

    '''def show_board1(self):
        row_labels: "ABCDE"
        for inner_list in self.board:
            print(f"{row_labels[i]}: ", end='')
            for obj in inner_list:
                if isinstance(obj, Units):
                    print(obj.myself(), end=' ')
                else:
                    print(' * ', end=' ')
            print()'''

    def show_board(self):
        row_labels = "ABCDE"
        print("    0   1   2   3   4")
        for i, inner_list in enumerate(self.board):
            print(f"{row_labels[i]}: ", end='')
            for obj in inner_list:
                if isinstance(obj, Units):
                    print(obj.myself(), end=' ')
                else:
                    print(' * ', end=' ')
            print()

    def get_position(self, name):
        for i, row in enumerate(self.board):
            for j, element in enumerate(row):
                if isinstance(element, Units):
                    if name == element.myself():
                        return i, j
        return None

    # print((obj1.get_position('aP9')))

    # this function can only be used in move()
    def position_occupied(self, row, col):
        if self.board[row][col] is not None:
            return True
        else:
            return False

    # print(obj1.position_occupied(2, 4))

    def engaged(self, tup):
        directions = [(tup[0], tup[1] + 1), (tup[0], tup[1] - 1), (tup[0] + 1, tup[1]), (tup[0] - 1, tup[1])]
        for x, y in directions:
            if x < 5 and y < 5:
                if isinstance(self.board[x][y], Units):
                    if self.board[x][y].faction != self.board[tup[0]][tup[1]].faction:
                        return True
        return False


# static functions
def convert2tuple(char, col):
    var = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
    # if not in var -> throw exception
    row = var[char]
    return row, col


obj1 = CheckerBoard()

obj1.show_board()

print((obj1.get_position('aP9')))

print(convert2tuple('C', 4))

print(obj1.position_occupied(2, 4))

print(obj1.engaged((2, 4)))
