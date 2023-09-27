%run engine.ipynb

class MainGameLoop:
    def __init__(self):
        self.engine = Engine()
        self.max_moves = 100
        self.current_move = 0

    def play_game(self):
        while True:
            #Check game-ending conditions: AI dead or max moves reached
            if self.engine.get_ai_dead():
                print("Attacker wins!")
                break
            if self.current_move >= self.max_moves:
                print("Maximum moves reached. A draw game.")
                break

            #Display game board
            print("Current Game Board:")
            self.engine.get_game_map().show_board()
            print(f"Move {self.current_move + 1}") #Count the move start from 1 

            #Determine current player
            current_player = 'defender' if self.current_move % 2 == 0 else 'attacker' #Attacker goes first
            print(f"Current Player: {current_player}")

            #Choose player action
            while True:
                print("Please choose an action:")
                print("1.Move")
                print("2.Attack")
                print("3.Repair")
                print("4.Self-Destruct")
                action_choice = input("Enter the number of your choice from integer 1-4: ")
                if action_choice in ['1', '2', '3', '4']:
                    break
                else:
                    print("Invalid choice. Please select a valid action from integer 1-4.")

            if action_choice == '1': #Move
                position = self.engine.select_unit()
                self.engine.move(position)
            elif action_choice == '2': #Attack
                print("Choose your unit to attack with:")
                s_position = self.engine.select_unit()
                print("Choose the target unit to be attacked:")
                t_position = self.engine.select_unit()
                self.engine.attack(s_position, t_position)
            elif action_choice == '3': #Repair
                print("Choose your unit to repair with:")
                s_position = self.engine.select_unit()
                print("Choose the target unit to be repaired:")
                t_position = self.engine.select_unit()
                self.engine.repair(s_position, t_position)
            elif action_choice == '4': #Self-Destruct
                print("Choose the unit to self-destruct:")
                position = self.engine.select_unit()
                self.engine.self_destruct(position)

            #Increment move counter
            self.current_move += 1

# Start the game
if __name__ == "__main__":
    game = MainGameLoop()
    game.play_game()
