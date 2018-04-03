// class Board extends Border {
//     constructor() {}
// }
/*
class Board {
    constructor(index, x, y, size) {
        // Parameter variables.
        this.index = index; // Position of the board in the 'games' array.
        this.x = x; // The position of the board on the X-axis.
        this.y = y; // The position of the board on the Y-axis.
        this.size = size; // The size of the board.
        // Rendering Variables.te
        this.pad = this.size * 0.167; // Thickness of the # lines.
        this.w = this.size + this.pad; // The total width of the board.
        this.h = this.w; // The total height of the board.
        this.bounds = { // The edges of the board.
            posX: this.x + (this.w / 2),
            negX: this.x - (this.w / 2),
            posY: this.y + (this.h / 2),
            negY: this.y - (this.h / 2)
        };
        this.swapSymbols = false; // Determines who gets 'X' and who gets 'O'.
        this.col = { // Contains the RGB values comprising the color of the board.
            r: 0,
            g: 0,
            b: 0
        };
        // Tracking variables.
        this.board = []; // Contains the tiles of the board. 
        this.turn = null; // Tracks who's turn it is.
        this.gameOn = false; // Tracks whether the game is idle or active.
        this.gameOver = false; // Tracks if the game has concluded.
        this.result = null; // Tracks the result of a concluded game.
        this.maxDepth = 15; // Limits the size of the search tree.
        this.blunder; // Chance that the computer has to make a mistake.
    }

    // Sets up the game board.
    initialize() {
        // Set turn by coin toss.
        if (random(1) > 0.5) {
            this.turn = human;
        } else {
            this.turn = computer;
        }
        // Choose symbols by coin toss.
        if (random(1) > 0.5) {
            this.swapSymbols = true;
        }
        // Set intelligence of computer AI.
        this.blunder = random(0.001, 0.15);
        // Create board.
        for (let i = 0; i < 9; i++) {
            // Find x in terms of i, this.w, and this.pad.
            let mx = i % 3;
            let x = ((this.w - this.pad) / 6 + mx * ((this.w - this.pad) / 3 + this.pad / 2)) + (this.x - this.w / 2);
            // Find y in terms of i, this.h, and this.pad
            let my1 = (i % 9) / 3;
            let my2 = my1 % 1;
            let my3;
            if (my2 == 0) {
                my3 = my1 * ((this.h - this.pad) / 3 + this.pad / 2);
            }
            let y = ((this.h - this.pad) / 6 + my3) + (this.y - this.h / 2);
            // Initialize tiles.
            this.board[i] = new Tile(i, games[this.index], x, y);
            this.board[i].setSymbol();
        }
        // First computer move is random.
        if (this.turn == computer) {
            this.randomMove(true);
        }
    };

    // Displays the game board.
    show() {
        // Setup
        this.col = this.setColor();
        noStroke();
        fill(this.col.r, this.col.g, this.col.b);
        // Show game board.
        rect(this.x, this.y, this.w, this.h);
        for (let i = 0; i < this.board.length; i++) {
            this.board[i].show(this.col);
        }
        // Computer's move.
        if (!this.gameOver && this.turn == computer) {
            if (random(1) > this.blunder) {
                this.minimax();
            } else {
                this.randomMove();
            }
        }
        // Show result of game.
        if (this.gameOver) {
            this.endGame();
        }
    };

    // Changes color of the board based on the game's progress.
    setColor() {
        // Game is waiting.
        if (this.gameOn == false) {
            this.col.r = 150;
            this.col.g = 150;
            this.col.b = 150;
        }
        // Game is being played.
        if (this.gameOn == true && this.gameOver == false) {
            this.col.r = 0;
            this.col.g = 0;
            this.col.b = 0;
        }
        // Game is over.
        if (this.gameOver) {
            if (this.result == 'win') {
                this.col.r = 0;
                this.col.g = 120;
                this.col.b = 0;
            }
            if (this.result == 'loss') {
                this.col.r = 170;
                this.col.g = 0;
                this.col.b = 0;
            }
            if (this.result == 'draw') {
                this.col.r = 0;
                this.col.g = 0;
                this.col.b = 170;
            }
        }
        return this.col;
    };

    // Invoke computer AI
    minimax() {
        this.board[this.compValue(this.board)].state = computer;
        this.switchTurn();
    };

    // Blundered Move.
    randomMove(first = false) {
        let emptyTiles = this.getEmptyTiles(this.board);
        let randomIndex = floor(random(0, emptyTiles.length));
        let randomTile = emptyTiles[randomIndex];
        this.board[randomTile].state = computer;
        if (first) {
            this.turn = human
        } else {
            this.switchTurn();
        }
    };

    // Draws the appropriate line if a player meets the win condition.
    endGame() {
        let winIndex = this.checkForWin(this.board, false, returnIndex = true);
        stroke(this.col.r - 40, this.col.g - 40, this.col.b - 40);
        let lineThickness = map(this.size, 25, 200, 1, 5);
        strokeWeight(lineThickness);
        switch (winIndex) {
            case 0:
                line(this.bounds.negX, this.board[0].y, this.bounds.posX, this.board[2].y);
                break;
            case 1:
                line(this.bounds.negX, this.board[3].y, this.bounds.posX, this.board[5].y);
                break;
            case 2:
                line(this.bounds.negX, this.board[6].y, this.bounds.posX, this.board[8].y);
                break;
            case 3:
                line(this.board[0].x, this.bounds.negY, this.board[6].x, this.bounds.posY);
                break;
            case 4:
                line(this.board[1].x, this.bounds.negY, this.board[7].x, this.bounds.posY);
                break;
            case 5:
                line(this.board[2].x, this.bounds.negY, this.board[8].x, this.bounds.posY);
                break;
            case 6:
                line(this.bounds.negX, this.bounds.negY, this.bounds.posX, this.bounds.posY);
                break;
            case 7:
                line(this.bounds.posX, this.bounds.negY, this.bounds.negX, this.bounds.posY);
                break;
        }
    };

    // Builds the search tree required to find the most optimal move.
    compValue(node, depth = 0, a = -999, b = 999, first = true) {
        let emptyTiles = this.getEmptyTiles(node);
        let winner = this.checkForWin(node, returnPlayer = true);
        // If the node is terminal, return the score for the node.
        let terminal = this.isTerminalNode(depth, emptyTiles, winner);
        if (typeof terminal == 'number') {
            return terminal;
        }
        // If the node is NOT terminal, create a child node and continue evaluating the search tree.
        let maxValue = -999;
        let index = null;
        for (let i = 0; i < emptyTiles.length; i++) {
            let childNode = this.createChildNode(node, emptyTiles[i], computer);
            let value = this.humanValue(childNode, depth++, a, b);
            if (value > maxValue) {
                maxValue = value;
                index = emptyTiles[i];
            }
            // Do not search through unecessary branches of the search tree.
            if (value > a) {
                a = value;
            }
            if (a >= b) {
                if (first) {
                    return index;
                } else {
                    return a;
                }
            }
        }
        // If this is the root of the search tree, return an index instead of a score.
        if (first) {
            return index;
        } else {
            return maxValue;
        }
    };

    // This function is run between each move.
    switchTurn() {
        // Checks if the game has concluded.
        let emptyTiles = this.getEmptyTiles(this.board);
        let winner = this.checkForWin(this.board, returnPlayer = true);
        if (typeof winner == 'number') {
            this.gameOver = true;
            if (winner == human) {
                this.result = 'win';
            }
            if (winner == computer) {
                this.result = 'loss';
            }
        } else if (emptyTiles.length == 0) {
            this.gameOver = true;
            this.result = 'draw';
        } else {
            // If no conclusion is found, switch the turn.
            this.turn *= -1;
        }
        // Essentially runs the "this.show()" function.
        redraw();
    };

    // Returns an array of the indices of all empty tiles.
    getEmptyTiles(onBoard) {
        let emptyTiles = [];
        for (let i = 0; i < onBoard.length; i++) {
            if (typeof onBoard[i] == 'number' && onBoard[i] == empty) {
                emptyTiles.push(i);
            } else if (typeof onBoard[i] == 'object' && onBoard[i].state == empty) {
                emptyTiles.push(onBoard[i].index);
            }
        }
        return emptyTiles;
    };

    // Evaluates the given game board and determines if anyone has won. 
    checkForWin(onBoard = board, returnPlayer = false, returnIndex = false) {
        let space1, space2, space3;
        for (let i = 0; i < winConditions.length; i++) {
            if (typeof onBoard[i] == "object") {
                space1 = onBoard[winConditions[i][0]].state;
                space2 = onBoard[winConditions[i][1]].state;
                space3 = onBoard[winConditions[i][2]].state;
            } else if (typeof onBoard[i] == "number") {
                space1 = onBoard[winConditions[i][0]];
                space2 = onBoard[winConditions[i][1]];
                space3 = onBoard[winConditions[i][2]];
            }
            if (space1 == space2 && space2 == space3 && space3 != empty) {
                if (returnPlayer) {
                    return space1;
                } else if (returnIndex) {
                    return i;
                } else {
                    return true;
                }
            }
        }
        return false;
    };

    // Checks to see if a node in the search tree is terminal. Returns a score for terminal nodes.
    isTerminalNode(depth, emptyTiles, winner) {
        if (depth > this.maxDepth || emptyTiles.length == 0 || typeof winner == "number") {
            if (emptyTiles.length == 0 && typeof winner != "number") {
                return 0;
            }
            if (typeof winner == "number") {
                return (10 - depth) * winner;
            }
        }
        return false;
    };

    // Creates a new node in the search tree.
    createChildNode(parentNode, emptyTileIndex, thisTurn) {
        let childNode = [];
        for (let i = 0; i < parentNode.length; i++) {
            if (typeof parentNode[i] == "object") {
                childNode.push(parentNode[i].state);
            } else if (typeof parentNode[i] == "number") {
                childNode.push(parentNode[i]);
            }
        }
        childNode[emptyTileIndex] = thisTurn;
        return childNode;
    };

    // Also builds the search tree required to find the most optimal move.
    humanValue(node, depth = 0, a, b) {
        let emptyTiles = this.getEmptyTiles(node);
        let winner = this.checkForWin(node, returnPlayer = true);
        // If the node is terminal, return the score for the node.
        let terminal = this.isTerminalNode(depth, emptyTiles, winner);
        if (typeof terminal == 'number') {
            return terminal;
        }
        // If the node is NOT terminal, create a child node and continue evaluating the search tree.
        let minValue = 999;
        for (let i = 0; i < emptyTiles.length; i++) {
            let childNode = this.createChildNode(node, emptyTiles[i], human);
            let value = this.compValue(childNode, depth++, a, b, false);
            if (value < minValue) {
                minValue = value;
            }
            // Do not search through unnecessary branches of the search tree. 
            if (value < b) {
                b = value;
            }
            if (a >= b) {
                return b;
            }
        }
        return minValue;
    };

    // Dictates the behavior of the board when it is clicked by the human player.
    clicked() {
        if (!this.gameOver) {
            if (mouseX < this.bounds.posX &&
                mouseX > this.bounds.negX &&
                mouseY < this.bounds.posY &&
                mouseY > this.bounds.negY) {
                // Changes the color of an inactive board.
                if (this.gameOn == false) {
                    this.gameOn = true;
                }
                // Tells the game tiles that the board has been clicked.
                for (let i = 0; i < this.board.length; i++) {
                    this.board[i].clicked();
                }
            }
        }
    };
}
*/