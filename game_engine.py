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

