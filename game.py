import sys

import game_engine as ge


class WarGame:
    def __init__(self):
        self.engine = ge.Engine()
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
            print()
        if mode == 2:
            self.human_ai()

    def human_human(self):
        print()

    def human_ai(self):
        print(self.engine.get_game_map())

    def main_game_loop(self):
        attacker_pos = None
        defender_pos = None
        turn = 0
        print('Attacker Starts First')
        while not self.engine.get_ai_dead():
            attacker_pos = self.engine.select_unit()
            while self.engine.get_unit_node(attacker_pos).get_faction() != 'attacker':
                continue


