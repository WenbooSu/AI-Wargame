import sys
import copy
import random
from enum import Enum
import time, datetime

class Player(Enum):
    attacker = 0
    defender = 1

    def next(self):
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

class Action:

    def __init__(self, action_name : str, myself : tuple, target : tuple) -> None:
        self.action_name = action_name
        self.myself = myself
        self.target = target
    
    def get_action_name(self):
        return self.action_name
    
    def get_myself(self):
        return self.myself
    
    def get_target(self):
        return self.target
    
    def __str__(self):
        return f"{self.get_action_name()}: my unit --> {self.get_myself()}  target unit --> {self.get_target()}"
        

class Game:


    def __init__(self):
        self.player = Player.attacker
        self.turn_played = 0
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
        return message
        # trace_records(message)

    def get_position(self, unit : Units):
        for i, row in enumerate(self.board):
            for j, element in enumerate(row):
                if isinstance(element, Units):
                    if unit.get_id() == element.get_id():
                        return i, j
        return None

    def get_unit(self, tup):
        unit = self.board[tup[0]][tup[1]]
        if isinstance(unit, Units):
            return unit
        else:
            return None
    
    def select_unit(self):
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

    def isfriendly(self, t : tuple):
        unit1 = self.get_unit(t)
        if unit1.get_faction() == self.player.name:
            return True
        else:
            return False

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
    
    def get_pieces(self, player:str):
        ai_pieces = []
        for i, row in enumerate(self.board):
            for j, unit in enumerate(row):
                if isinstance(unit, Units) and unit.get_faction() == player:
                    ai_pieces.append((i, j))
        return ai_pieces

    def get_valid_adjacents(self, tup):
        valid_adjacents = []
        directions = [(tup[0], tup[1] + 1), (tup[0], tup[1] - 1), (tup[0] + 1, tup[1]), (tup[0] - 1, tup[1])]
        #print(directions)
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
            adj_unit = self.get_unit(adjacent)
            if isinstance(adj_unit, Units):
                if unit.get_faction() != adj_unit.get_faction():
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
                adj_unit = self.get_unit(adjacent)
                if isinstance(adj_unit, Units) and adj_unit.get_faction() == unit.get_faction() and adj_unit.get_hp() < 9:
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
                'Tech': 1,
                'Program': 0,
                'Firewall': 0,
                'AI': 0
            },
            'Tech': {
                'AI': 3,
                'Firewall': 3,
                'Program': 3,
                'Tech': 0,
                'Virus': 0
            },
            'Virus':{
                'AI': 0,
                'Firewall': 0,
                'Program': 0,
                'Tech': 0,
                'Virus': 0
            },
            'Firewall':{
                'AI': 0,
                'Firewall': 0,
                'Program': 0,
                'Tech': 0,
                'Virus': 0
            },
            'Program':{
                'AI': 0,
                'Firewall': 0,
                'Program': 0,
                'Tech': 0,
                'Virus': 0
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
        surroundings = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1), (x, y + 1), (x + 1, y - 1), (x + 1, y),
                        (x + 1, y + 1)]
        unit = self.get_unit(tup)
        unit.set_hp(0)
        for row, col in surroundings:
            if (0 <= row < 5) and (0 <= col < 5):
                node = self.get_unit((row, col))
                if isinstance(node, Units):
                    node.hp_decrease_by(2)

    def clear(self): # must call before check_winner()
            for row in self.board:
                for unit in row:
                    if isinstance(unit, Units) and unit.get_hp() <= 0:
                        x, y =self.get_position(unit)
                        self.board[x][y] = None
    
    def check_winner(self):
        alive = []
        for row in self.board:
            for unit in row:
                if isinstance(unit, Units) and unit.get_unit_name() == 'AI':
                    alive.append(unit)
        if alive == None:
            print('Game Tied!')
            return 'Tie'
        if len(alive) == 1 and isinstance(alive[0], Units) and alive[0].get_faction() == 'defender':
            print('Defender Win!')
            return 'defender'
        if len(alive) == 1 and isinstance(alive[0], Units) and alive[0].get_faction() == 'attacker':
            print('Attacker Win!')
            return 'attacker'
        if len(alive) == 2:
            return None
    
    def game_over(self):
        if self.check_winner() == None:
            return False
        else:
            return True
    
    def switch_turn(self):
        self.player = self.player.next()

    def heuristic(self):
        def calculate_scores(player):
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
        VP1, TP1, FP1, PP1, AIP1 = calculate_scores('attacker')
        VP2, TP2, FP2, PP2, AIP2 = calculate_scores('defender')
        score = (3 * VP1 + 3 * TP1 + 3 * FP1 + 3 * PP1 + 9999 * AIP1) - (3 * VP2 + 3 * TP2 + 3 * FP2 + 3 * PP2 + 9999 * AIP2)
        return score

    def evaluate_function_1(self, player:str):
        unit_weight = 1.0
        my_health_weight = 0.5
        enemy_health_weight = -0.5
        board = self.get_board()
        score = 0
        for row in board:
            for unit in row:
                if unit:
                    if isinstance(unit, Units) and unit.get_faction() == player:
                        score += unit_weight
                        score += my_health_weight * unit.get_hp()
                    else:
                        score += enemy_health_weight * unit.get_hp()
        return score
    
    def evaluate_function_2(self, player:str):
        unit_weights = {
            'Program': 1.0,
            'Firewall': 2.0,
            'Virus': 2.5,
            'AI': 3.0,
            'Tech': 1.0
        }
    
        unit_weight = 1.0
        my_health_weight = 0.5  
        enemy_health_weight = -0.5  

        board = self.get_board()
        score = 0

        for row in board:
            for unit in row:
                if isinstance(unit, Units):
                    unit_type = unit.get_unit_name()
                    if unit.get_faction() == player:
                        score += unit_weight * unit_weights[unit_type]
                        score += my_health_weight * unit.get_hp()
                    else:
                        score += enemy_health_weight * unit.get_hp()
        
        return score

    def get_all_possible_actions(self, player:str):
        actions = []
        my_units_positions = self.get_pieces(player)
        for unit_pos in my_units_positions:
            # move
            valid_moves = self.valid_move(unit_pos)
            if valid_moves:
                for move in valid_moves:
                    action_move = Action('move', unit_pos, move)
                    actions.append(action_move)
            # attack
            valid_attacks = self.valid_attack(unit_pos)
            if valid_attacks:
                for target in valid_attacks:
                    action_attack = Action('attack', unit_pos, target)
                    actions.append(action_attack)
            # repair
            valid_repairs = self.valid_repair(unit_pos)
            if valid_repairs:
                for patient in valid_repairs:
                    action_repair = Action('repair', unit_pos, patient)
                    actions.append(action_repair)
            # destruct
            """action_destruct = Action('destruct', unit_pos, unit_pos)
            actions.append(action_destruct)"""
        return actions

    def perform_action(self, action:Action):
        if action.get_action_name() == 'move':
            message = f"{self.get_unit(action.get_myself()).myself()} moved to position {action.get_target()}"
            self.move(action.get_myself(), action.get_target())
            return message
        if action.get_action_name() == 'attack':
            self.attack(action.get_myself(), action.get_target())
            return f"{self.get_unit(action.get_myself()).myself()} attacked {self.get_unit(action.get_target()).myself()}"
        if action.get_action_name() == 'repair':
            self.repair(action.get_myself(), action.get_target())
            return f"{self.get_unit(action.get_myself()).myself()} repaired {self.get_unit(action.get_target()).myself()}"
        if action.get_action_name() == 'destruct':
            self.destruct(action.get_myself())
            return f"{self.get_unit(action.get_myself()).myself()} destructed itself"
            
        

    def simulate_action(self, action : Action):
        new_game = copy.deepcopy(self)
        if action.get_action_name() == 'move':
            new_game.move(action.get_myself(), action.get_target())
            return new_game
        if action.get_action_name() == 'attack':
            new_game.attack(action.get_myself(), action.get_target())
            return new_game
        if action.get_action_name() == 'repair':
            new_game.repair(action.get_myself(), action.get_target())
            return new_game
        if action.get_action_name() == 'destruct':
            new_game.destruct(action.get_myself())
            return new_game

    def minimax(self, depth, is_maximizing):
        if depth == 0 or self.game_over():
            return (self.evaluate_game_state(self.player.name), None)

        best_moves = []

        if is_maximizing:
            best_score = float('-inf')
            for move in self.get_all_possible_actions(self.player.name):
                game_copy = self.clone()
                game_copy.simulate_action(move)
                current_score, _ = game_copy.minimax(depth - 1, False)
                if current_score > best_score:
                    best_score = current_score
                    best_moves = [move]
                elif current_score == best_score:
                    best_moves.append(move)
        else:
            best_score = float('inf')
            for move in self.get_all_possible_actions(self.player.name):
                game_copy = self.clone()
                game_copy.simulate_action(move)
                current_score, _ = game_copy.minimax(depth - 1, True)

                if current_score < best_score:
                    best_score = current_score
                    best_moves = [move]
                elif current_score == best_score:
                    best_moves.append(move)
        best_move = random.choice(best_moves) if best_moves else None

        return (best_score, best_move)
    def minimax_time(self, depth, is_maximizing, start_time, time_limit):
        if time.time() - start_time > time_limit:
            return (self.heuristic(), None)

        if depth == 0 or self.game_over():
            return (self.heuristic(), None)

        best_moves = []

        if is_maximizing:
            best_score = float('-inf')
            for move in self.get_all_possible_actions(self.player.name):
                game_copy = self.clone()
                game_copy.simulate_action(move)
                current_score, _ = game_copy.minimax_time(depth - 1, False, start_time, time_limit)

                
                if time.time() - start_time > time_limit:
                    break

                if current_score > best_score:
                    best_score = current_score
                    best_moves = [move]
                elif current_score == best_score:
                    best_moves.append(move)
        else:
            best_score = float('inf')
            for move in self.get_all_possible_actions(self.player.name):
                game_copy = self.clone()
                game_copy.simulate_action(move)
                current_score, _ = game_copy.minimax_time(depth - 1, True, start_time, time_limit)

                # check the time constraint after the recursive call
                if time.time() - start_time > time_limit:
                    break

                if current_score < best_score:
                    best_score = current_score
                    best_moves = [move]
                elif current_score == best_score:
                    best_moves.append(move)

        best_move = random.choice(best_moves) if best_moves else None
        return (best_score, best_move)

    def alpha_beta_search(self, depth, alpha, beta, maximizing):
        if depth == 0 or self.game_over():
            return (self.heuristic(), None)

        best_moves = []
        best_score = float('-inf') if maximizing else float('inf')

        for action in self.get_all_possible_actions(self.player.name):
            new_game = self.simulate_action(action)
            score, _ = new_game.alpha_beta_search(depth - 1, alpha, beta, not maximizing)

            
            if (maximizing and score > best_score) or (not maximizing and score < best_score):
                best_score = score
                best_moves = [action]
            elif score == best_score:
                best_moves.append(action)

            if maximizing:
                alpha = max(alpha, score)
            else:
                beta = min(beta, score)

            if alpha >= beta:
                break  # prune

        best_move = random.choice(best_moves) if best_moves else None
        return (best_score, best_move)

    
    def find_best_action_alpha_beta(self, player, depth:int):
        alpha = float('-inf')
        beta = float('inf')
        maximizing = player == 'attacker'

        best_score, best_move = self.alpha_beta_search(depth, alpha, beta, maximizing)

        return (best_score, best_move)


    def clone(self):
        new = copy.deepcopy(self)
        new.board = copy.deepcopy(self.board)
        return new


