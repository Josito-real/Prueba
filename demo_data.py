"""
Demo Data Generator - For testing without internet connection
Generates realistic market data for demonstration purposes
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def generate_demo_stock_data(symbol, days=180, base_price=150.0, volatility=0.02):
    """
    Generate realistic demo stock data

    Args:
        symbol: Stock symbol
        days: Number of days of data
        base_price: Starting price
        volatility: Price volatility (0.02 = 2%)
    """
    np.random.seed(hash(symbol) % 2**32)  # Consistent data for same symbol

    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')

    # Generate price movement with random walk
    returns = np.random.normal(0.0005, volatility, days)
    prices = base_price * np.exp(np.cumsum(returns))

    # Generate OHLCV data
    data = {
        'Open': prices * (1 + np.random.uniform(-0.01, 0.01, days)),
        'High': prices * (1 + np.random.uniform(0.005, 0.02, days)),
        'Low': prices * (1 + np.random.uniform(-0.02, -0.005, days)),
        'Close': prices,
        'Volume': np.random.randint(50000000, 150000000, days)
    }

    df = pd.DataFrame(data, index=dates)

    # Ensure High is highest and Low is lowest
    df['High'] = df[['Open', 'High', 'Close']].max(axis=1)
    df['Low'] = df[['Open', 'Low', 'Close']].min(axis=1)

    return df


def generate_demo_crypto_data(symbol, days=180, base_price=50000.0, volatility=0.04):
    """Generate realistic demo cryptocurrency data (more volatile)"""
    return generate_demo_stock_data(symbol, days, base_price, volatility)


DEMO_SYMBOLS = {
    # Stocks
    'AAPL': {'name': 'Apple Inc.', 'base_price': 180.0, 'volatility': 0.02},
    'MSFT': {'name': 'Microsoft', 'base_price': 370.0, 'volatility': 0.018},
    'GOOGL': {'name': 'Alphabet', 'base_price': 140.0, 'volatility': 0.022},
    'AMZN': {'name': 'Amazon', 'base_price': 170.0, 'volatility': 0.025},
    'TSLA': {'name': 'Tesla', 'base_price': 240.0, 'volatility': 0.035},
    'NVDA': {'name': 'NVIDIA', 'base_price': 500.0, 'volatility': 0.03},
    'META': {'name': 'Meta', 'base_price': 350.0, 'volatility': 0.028},
    'JPM': {'name': 'JPMorgan', 'base_price': 155.0, 'volatility': 0.015},
    'V': {'name': 'Visa', 'base_price': 260.0, 'volatility': 0.016},
    'WMT': {'name': 'Walmart', 'base_price': 165.0, 'volatility': 0.012},

    # Crypto
    'BTC-USD': {'name': 'Bitcoin', 'base_price': 65000.0, 'volatility': 0.04},
    'ETH-USD': {'name': 'Ethereum', 'base_price': 3500.0, 'volatility': 0.045},
    'BNB-USD': {'name': 'Binance Coin', 'base_price': 580.0, 'volatility': 0.05},
    'SOL-USD': {'name': 'Solana', 'base_price': 140.0, 'volatility': 0.06},
    'XRP-USD': {'name': 'Ripple', 'base_price': 0.60, 'volatility': 0.055},
    'ADA-USD': {'name': 'Cardano', 'base_price': 0.65, 'volatility': 0.05},
    'DOGE-USD': {'name': 'Dogecoin', 'base_price': 0.15, 'volatility': 0.07},
    'MATIC-USD': {'name': 'Polygon', 'base_price': 1.10, 'volatility': 0.055},
    'DOT-USD': {'name': 'Polkadot', 'base_price': 7.50, 'volatility': 0.05},
    'AVAX-USD': {'name': 'Avalanche', 'base_price': 38.0, 'volatility': 0.058},
}


def get_demo_data(symbol, period='1y'):
    """Get demo data for a symbol"""
    if symbol not in DEMO_SYMBOLS:
        return None

    # Map period to days
    period_map = {
        '1d': 1,
        '5d': 5,
        '1mo': 30,
        '3mo': 90,
        '6mo': 180,
        '1y': 365,
        '2y': 730,
        '5y': 1825,
        'max': 1825
    }

    days = period_map.get(period, 180)
    info = DEMO_SYMBOLS[symbol]

    if '-USD' in symbol:  # Crypto
        return generate_demo_crypto_data(
            symbol,
            days=days,
            base_price=info['base_price'],
            volatility=info['volatility']
        )
    else:  # Stock
        return generate_demo_stock_data(
            symbol,
            days=days,
            base_price=info['base_price'],
            volatility=info['volatility']
        )


def is_demo_mode():
    """Check if we should use demo mode"""
    import os
    return os.getenv('DEMO_MODE', 'false').lower() == 'true'


if __name__ == "__main__":
    # Test demo data generation
    print("Testing demo data generation...")

    for symbol in ['AAPL', 'BTC-USD']:
        df = get_demo_data(symbol, '1mo')
        if df is not None:
            print(f"\n{symbol}:")
            print(f"  Data points: {len(df)}")
            print(f"  Latest close: ${df['Close'].iloc[-1]:.2f}")
            print(f"  Price range: ${df['Low'].min():.2f} - ${df['High'].max():.2f}")
        else:
            print(f"\n{symbol}: Failed to generate data")

    print("\n✓ Demo data generation test completed")
