from flask import Flask, render_template, jsonify, request
import random
import time

app = Flask(__name__)

# Game state
board = [""] * 9
player_symbol = "X"
bot_symbol = "O"
current_player = player_symbol

# Check if the game is over
def is_game_over():
    return any(
        (all(board[i] == player_symbol for i in group) or
         all(board[i] == bot_symbol for i in group))
        for group in [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    ) or all(cell != "" for cell in board)


# Bot makes a move
def bot_move():
    available_moves = [i for i, cell in enumerate(board) if cell == ""]
    if available_moves and not is_game_over():
        # Improved bot logic: prioritize winning moves, then blocking the player, and finally random move
        for move in available_moves:
            temp_board = board.copy()
            temp_board[move] = bot_symbol
            if any(all(temp_board[i] == bot_symbol for i in group) for group in [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]):
                board[move] = bot_symbol
                return
        for move in available_moves:
            temp_board = board.copy()
            temp_board[move] = player_symbol
            if any(all(temp_board[i] == player_symbol for i in group) for group in [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]):
                board[move] = bot_symbol
                return
        # If no winning move or blocking move, make a random move
        move = random.choice(available_moves)
        board[move] = bot_symbol

def player_move(position):
    global current_player
    if board[position] == "" and not is_game_over():
        board[position] = player_symbol
        if not is_game_over():
            current_player = bot_symbol
            bot_move()
    return board  # Always return the board

# Restart the game
def restart_game():
    global board, current_player
    board = [""] * 9
    current_player = player_symbol

@app.route("/")
def index():
    return render_template("index.html", board=board, current_player=current_player)

@app.route("/make_move", methods=["POST"])
def make_move():
    position = int(request.json["position"])
    updated_board = player_move(position)  # Update the board and get the updated version
    return jsonify({"board": updated_board, "current_player": current_player, "game_over": is_game_over()})

@app.route("/restart", methods=["POST"])
def restart():
    restart_game()
    return jsonify({"board": board, "current_player": current_player, "game_over": is_game_over()})

if __name__ == "__main__":
    app.run(debug=True)
