"""
Test script to verify Sarvam AI-only mode
"""

import requests
import json

API_BASE_URL = "http://localhost:5000"

def test_sarvam_query(message):
    """Test a Sarvam AI related query"""
    print(f"\n{'='*70}")
    print(f"Query: {message}")
    print('='*70)
    
    response = requests.post(
        f"{API_BASE_URL}/api/chat",
        json={"message": message, "language": "en"},
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"\n✓ Success")
            print(f"\nResponse:\n{data.get('response')}")
        else:
            print(f"\n✗ Error: {data.get('error')}")
    else:
        print(f"\n✗ HTTP Error {response.status_code}")

def main():
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "Sarvam AI - Strict Mode Test Suite" + " "*18 + "║")
    print("╚" + "="*68 + "╝")
    
    print("\n⚠️  NOTE: Flask server must be running on http://localhost:5000")
    print("\nStarting in new terminal:")
    print("  python app.py\n")
    
    # Test 1: Sarvam AI product queries (should answer)
    test_sarvam_query("What is Saaras v3 and how does it work?")
    test_sarvam_query("Tell me about Samvaad Studio and its use cases")
    test_sarvam_query("What languages does Sarvam AI support?")
    test_sarvam_query("How do I get started with Sarvam AI APIs?")
    test_sarvam_query("What is Sarvam-M LLM?")
    
    # Test 2: General knowledge queries (should decline)
    test_sarvam_query("What is the capital of India?")
    test_sarvam_query("Tell me a joke")
    test_sarvam_query("How do I cook pasta?")
    test_sarvam_query("What is quantum physics?")
    
    # Test 3: Off-topic queries (should redirect)
    test_sarvam_query("How to learn Python?")
    test_sarvam_query("What is the weather today?")
    test_sarvam_query("Recommend a movie for me")
    
    print("\n" + "="*70)
    print("Test Suite Complete")
    print("="*70 + "\n")

if __name__ == "__main__":
    try:
        # Try a quick health check first
        print("\nChecking if Flask server is running...")
        response = requests.get(f"{API_BASE_URL}/api/health", timeout=2)
        if response.status_code == 200:
            print("✓ Server is running!\n")
            main()
        else:
            print("✗ Server responded but not healthy")
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to Flask server")
        print("\n❌ Please start the Flask server in a terminal:")
        print("   python app.py\n")
        print("Then run this test again.")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
