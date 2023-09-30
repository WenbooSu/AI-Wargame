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
        
    def log_action(self, action, filename):
        self.actions.append(action)
        with open(filename, 'w') as file:
            for action in self.actions:
                file.write(action + '\n')

    def write_actions_to_file(self, filename):
        with open(filename, 'w') as file:
            for action in self.actions:
                file.write(action + '\n')
                
    def play_game(self):
        while True:
            #Check game-ending conditions: AI dead or max moves reached
            if self.engine.get_ai_dead('defender') and not self.engine.get_ai_dead('attacker'):
                print("Attacker wins!")
                self.log_action("Attacker wins!", 'game_actions.txt')
                break
            elif self.engine.get_ai_dead('attacker') and not self.engine.get_ai_dead('defender'):
                print("Defender wins!")
                self.log_action("Defender wins!", 'game_actions.txt')
                break
            elif self.current_move >= self.max_moves:
                print("Maximum moves reached. A draw game.")
                self.log_action("Maximum moves reached. A draw game.", 'game_actions.txt')
                break

            #Display game board
            print("Current Game Board:")
            self.engine.get_game_map().show_board()
            print("")
            print(f"Move {self.current_move + 1}") #Count the move start from 1 

            #Determine current player
            current_player = 'attacker' if self.current_move % 2 == 0 else 'defender'
            print(f"Current Player: {current_player}")

            #Choose player action
            while True:
                #Choose player unit
                
                s_position = self.engine.select_unit()
                
                if self.engine.get_unit_node((s_position[0], s_position[1])).get_faction() != current_player:
                    print("You can't' choose an enemy's unit.")
                    continue
            
                print("Please choose an action:")
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

            if action_choice == '1': #Move
                if self.engine.movable(s_position):
                    self.engine.move1(s_position)
                    self.log_action(f"{current_player} - Action {self.current_move + 1}: Move", 'game_actions.txt')
                else:
                    print("The selected unit can't move. Please select another one.")
                    continue
                
            elif action_choice == '2': #Attack
                print("Choose the target unit to be attacked:")
                t_position = self.engine.select_unit()
                self.engine.attack(s_position, t_position)
                self.log_action(f"{current_player} - Action {self.current_move + 1}: Attack", 'game_actions.txt')
            
            elif action_choice == '3': #Repair
                print("Choose the target unit to be repaired:")
                t_position = self.engine.select_unit()
                self.engine.repair(s_position, t_position)
                self.log_action(f"{current_player} - Action {self.current_move + 1}: Repair", 'game_actions.txt')
            
            elif action_choice == '4': #Self-Destruct
                self.engine.self_destruct(s_position)
                self.log_action(f"{current_player} - Action {self.current_move + 1}: Self-destruct", 'game_actions.txt')

            elif action_choice == '5':  #End Turn
                break
            
            #Display game board after each action
            self.engine.get_game_map().show_board()
    
            #Switch turn to the other player
            self.switch_player()
            
            #Increment move counter
            self.current_move += 1

# Start the game
if __name__ == "__main__":
    game = MainGameLoop()
    game.play_game()
    game.write_actions_to_file('game_actions.txt')
    
    
