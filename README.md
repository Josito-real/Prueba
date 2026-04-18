# Prueba Repository

Este repositorio contiene tres proyectos:

## 🚀 Market Predictor AI

**Una aplicación avanzada de predicción de mercados financieros con Machine Learning y Análisis Técnico**

Aplicación completa para predecir el comportamiento de acciones y criptomonedas usando modelos de Machine Learning (Random Forest, Gradient Boosting) y más de 30 indicadores técnicos.

### Características Principales
- 📊 Análisis técnico completo (RSI, MACD, Bollinger Bands, etc.)
- 🤖 Predicciones con Machine Learning
- 📈 Proyecciones a 7 días
- 💹 Señales de trading automáticas
- 🌐 Interfaz web moderna y responsiva
- 🔄 Datos en tiempo real de Yahoo Finance

### Quick Start
```bash
# Linux/Mac
./start.sh

# Windows
start.bat

# O manualmente
pip install -r requirements.txt
python app.py
```

📖 **[Ver documentación completa](MARKET_PREDICTOR_README.md)**

---

## 🎮 Minesweeper Game

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

## 🗂️ Krill Planner

**Internal project-planning prototype for Krill Energy C.A.** — a department-facing tool for engineers and leadership.

Designed in [Claude Design](https://claude.ai/design) and handed off as an HTML/React prototype. Lives under [`krill_planner/`](krill_planner/).

### Features

- **Command rail** — navy spine of project glyphs that hover-expands into full navigation
- **Today time-strip** — horizontal day timeline with focus, meeting, and review blocks (+ Classic and Focus variants)
- **Roadmap** with quarter lanes, capacity heat band, and dashed cross-project dependency threads
- Project detail (Overview / Tasks / Timeline / Docs / Activity), Kanban, List, Table, Calendar, Capacity, Exec status, Inbox
- **Mobile** companion view in an iOS frame
- **⌘K command palette**
- **Tweaks panel**: accent color (5 presets), density (compact / comfortable / spacious), hero variant (Strip / Classic / Focus), mobile toggle

### Running it

The app loads React 18 and Babel from unpkg and uses relative `./src/*.jsx` scripts, so it **must be served over HTTP** (opening the file directly will hit CORS errors):

```bash
# from the repo root
python3 -m http.server 8000
# then visit http://localhost:8000/krill_planner/
```

Requires internet for CDN fonts and React. State (last view, active project) is persisted in `localStorage` under `krill.view` / `krill.project`.

### Files

- `krill_planner/index.html` — entry point
- `krill_planner/src/` — React components (data, icons, UI primitives, shell, views, mobile, tweaks, app)
- `krill_planner/Krill Planner-print.html` — print-ready landscape version (use "Save as PDF", margins: None, enable Background graphics)
- `krill_planner/design-source/` — original Claude Design handoff README and chat transcript

---

Enjoy the game!
