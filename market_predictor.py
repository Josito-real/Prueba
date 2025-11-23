"""
Market Predictor Module
Implements advanced prediction models for stocks and cryptocurrencies
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
warnings.filterwarnings('ignore')


class MarketPredictor:
    """Advanced market prediction using multiple techniques"""

    def __init__(self):
        self.scaler = MinMaxScaler()
        self.model = None

    def fetch_market_data(self, symbol, period='1y', interval='1d'):
        """
        Fetch historical market data

        Args:
            symbol: Stock or crypto symbol (e.g., 'BTC-USD', 'AAPL')
            period: Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval: Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
        """
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, interval=interval)

            if df.empty:
                return None

            # Add technical indicators
            df = self._add_technical_indicators(df)

            return df
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None

    def _add_technical_indicators(self, df):
        """Add comprehensive technical analysis indicators"""
        try:
            # Clean data
            df = dropna(df)

            # Add all technical indicators
            df = add_all_ta_features(
                df,
                open="Open",
                high="High",
                low="Low",
                close="Close",
                volume="Volume",
                fillna=True
            )

            # Additional custom indicators
            df['Price_Change'] = df['Close'].pct_change()
            df['Price_Range'] = df['High'] - df['Low']
            df['Average_Price'] = (df['High'] + df['Low'] + df['Close']) / 3

            # Moving averages
            df['MA_7'] = df['Close'].rolling(window=7).mean()
            df['MA_14'] = df['Close'].rolling(window=14).mean()
            df['MA_30'] = df['Close'].rolling(window=30).mean()

            # Volatility
            df['Volatility'] = df['Close'].rolling(window=10).std()

            # Drop NaN values
            df = df.dropna()

            return df
        except Exception as e:
            print(f"Error adding technical indicators: {e}")
            return df

    def prepare_features(self, df, target_col='Close', look_back=10):
        """
        Prepare features for machine learning model

        Args:
            df: DataFrame with market data
            target_col: Target column to predict
            look_back: Number of previous days to use as features
        """
        # Select relevant features
        feature_columns = [col for col in df.columns if col not in ['Dividends', 'Stock Splits']]

        df_features = df[feature_columns].copy()

        # Create lagged features
        for i in range(1, look_back + 1):
            df_features[f'{target_col}_lag_{i}'] = df[target_col].shift(i)

        # Drop rows with NaN
        df_features = df_features.dropna()

        return df_features

    def train_model(self, df, target_col='Close', model_type='rf'):
        """
        Train prediction model

        Args:
            df: DataFrame with prepared features
            target_col: Target column to predict
            model_type: 'rf' for Random Forest, 'gb' for Gradient Boosting
        """
        # Prepare data
        X = df.drop(columns=[target_col])
        y = df[target_col]

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, shuffle=False
        )

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

        self.model.fit(X_train_scaled, y_train)

        # Calculate accuracy
        train_score = self.model.score(X_train_scaled, y_train)
        test_score = self.model.score(X_test_scaled, y_test)

        return {
            'train_score': train_score,
            'test_score': test_score,
            'model': self.model
        }

    def predict_future(self, df, days_ahead=7):
        """
        Predict future prices

        Args:
            df: DataFrame with current market data
            days_ahead: Number of days to predict ahead
        """
        predictions = []
        last_row = df.iloc[-1:].copy()

        for _ in range(days_ahead):
            # Prepare features
            features = last_row.drop(columns=['Close'])
            features_scaled = self.scaler.transform(features)

            # Make prediction
            pred = self.model.predict(features_scaled)[0]
            predictions.append(pred)

            # Update for next prediction (simplified)
            last_row['Close'] = pred

        return predictions

    def calculate_signals(self, df):
        """
        Calculate buy/sell signals based on technical indicators

        Returns:
            dict: Trading signals and recommendations
        """
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
            if rsi < 30:
                signals['indicators']['RSI'] = 'Oversold - BUY signal'
                score += 2
            elif rsi > 70:
                signals['indicators']['RSI'] = 'Overbought - SELL signal'
                score -= 2
            else:
                signals['indicators']['RSI'] = 'Neutral'

        # MACD Signal
        if 'trend_macd' in df.columns and 'trend_macd_signal' in df.columns:
            macd = latest['trend_macd']
            macd_signal = latest['trend_macd_signal']
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

        return signals

    def get_market_analysis(self, symbol, period='6mo'):
        """
        Complete market analysis for a symbol

        Args:
            symbol: Market symbol
            period: Historical data period

        Returns:
            dict: Complete analysis including predictions and signals
        """
        # Fetch data
        df = self.fetch_market_data(symbol, period=period)

        if df is None or len(df) < 50:
            return {'error': 'Insufficient data for analysis'}

        # Prepare features
        df_prepared = self.prepare_features(df)

        if len(df_prepared) < 30:
            return {'error': 'Insufficient data after feature preparation'}

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

        return {
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
                'dates': [str(date) for date in df.index[-30:]],
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
