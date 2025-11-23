# 🚀 Market Predictor AI

Una aplicación avanzada de predicción de mercados financieros que utiliza **Machine Learning** y **Análisis Técnico** para generar predicciones sobre acciones y criptomonedas.

![Market Predictor AI](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Características

- 📊 **Análisis Técnico Completo**: RSI, MACD, Bollinger Bands, Moving Averages y más
- 🤖 **Machine Learning**: Modelos Random Forest y Gradient Boosting para predicciones precisas
- 📈 **Predicciones a 7 Días**: Proyecciones de precios futuros basadas en datos históricos
- 💹 **Señales de Trading**: Recomendaciones automáticas (STRONG BUY, BUY, HOLD, SELL, STRONG SELL)
- 🔄 **Datos en Tiempo Real**: Integración con Yahoo Finance para datos actualizados
- 🌐 **Interfaz Moderna**: UI responsiva y atractiva con visualizaciones interactivas
- 📉 **Comparación de Símbolos**: Compara múltiples acciones o criptomonedas
- 🎯 **Alta Precisión**: Modelos entrenados con validación cruzada

## 🛠️ Tecnologías Utilizadas

### Backend
- **Python 3.8+**
- **Flask**: Framework web para API REST
- **pandas & numpy**: Manipulación y análisis de datos
- **scikit-learn**: Modelos de Machine Learning
- **yfinance**: Obtención de datos de mercado
- **ta (Technical Analysis)**: Indicadores técnicos
- **Prophet**: Predicción de series temporales

### Frontend
- **HTML5 & CSS3**: Interfaz moderna y responsiva
- **JavaScript (Vanilla)**: Lógica de aplicación sin dependencias
- **Chart.js**: Visualizaciones interactivas de datos

## 📦 Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Paso 1: Clonar el Repositorio
```bash
git clone <repository-url>
cd Prueba
```

### Paso 2: Crear Entorno Virtual (Recomendado)
```bash
python -m venv venv

# En Windows
venv\Scripts\activate

# En Linux/Mac
source venv/bin/activate
```

### Paso 3: Instalar Dependencias
```bash
pip install -r requirements.txt
```

### Paso 4: Configurar Variables de Entorno (Opcional)
```bash
cp .env.example .env
# Edita .env según tus necesidades
```

## 🚀 Uso

### Iniciar el Servidor
```bash
python app.py
```

El servidor se iniciará en `http://localhost:5000`

### Acceder a la Aplicación
Abre tu navegador y ve a:
```
http://localhost:5000
```

## 📖 Documentación de la API

### Endpoints Disponibles

#### 1. Obtener Símbolos Populares
```http
GET /api/symbols
```

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "stocks": [...],
    "crypto": [...]
  }
}
```

#### 2. Analizar un Símbolo
```http
GET /api/analyze/<symbol>?period=6mo
```

**Parámetros:**
- `symbol`: Símbolo a analizar (ej: AAPL, BTC-USD)
- `period`: Período de datos (1mo, 3mo, 6mo, 1y, 2y, 5y)

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "symbol": "AAPL",
    "current_price": 150.25,
    "change_percent": 2.5,
    "predictions": {
      "next_7_days": [151.2, 152.5, ...],
      "trend": "BULLISH"
    },
    "signals": {
      "recommendation": "BUY",
      "confidence": 75,
      "indicators": {...}
    },
    "model_accuracy": {
      "train_score": 0.95,
      "test_score": 0.87
    },
    "historical_data": {...},
    "statistics": {...}
  }
}
```

#### 3. Análisis Rápido de Múltiples Símbolos
```http
POST /api/quick-analysis
Content-Type: application/json

{
  "symbols": ["AAPL", "MSFT", "BTC-USD"]
}
```

#### 4. Comparar Símbolos
```http
POST /api/compare
Content-Type: application/json

{
  "symbols": ["AAPL", "MSFT", "GOOGL"]
}
```

