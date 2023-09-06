import pytest
from app import (app, board, player_symbol, bot_symbol,
                 current_player, is_game_over, bot_move,
                 player_move, restart_game)


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Tic Tac Toe' in response.data


def test_make_move(client):
    position = 0
    response = client.post('/make_move', json={'position': position})
    assert response.status_code == 200
    data = response.get_json()
    assert 'board' in data
    assert 'current_player' in data
    assert 'game_over' in data
    assert data['board'][position] == player_symbol
    assert (data['current_player'] == bot_symbol or
            data['current_player'] == player_symbol)

    assert isinstance(data['game_over'], bool)


def test_restart(client):
    response = client.post('/restart')
    assert response.status_code == 200
    data = response.get_json()
    assert 'board' in data
    assert 'current_player' in data
    assert 'game_over' in data
    assert data['board'] == [""] * 9
    assert data['current_player'] == player_symbol
    assert isinstance(data['game_over'], bool)


def test_is_game_over():
    # Test when the game is not over
    assert not is_game_over()


def test_bot_move():
    # Test when there are no available moves
    board[0] = board[1] = board[2] = player_symbol
    board[3] = board[4] = board[5] = bot_symbol
    board[6] = board[7] = board[8] = player_symbol
    bot_move()
    assert all(cell != "" for cell in board)


def test_player_move():
    position = 0
    updated_board = player_move(position)
    assert updated_board[position] == player_symbol
    assert current_player == bot_symbol or current_player == player_symbol

    # Test when the position is already occupied
    position = 0
    board[position] = player_symbol
    updated_board = player_move(position)
    assert updated_board[position] == player_symbol


def test_restart_game():
    # Set up the initial game state
    board = ["", "", "", "", "", "", "", "", #""]

    # Call the restart_game() function
    restart_game()

    # Check if the board is reset
    assert board == ["", "", "", "", "", "", "", "", ""]
