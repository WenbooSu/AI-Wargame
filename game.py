import sys
import game_engine as ge


class MainGameLoop:
    def __init__(self):
        self.engine = ge.Engine()
        self.max_moves = 100
        self.current_move = 0
        self.player1 = 'attacker'
        self.player2 = 'defender'

    @staticmethod
    def main_menu_page():
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< WAR GAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print('Choose Game Mode to Start Playing\n')
        print('1: Human vs. Human')
        print('2: AI vs. Human')
        print('3: AI vs. AI\n')
        print('                                                         credit to: CloseAI Ultd\n')
        mode = input('Enter The Mode Number: ')
        if mode not in [1, 2, 3]:
            sys.exit()
        else:
            return mode

    def start_game(self, mode):
        if mode == 1:
            self.play_game_human_human()
        if mode == 2:
            self.human_ai()

    def play_game_human_human(self):
        while self.current_move <= 100:
            # Check game-ending conditions: AI dead or max moves reached
            if self.engine.get_ai_dead():
                print("Attacker wins!")
                break
            if self.current_move >= self.max_moves:
                print("Maximum moves reached. A draw game.")
                break

            # Display game board
            print("Current Game Board:")
            self.engine.get_game_map().show_board()
            print(f"Move {self.current_move + 1}")  # Count the move start from 1

            # Determine current player
            current_player = 'defender' if self.current_move % 2 == 0 else 'attacker'  # Attacker goes first
            print(f"Current Player: {current_player}")

            # Choose player action
            while True:

                s_position = self.engine.select_unit()

                if self.engine.get_unit_node((s_position[0], s_position[1])).get_faction() != current_player:
                    print('Cannot Select Enemy''s Unit')
                    continue

                print("\nPlease choose an action:")
                print("1. Move")
                print("2. Attack")
                print("3. Repair")
                print("4. Self-Destruct")
                print("5. Select Another Unit\n")
                action_choice = input("Enter the number of your choice from integer 1-4: ")
                if action_choice in ['1', '2', '3', '4', '5']:
                    break
                else:
                    print("Invalid choice. Please select a valid action from integer 1-5.")

                if action_choice == '1':  # Move
                    if self.engine.movable(s_position):
                        self.engine.move(s_position)
                        break
                    else:
                        print('Unit Cannot Move')
                        continue
                elif action_choice == '2':  # Attack
                    print("Choose the target unit to be attacked:")
                    t_position = self.engine.select_unit()
                    var = self.engine.attack(s_position, t_position)
                    if var:
                        break
                    else:
                        continue
                elif action_choice == '3':  # Repair
                    print("Choose the target unit to be repaired:")
                    t_position = self.engine.select_unit()
                    var = self.engine.repair(s_position, t_position)
                    if var:
                        break
                    else:
                        continue
                elif action_choice == '4':  # Self-Destruct
                    self.engine.self_destruct(s_position)
                    break

            # Increment move counter
            self.current_move += 1

    def human_ai(self):
        print(self.engine.get_game_map()) # To Do

    def main_game_loop(self):
        attacker_pos = None
        defender_pos = None
        turn = 0
        print('Attacker Starts First')
        while not self.engine.get_ai_dead():
            attacker_pos = self.engine.select_unit()
            while self.engine.get_unit_node(attacker_pos).get_faction() != 'attacker':
                continue
