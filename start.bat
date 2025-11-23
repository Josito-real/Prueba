@echo off
REM Market Predictor AI - Quick Start Script for Windows

echo ╔══════════════════════════════════════════════╗
echo ║      Market Predictor AI - Quick Start       ║
echo ╚══════════════════════════════════════════════╝
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creando entorno virtual...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activando entorno virtual...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Instalando dependencias...
pip install -q -r requirements.txt

REM Create .env if not exists
if not exist ".env" (
    echo ⚙️  Creando archivo .env...
    copy .env.example .env
)

REM Start the application
echo.
echo 🚀 Iniciando Market Predictor AI...
echo 📍 La aplicación estará disponible en: http://localhost:5000
echo.
python app.py
