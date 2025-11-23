"""
Enhanced Market Predictor Module
Implements advanced prediction models with robust data fetching
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import yfinance as yf
from ta import add_all_ta_features
from ta.utils import dropna
from datetime import datetime, timedelta
import warnings
import time
import logging
import requests
from functools import lru_cache

warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MarketDataFetcher:
    """Robust market data fetcher with multiple sources and retry logic"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def fetch_with_retry(self, symbol, period='1y', interval='1d', max_retries=3):
        """
        Fetch data with retry logic and exponential backoff

        Args:
            symbol: Stock or crypto symbol
            period: Data period
            interval: Data interval
            max_retries: Maximum number of retry attempts
        """
        for attempt in range(max_retries):
            try:
                logger.info(f"Fetching data for {symbol} (attempt {attempt + 1}/{max_retries})")

                # Configure yfinance with session
                ticker = yf.Ticker(symbol, session=self.session)

                # Fetch historical data
                df = ticker.history(
                    period=period,
                    interval=interval,
                    auto_adjust=True,
                    actions=False
                )

                if df.empty:
                    logger.warning(f"Empty dataframe for {symbol}")
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)  # Exponential backoff
                        continue
                    return None

                # Verify data integrity
                if len(df) < 10:
                    logger.warning(f"Insufficient data points for {symbol}: {len(df)}")
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)
                        continue
                    return None

                # Check for valid columns
                required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
                if not all(col in df.columns for col in required_cols):
                    logger.error(f"Missing required columns for {symbol}")
                    return None

                logger.info(f"Successfully fetched {len(df)} data points for {symbol}")
                return df

            except Exception as e:
                logger.error(f"Error fetching {symbol} on attempt {attempt + 1}: {str(e)}")
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Failed to fetch data for {symbol} after {max_retries} attempts")
                    return None

        return None

    def get_current_price(self, symbol):
        """Get current price for a symbol"""
        try:
            ticker = yf.Ticker(symbol, session=self.session)
            info = ticker.info

            # Try different price fields
            price_fields = ['currentPrice', 'regularMarketPrice', 'previousClose']
            for field in price_fields:
                if field in info and info[field]:
                    return float(info[field])

            # Fallback to last close price
            hist = ticker.history(period='1d')
            if not hist.empty:
                return float(hist['Close'].iloc[-1])

        except Exception as e:
            logger.error(f"Error getting current price for {symbol}: {str(e)}")

        return None


