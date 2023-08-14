function makeMove(cell) {
    const position = cell.getAttribute("data-position");
    fetch("/make_move", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ position }),
    })
    .then(response => response.json())
    .then(data => {
        updateBoard(data.board);
        updateCurrentPlayer(data.current_player);
        if (data.game_over) {
            showResult();
        }
    });
}

function updateBoard(board) {
    const cells = document.querySelectorAll(".cell");
    for (let i = 0; i < board.length; i++) {
        cells[i].querySelector(".tile").innerText = board[i];
    }
}

function updateCurrentPlayer(currentPlayer) {
    document.querySelector("h3#current_player").innerText = `Current Player: ${currentPlayer}`;
}

function showResult() {
    const resultElement = document.querySelector("h2#result");
    resultElement.innerText = "Game Over";
    setTimeout(restartGame, 3000);  // Restart the game after 5 seconds
}

function restartGame() {
    fetch("/restart", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
    })
    .then(response => response.json())
    .then(data => {
        updateBoard(data.board);
        updateCurrentPlayer(data.current_player);
        hideResult();
    });
}

function hideResult() {
    document.querySelector("h2#result").innerText = "";
}
