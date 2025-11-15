"""
Test script for monitoring API
Tests server and client monitoring endpoints
"""
import requests
import json
import time
import sys


def test_server_monitoring(base_url="http://localhost:8082"):
    """Test server monitoring endpoints"""
    print("=" * 70)
    print("Testing Server Monitoring API")
    print("=" * 70)
    print(f"Base URL: {base_url}\n")
    
    # Test status
    print("1. Testing /monitoring/status...")
    try:
        response = requests.get(f"{base_url}/monitoring/status", timeout=5)
        if response.status_code == 200:
            print("   [OK] Status retrieved")
            data = response.json()
            print(f"   Current round: {data.get('current_round')}")
            print(f"   Total rounds: {data.get('total_rounds')}")
            print(f"   Is training: {data.get('is_training')}")
        else:
            print(f"   [FAIL] Status request failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   [ERROR] Connection error - is the server running?")
        return False
    except Exception as e:
        print(f"   [ERROR] {e}")
        return False
    
    print()
    
    # Test history
    print("2. Testing /monitoring/history...")
    try:
        response = requests.get(f"{base_url}/monitoring/history", timeout=5)
        if response.status_code == 200:
            print("   [OK] History retrieved")
            data = response.json()
            print(f"   Total rounds: {data.get('total_rounds')}")
            print(f"   History entries: {len(data.get('history', []))}")
        else:
            print(f"   [FAIL] History request failed: {response.status_code}")
    except Exception as e:
        print(f"   [ERROR] {e}")
    
    print()
    
    # Test summary
    print("3. Testing /monitoring/summary...")
    try:
        response = requests.get(f"{base_url}/monitoring/summary", timeout=5)
        if response.status_code == 200:
            print("   [OK] Summary retrieved")
            data = response.json()
            if "message" in data:
                print(f"   {data['message']}")
            else:
                print(f"   Average loss: {data.get('average_loss')}")
                print(f"   Latest loss: {data.get('latest_loss')}")
        else:
            print(f"   [FAIL] Summary request failed: {response.status_code}")
    except Exception as e:
        print(f"   [ERROR] {e}")
    
    print()
    return True


def test_client_monitoring(base_url="http://localhost:8081"):
    """Test client monitoring endpoints"""
    print("=" * 70)
    print("Testing Client Monitoring API")
    print("=" * 70)
    print(f"Base URL: {base_url}\n")
    
    # Test status
    print("1. Testing /monitoring/status...")
    try:
        response = requests.get(f"{base_url}/monitoring/status", timeout=5)
        if response.status_code == 200:
            print("   [OK] Status retrieved")
            data = response.json()
            print(f"   Client ID: {data.get('client_id')}")
            print(f"   Total trainings: {data.get('total_trainings')}")
            print(f"   Is training: {data.get('is_training')}")
        else:
            print(f"   [FAIL] Status request failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   [ERROR] Connection error - is the client running?")
        return False
    except Exception as e:
        print(f"   [ERROR] {e}")
        return False
    
    print()
    
    # Test history
    print("2. Testing /monitoring/history...")
    try:
        response = requests.get(f"{base_url}/monitoring/history?limit=10", timeout=5)
        if response.status_code == 200:
            print("   [OK] History retrieved")
            data = response.json()
            print(f"   Client ID: {data.get('client_id')}")
            print(f"   History entries: {len(data.get('history', []))}")
        else:
            print(f"   [FAIL] History request failed: {response.status_code}")
    except Exception as e:
        print(f"   [ERROR] {e}")
    
    print()
    
    # Test summary
    print("3. Testing /monitoring/summary...")
    try:
        response = requests.get(f"{base_url}/monitoring/summary", timeout=5)
        if response.status_code == 200:
            print("   [OK] Summary retrieved")
            data = response.json()
            if "message" in data:
                print(f"   {data['message']}")
            else:
                print(f"   Average training loss: {data.get('average_training_loss')}")
                print(f"   Latest training loss: {data.get('latest_training_loss')}")
        else:
            print(f"   [FAIL] Summary request failed: {response.status_code}")
    except Exception as e:
        print(f"   [ERROR] {e}")
    
    print()
    return True


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test monitoring API")
    parser.add_argument("--server-url", type=str, default="http://localhost:8082",
                       help="Server monitoring API URL")
    parser.add_argument("--client-url", type=str, default="http://localhost:8081",
                       help="Client monitoring API URL")
    parser.add_argument("--server-only", action="store_true",
                       help="Test only server monitoring")
    parser.add_argument("--client-only", action="store_true",
                       help="Test only client monitoring")
    args = parser.parse_args()
    
    success = True
    
    if not args.client_only:
        print("\n")
        if not test_server_monitoring(args.server_url):
            success = False
    
    if not args.server_only:
        print("\n")
        if not test_client_monitoring(args.client_url):
            success = False
    
    print("=" * 70)
    if success:
        print("Monitoring API Testing Complete")
    else:
        print("Some tests failed")
    print("=" * 70)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