def human_vs_ai(turn_limit:int, time_limit:int, is_minimax:bool):
    def trace_records(message):
        try:
            with open(f'gameTrace-{is_minimax}-{time_limit}-{turn_limit}.txt', 'a') as file:  # 'a' mode appends to the file
                file.write(message + '\n')
        except Exception as e:
            print(f"Error to Create/Open File")
    game = Game()
    map = game.show_board()
    message = ''
    trace_records(map)
    turn = 0
    print('Game Start!')
    trace_records('Game Start \n')
    while not game.game_over():
        print(f"Turn: {turn+1}")
        trace_records(f"Turn: {turn+1}")
        if game.player.name == 'attacker':
            print(game.player.name)
            trace_records(game.player.name)
            game.clear()
            unit_pos = game.select_unit()
            while not game.isfriendly(unit_pos):
                print('Cannot Choose Enemy Unit')
                unit_pos = game.select_unit()
            action_choice = 0
            while True:
                print("\nPlease choose an action:")
                print("1. Move")
                print("2. Attack")
                print("3. Repair")
                print("4. Self-Destruct")
                print("5. Select Another Unit\n")
                action_choice = input("Enter the number of your choice from integer 1-4: ")
                if action_choice  not in ['1', '2', '3', '4', '5']:
                    print("Invalid choice. Please select a valid action from integer 1-5.")
                    continue
                if action_choice == '1':
                    move_list = game.valid_move(unit_pos)
                    if move_list == None:
                        print('Unit Cannot Move')
                        continue
                    else:
                        destination = game.select_unit()
                        if destination not in move_list:
                            print('Invalid Operation')
                            continue
                        else:
                            game.move(unit_pos, destination)
                            message = f"Moved from {unit_pos} to {destination}"
                            trace_records(message)
                            break
                if action_choice == '2':
                    attack_list = game.valid_attack(unit_pos)
                    if not attack_list:
                        print('Unit Cannot Attack')
                        print(attack_list)
                        continue
                    else:
                        target = game.select_unit()
                        if target not in attack_list:
                            print('Invalid Operation')
                            continue
                        else:
                            game.attack(unit_pos, target)
                            message = f"{unit_pos} attacked to {target}"
                            trace_records(message)
                            game.clear()
                            break

                if action_choice == '3':
                    repair_list = game.valid_repair(unit_pos)
                    if not repair_list:
                        print('Unit Cannot Repair')
                    else:
                        patient = game.select_unit
                        if patient not in repair_list:
                            print('Invalid Operation')
                            continue
                        else:
                            game.repair(unit_pos, patient)
                            message = f"{unit_pos} attacked to {patient}"
                            trace_records(message)
                            break
                
                if action_choice == '4':
                    game.destruct(unit_pos)
                    message = f"{unit_pos} destructed itself"
                    trace_records(message)
                    game.clear()
                    break
            game.clear()
            map1 = game.show_board()
            trace_records(map1)
            game.switch_turn()
        else:
            start = time.time()
            print(game.player.name)
            trace_records(game.player.name)
            print(f"Turn: {turn+1}")
            trace_records(f"Turn: {turn+1}")
            if is_minimax:
                defender_move = game.minimax_time(4, False, start, time_limit)
            else:
                defender_move = game.find_best_action_alpha_beta('defender', 4)
            end = time.time()
            elapsed = end - start
            elapsed_seconds_float = float(elapsed)
            print(f'Search Time: {elapsed_seconds_float:.2f} seconds')
            trace_records(f'Search Time: {elapsed_seconds_float:.2f} seconds')
            print(f'defender_move Score: {defender_move[0]}')
            trace_records(f'defender_move Score: {defender_move[0]}')
            message = game.perform_action(defender_move[1])
            trace_records(message)
            game.clear()
            map2 = game.show_board()
            trace_records(map2)
            turn += 1
            game.switch_turn()
        if turn == turn_limit:
            print('Maximum Turns Reached! Game Tied')
            break
        turn += 1
    if game.game_over():
        print(f"In {turn} Moves")


