
"""
Fake News Detection Web Application - Production Ready
Uses a simple keyword-based approach for demonstration
"""

from flask import Flask, render_template, request, jsonify
import logging
from waitress import serve

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Simple keyword-based fake news detection
FAKE_NEWS_KEYWORDS = [
    'breaking', 'urgent', 'shocking', 'unbelievable', 'exclusive', 'leaked',
    'secret', 'hidden', 'exposed', 'revealed', 'conspiracy', 'cover-up',
    'they don\'t want you to know', 'mainstream media', 'fake news',
    'hoax', 'scam', 'lie', 'deception', 'propaganda'
]

RELIABLE_KEYWORDS = [
    'according to', 'research shows', 'study finds', 'experts say',
    'official statement', 'confirmed by', 'verified', 'fact-checked',
    'peer-reviewed', 'published in', 'data shows', 'statistics indicate'
]

def analyze_news_simple(text):
    """
    Simple keyword-based analysis for demonstration
    Returns prediction and confidence score
    """
    text_lower = text.lower()
    
    fake_score = 0
    real_score = 0
    
    # Count fake news indicators
    for keyword in FAKE_NEWS_KEYWORDS:
        if keyword in text_lower:
            fake_score += 1
    
    # Count reliable news indicators
    for keyword in RELIABLE_KEYWORDS:
        if keyword in text_lower:
            real_score += 1
    
    # Simple scoring logic
    total_indicators = fake_score + real_score
    
    if total_indicators == 0:
        # No clear indicators, default to neutral/real
        return "Real News", 60.0
    
    fake_ratio = fake_score / total_indicators
    
    if fake_ratio > 0.5:
        confidence = min(70 + (fake_ratio * 30), 95)
        return "Fake News", confidence
    else:
        confidence = min(60 + ((1 - fake_ratio) * 30), 90)
        return "Real News", confidence

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/check-news', methods=['POST'])
def check_news():
    """
    API endpoint to check if news is fake or real
    Expects JSON with 'news_text' key
    """
    try:
        # Get the news text from request
        data = request.get_json()
        news_text = data.get('news_text', '').strip()

        # Validate input
        if not news_text:
            return jsonify({
                'error': 'Please enter some news text',
                'status': 'error'
            }), 400

        # Check text length (minimum 10 characters for meaningful analysis)
        if len(news_text) < 10:
            return jsonify({
                'error': 'Please enter at least 10 characters of news text',
                'status': 'error'
            }), 400

        logger.info(f"Analyzing news text: {news_text[:100]}...")

        # Run simple analysis
        prediction, confidence = analyze_news_simple(news_text)
        
        # Set color based on prediction
        color = 'red' if prediction == 'Fake News' else 'green'

        response = {
            'prediction': prediction,
            'confidence': round(confidence, 2),
            'color': color,
            'status': 'success',
            'method': 'Simple keyword-based analysis'
        }

        logger.info(f"Analysis complete - Prediction: {prediction}, Confidence: {confidence}%")
        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        return jsonify({
            'error': f'An error occurred: {str(e)}',
            'status': 'error'
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info("Starting Fake News Detection App (Production Version)")
    logger.info("This version uses keyword-based analysis and Waitress WSGI server")
    logger.info("Server running on http://127.0.0.1:5000")
    
    # Use Waitress WSGI server for production (no warnings)
    try:
        serve(app, host='127.0.0.1', port=5000, threads=4)
    except ImportError:
        logger.warning("Waitress not installed, falling back to Flask development server")
        app.run(debug=False, host='127.0.0.1', port=5000)