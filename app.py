"""
Market Prediction API Server
Flask REST API for market predictions
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from market_predictor import MarketPredictor, get_popular_symbols
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='.')
CORS(app)

# Initialize predictor
predictor = MarketPredictor()


@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'market_app.html')


@app.route('/api/symbols', methods=['GET'])
def get_symbols():
    """Get list of popular symbols"""
    try:
        symbols = get_popular_symbols()
        return jsonify({
            'success': True,
            'data': symbols
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/analyze/<symbol>', methods=['GET'])
def analyze_symbol(symbol):
    """
    Analyze a specific market symbol

    Query parameters:
        period: Data period (default: 6mo)
    """
    try:
        period = request.args.get('period', '6mo')

        # Validate symbol
        symbol = symbol.upper()

        # Get analysis
        analysis = predictor.get_market_analysis(symbol, period=period)

        if 'error' in analysis:
            return jsonify({
                'success': False,
                'error': analysis['error']
            }), 400

        return jsonify({
            'success': True,
            'data': analysis
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Analysis failed: {str(e)}'
        }), 500


@app.route('/api/quick-analysis', methods=['POST'])
def quick_analysis():
    """
    Analyze multiple symbols quickly

    Request body:
        {
            "symbols": ["AAPL", "BTC-USD", ...]
        }
    """
    try:
        data = request.get_json()
        symbols = data.get('symbols', [])

        if not symbols:
            return jsonify({
                'success': False,
                'error': 'No symbols provided'
            }), 400

        results = []
        for symbol in symbols[:10]:  # Limit to 10 symbols
            try:
                analysis = predictor.get_market_analysis(symbol, period='3mo')
                if 'error' not in analysis:
                    results.append({
                        'symbol': symbol,
                        'current_price': analysis['current_price'],
                        'change_percent': analysis['change_percent'],
                        'recommendation': analysis['signals']['recommendation'],
                        'confidence': analysis['signals']['confidence'],
                        'trend': analysis['predictions']['trend']
                    })
            except:
                continue

        return jsonify({
            'success': True,
            'data': results
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/compare', methods=['POST'])
def compare_symbols():
    """
    Compare multiple symbols

    Request body:
        {
            "symbols": ["AAPL", "MSFT", ...]
        }
    """
    try:
        data = request.get_json()
        symbols = data.get('symbols', [])

        if len(symbols) < 2:
            return jsonify({
                'success': False,
                'error': 'At least 2 symbols required for comparison'
            }), 400

        comparisons = []
        for symbol in symbols[:5]:  # Limit to 5 symbols
            try:
                analysis = predictor.get_market_analysis(symbol, period='3mo')
                if 'error' not in analysis:
                    comparisons.append({
                        'symbol': symbol,
                        'current_price': analysis['current_price'],
                        'change_percent': analysis['change_percent'],
                        'prediction_change': ((analysis['predictions']['next_7_days'][-1] - analysis['current_price']) / analysis['current_price']) * 100,
                        'recommendation': analysis['signals']['recommendation'],
                        'model_accuracy': analysis['model_accuracy']['test_score']
                    })
            except:
                continue

        return jsonify({
            'success': True,
            'data': comparisons
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'message': 'Market Prediction API is running'
    })


@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'

    print(f"""
    ╔══════════════════════════════════════════════╗
    ║   Market Prediction API Server               ║
    ║   Running on http://localhost:{port}         ║
    ╚══════════════════════════════════════════════╝
    """)

    app.run(host='0.0.0.0', port=port, debug=debug)
