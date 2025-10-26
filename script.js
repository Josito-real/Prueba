class Minesweeper {
    constructor() {
        this.difficulties = {
            easy: { rows: 9, cols: 9, mines: 10 },
            medium: { rows: 16, cols: 16, mines: 40 },
            hard: { rows: 16, cols: 30, mines: 99 }
        };

        this.currentDifficulty = 'easy';
        this.board = [];
        this.revealedCount = 0;
        this.flaggedCount = 0;
        this.gameOver = false;
        this.gameStarted = false;
        this.timer = 0;
        this.timerInterval = null;

        this.initializeEventListeners();
        this.initializeGame();
    }

    initializeEventListeners() {
        document.getElementById('easy').addEventListener('click', () => this.changeDifficulty('easy'));
        document.getElementById('medium').addEventListener('click', () => this.changeDifficulty('medium'));
        document.getElementById('hard').addEventListener('click', () => this.changeDifficulty('hard'));
        document.getElementById('restart').addEventListener('click', () => this.initializeGame());
    }

    changeDifficulty(difficulty) {
        this.currentDifficulty = difficulty;

        // Update button states
        document.querySelectorAll('.diff-btn').forEach(btn => btn.classList.remove('active'));
        document.getElementById(difficulty).classList.add('active');

        this.initializeGame();
    }

    initializeGame() {
        const config = this.difficulties[this.currentDifficulty];
        this.rows = config.rows;
        this.cols = config.cols;
        this.totalMines = config.mines;
        this.revealedCount = 0;
        this.flaggedCount = 0;
        this.gameOver = false;
        this.gameStarted = false;
        this.timer = 0;

        clearInterval(this.timerInterval);
        this.updateTimer();
        this.updateMinesCount();

        this.createBoard();
        this.renderBoard();
        this.hideMessage();
    }

    createBoard() {
        this.board = [];
        for (let row = 0; row < this.rows; row++) {
            this.board[row] = [];
            for (let col = 0; col < this.cols; col++) {
                this.board[row][col] = {
                    isMine: false,
                    isRevealed: false,
                    isFlagged: false,
                    neighborMines: 0
                };
            }
        }
    }

    placeMines(firstClickRow, firstClickCol) {
        let minesPlaced = 0;

        while (minesPlaced < this.totalMines) {
            const row = Math.floor(Math.random() * this.rows);
            const col = Math.floor(Math.random() * this.cols);

            // Don't place mine on first click or adjacent cells
            const isFirstClick = row === firstClickRow && col === firstClickCol;
            const isAdjacent = Math.abs(row - firstClickRow) <= 1 &&
                              Math.abs(col - firstClickCol) <= 1;

            if (!this.board[row][col].isMine && !isFirstClick && !isAdjacent) {
                this.board[row][col].isMine = true;
                minesPlaced++;
            }
        }

        this.calculateNeighborMines();
    }

    calculateNeighborMines() {
        for (let row = 0; row < this.rows; row++) {
            for (let col = 0; col < this.cols; col++) {
                if (!this.board[row][col].isMine) {
                    let count = 0;
                    this.getNeighbors(row, col).forEach(([r, c]) => {
                        if (this.board[r][c].isMine) count++;
                    });
                    this.board[row][col].neighborMines = count;
                }
            }
        }
    }

    getNeighbors(row, col) {
        const neighbors = [];
        for (let r = row - 1; r <= row + 1; r++) {
            for (let c = col - 1; c <= col + 1; c++) {
                if (r >= 0 && r < this.rows && c >= 0 && c < this.cols && !(r === row && c === col)) {
                    neighbors.push([r, c]);
                }
            }
        }
        return neighbors;
    }

    renderBoard() {
        const gameBoard = document.getElementById('game-board');
        gameBoard.innerHTML = '';
        gameBoard.style.gridTemplateColumns = `repeat(${this.cols}, 30px)`;

        for (let row = 0; row < this.rows; row++) {
            for (let col = 0; col < this.cols; col++) {
                const cell = document.createElement('div');
                cell.className = 'cell';
                cell.dataset.row = row;
                cell.dataset.col = col;

                cell.addEventListener('click', () => this.handleCellClick(row, col));
                cell.addEventListener('contextmenu', (e) => {
                    e.preventDefault();
                    this.handleCellRightClick(row, col);
                });

                gameBoard.appendChild(cell);
            }
        }
    }

    handleCellClick(row, col) {
        if (this.gameOver || this.board[row][col].isRevealed || this.board[row][col].isFlagged) {
            return;
        }

        if (!this.gameStarted) {
            this.gameStarted = true;
            this.placeMines(row, col);
            this.startTimer();
        }

        this.revealCell(row, col);
    }

    handleCellRightClick(row, col) {
        if (this.gameOver || this.board[row][col].isRevealed) {
            return;
        }

        const cell = this.board[row][col];
        cell.isFlagged = !cell.isFlagged;

        if (cell.isFlagged) {
            this.flaggedCount++;
        } else {
            this.flaggedCount--;
        }

        this.updateMinesCount();
        this.updateCell(row, col);
        this.checkWin();
    }

    revealCell(row, col) {
        const cell = this.board[row][col];

        if (cell.isRevealed || cell.isFlagged) {
            return;
        }

        cell.isRevealed = true;
        this.revealedCount++;
        this.updateCell(row, col);

        if (cell.isMine) {
            this.gameOver = true;
            this.revealAllMines();
            this.endGame(false);
            return;
        }

        if (cell.neighborMines === 0) {
            this.getNeighbors(row, col).forEach(([r, c]) => {
                this.revealCell(r, c);
            });
        }

        this.checkWin();
    }

    updateCell(row, col) {
        const cell = this.board[row][col];
        const cellElement = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);

        cellElement.className = 'cell';

        if (cell.isFlagged) {
            cellElement.classList.add('flagged');
        } else if (cell.isRevealed) {
            cellElement.classList.add('revealed');

            if (cell.isMine) {
                cellElement.classList.add('mine');
            } else if (cell.neighborMines > 0) {
                cellElement.classList.add(`number-${cell.neighborMines}`);
                cellElement.textContent = cell.neighborMines;
            }
        }
    }

    revealAllMines() {
        for (let row = 0; row < this.rows; row++) {
            for (let col = 0; col < this.cols; col++) {
                if (this.board[row][col].isMine) {
                    this.board[row][col].isRevealed = true;
                    this.updateCell(row, col);
                }
            }
        }
    }

    checkWin() {
        const totalCells = this.rows * this.cols;
        const nonMineCells = totalCells - this.totalMines;

        if (this.revealedCount === nonMineCells) {
            this.gameOver = true;
            this.endGame(true);
        }
    }

    endGame(won) {
        clearInterval(this.timerInterval);

        const message = document.getElementById('game-message');
        message.classList.remove('hidden', 'win', 'lose');

        if (won) {
            message.classList.add('win');
            message.textContent = `Congratulations! You won in ${this.timer} seconds!`;
        } else {
            message.classList.add('lose');
            message.textContent = 'Game Over! You hit a mine!';
        }
    }

    hideMessage() {
        const message = document.getElementById('game-message');
        message.classList.add('hidden');
    }

    startTimer() {
        this.timerInterval = setInterval(() => {
            this.timer++;
            this.updateTimer();
        }, 1000);
    }

    updateTimer() {
        const timerElement = document.getElementById('timer');
        timerElement.textContent = String(this.timer).padStart(3, '0');
    }

    updateMinesCount() {
        const minesElement = document.getElementById('mines-count');
        const remainingMines = this.totalMines - this.flaggedCount;
        minesElement.textContent = remainingMines;
    }
}

// Initialize the game when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new Minesweeper();
});
