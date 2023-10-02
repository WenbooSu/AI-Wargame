import engine as eg

class MainGameLoop:
    def __init__(self):
        self.engine = eg.Engine()
        self.max_moves = 100
        self.current_move = 0
        self.current_player = 'attacker' #Attacker goes first
        self.actions = []  #Store actions
        
    def switch_player(self):
        self.current_player = 'defender' if self.current_player == 'attacker' else 'attacker'
        
    def log_action(self, action, game_board, filename):
        round_info = f"Round {self.current_move + 1}: {action}\n"
        action_detail = ""
        game_board = self.engine.get_game_map()
        board_str = game_board.get_map_str()
        
        action_detail += f"Details:\n{board_str}"
        self.actions.append(round_info + action_detail)

        #Clear previous content if it's a new game
        if self.current_move == 0:
            with open(filename, 'w') as file:
                file.write(round_info + action_detail)
        else:
            with open(filename, 'a') as file:
                file.write(round_info + action_detail)

    @staticmethod
    def main_menu():
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< WAR GAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print('Choose a game mode to start playing\n')
        print('1: Human vs. Human')
        print('2: AI vs. Human')
        print('3: AI vs. AI\n')
        mode = input('Enter the mode number: ')
        if mode not in ['1', '2', '3']:
            return 1
        else:
            return mode

    def start_game(self, mode):
        if mode == '1':
            self.play_game_hh()
        if mode == '2':
            self.human_ai()
        if mode == '3':
            self.ai_ai()
            
    def play_game_hh(self):
        while self.current_move <= self.max_moves or self.engine.get_ai_dead():
            #Check game-ending conditions: AI dead or max moves reached
            if self.engine.get_ai_dead(): 
                if self.current_move % 2 == 0:
                    print(f"Attacker wins in {self.current_move} moves!")
                    self.log_action(f"Attacker wins in {self.current_move} moves!", updated_board, 'game_actions.txt')
                    break
                else:
                    print(f"Defender wins in {self.current_move} moves!")
                    self.log_action(f"Defender wins in {self.current_move} moves!", updated_board, 'game_actions.txt')
                    break
            if self.current_move >= self.max_moves:
                print(f"Maximum moves reached. A draw game.")
                self.log_action(f"Maximum moves reached. A draw game.", updated_board, 'game_actions.txt')
                break

            #Display game board
            print("Current Game Board:")
            self.engine.get_game_map().show_board()
            print("")
            print(f"Move {self.current_move + 1}") #Count the move start from 1 

            #Determine current player
            current_player = 'attacker' if self.current_move % 2 == 0 else 'defender'
            print(f"Current Player: {current_player}")
            
            updated_board = self.engine.get_game_map()
            #Choose player action
            while True:
                #Choose player unit
                s_position = self.engine.select_unit()
                
                if self.engine.get_unit_node((s_position[0], s_position[1])) is None:
                        print('Cannot Select None Unit')
                        continue
                if self.engine.get_unit_node((s_position[0], s_position[1])).get_faction() != current_player:
                    print("You can't' choose an enemy's unit.")
                    continue
                break
            
            while True:
                print("\nPlease choose an action:")
                print("1.Move")
                print("2.Attack")
                print("3.Repair")
                print("4.Self-Destruct")
                print("5.Select another unit\n")
                
                action_choice = input("Enter the number of your choice from integer 1-5: ")
                if action_choice in ['1', '2', '3', '4', '5']:
                    break
                else:
                    print("Invalid choice. Please select a valid action from integer 1-5.")
                    continue
                
            if action_choice == '1': #Move
                if self.engine.movable(s_position):
                    move_result = self.engine.move1(s_position)
                    move_info = f"{current_player} moved from {s_position} to {move_result}."
                    self.log_action(f"Round {self.current_move + 1}: {move_info}", updated_board, 'game_actions.txt')
                else:
                    print("The selected unit can't move.")
                    continue
                
            elif action_choice == '2': #Attack
                print("Choose the target unit to be attacked:")
                t_position = self.engine.select_unit()
                attack_result = self.engine.attack(s_position, t_position)
                attack_info = f"{current_player} attacked {t_position} with {s_position}, casued  damage."
                self.log_action(f"Round {self.current_move + 1}: {attack_info}", updated_board,'game_actions.txt')

            elif action_choice == '3': #Repair
                print("Choose the target unit to be repaired:")
                t_position = self.engine.select_unit()
                repair_result = self.engine.repair(s_position, t_position)
                repair_info = f"{current_player} repaired {t_position} with {s_position}, restored  heart point."  
                self.log_action(f"Round {self.current_move + 1}: {repair_info}", updated_board,'game_actions.txt')

            elif action_choice == '4': #Self-Destruct
                self.engine.self_destruct(s_position) 
                self.log_action(f"{current_player} - Round {self.current_move + 1}: Self-destructed {s_position}.", updated_board,'game_actions.txt')

            elif action_choice == '5':  #End Turn
                break
            
            #Display game board after each action
            self.engine.get_game_map().show_board()
            print("")
    
            #Switch turn to the other player
            self.switch_player()
            
            #Increment move counter
            self.current_move += 1

# Start the game
if __name__ == "__main__":
    game = MainGameLoop()
    game_mode = game.main_menu()
    game.start_game(game_mode)

    
    
