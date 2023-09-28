import sys

import keyboard


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

    def hp_decrease_by(self, damage):
        self.hp = self.hp - damage

    def hp_increase_by(self, recovery):
        self.hp = self.hp + recovery

    def set_hp(self, hp):
        self.hp = hp

    def myself(self):
        return f"{self.faction[0]}{self.unit_name[0]}{self.hp}"


class CheckerBoard:

    def __init__(self):

        dA = Units('defender', 'AI')
        dT1 = Units('defender', 'Tech')
        dT2 = Units('defender', 'Tech')
        dF1 = Units('defender', 'Firewall')
        dF2 = Units('defender', 'Firewall')
        dP = Units('defender', 'Program')

        aP1 = Units('attacker', 'Program')
        aP2 = Units('attacker', 'Program')
        aF = Units('attacker', 'Firewall')
        aV1 = Units('attacker', 'Virus')
        aV2 = Units('attacker', 'Virus')
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

    def get_board(self):
        return self.board

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

    # switch_position only switches a Unit node and a None node
    def switch_position(self, current_position, to_destination):
        self.board[current_position[0]][current_position[1]], self.board[to_destination[0]][to_destination[1]] = \
            self.board[to_destination[0]][to_destination[1]], self.board[current_position[0]][current_position[1]]

    # this function can only be used in move()
    def position_occupied(self, tup):
        if self.board[tup[0]][tup[1]] is not None:
            return True
        else:
            return False

    # print(obj1.position_occupied(2, 4))
    # if engaged -> AI, Firewall, Program cannot move
    def engaged(self, tup):
        directions = [(tup[0], tup[1] + 1), (tup[0], tup[1] - 1), (tup[0] + 1, tup[1]), (tup[0] - 1, tup[1])]
        for x, y in directions:
            if 0 <= x < 5 and 0 <= y < 5:
                if isinstance(self.board[x][y], Units):
                    if self.board[x][y].faction != self.board[tup[0]][tup[1]].faction:
                        return True
        return False

    # Assume to enter [A] [1] as the selection of unit
    # def move_to(self, position):


