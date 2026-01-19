"""
Fake News Detection Web Application
Uses HuggingFace Transformers for news classification
"""

from flask import Flask, render_template, request, jsonify
from transformers import pipeline
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Initialize the pre-trained model pipeline (loaded once at startup)
logger.info("Loading pre-trained model from HuggingFace...")
classifier = pipeline(
    "text-classification",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    device=-1  # Use CPU (set to 0 for GPU if available)
)
logger.info("Model loaded successfully!")


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

        # Truncate text to avoid token limit issues (512 tokens max for distilbert)
        # Approximately 2000 characters is safe
        truncated_text = news_text[:2000]

        logger.info(f"Analyzing news text: {truncated_text[:100]}...")

        # Run classification
        result = classifier(truncated_text)[0]

        # Extract label and confidence
        label = result['label']
        confidence = round(result['score'] * 100, 2)

        # Map the labels for user-friendly output
        # The model trained on SST-2 outputs POSITIVE/NEGATIVE
        # We interpret: POSITIVE as "Real News", NEGATIVE as "Fake News"
        if label == 'POSITIVE':
            prediction = 'Real News'
            color = 'green'
        else:
            prediction = 'Fake News'
            color = 'red'

        response = {
            'prediction': prediction,
            'confidence': confidence,
            'color': color,
            'status': 'success'
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
    # Run the Flask app
    # Debug=False for production, True for development
    app.run(debug=True, host='127.0.0.1', port=5000)