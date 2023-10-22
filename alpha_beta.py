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
