# 🔧 Guía de Solución de Problemas

## Problemas de Conexión con Datos de Mercado

### 1. Test de Conectividad

Antes de instalar las dependencias completas, prueba la conexión:

```bash
python test_connection.py
```

Este script verificará:
- ✅ Conexión a internet
- ✅ Acceso a Yahoo Finance
- ✅ Capacidad de obtener datos de mercado

### 2. Errores Comunes y Soluciones

#### Error: "No module named 'pandas'"
**Causa**: Dependencias no instaladas

**Solución**:
```bash
pip install -r requirements.txt
```

#### Error: "Insufficient data for analysis"
**Causas posibles**:
- Símbolo incorrecto o no disponible
- Problemas de conectividad
- Yahoo Finance temporalmente no disponible

**Soluciones**:
1. Verifica que el símbolo esté correctamente escrito
   - Acciones: AAPL, MSFT, GOOGL
   - Criptomonedas: BTC-USD, ETH-USD (nota el sufijo -USD)

2. Prueba con un período de datos más largo:
   ```
   period='1y' en lugar de period='1mo'
   ```

3. Verifica tu conexión:
   ```bash
   python test_connection.py
   ```

#### Error: "Failed to fetch data after 3 attempts"
**Causas posibles**:
- Rate limiting de Yahoo Finance
- Firewall o proxy bloqueando el acceso
- DNS issues

**Soluciones**:

1. **Espera y reintenta**: Yahoo Finance tiene rate limits
   ```
   Espera 1-2 minutos entre solicitudes masivas
   ```

2. **Configura un proxy** (si estás detrás de un firewall corporativo):
   ```bash
   export HTTP_PROXY="http://proxy.example.com:8080"
   export HTTPS_PROXY="http://proxy.example.com:8080"
   ```

3. **Usa VPN**: Si Yahoo Finance está bloqueado en tu región

4. **Verifica DNS**:
   ```bash
   ping finance.yahoo.com
   nslookup finance.yahoo.com
   ```

#### Error: "SSL Certificate Verification Failed"
**Causa**: Problemas con certificados SSL

**Solución**:
```bash
pip install --upgrade certifi
pip install --upgrade urllib3
```

#### Error: "Connection timeout"
**Causa**: Red lenta o inestable

**Solución**: El código ya incluye reintentos automáticos con backoff exponencial, pero puedes:
- Aumentar el timeout en el código
- Verificar tu velocidad de internet
- Usar una conexión más estable

### 3. Mejoras de Robustez Implementadas

La versión mejorada incluye:

✅ **Sistema de Reintentos**: 3 intentos con backoff exponencial (1s, 2s, 4s)
✅ **Caché de Datos**: 5 minutos de caché para reducir llamadas API
✅ **Logging Detallado**: Mensajes informativos sobre el estado de la conexión
✅ **Validación de Datos**: Verifica la integridad de los datos recibidos
✅ **Manejo de Errores Robusto**: Continúa funcionando incluso con errores parciales
✅ **Session Reutilizable**: Mejor rendimiento con conexiones persistentes

### 4. Verificar Logs

Los logs te dirán exactamente qué está pasando:

```python
# Los logs se muestran automáticamente en la consola
# Busca mensajes como:
# INFO - Fetching data for AAPL (attempt 1/3)
# INFO - Successfully fetched 126 data points for AAPL
# ERROR - Failed to fetch data for XYZ after 3 attempts
```

### 5. Símbolos Recomendados para Pruebas

**Acciones que funcionan bien**:
- AAPL (Apple)
- MSFT (Microsoft)
- GOOGL (Google)
- TSLA (Tesla)
- AMZN (Amazon)

**Criptomonedas que funcionan bien**:
- BTC-USD (Bitcoin)
- ETH-USD (Ethereum)
- BNB-USD (Binance Coin)

**Evitar**:
- Símbolos de mercados cerrados o poco líquidos
- Símbolos de empresas muy pequeñas
- Criptomonedas poco conocidas

### 6. Alternativas si Yahoo Finance no Funciona

Si Yahoo Finance está completamente bloqueado, puedes:

1. **Usar un VPN** para cambiar tu ubicación virtual
2. **Configurar un proxy** para redirigir el tráfico
3. **Modificar el código** para usar APIs alternativas (Alpha Vantage, CoinGecko)

### 7. Performance Tips

Para mejor rendimiento:

1. **Usa el caché**: No analices el mismo símbolo múltiples veces seguidas
2. **Períodos razonables**: Usa '6mo' o '1y' en lugar de 'max'
3. **Lotes pequeños**: No compares más de 5 símbolos a la vez
4. **Espera entre requests**: Deja 1-2 segundos entre análisis diferentes

### 8. Verificar Instalación de Dependencias

```bash
# Verifica que todas las dependencias estén instaladas
pip list | grep -E "yfinance|pandas|scikit-learn|flask|ta"

# Versiones esperadas:
# yfinance         0.2.36
# pandas           2.1.4
# scikit-learn     1.3.2
# flask            3.0.0
# ta               0.11.0
```

### 9. Modo Debug

Para ver más información sobre errores:

1. Edita `.env` y agrega:
   ```
   FLASK_DEBUG=True
   LOG_LEVEL=DEBUG
   ```

2. O ejecuta con logging detallado:
   ```bash
   python app.py --debug
   ```

### 10. Contacto y Soporte

Si ninguna de estas soluciones funciona:

1. Verifica los logs en consola
2. Prueba el script de test: `python test_connection.py`
3. Reporta el issue con:
   - Sistema operativo
   - Versión de Python
   - Mensaje de error completo
   - Salida del test de conexión

## Preguntas Frecuentes

### ¿Por qué algunos símbolos no funcionan?
Yahoo Finance no tiene datos para todos los símbolos. Verifica en finance.yahoo.com primero.

### ¿Cuántas requests puedo hacer?
Yahoo Finance tiene rate limits. El caché ayuda, pero evita más de 2000 requests/hora.

### ¿Los datos son en tiempo real?
Los datos tienen un retraso de ~15 minutos para acciones y pueden ser en tiempo real para criptos.

### ¿Funciona en todos los países?
Sí, pero algunos países pueden bloquear Yahoo Finance. Usa VPN si es necesario.

### ¿Puedo usar otros proveedores de datos?
Sí, el código es modular. Puedes agregar otros proveedores en `market_predictor.py`.