class MarketPredictor:
    """Advanced market prediction using multiple techniques"""

    def __init__(self):
        self.scaler = MinMaxScaler()
        self.model = None
        self.fetcher = MarketDataFetcher()
        self.cache = {}
        self.cache_timeout = 300  # 5 minutes

    @lru_cache(maxsize=100)
    def fetch_market_data(self, symbol, period='1y', interval='1d'):
        """
        Fetch historical market data with caching

        Args:
            symbol: Stock or crypto symbol (e.g., 'BTC-USD', 'AAPL')
            period: Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval: Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
        """
        cache_key = f"{symbol}_{period}_{interval}"
        current_time = time.time()

        # Check cache
        if cache_key in self.cache:
            cached_data, cached_time = self.cache[cache_key]
            if current_time - cached_time < self.cache_timeout:
                logger.info(f"Using cached data for {symbol}")
                return cached_data

        # Fetch new data
        df = self.fetcher.fetch_with_retry(symbol, period, interval)

        if df is None or df.empty:
            logger.error(f"Failed to fetch data for {symbol}")
            return None

        try:
            # Add technical indicators
            df = self._add_technical_indicators(df)

            # Cache the result
            self.cache[cache_key] = (df, current_time)

            return df
        except Exception as e:
            logger.error(f"Error processing data for {symbol}: {str(e)}")
            return None

    def _add_technical_indicators(self, df):
        """Add comprehensive technical analysis indicators with error handling"""
        try:
            # Make a copy to avoid modifying original
            df = df.copy()

            # Clean data
            df = dropna(df)

            if len(df) < 20:
                logger.warning("Insufficient data for technical indicators")
                return df

            # Add all technical indicators with error handling
            try:
                df = add_all_ta_features(
                    df,
                    open="Open",
                    high="High",
                    low="Low",
                    close="Close",
                    volume="Volume",
                    fillna=True
                )
            except Exception as e:
                logger.warning(f"Error adding some technical indicators: {str(e)}")
                # Continue with basic indicators

            # Additional custom indicators
            df['Price_Change'] = df['Close'].pct_change()
            df['Price_Range'] = df['High'] - df['Low']
            df['Average_Price'] = (df['High'] + df['Low'] + df['Close']) / 3

            # Moving averages with error handling
            for window in [7, 14, 30]:
                if len(df) >= window:
                    df[f'MA_{window}'] = df['Close'].rolling(window=window).mean()

            # Volatility
            if len(df) >= 10:
                df['Volatility'] = df['Close'].rolling(window=10).std()

            # Drop NaN values
            df = df.dropna()

            logger.info(f"Successfully added technical indicators, {len(df)} rows remaining")
            return df

        except Exception as e:
            logger.error(f"Error adding technical indicators: {str(e)}")
            # Return dataframe with basic columns at minimum
            return df

    def prepare_features(self, df, target_col='Close', look_back=10):
        """
        Prepare features for machine learning model

        Args:
            df: DataFrame with market data
            target_col: Target column to predict
            look_back: Number of previous days to use as features
        """
        try:
            # Select relevant features
            exclude_cols = ['Dividends', 'Stock Splits']
            feature_columns = [col for col in df.columns if col not in exclude_cols]

            df_features = df[feature_columns].copy()

            # Create lagged features
            for i in range(1, look_back + 1):
                df_features[f'{target_col}_lag_{i}'] = df[target_col].shift(i)

            # Drop rows with NaN
            df_features = df_features.dropna()

            logger.info(f"Prepared {len(df_features)} feature rows with {len(df_features.columns)} columns")
            return df_features

        except Exception as e:
            logger.error(f"Error preparing features: {str(e)}")
            raise

    def train_model(self, df, target_col='Close', model_type='rf'):
        """
        Train prediction model

        Args:
            df: DataFrame with prepared features
            target_col: Target column to predict
            model_type: 'rf' for Random Forest, 'gb' for Gradient Boosting
        """
        try:
            # Prepare data
            X = df.drop(columns=[target_col])
            y = df[target_col]

            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, shuffle=False
            )

            logger.info(f"Training with {len(X_train)} samples, testing with {len(X_test)} samples")

            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)

            # Train model
            if model_type == 'rf':
                self.model = RandomForestRegressor(
                    n_estimators=100,
                    max_depth=10,
                    random_state=42,
                    n_jobs=-1
                )
            else:
                self.model = GradientBoostingRegressor(
                    n_estimators=100,
                    max_depth=5,
                    learning_rate=0.1,
                    random_state=42
                )

            logger.info(f"Training {model_type} model...")
            self.model.fit(X_train_scaled, y_train)

            # Calculate accuracy
            train_score = self.model.score(X_train_scaled, y_train)
            test_score = self.model.score(X_test_scaled, y_test)

            logger.info(f"Model trained - Train score: {train_score:.4f}, Test score: {test_score:.4f}")

            return {
                'train_score': train_score,
                'test_score': test_score,
                'model': self.model
            }

        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            raise

    def predict_future(self, df, days_ahead=7):
        """
        Predict future prices

        Args:
            df: DataFrame with current market data
            days_ahead: Number of days to predict ahead
        """
        try:
            predictions = []
            last_row = df.iloc[-1:].copy()

            for i in range(days_ahead):
                # Prepare features
                features = last_row.drop(columns=['Close'])
                features_scaled = self.scaler.transform(features)

                # Make prediction
                pred = self.model.predict(features_scaled)[0]
                predictions.append(pred)

                # Update for next prediction (simplified)
                last_row['Close'] = pred

            logger.info(f"Generated {len(predictions)} predictions")
            return predictions

        except Exception as e:
            logger.error(f"Error making predictions: {str(e)}")
            raise

    def calculate_signals(self, df):
        """
        Calculate buy/sell signals based on technical indicators

        Returns:
            dict: Trading signals and recommendations
        """
        try:
            latest = df.iloc[-1]

            signals = {
                'recommendation': 'HOLD',
                'confidence': 0,
                'indicators': {}
            }

            score = 0

            # RSI Signal
            if 'momentum_rsi' in df.columns:
                rsi = latest['momentum_rsi']
                if pd.notna(rsi):
                    if rsi < 30:
                        signals['indicators']['RSI'] = 'Oversold - BUY signal'
                        score += 2
                    elif rsi > 70:
                        signals['indicators']['RSI'] = 'Overbought - SELL signal'
                        score -= 2
                    else:
                        signals['indicators']['RSI'] = f'Neutral ({rsi:.1f})'

            # MACD Signal
            if 'trend_macd' in df.columns and 'trend_macd_signal' in df.columns:
                macd = latest['trend_macd']
                macd_signal = latest['trend_macd_signal']
                if pd.notna(macd) and pd.notna(macd_signal):
                    if macd > macd_signal:
                        signals['indicators']['MACD'] = 'Bullish - BUY signal'
                        score += 1
                    else:
                        signals['indicators']['MACD'] = 'Bearish - SELL signal'
                        score -= 1

            # Moving Average Signal
            if all(col in df.columns for col in ['MA_7', 'MA_30', 'Close']):
                ma_7 = latest['MA_7']
                ma_30 = latest['MA_30']
                close = latest['Close']

                if pd.notna(ma_7) and pd.notna(ma_30):
                    if ma_7 > ma_30 and close > ma_7:
                        signals['indicators']['MA_Cross'] = 'Golden Cross - BUY signal'
                        score += 1
                    elif ma_7 < ma_30 and close < ma_7:
                        signals['indicators']['MA_Cross'] = 'Death Cross - SELL signal'
                        score -= 1
                    else:
                        signals['indicators']['MA_Cross'] = 'Neutral'

            # Bollinger Bands
            if 'volatility_bbh' in df.columns and 'volatility_bbl' in df.columns:
                bb_high = latest['volatility_bbh']
                bb_low = latest['volatility_bbl']
                close = latest['Close']

                if pd.notna(bb_high) and pd.notna(bb_low):
                    if close < bb_low:
                        signals['indicators']['Bollinger'] = 'Below lower band - BUY signal'
                        score += 1
                    elif close > bb_high:
                        signals['indicators']['Bollinger'] = 'Above upper band - SELL signal'
                        score -= 1
                    else:
                        signals['indicators']['Bollinger'] = 'Within bands - Neutral'

            # Determine recommendation
            if score >= 3:
                signals['recommendation'] = 'STRONG BUY'
                signals['confidence'] = min(score * 15, 95)
            elif score >= 1:
                signals['recommendation'] = 'BUY'
                signals['confidence'] = min(score * 20, 80)
            elif score <= -3:
                signals['recommendation'] = 'STRONG SELL'
                signals['confidence'] = min(abs(score) * 15, 95)
            elif score <= -1:
                signals['recommendation'] = 'SELL'
                signals['confidence'] = min(abs(score) * 20, 80)
            else:
                signals['recommendation'] = 'HOLD'
                signals['confidence'] = 50

            logger.info(f"Generated signals - Recommendation: {signals['recommendation']}, Confidence: {signals['confidence']}")
            return signals

        except Exception as e:
            logger.error(f"Error calculating signals: {str(e)}")
            return {
                'recommendation': 'HOLD',
                'confidence': 0,
                'indicators': {'error': str(e)}
            }

    def get_market_analysis(self, symbol, period='6mo'):
        """
        Complete market analysis for a symbol

        Args:
            symbol: Market symbol
            period: Historical data period

        Returns:
            dict: Complete analysis including predictions and signals
        """
        try:
            logger.info(f"Starting market analysis for {symbol} with period {period}")

            # Fetch data
            df = self.fetch_market_data(symbol, period=period)

            if df is None or len(df) < 50:
                error_msg = f'Insufficient data for {symbol}. Try a different symbol or check your internet connection.'
                logger.error(error_msg)
                return {'error': error_msg}

            # Prepare features
            df_prepared = self.prepare_features(df)

            if len(df_prepared) < 30:
                error_msg = f'Insufficient data after feature preparation for {symbol}'
                logger.error(error_msg)
                return {'error': error_msg}

            # Train model
            train_results = self.train_model(df_prepared)

            # Make predictions
            predictions = self.predict_future(df_prepared, days_ahead=7)

            # Calculate signals
            signals = self.calculate_signals(df)

            # Get current price info
            current_price = df['Close'].iloc[-1]
            prev_price = df['Close'].iloc[-2]
            change = ((current_price - prev_price) / prev_price) * 100

            result = {
                'symbol': symbol,
                'current_price': float(current_price),
                'change_percent': float(change),
                'predictions': {
                    'next_7_days': [float(p) for p in predictions],
                    'trend': 'BULLISH' if predictions[-1] > current_price else 'BEARISH'
                },
                'model_accuracy': {
                    'train_score': float(train_results['train_score']),
                    'test_score': float(train_results['test_score'])
                },
                'signals': signals,
                'historical_data': {
                    'dates': [str(date.date()) for date in df.index[-30:]],
                    'prices': [float(p) for p in df['Close'].tail(30)],
                    'volumes': [float(v) for v in df['Volume'].tail(30)]
                },
                'statistics': {
                    'high_52w': float(df['High'].tail(252).max()) if len(df) >= 252 else float(df['High'].max()),
                    'low_52w': float(df['Low'].tail(252).min()) if len(df) >= 252 else float(df['Low'].min()),
                    'avg_volume': float(df['Volume'].tail(30).mean()),
                    'volatility': float(df['Volatility'].iloc[-1]) if 'Volatility' in df.columns else 0
                }
            }

            logger.info(f"Successfully completed analysis for {symbol}")
            return result

        except Exception as e:
            error_msg = f'Analysis failed for {symbol}: {str(e)}'
            logger.error(error_msg)
            return {'error': error_msg}


