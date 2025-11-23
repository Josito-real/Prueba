#!/usr/bin/env python3
"""
Simple connectivity test script - no external dependencies required
"""

import urllib.request
import json
import ssl

def test_yahoo_finance():
    """Test connection to Yahoo Finance"""
    print("Testing Yahoo Finance connectivity...")

    try:
        # Create SSL context that doesn't verify certificates (for testing)
        context = ssl._create_unverified_context()

        # Test symbol
        symbol = "AAPL"
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=5d"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        req = urllib.request.Request(url, headers=headers)

        print(f"Fetching data for {symbol}...")
        with urllib.request.urlopen(req, context=context, timeout=10) as response:
            data = json.loads(response.read().decode())

            if 'chart' in data and 'result' in data['chart']:
                result = data['chart']['result'][0]
                timestamps = result.get('timestamp', [])
                quotes = result.get('indicators', {}).get('quote', [{}])[0]
                closes = quotes.get('close', [])

                if closes:
                    latest_price = [c for c in closes if c is not None][-1]
                    print(f"✓ SUCCESS: Connected to Yahoo Finance")
                    print(f"  Symbol: {symbol}")
                    print(f"  Latest Close: ${latest_price:.2f}")
                    print(f"  Data points: {len(timestamps)}")
                    return True

        print("✗ FAILED: No data received")
        return False

    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
        return False

def test_internet_connection():
    """Test basic internet connectivity"""
    print("\nTesting internet connectivity...")

    test_urls = [
        "https://www.google.com",
        "https://finance.yahoo.com",
        "https://www.python.org"
    ]

    for url in test_urls:
        try:
            context = ssl._create_unverified_context()
            with urllib.request.urlopen(url, context=context, timeout=5) as response:
                if response.status == 200:
                    print(f"✓ {url}: OK")
                else:
                    print(f"✗ {url}: Status {response.status}")
        except Exception as e:
            print(f"✗ {url}: {str(e)}")

if __name__ == "__main__":
    print("="*60)
    print("Market Predictor - Connection Test")
    print("="*60)

    test_internet_connection()
    print()
    success = test_yahoo_finance()

    print("\n" + "="*60)
    if success:
        print("✓ All tests passed! You can proceed with installation.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run the app: python app.py")
    else:
        print("✗ Connection test failed!")
        print("\nTroubleshooting:")
        print("- Check your internet connection")
        print("- Verify firewall settings")
        print("- Try using a VPN if Yahoo Finance is blocked")
        print("- Check if you're behind a proxy")
    print("="*60)
