def e2(self, player:str):
    UNIT_WEIGHTS = {
        'Program': 1.0,
        'Firewall': 2.0,
        'Virus': 2.5,
        'AI': 3.0,
        'Tech': 1.0
    }
  
    AI_UNIT_WEIGHT = 1.0
    AI_HEALTH_WEIGHT = 0.5  
    ENEMY_HEALTH_WEIGHT = -0.5  

    board = self.get_board()
    ai_score = 0.0

    for row in board:
        for unit in row:
            if isinstance(unit, Units):
                unit_type = unit.get_unit_name()
                if unit.get_faction() == player:
                    ai_score += AI_UNIT_WEIGHT * UNIT_WEIGHTS[unit_type]
                    ai_score += AI_HEALTH_WEIGHT * unit.get_hp()
                else:
                    ai_score += ENEMY_HEALTH_WEIGHT * unit.get_hp()
    
    return ai_score
