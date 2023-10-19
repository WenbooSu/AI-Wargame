import sys
from enum import Enum

class Player(Enum):
    """The 2 players."""
    attacker = 0
    defender = 1

    def next(self):
        """The next (other) player."""
        if self is Player.attacker:
            return Player.defender
        else:
            return Player.attacker

class Units:

    def __init__(self, faction, unit_name, id: int):
        self.faction = faction
        self.hp = 9
        self.unit_name = unit_name
        self.id = id

    def get_faction(self):
        return self.faction

    def get_hp(self):
        return self.hp

    def get_unit_name(self):
        return self.unit_name
    
    def get_id(self):
        return self.id

    def hp_decrease_by(self, damage):
        self.hp = self.hp - damage

    def hp_increase_by(self, recovery):
        self.hp = self.hp + recovery

    def set_hp(self, hp):
        self.hp = hp

    def myself(self):
        return f"{self.faction[0]}{self.unit_name[0]}{self.hp}"
    
class Game:


    def __init__(self):
        self.player = Player.attacker
        dA = Units('defender', 'AI', 1)
        dT1 = Units('defender', 'Tech', 2)
        dT2 = Units('defender', 'Tech', 3)
        dF1 = Units('defender', 'Firewall', 4)
        dF2 = Units('defender', 'Firewall', 5)
        dP = Units('defender', 'Program', 6)

        aP1 = Units('attacker', 'Program', 7)
        aP2 = Units('attacker', 'Program', 8)
        aF = Units('attacker', 'Firewall', 9)
        aV1 = Units('attacker', 'Virus', 10)
        aV2 = Units('attacker', 'Virus', 11)
        aA = Units('attacker', 'AI', 12)

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

    def get_board(self):
        return self.board

    def show_board(self):
        row_labels = "ABCDE"
        message = ''
        print("    0   1   2   3   4")
        message += "    0   1   2   3   4\n"
        for i, inner_list in enumerate(self.board):
            print(f"{row_labels[i]}: ", end='')
            message += f"{row_labels[i]}: "
            for obj in inner_list:
                if isinstance(obj, Units):
                    print(obj.myself(), end=' ')
                    message += f"{obj.myself()} "
                else:
                    print(' * ', end=' ')
                    message += ' *  '
            print()
            message += '\n'
        # trace_records(message)

    def get_position(self, unit : Units):
        for i, row in enumerate(self.board):
            for j, element in enumerate(row):
                if isinstance(element, Units):
                    if unit.get_id() == element.get_id():
                        return i, j
        return None

    def get_unit(self, tup):
        unit = self.board[tup(0)][tup[1]]
        if isinstance(unit, Units):
            return unit
        else:
            return None
    
    def select_unit():
        user_input = input("Choose Your Unit: ")
        while len(user_input) != 2 or user_input[0].upper() not in ['A', 'B', 'C', 'D', 'E'] \
                or not user_input[1].isnumeric() or int(user_input[1]) < 0 or int(user_input[1]) > 5:
            print("Invalid Input. Please Enter a Proper Position: ")
            user_input = input("Choose Your Unit: ")
        def convert2board_index(char, col):
            tup_dict = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
            # if not in var -> throw exception
            row = tup_dict[char]
            return (row, col)
        return convert2board_index(user_input[0].upper(), int(user_input[1]))

    # this function can only be used in move()
    def position_occupied(self, tup):
        if self.board[tup[0]][tup[1]] is not None:
            return True
        else:
            return False
    
    def engaged(self, tup):
        unit = self.get_unit(tup)
        directions = [(tup[0], tup[1] + 1), (tup[0], tup[1] - 1), (tup[0] + 1, tup[1]), (tup[0] - 1, tup[1])]
        for x, y in directions:
            if 0 <= x < 5 and 0 <= y < 5:
                adjacent = self.board[x][y]
                if isinstance(adjacent, Units) and isinstance(unit, Units):
                    if adjacent.get_faction() != unit.get_faction():
                        return True
        return False
    
    def get_pieces(self):
        ai_pieces = []
        faction = self.player.name
        for i, row in enumerate(self.board):
            for j, unit in enumerate(row):
                if isinstance(unit, Units) and unit.get_faction() == faction:
                    ai_pieces.append((i, j))
        return ai_pieces

    def get_valid_adjacents(self, tup):
        valid_adjacents = []
        directions = [(tup[0], tup[1] + 1), (tup[0], tup[1] - 1), (tup[0] + 1, tup[1]), (tup[0] - 1, tup[1])]
        for x, y in directions:
            if 0 <= x < 5 and 0 <= y < 5:
                valid_adjacents.append((x,y))
        return valid_adjacents
    
    # def move(self, unit : Units):
    def valid_move(self, tup):
        valid_move_list = []
        unit = self.get_unit(tup)
        adjacents = self.get_valid_adjacents(tup)
        if self.engaged(tup) and unit.get_unit_name() not in ['Tech', 'Virus']:
            return None
        else:
            for adjacent in adjacents:
                if self.get_unit(adjacent) == None:
                    valid_move_list.append(adjacent)
        return valid_move_list
    
    def valid_attack(self, tup):
        valid_attack_list = []
        unit = self.get_unit(tup)
        adjacents = self.get_valid_adjacents(tup)
        for adjacent in adjacents:
            if self.get_unit(adjacent).get_faction() != unit.get_faction():
                valid_attack_list.append(adjacent)
        return valid_attack_list
    
    def valid_repair(self, tup):
        valid_repair_list = []
        unit = self.get_unit(tup)
        if unit.get_unit_name() not in ['Tech', 'AI']:
            return None
        else:
            adjacents = self.get_valid_adjacents(tup)
            for adjacent in adjacents:
                if self.get_unit(adjacent).get_faction() == unit.get_faction() and self.get_unit(adjacent).get_hp() < 9:
                    valid_repair_list.append(adjacent)
        return valid_repair_list
    
    # switch_position only switches a Unit node and a None node
    def move(self, a, b):
        self.board[a[0]][a[1]], self.board[b[0]][b[1]] = self.board[b[0]][b[1]], self.board[a[0]][a[1]]

    def attack(self, s, t): # must pass value from: valid_attack() // s is current node
        damage_table = {
            'AI': {
                'AI': 3,
                'Virus': 3,
                'Tech': 3,
                'Firewall': 1,
                'Program': 3
            },
            'Virus': {
                'AI': 9,
                'Virus': 1,
                'Tech': 6,
                'Firewall': 1,
                'Program': 6
            },
            'Tech': {
                'AI': 1,
                'Virus': 6,
                'Tech': 1,
                'Firewall': 1,
                'Program': 1
            },
            'Firewall': {
                'AI': 1,
                'Virus': 1,
                'Tech': 1,
                'Firewall': 1,
                'Program': 1
            },
            'Program': {
                'AI': 3,
                'Virus': 3,
                'Tech': 3,
                'Firewall': 1,
                'Program': 3
            }
        }
        attacker = self.get_unit(s)
        target = self.get_unit(t)
        damage_t = damage_table[attacker.get_unit_name()][target.get_unit_name()]
        damage_s = damage_table[target.get_unit_name()][attacker.get_unit_name()]
        target.hp_decrease_by(damage_t)
        attacker.hp_decrease_by(damage_s)
    
    def repair(self, s, t): # must pass value from: valid_repair() // s is current node
        repair_table = {
            'AI': {
                'Virus': 1,
                'Tech': 1
            },
            'Tech': {
                'AI': 3,
                'Firewall': 3,
                'Program': 3
            }
        }
        doctor = self.get_unit(s)
        patient = self.get_unit(t)
        recovery = repair_table[doctor.get_unit_name()][patient.get_unit_name()]
        if (patient.get_hp() + recovery) >= 9:
            patient.set_hp(9)
        else:
            patient.hp_increase_by(recovery)
    
    def destruct(self, tup):
        x, y = tup
        surroundings = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1), (x, y + 1), (x + 1, y - 1), (x, y - 1),
                        (x + 1, y + 1)]
        unit = self.get_unit(tup)
        unit = None
        for row, col in surroundings:
            if (0 <= row < 5) and (0 <= col < 5):
                node = self.get_unit((row, col))
                if isinstance(node, Units):
                    node.hp_decrease_by(2)

    def clear(self): # must call before check_winner()
            for row in self.board:
                for unit in row:
                    if isinstance(unit, Units) and unit.get_hp() <= 0:
                        unit = None
    
    def check_winner(self):
        alive = []
        for row in self.board:
            for unit in row:
                if isinstance(unit, Units) and unit.get_unit_name == 'AI':
                    alive.append(unit)
        if alive == None:
            return 'Tie'
        if len(alive) == 1 and isinstance(alive[0], Units) and alive[0].get_faction == 'defender':
            return 'defender'
        if len(alive) == 1 and isinstance(alive[0], Units) and alive[0].get_faction == 'attacker':
            return 'attacker'
        if len(alive) == 2:
            return None
    
    def heuristic(self):
        def calculate_scores(self, player : str):
            V = T = F = P = AI =0
            for row in self.board:
                for unit in row:
                    if isinstance(unit, Units) and unit.get_faction() == player:
                        if unit.get_unit_name() == 'Virus':
                            V += 1
                        elif unit.get_unit_name() == 'Tech':
                            T += 1
                        elif unit.get_unit_name() == 'Firewall':
                            F += 1
                        elif unit.get_unit_name() == 'Program':
                            P += 1
                        elif unit.get_unit_name() == 'AI':
                            AI += 1
            return V, T, F, P, AI
        VP1, TP1, FP1, PP1, AIP1 = self.calculate_player_scores('attacker')
        VP2, TP2, FP2, PP2, AIP2 = self.calculate_player_scores('defender')
        score = (3 * VP1 + 3 * TP1 + 3 * FP1 + 3 * PP1 + 9999 * AIP1) - (3 * VP2 + 3 * TP2 + 3 * FP2 + 3 * PP2 + 9999 * AIP2)
        return score







    


    