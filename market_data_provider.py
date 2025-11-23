"""
Market Data Provider - Wrapper for both real and demo data
Automatically switches between Yahoo Finance and demo data
"""

import os
import logging

logger = logging.getLogger(__name__)

# Check environment
DEMO_MODE = os.getenv('DEMO_MODE', 'true').lower() == 'true'


def get_market_data(symbol, period='1y', interval='1d'):
    """
    Get market data from available source
    Tries real data first, falls back to demo if unavailable
    """

    # Try real data first if not in demo mode
    if not DEMO_MODE:
        try:
            from market_predictor import MarketDataFetcher
            fetcher = MarketDataFetcher()
            df = fetcher.fetch_with_retry(symbol, period, interval)

            if df is not None and not df.empty:
                logger.info(f"Using REAL data for {symbol}")
                return df, 'real'
        except Exception as e:
            logger.warning(f"Failed to fetch real data: {e}")

    # Fall back to demo data
    try:
        from demo_data import get_demo_data
        df = get_demo_data(symbol, period)

        if df is not None and not df.empty:
            logger.info(f"Using DEMO data for {symbol}")
            return df, 'demo'
    except Exception as e:
        logger.error(f"Failed to get demo data: {e}")

    return None, 'none'


if __name__ == "__main__":
    # Test data provider
    print(f"Demo Mode: {DEMO_MODE}")
    print("\nTesting data provider...")

    test_symbols = ['AAPL', 'BTC-USD']

    for symbol in test_symbols:
        df, source = get_market_data(symbol, '1mo')

        if df is not None:
            print(f"\n✓ {symbol} ({source}):")
            print(f"  Data points: {len(df)}")
            print(f"  Latest close: ${df['Close'].iloc[-1]:.2f}")
        else:
            print(f"\n✗ {symbol}: No data available")
