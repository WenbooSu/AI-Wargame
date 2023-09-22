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

    def show_board(self):
        for inner_list in self.board:
            for obj in inner_list:
                if isinstance(obj, Units):
                    print(obj.myself(), end=' ')
                else:
                    print(' * ', end=' ')
            print()


obj1 = CheckerBoard()

obj1.show_board()
