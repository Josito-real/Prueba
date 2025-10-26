# Minesweeper Game

A classic Minesweeper game built with HTML, CSS, and JavaScript. Play the timeless puzzle game right in your browser!

## Features

- Three difficulty levels:
  - **Easy**: 9x9 grid with 10 mines
  - **Medium**: 16x16 grid with 40 mines
  - **Hard**: 16x30 grid with 99 mines
- Timer to track your solving speed
- Mine counter showing remaining unflagged mines
- Flag system to mark suspected mines
- Automatic cell revealing for empty areas
- Win/lose detection
- Restart functionality
- Responsive design
- Clean, modern UI

## How to Play

1. **Start the Game**: Open `index.html` in any modern web browser

2. **Basic Rules**:
   - Left-click on a cell to reveal it
   - Right-click on a cell to place/remove a flag
   - Numbers indicate how many mines are adjacent to that cell
   - The goal is to reveal all non-mine cells without clicking on any mines

3. **Game Controls**:
   - Select your difficulty level (Easy, Medium, or Hard)
   - Click "New Game" to restart at any time
   - The timer starts when you click your first cell

4. **Tips**:
   - Start by clicking on cells in corners or edges
   - Use flags to mark cells you're certain contain mines
   - Use the number clues to deduce mine locations
   - If you reveal a cell with 0 adjacent mines, all neighboring cells are automatically revealed

## Installation

No installation required! Simply:

1. Clone or download this repository
2. Open `index.html` in your web browser
3. Start playing!

## Files

- `index.html` - Main HTML structure
- `style.css` - Game styling and visual design
- `script.js` - Game logic and functionality
- `README.md` - This file

## Game Logic

The game implements the following features:

- **Mine Generation**: Mines are randomly placed after the first click to ensure you never hit a mine on your first move
- **Safe First Click**: The first click and its adjacent cells are guaranteed to be mine-free
- **Flood Fill**: When revealing a cell with no adjacent mines, all connected safe cells are automatically revealed
- **Win Condition**: Reveal all non-mine cells to win
- **Lose Condition**: Click on a mine to lose

## Browser Compatibility

This game works on all modern browsers including:
- Chrome
- Firefox
- Safari
- Edge
- Opera

## Technologies Used

- HTML5
- CSS3 (with Flexbox and Grid)
- Vanilla JavaScript (ES6+)

## License

Feel free to use and modify this code for your own projects!

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

---

Enjoy the game!
