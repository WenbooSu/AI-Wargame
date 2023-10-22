def alpha_beta_search(self, depth, alpha, beta, maximizing):
    if depth == 0 or self.game_over():
        return (self.evaluate_game_state(self.player.name), None)
    
    best_move = None

    if maximizing:
        best_score = float('-inf') 
        #alpha: maximizing player (not found good moves yet), update alpha if found a greater value
        for action in self.get_all_possible_actions(self.player.name):
            new_game = self.simulate_action(action)
            score, _ = new_game.alpha_beta_search(depth - 1, alpha, beta, False)
            if score > best_score:
                best_score = score
                best_move = action
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return (best_score, best_move)
    else:
        best_score = float('inf')
        #beta: minimizing player, update beta if found a less value
        for action in self.get_all_possible_actions(self.player.name):
            new_game = self.simulate_action(action)
            score, _ = new_game.alpha_beta_search(depth - 1, alpha, beta, True)
            if score < best_score:
                best_score = score
                best_move = action
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return (best_score, best_move)

def find_best_action_alpha_beta(self, player):
    best_score = float('-inf') if player == 'attacker' else float('inf')
    best_move = None
    alpha = float('-inf')
    beta = float('inf')
    for action in self.get_all_possible_actions(player):
        new_game = self.simulate_action(action)
        score, _ = new_game.alpha_beta_search(3, alpha, beta, player == 'attacker') #_: ignore best_move, only store score
        if (player == 'attacker' and score > best_score) or (player == 'defender' and score < best_score):
            best_score = score
            best_move = action
        if player == 'attacker':
            alpha = max(alpha, best_score)
        else:
            beta = min(beta, best_score)
        if beta <= alpha:
            break
    return best_move

def main():
    game = Game()
    over = False
    while not game.game_over():
        game.show_board()
        if game.player.name == 'attacker':
            print(game.player.name)
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
                if action_choice not in ['1', '2', '3', '4', '5']:
                    print("Invalid choice. Please select a valid action from integer 1-5.")
                    continue
                if action_choice == '1':
                    move_list = game.valid_move(unit_pos)
                    if move_list is None:
                        print('Unit Cannot Move')
                        continue
                    else:
                        destination = game.select_unit()
                        if destination not in move_list:
                            print('Invalid Operation')
                            continue
                        else:
                            game.move(unit_pos, destination)
                            break
                if action_choice == '2':
                    attack_list = game.valid_attack(unit_pos)
                    if not attack_list:
                        print('Unit Cannot Attack')
                        continue
                    else:
                        target = game.select_unit()
                        if target not in attack_list:
                            print('Invalid Operation')
                            continue
                        else:
                            game.attack(unit_pos, target)
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
                            break
                if action_choice == '4':
                    game.destruct(unit_pos)
                    game.clear()
                    break
            game.switch_turn()
        else:
            print('AI turn')
            ai_move = game.find_best_action_alpha_beta('attacker')
            print(ai_move)
            game.perform_action(ai_move)
            game.clear()
            game.switch_turn()

