import pytest
from app import app, board, is_game_over, player_move, restart_game

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_initial_board_state():
    assert len(board) == 9
    assert all(cell == "" for cell in board)

def test_is_game_over_empty_board():
    restart_game()
    assert not is_game_over()

def test_player_move_and_is_game_over(client):
    restart_game()

    # Player makes a move
    response = client.post('/make_move', json={'position': 0})
    data = response.get_json()
    assert data['board'][0] == "X"
    assert data['current_player'] == "O"
    assert not data['game_over']

    # Bot makes a move (we don't know the exact cell, so we just check that the board is updated)
    response = client.post('/make_move', json={'position': 1})
    data = response.get_json()
    assert data['current_player'] == "O"  # The bot's move changes the current player to "O"
    assert not data['game_over']
    assert "O" in data['board']  # Check that the board has been updated with the bot's move

    # Player makes another move (we continue the game to check game over conditions)
    response = client.post('/make_move', json={'position': 2})
    data = response.get_json()
    assert data['board'][2] == "X"
    assert data['current_player'] == "O"
    assert not data['game_over']

    # Continue with additional moves if needed
    # ...

    # Eventually, the game will be over, and we can check for the game over condition
    assert data['game_over']



def test_restart_game(client):
    restart_game()

    # Player makes a move
    response = client.post('/make_move', json={'position': 0})
    data = response.get_json()
    assert data['board'][0] == "X"

    # Restart the game
    response = client.post('/restart')
    data = response.get_json()
    assert all(cell == "" for cell in data['board'])
    assert data['current_player'] == "X"
    assert not data['game_over']