def ai_vs_ai(turn_limit:int, time_limit:int, is_minimax:bool):
    def trace_records(message):
        try:
            with open(f'gameTrace-{is_minimax}-{time_limit}-{turn_limit}.txt', 'a') as file:  # 'a' mode appends to the file
                file.write(message + '\n')
        except Exception as e:
            print(f"Error to Create/Open File")
    game = Game()
    turn = 0
    map = game.show_board()
    trace_records(map)
    print('GAME Start')
    trace_records('Game Start')
    while not game.game_over():
        if game.player.name == 'attacker':
            start = time.time()
            print(f"Turn: {turn+1}")
            trace_records(f"Turn: {turn+1}")
            print(game.player.name)
            trace_records(game.player.name)
            
            if is_minimax:
                attacker_move = game.minimax_time(4, True, start, time_limit)
            else:
                attacker_move = game.find_best_action_alpha_beta('attacker', 4)
            end = time.time()
            elapsed = end - start
            elapsed_seconds_float = float(elapsed)
            print(f'Search Time: {elapsed_seconds_float:.2f} seconds')
            trace_records(f'Search Time: {elapsed_seconds_float:.2f} seconds')
            print(f'Heuristic Score: {attacker_move[0]}')
            trace_records(f'Heuristic Score: {attacker_move[0]}')
            msg = game.perform_action(attacker_move[1])
            trace_records(msg)
            game.clear()
            map1 = game.show_board()
            trace_records(map1)
            turn += 1
            game.switch_turn()
        else:
            start = time.time()
            print(game.player.name)
            trace_records(game.player.name)
            print(f"Turn: {turn+1}")
            trace_records(f"Turn: {turn+1}")
            if is_minimax:
                defender_move = game.minimax_time(4, False, start, time_limit)
            else:
                defender_move = game.find_best_action_alpha_beta('defender', 4)
            end = time.time()
            elapsed = end - start
            elapsed_seconds_float = float(elapsed)
            print(f'Search Time: {elapsed_seconds_float:.2f} seconds')
            trace_records(f'Search Time: {elapsed_seconds_float:.2f} seconds')
            print(f'Heuristic Score: {defender_move[0]}')
            trace_records(f'Heuristic Score: {defender_move[0]}')
            msg2 = game.perform_action(defender_move[1])
            trace_records(msg2)
            game.clear()
            map2 = game.show_board()
            trace_records(map2)
            turn += 1
            game.switch_turn()
        if turn == turn_limit:
            print('Maximum Turns Reached! Game Tied')
            break
    winner = game.check_winner()
    if winner != None:
        trace_records(f"{winner} won the game in {turn} turns")

def play():
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< WAR GAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print('Choose Game Mode to Start Playing\n')
    print('2: AI vs. Human')
    print('3: AI vs. AI\n')
    mode = input('Enter The Mode Number: ')
    if mode not in [1, 2, 3]:
        mode ==  3
    ai_mode = input('Turn on Minimax? (Enter Y to turn on Minimax and close alpha/beta)')
    is_minimax = True
    if ai_mode == 'Y':
        is_minimax = True
    else:
        is_minimax = False
    time_limit = input('Enter The Time Limit for Searching in Seconds: ')
    turn_limit = input('Enter The Max Turn Limit: ')
    if mode == '2' and is_minimax == False:
        human_vs_ai(int(turn_limit), int(time_limit), is_minimax)
    if mode == '2' and is_minimax:
        human_vs_ai(int(turn_limit), int(time_limit), is_minimax)
    if mode == '3' and is_minimax == False:
        ai_vs_ai(int(turn_limit), int(time_limit), is_minimax)
    if mode == '3' and is_minimax:
        ai_vs_ai(int(turn_limit), int(time_limit), is_minimax)

if __name__ == "__main__":
    play()


    
    
    
    




    
