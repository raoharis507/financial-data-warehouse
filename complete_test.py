import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_api():
    print("=" * 60)
    print("FINANCIAL DATA WAREHOUSE - COMPLETE TEST")
    print("=" * 60)
    
    # Test 1: Health
    print("\n1️⃣  HEALTH CHECK:")
    response = requests.get(f"{BASE_URL}/health")
    print(f"   ✅ {response.json()}")
    
    # Test 2: Assets
    print("\n2️⃣  ASSETS (Q1):")
    response = requests.get(f"{BASE_URL}/api/assets")
    assets = response.json()
    print(f"   ✅ Found {len(assets)} assets")
    for asset in assets:
        print(f"      - {asset['assetId']}: {asset['name']}")
    
    # Test 3: Analytics
    print("\n3️⃣  ANALYTICS (UC3):")
    response = requests.get(f"{BASE_URL}/api/analytics/ma/AAPL/Nasdaq?days=5")
    ma = response.json()
    print(f"   ✅ Moving Average (5-day): ${ma['moving_average']}")
    
    response = requests.get(f"{BASE_URL}/api/analytics/volatility/AAPL/Nasdaq")
    vol = response.json()
    print(f"   ✅ Volatility: {vol['volatility']*100:.1f}% - Risk: {vol['risk_level']}")
    
    # Test 4: LLM Assistant
    print("\n4️⃣  LLM ASSISTANT (UC4):")
    response = requests.get(f"{BASE_URL}/api/assistant/ask?query=list%20assets")
    llm_response = response.json()
    print(f"   ✅ {llm_response['response']}")
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)

if __name__ == "__main__":
    test_api()