class Engine:

    def __init__(self):
        self.game_map = CheckerBoard()
        self.ai_dead = False

    def get_game_map(self):
        return self.game_map

    def set_ai_dead(self, boolean_value):
        self.ai_dead = boolean_value

    def get_ai_dead(self):
        return self.ai_dead

    # Return the Tuple of a Unit Index on Game Board -> IMPORTANT for entire game
    @staticmethod
    def select_unit():
        user_input = input("Choose Your Unit: ")
        while len(user_input) != 2 or user_input[0].upper() not in ['A', 'B', 'C', 'D', 'E'] \
                or not user_input[1].isnumeric() or int(user_input[1]) < 1 or int(user_input[1]) > 5:
            print("Invalid Input. Please Enter a Proper Position: ")
            user_input = input("Choose Your Unit: ")
        return convert2board_index(user_input[0].upper(), int(user_input[1]))

    def get_unit_node(self, pos_tup):
        return self.get_game_map().get_board()[pos_tup[0]][pos_tup[1]]

    # Parameters are tuple only
    def move(self, my_position):
        command = ''
        while True:
            print("Your Command: ")
            if self.get_unit_node(my_position).get_unit_name() in ['Tech', 'Virus']:
                command = keyboard_command_move()
                if command == 'up':  # [x][y] -> [x-1][y]
                    new_position = (my_position[0] - 1, my_position[1])
                    if self.get_game_map().position_occupied(new_position):
                        print("Invalid Move: a Unit on this Position")
                        continue
                    else:
                        if within_range(new_position):
                            self.get_game_map().switch_position(my_position, new_position)
                            self.get_game_map().show_board()
                            break
                        else:
                            print('Invalid Move: Out of Range')
                if command == 'down':  # [x][y] -> [x+1][y]
                    new_position = (my_position[0] + 1, my_position[1])
                    if self.get_game_map().position_occupied(new_position):
                        print("Invalid Move: a Unit on this Position")
                        continue
                    else:
                        if within_range(new_position):
                            self.get_game_map().switch_position(my_position, new_position)
                            self.get_game_map().show_board()
                            break
                        else:
                            print('Invalid Move: Out of Range')
                if command == 'left':  # [x][y] -> [x][y-1]
                    new_position = (my_position[0], my_position[1] - 1)
                    if self.get_game_map().position_occupied(new_position):
                        print("Invalid Move: a Unit on this Position")
                        continue
                    else:
                        if within_range(new_position):
                            self.get_game_map().switch_position(my_position, new_position)
                            self.get_game_map().show_board()
                            break
                        else:
                            print('Invalid Move: Out of Range')
                if command == 'right':  # [x][y] -> [x][y+1]
                    new_position = (my_position[0], my_position[1] + 1)
                    if self.get_game_map().position_occupied(new_position):
                        print("Invalid Move: a Unit on this Position")
                        continue
                    else:
                        if within_range(new_position):
                            self.get_game_map().switch_position(my_position, new_position)
                            self.get_game_map().show_board()
                            break
                        else:
                            print('Invalid Move: Out of Range')
            if self.get_unit_node(my_position).get_unit_name() in ['AI', 'Firewall', 'Program']:
                command = keyboard_command_move()
                if self.get_game_map().engaged(my_position):
                    print("This Unit is Engaged in Combat")
                    break
                else:
                    if self.get_unit_node(my_position).get_faction() == 'defender':
                        if command not in ['down', 'right']:
                            print('Illegal Move for Defender')
                            continue
                        else:
                            if command == 'down':
                                new_position = (my_position[0] + 1, my_position[1])
                                if self.get_game_map().position_occupied(new_position):
                                    print("Invalid Move: a Unit on this Position")
                                    continue
                                else:
                                    if within_range(new_position):
                                        self.get_game_map().switch_position(my_position, new_position)
                                        self.get_game_map().show_board()
                                        break
                                    else:
                                        print('Invalid Move: Out of Range')
                            if command == 'right':
                                new_position = (my_position[0], my_position[1] + 1)
                                if self.get_game_map().position_occupied(new_position):
                                    print("Invalid Move: a Unit on this Position")
                                    continue
                                else:
                                    if within_range(new_position):
                                        self.get_game_map().switch_position(my_position, new_position)
                                        self.get_game_map().show_board()
                                        break
                                    else:
                                        print('Invalid Move: Out of Range')
                    if self.get_unit_node(my_position).get_faction() == 'attacker':
                        if command not in ['up', 'left']:
                            print('Illegal Move for Attacker')
                            continue
                        else:
                            if command == 'up':
                                new_position = (my_position[0] - 1, my_position[1])
                                if self.get_game_map().position_occupied(new_position):
                                    print("Invalid Move: a Unit on this Position")
                                    continue
                                else:
                                    if within_range(new_position):
                                        self.get_game_map().switch_position(my_position, new_position)
                                        self.get_game_map().show_board()
                                        break
                                    else:
                                        print('Invalid Move: Out of Range')
                            if command == 'left':
                                new_position = (my_position[0], my_position[1] - 1)
                                if self.get_game_map().position_occupied(new_position):
                                    print("Invalid Move: a Unit on this Position")
                                    continue
                                else:
                                    if within_range(new_position):
                                        self.get_game_map().switch_position(my_position, new_position)
                                        self.get_game_map().show_board()
                                        break
                                    else:
                                        print('Invalid Move: Out of Range')

    # Better Structured move() -> to be decent a guy
    def move1(self, my_position):
        def is_valid_move(new_position):
            if not self.get_game_map().position_occupied(new_position):
                if within_range(new_position):
                    self.get_game_map().switch_position(my_position, new_position)
                    return True
                else:
                    print('Invalid Move: Out of Range')
            else:
                print("Invalid Move: a Unit on this Position")
            return False

        command = ''
        unit_name = self.get_unit_node(my_position).get_unit_name()
        faction = self.get_unit_node(my_position).get_faction()
        new_position = None
        while True:
            print("Your Command: ")
            command = keyboard_command_move()

            if unit_name in ['Tech', 'Virus']:
                if command == 'up':  # [x][y] -> [x-1][y]
                    new_position = (my_position[0] - 1, my_position[1])
                elif command == 'down':  # [x][y] -> [x+1][y]
                    new_position = (my_position[0] + 1, my_position[1])
                elif command == 'left':  # [x][y] -> [x][y-1]
                    new_position = (my_position[0], my_position[1] - 1)
                elif command == 'right':  # [x][y] -> [x][y+1]
                    new_position = (my_position[0], my_position[1] + 1)
                else:
                    print("Invalid Move: Unsupported command for this unit type")
                    continue

                if is_valid_move(new_position):
                    self.get_game_map().show_board()
                    break

            elif unit_name in ['AI', 'Firewall', 'Program']:
                if faction == 'defender':
                    valid_commands = ['down', 'right']
                else:
                    valid_commands = ['up', 'left']

                if command not in valid_commands:
                    print(f'Illegal Move for {faction.capitalize()}')
                    continue

                if command == 'up':
                    new_position = (my_position[0] - 1, my_position[1])
                elif command == 'down':
                    new_position = (my_position[0] + 1, my_position[1])
                elif command == 'left':
                    new_position = (my_position[0], my_position[1] - 1)
                elif command == 'right':
                    new_position = (my_position[0], my_position[1] + 1)

                if is_valid_move(new_position):
                    self.get_game_map().show_board()
                    break

    def movable(self, tup):
        if self.get_unit_node(tup).get_unit_name() in ['Tech', 'Virus']:
            directions = [(tup[0] + 1, tup[1]), (tup[0] - 1, tup[1]), (tup[0], tup[1] + 1), (tup[0], tup[1] - 1)]
            for direction in directions:
                if within_range(direction):
                    if self.get_unit_node(direction) is None:
                        return True
        else:
            if self.get_unit_node(tup).get_faction() == 'attacker':
                directions = [(tup[0] - 1, tup[1]), (tup[0], tup[1] - 1)]
                for direction in directions:
                    if within_range(direction):
                        if self.get_unit_node(direction) is None:
                            return True
            if self.get_unit_node(tup).get_faction() == 'defender':
                directions = [(tup[0] + 1, tup[1]), (tup[0], tup[1] + 1)]
                for direction in directions:
                    if within_range(direction):
                        if self.get_unit_node(direction) is None:
                            return True
        return False

    def attack(self, s_tup, t_tup):
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
        if is_adjacent(s_tup, t_tup):
            s = self.get_unit_node(s_tup)
            t = self.get_unit_node(t_tup)
            if isinstance(s, Units) and isinstance(t, Units):
                if s.get_faction() != t.get_faction():
                    # damage S to T
                    damage_value_to_t = damage_table[s.get_unit_name()][t.get_unit_name()]
                    self.get_unit_node(t_tup).hp_decrease_by(damage_value_to_t)
                    # damage T to S
                    damage_value_to_s = damage_table[t.get_unit_name()][s.get_unit_name()]
                    self.get_unit_node(s_tup).hp_decrease_by(damage_value_to_s)
                    if self.get_unit_node(t_tup).get_hp() <= 0 and self.get_unit_node(t_tup).get_unit_name() == 'AI':
                        print(f"{t.get_unit_name()} Has Been Destroyed")
                        self.get_game_map().get_board()[t_tup[0]][t_tup[1]] = None
                        print(f"{t.get_faction()} Lost the Game!")
                        self.set_ai_dead(True)
                        # sys.exit()
                    elif self.get_unit_node(s_tup).get_hp() <= 0 and self.get_unit_node(s_tup).get_unit_name() == 'AI':
                        print(f"{s.get_unit_name()} Has Been Destroyed")
                        self.get_game_map().get_board()[s_tup[0]][s_tup[1]] = None
                        print(f"{s.get_faction()} Lost the Game!")
                        self.set_ai_dead(True)
                        # sys.exit()
                    else:
                        if self.get_unit_node(t_tup).get_hp() <= 0:
                            print(f"{t.myself()} Has Been Destroyed!")
                            self.get_game_map().get_board()[t_tup[0]][t_tup[1]] = None
                        if self.get_unit_node(s_tup).get_hp() <= 0:
                            print(f"{s.myself()} Has Been Destroyed!")
                            self.get_game_map().get_board()[s_tup[0]][s_tup[1]] = None
                return True
        else:
            print("You Don't Have Missile to Reach This Far :)")
        return False

    def repair(self, s_tup, t_tup):
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
        if is_adjacent(s_tup, t_tup):
            s = self.get_unit_node(s_tup)
            t = self.get_unit_node(t_tup)
            if isinstance(s, Units) and isinstance(t, Units):
                if s.get_faction() == t.get_faction():
                    try:
                        repair_value_s_2_t = repair_table[s.get_unit_name()][t.get_unit_name()]
                    except KeyError:
                        print(f"Invalid Action: {s.get_unit_name()} Cannot Repair {t.get_unit_name()}")
                    else:
                        if (self.get_unit_node(t_tup).get_hp() + repair_value_s_2_t) >= 9:
                            self.get_unit_node(t_tup).set_hp(9)
                        else:
                            self.get_unit_node(t_tup).hp_increase_by(repair_value_s_2_t)
                    return True
            else:
                print("You traitor or what?")
        return False

    def self_destruct(self, tup):
        x, y = tup
        surroundings = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1), (x, y + 1), (x + 1, y - 1), (x, y - 1),
                        (x + 1, y + 1)]
        self_destruct_unit = self.get_unit_node(tup)
        print(f"{self_destruct_unit.get_unit_name()} Destructed Itself")
        self.get_game_map().get_board()[tup[0]][tup[1]] = None
        for row, col in surroundings:
            if (0 <= row < 5) and (0 <= col < 5):
                node = self.get_unit_node((row, col))
                if isinstance(node, Units):
                    self.get_game_map().get_board()[row][col].hp_decrease_by(2)
                    if self.get_game_map().get_board()[row][col].get_hp() <= 0:
                        if self.get_game_map().get_board()[row][col].get_unit_name() == 'AI':
                            print(f"{self.get_game_map().get_board()[row][col].get_unit_name()} Has Been Destroyed")
                            print(f"{self.get_game_map().get_board()[row][col].get_faction()} Lost the Game")
                            self.get_game_map().get_board()[row][col] = None
                            self.set_ai_dead(True)
                        else:
                            print(f"{self.get_game_map().get_board()[row][col].get_unit_name()} Has Been Destroyed")
                            self.get_game_map().get_board()[row][col] = None


