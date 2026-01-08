"""
Test script for the fake news detection app
"""

import requests
import json

def test_fake_news_detection():
    """Test the fake news detection API"""
    
    # Test cases
    test_cases = [
        {
            "name": "Fake News Example",
            "text": "BREAKING: Shocking secret revealed! They don't want you to know this unbelievable truth about the government conspiracy!"
        },
        {
            "name": "Real News Example", 
            "text": "According to a peer-reviewed study published in Nature, researchers have confirmed that climate change is affecting global weather patterns. The data shows significant temperature increases over the past decade."
        },
        {
            "name": "Neutral Example",
            "text": "The weather today is sunny with a temperature of 25 degrees Celsius. Many people are enjoying outdoor activities in the park."
        }
    ]
    
    print("=" * 60)
    print("FAKE NEWS DETECTION APP - TEST RESULTS")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['name']}")
        print("-" * 40)
        print(f"Input Text: {test_case['text'][:100]}...")
        
        try:
            # Make API request
            response = requests.post(
                'http://127.0.0.1:5000/check-news',
                headers={'Content-Type': 'application/json'},
                json={'news_text': test_case['text']},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"Prediction: {result['prediction']}")
                print(f"Confidence: {result['confidence']}%")
                print(f"Status: {result['status']}")
                if 'method' in result:
                    print(f"Method: {result['method']}")
            else:
                print(f"Error: HTTP {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
        
        print()

if __name__ == '__main__':
    test_fake_news_detection()