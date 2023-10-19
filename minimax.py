import math

# The initial state of the game
board = [' ' for _ in range(9)]  # A list of empty spaces

# Function to print the Tic Tac Toe board
def print_board():
    for i in range(3):
        print(board[i * 3:(i + 1) * 3])
    print()

# Function to check if a player has won
def winning(board, player):
    # Possible winning combinations
    win_cond = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # horizontal wins
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # vertical wins
        [0, 4, 8], [2, 4, 6]              # diagonal wins
    ]
    return any(all(board[pos] == player for pos in combination) for combination in win_cond)

# Function to check if the game is over (won or tied)
def game_over(board):
    return winning(board, 'X') or winning(board, 'O') or ' ' not in board

# The Minimax algorithm, returning the best score for the current board state
def minimax(board, depth, is_maximizing):
    if winning(board, 'X'):
        return -1
    if winning(board, 'O'):
        return 1
    if game_over(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'  # The AI's move
                score = minimax(board, depth + 1, False)
                board[i] = ' '  # Reset to empty space after trying
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'  # The human's move
                score = minimax(board, depth + 1, True)
                board[i] = ' '  # Reset to empty space after trying
                best_score = min(score, best_score)
        return best_score

# Find the best move for the AI by running the Minimax algorithm
def find_best_move(board):
    best_score = -math.inf
    move = -1
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'  # Try playing here
            score = minimax(board, 0, False)
            board[i] = ' '  # Reset after trying
            if score > best_score:
                best_score = score
                move = i
    return move

# Main game loop
def main():
    current_player = 'X'  # Human player goes first

    while not game_over(board):
        print_board()
        if current_player == 'X':
            # Human player's turn
            move_position = int(input("Enter your move (1-9): ")) - 1
            if board[move_position] == ' ':
                board[move_position] = 'X'
                current_player = 'O'
            else:
                print("Invalid move! Try again.")
        else:
            # AI's turn
            print("AI is making a move...")
            ai_move = find_best_move(board)
            board[ai_move] = 'O'
            current_player = 'X'

    # Game over
    print_board()
    if winning(board, 'X'):
        print("You win!")
    elif winning(board, 'O'):
        print("AI wins!")
    else:
        print("It's a tie!")

# Run the game
if __name__ == "__main__":
    main()
