"""
Diagnostic script to test Sarvam API authentication
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SARVAM_API_KEY")
API_BASE_URL = os.getenv("SARVAM_API_BASE_URL", "https://api.sarvam.ai")

print("="*60)
print("Sarvam API Authentication Diagnostic")
print("="*60)

# Test 1: Check API Key
print(f"\n[Test 1] API Key Check:")
print(f"  Key loaded: {'✓ Yes' if API_KEY else '✗ No'}")
if API_KEY:
    print(f"  Key prefix: {API_KEY[:15]}...")
    print(f"  Key length: {len(API_KEY)} characters")
else:
    print("  ✗ API key not found in .env file!")
    exit(1)

# Test 2: Test Chat API (this was working)
print(f"\n[Test 2] Testing Chat API:")
try:
    headers = {
        "api-subscription-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "sarvam-m",
        "messages": [
            {
                "role": "user",
                "content": "Hi"
            }
        ],
        "temperature": 0.2,
        "max_tokens": 50
    }
    
    response = requests.post(
        f"{API_BASE_URL}/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=10
    )
    
    print(f"  Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"  ✓ Chat API works!")
    else:
        print(f"  ✗ Chat API failed: {response.text[:200]}")
except Exception as e:
    print(f"  ✗ Error: {str(e)}")

# Test 3: Test Speech-to-Text API
print(f"\n[Test 3] Testing Speech-to-Text API:")
print(f"  Note: This requires an actual audio file")
print(f"  Checking if API key is accepted...")

try:
    # Create a minimal test request (will fail without proper audio, but we can check auth)
    headers = {
        "api-subscription-key": API_KEY
    }
    
    # Try with minimal data to test authentication
    files = {
        'file': ('test.wav', b'test', 'audio/wav')
    }
    
    data = {
        'model': 'saaras:v3',
        'language_code': 'en-IN'
    }
    
    response = requests.post(
        f"{API_BASE_URL}/speech-to-text",
        headers=headers,
        files=files,
        data=data,
        timeout=10
    )
    
    print(f"  Status Code: {response.status_code}")
    
    if response.status_code == 403:
        error_data = response.json()
        print(f"  ✗ Authentication Failed!")
        print(f"  Error: {error_data}")
        print(f"\n  Possible causes:")
        print(f"    1. API key is invalid or expired")
        print(f"    2. API key doesn't have STT permissions")
        print(f"    3. API key needs to be regenerated")
        print(f"\n  Action Required:")
        print(f"    → Go to https://dashboard.sarvam.ai/")
        print(f"    → Generate a new API key")
        print(f"    → Update your .env file")
    elif response.status_code == 422:
        print(f"  ✓ Authentication works! (422 = invalid audio data, which is expected)")
    elif response.status_code == 200:
        print(f"  ✓ Speech-to-Text API works!")
    else:
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.text[:200]}")
        
except Exception as e:
    print(f"  ✗ Error: {str(e)}")

print("\n" + "="*60)
print("Diagnostic Complete")
print("="*60)