#### 5. Health Check
```http
GET /api/health
```

## 🎯 Funcionalidades Principales

### 1. Dashboard
- Vista general de símbolos populares
- Estadísticas en tiempo real
- Acceso rápido a análisis

### 2. Análisis Detallado
- Indicadores técnicos completos
- Predicciones a 7 días
- Gráficos interactivos
- Recomendaciones de trading
- Estadísticas históricas

### 3. Comparación
- Compara hasta 5 símbolos simultáneamente
- Tabla comparativa con métricas clave
- Predicciones y recomendaciones lado a lado

## 🔍 Indicadores Técnicos Incluidos

- **RSI (Relative Strength Index)**: Detecta sobrecompra/sobreventa
- **MACD (Moving Average Convergence Divergence)**: Identifica cambios de tendencia
- **Bollinger Bands**: Mide volatilidad y niveles de precio
- **Moving Averages (7, 14, 30 días)**: Identifica tendencias
- **Volumen**: Confirma movimientos de precio
- **Volatilidad**: Mide riesgo del activo

## 🤖 Modelos de Machine Learning

### Random Forest Regressor
- 100 árboles de decisión
- Profundidad máxima: 10
- Características: Indicadores técnicos + precios históricos

### Gradient Boosting Regressor
- 100 estimadores
- Tasa de aprendizaje: 0.1
- Optimizado para series temporales financieras

### Preparación de Datos
- Normalización con MinMaxScaler
- Look-back window de 10 días
- Train/Test split: 80/20
- Validación temporal (no aleatoria)

## 📊 Precisión del Modelo

Los modelos típicamente logran:
- **Train Score**: 85-95%
- **Test Score**: 70-90%

*Nota: La precisión varía según el símbolo y la volatilidad del mercado.*

## ⚠️ Advertencias Importantes

1. **No es Asesoramiento Financiero**: Esta aplicación es solo para fines educativos e informativos.
2. **Riesgo de Inversión**: Los mercados financieros son volátiles. Nunca inviertas más de lo que puedas permitirte perder.
3. **Datos Históricos**: Las predicciones se basan en datos históricos y no garantizan resultados futuros.
4. **Decisiones Propias**: Siempre realiza tu propia investigación antes de tomar decisiones de inversión.

## 🐛 Solución de Problemas

### Error: "Insufficient data for analysis"
- El símbolo puede no estar disponible en Yahoo Finance
- Intenta con un período de datos más largo
- Verifica que el símbolo esté correctamente escrito

### Error de Conexión
- Asegúrate de que el servidor Flask esté ejecutándose
- Verifica que el puerto 5000 esté disponible
- Revisa la configuración de CORS si accedes desde otro dominio

### Errores de Instalación
```bash
# Si tienes problemas con Prophet
pip install pystan==2.19.1.1
pip install prophet

# Si tienes problemas con ta-lib
# En Ubuntu/Debian:
sudo apt-get install ta-lib
pip install TA-Lib
```

## 🔄 Actualizaciones Futuras

- [ ] Integración con más fuentes de datos (Alpha Vantage, CoinGecko)
- [ ] Modelos LSTM y GRU para series temporales
- [ ] Sistema de alertas por email/SMS
- [ ] Análisis de sentimiento de noticias
- [ ] Portafolio tracking
- [ ] Backtesting de estrategias
- [ ] Modo oscuro

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

Creado con ❤️ usando Claude Code

## 🙏 Agradecimientos

- Yahoo Finance por proporcionar datos de mercado gratuitos
- La comunidad de código abierto por las increíbles bibliotecas
- Todos los contribuidores y usuarios

---

**⚠️ Disclaimer**: Esta herramienta es solo para fines educativos. No proporciona asesoramiento financiero. Siempre consulta con un profesional financiero antes de tomar decisiones de inversión.

**🌟 Si te gusta este proyecto, dale una estrella en GitHub!**