# static functions
def convert2board_index(char, col):
    tup_dict = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
    # if not in var -> throw exception
    row = tup_dict[char]
    return row, col


def keyboard_command_move():
    while True:
        keyboard_event = keyboard.read_event(suppress=True)
        if keyboard_event.event_type == keyboard.KEY_DOWN:
            if keyboard_event.name in ['left', 'right', 'up', 'down']:
                return keyboard_event.name
            else:
                print("Invalid Keyboard Input")


def keyboard_command_attack():
    while True:
        keyboard_event = keyboard.read_event(suppress=True)
        if keyboard_event.event_type == keyboard.KEY_DOWN:
            if keyboard_event.name == 'a':
                return keyboard_event.name
            else:
                print("Invalid Keyboard Input")


class MainGameLoop:
    def __init__(self):
        self.var = Engine()


def keyboard_command_repair():
    while True:
        keyboard_event = keyboard.read_event(suppress=True)
        if keyboard_event.event_type == keyboard.KEY_DOWN:
            if keyboard_event.name == 'r':
                return keyboard_event.name
            else:
                print("Invalid Keyboard Input")


def keyboard_command_self_destruct():
    while True:
        keyboard_event = keyboard.read_event(suppress=True)
        if keyboard_event.event_type == keyboard.KEY_DOWN:
            if keyboard_event.name == 'space':
                return keyboard_event.name
            else:
                print("Invalid Keyboard Input")


def within_range(tup):
    if 0 <= tup[0] < 5 and 0 <= tup[1] < 5:
        return True
    else:
        return False


def is_adjacent(tup1, tup2):
    if tup1 in [(tup2[0], tup2[1] + 1), (tup2[0], tup2[1] - 1), (tup2[0] + 1, tup2[1]), (tup2[0] - 1, tup2[1])]:
        return True
    else:
        return False


def customized_print(message, file):
    print(message)
    file.write(message + '\n')