def get_popular_symbols():
    """Return list of popular stocks and cryptocurrencies"""
    return {
        'stocks': [
            {'symbol': 'AAPL', 'name': 'Apple Inc.'},
            {'symbol': 'MSFT', 'name': 'Microsoft Corporation'},
            {'symbol': 'GOOGL', 'name': 'Alphabet Inc.'},
            {'symbol': 'AMZN', 'name': 'Amazon.com Inc.'},
            {'symbol': 'TSLA', 'name': 'Tesla Inc.'},
            {'symbol': 'NVDA', 'name': 'NVIDIA Corporation'},
            {'symbol': 'META', 'name': 'Meta Platforms Inc.'},
            {'symbol': 'JPM', 'name': 'JPMorgan Chase & Co.'},
            {'symbol': 'V', 'name': 'Visa Inc.'},
            {'symbol': 'WMT', 'name': 'Walmart Inc.'}
        ],
        'crypto': [
            {'symbol': 'BTC-USD', 'name': 'Bitcoin'},
            {'symbol': 'ETH-USD', 'name': 'Ethereum'},
            {'symbol': 'BNB-USD', 'name': 'Binance Coin'},
            {'symbol': 'SOL-USD', 'name': 'Solana'},
            {'symbol': 'XRP-USD', 'name': 'Ripple'},
            {'symbol': 'ADA-USD', 'name': 'Cardano'},
            {'symbol': 'DOGE-USD', 'name': 'Dogecoin'},
            {'symbol': 'MATIC-USD', 'name': 'Polygon'},
            {'symbol': 'DOT-USD', 'name': 'Polkadot'},
            {'symbol': 'AVAX-USD', 'name': 'Avalanche'}
        ]
    }


# Test function
def test_connection():
    """Test data connection with a simple symbol"""
    logger.info("Testing market data connection...")
    predictor = MarketPredictor()

    test_symbols = ['AAPL', 'MSFT', 'BTC-USD']

    for symbol in test_symbols:
        logger.info(f"\nTesting {symbol}...")
        df = predictor.fetch_market_data(symbol, period='1mo')

        if df is not None and not df.empty:
            logger.info(f"✓ {symbol}: Successfully fetched {len(df)} data points")
            logger.info(f"  Latest close: ${df['Close'].iloc[-1]:.2f}")
        else:
            logger.error(f"✗ {symbol}: Failed to fetch data")

    logger.info("\nConnection test completed")


if __name__ == "__main__":
    test_connection()
