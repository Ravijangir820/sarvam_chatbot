"""
Simple test script for Sarvam Chatbot APIs
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test the health check endpoint"""
    print("\n" + "="*50)
    print("Testing Health Check Endpoint")
    print("="*50)
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_chat(message, language="en"):
    """Test the chat endpoint"""
    print("\n" + "="*50)
    print("Testing Chat Endpoint")
    print("="*50)
    print(f"Message: {message}")
    print(f"Language: {language}")
    
    try:
        payload = {
            "message": message,
            "language": language
        }
        
        response = requests.post(
            f"{API_BASE_URL}/api/chat",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        
        if result.get('success'):
            print(f"\n✓ Bot Response: {result.get('response')}")
            return True
        else:
            print(f"\n✗ Error: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_api_key_validation():
    """Test if API key is properly configured"""
    print("\n" + "="*50)
    print("Validating API Configuration")
    print("="*50)
    
    api_key = os.getenv("SARVAM_API_KEY")
    api_url = os.getenv("SARVAM_API_BASE_URL")
    
    if not api_key:
        print("✗ SARVAM_API_KEY not found in .env file")
        return False
    
    if not api_url:
        print("✗ SARVAM_API_BASE_URL not found in .env file")
        return False
    
    print(f"✓ API Key configured: {api_key[:15]}...{api_key[-5:]}")
    print(f"✓ API URL: {api_url}")
    return True

def main():
    """Run all tests"""
    print("\n")
    print("╔════════════════════════════════════════════════╗")
    print("║   Sarvam Chatbot API Test Suite                ║")
    print("╚════════════════════════════════════════════════╝")
    
    # Test configuration
    print("\n[1/4] Testing API Configuration...")
    config_valid = test_api_key_validation()
    
    if not config_valid:
        print("\n❌ Configuration invalid. Please check .env file.")
        return
    
    # Test API Health
    print("\n[2/4] Testing API Health...")
    health_ok = test_health_check()
    
    if not health_ok:
        print("\n❌ API is not running. Start the Flask server with: python app.py")
        return
    
    # Test Chat - English
    print("\n[3/4] Testing Chat (English)...")
    chat_en = test_chat("Hello, how are you?", "en")
    
    # Test Chat - Hindi
    print("\n[4/4] Testing Chat (Hindi)...")
    chat_hi = test_chat("नमस्ते, आप कैसे हैं?", "hi")
    
    # Summary
    print("\n" + "="*50)
    print("Test Summary")
    print("="*50)
    print(f"Configuration: {'✓ Passed' if config_valid else '✗ Failed'}")
    print(f"API Health: {'✓ Passed' if health_ok else '✗ Failed'}")
    print(f"Chat (English): {'✓ Passed' if chat_en else '✗ Failed'}")
    print(f"Chat (Hindi): {'✓ Passed' if chat_hi else '✗ Failed'}")
    
    all_passed = config_valid and health_ok and chat_en and chat_hi
    print("\n" + ("="*50))
    print(f"Overall Result: {'✓ All Tests Passed!' if all_passed else '✗ Some Tests Failed'}")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
