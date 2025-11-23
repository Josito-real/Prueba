#!/bin/bash

# Market Predictor AI - Quick Start Script

echo "╔══════════════════════════════════════════════╗"
echo "║      Market Predictor AI - Quick Start       ║"
echo "╚══════════════════════════════════════════════╝"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Install dependencies
echo "📥 Instalando dependencias..."
pip install -q -r requirements.txt

# Create .env if not exists
if [ ! -f ".env" ]; then
    echo "⚙️  Creando archivo .env..."
    cp .env.example .env
fi

# Start the application
echo ""
echo "🚀 Iniciando Market Predictor AI..."
echo "📍 La aplicación estará disponible en: http://localhost:5000"
echo ""
python app.py
