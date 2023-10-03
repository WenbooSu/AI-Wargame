import sys
import game_engine as ge


def trace_records(message):
    try:
        with open('gameTrace-false-none-100.txt', 'a') as file:  # 'a' mode appends to the file
            file.write(message + '\n')
    except Exception as e:
        print(f"Error to Create/Open File")


class MainGameLoop:
    def __init__(self):
        self.engine = ge.Engine()
        self.max_round = 100
        self.current_round = 1
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
            return 1
        else:
            return mode

    def start_game(self, mode):
        if mode == 1:
            trace_records('Game Mode: Human vs. Human\n\n Max Turns: 100 \n\n')
            self.play_game_human_human()
        if mode == 2:
            self.human_ai()

    def play_game_human_human(self):
        while self.current_round <= 100 or self.engine.get_ai_dead():
            # Check game-ending conditions: AI dead or max moves reached
            if self.engine.get_ai_dead():
                if self.current_round % 2 == 0:
                    trace_records(f'Defender Wins in {self.current_round-1} Moves\n')
                    print(f'Defender Wins in {self.current_round-1} Moves')
                    break
                else:
                    trace_records(f'Attacker Wins in {self.current_round-1} Moves\n')
                    print(f'Attacker Wins in {self.current_round-1} Moves')
                    break
            if self.current_round >= self.max_round:
                print("Maximum moves reached. A draw game.")
                break

            # Display game board
            print("\nCurrent Game Board:")
            self.engine.get_game_map().show_board()
            # print(f"Move {self.current_move + 1}")  # Count the move start from 1
            # 0 1 2 3 4 5 6
            # Determine current player
            current_player = 'defender' if self.current_round % 2 == 0 else 'attacker'  # Attacker goes first
            print(f"\nCurrent Player: {current_player}")
            trace_records(f"\nCurrent Player: {current_player}")

            # Choose player action
            while True:
                print(f'ROUND: {self.current_round}')
                trace_records(f'ROUND: {self.current_round}')

                while True:
                    s_position = self.engine.select_unit()
                    if self.engine.get_unit_node((s_position[0], s_position[1])) is None:
                        print('Cannot Select None Unit')
                        continue
                    if self.engine.get_unit_node((s_position[0], s_position[1])).get_faction() != current_player:
                        print('Cannot Select Enemy''s Unit')
                        continue
                    break

                action_choice = 0
                while True:
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
                        continue

                if action_choice == '1':  # Move
                    if self.engine.movable(s_position):
                        trace_records(f'Unit: {self.engine.get_unit_node(s_position).myself()} ')
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
            self.current_round += 1

    def human_ai(self):
        print(self.engine.get_game_map())  # To Do


if __name__ == "__main__":
    game = MainGameLoop()
    game_mode = game.main_menu_page()
    game.start_game(game_mode)
