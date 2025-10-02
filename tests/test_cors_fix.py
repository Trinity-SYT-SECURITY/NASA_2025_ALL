#!/usr/bin/env python3
"""
Test script to verify CORS fix
"""

import requests
import json

def test_cors_headers():
    """Test CORS headers on Render backend"""
    print("🔧 Testing CORS Headers on Render Backend")
    print("=" * 60)
    
    api_url = "https://test-backend-2-ikqg.onrender.com"
    
    # Test different endpoints
    endpoints = [
        "/health",
        "/stats", 
        "/exoplanets",
        "/test-ml"
    ]
    
    for endpoint in endpoints:
        print(f"\n🔍 Testing endpoint: {endpoint}")
        
        try:
            # Make a request with Origin header to simulate CORS
            headers = {
                'Origin': 'https://nasa-2025-frontend-4ksyd0yih-memes-projects-e276d7bb.vercel.app',
                'Accept': 'application/json'
            }
            
            response = requests.get(f"{api_url}{endpoint}", headers=headers, timeout=10)
            
            print(f"   Status: {response.status_code}")
            
            # Check CORS headers
            cors_headers = {
                'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
                'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
                'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
                'Access-Control-Allow-Credentials': response.headers.get('Access-Control-Allow-Credentials')
            }
            
            print(f"   CORS Headers:")
            for header, value in cors_headers.items():
                if value:
                    print(f"     {header}: {value}")
                else:
                    print(f"     {header}: ❌ Missing")
            
            if response.status_code == 200:
                print(f"   ✅ Endpoint accessible")
            else:
                print(f"   ❌ Endpoint error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Request failed: {e}")
    
    # Test OPTIONS request (preflight)
    print(f"\n🔍 Testing CORS preflight (OPTIONS):")
    try:
        headers = {
            'Origin': 'https://nasa-2025-frontend-4ksyd0yih-memes-projects-e276d7bb.vercel.app',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        
        response = requests.options(f"{api_url}/predict", headers=headers, timeout=10)
        
        print(f"   Status: {response.status_code}")
        print(f"   Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', '❌ Missing')}")
        print(f"   Allow-Methods: {response.headers.get('Access-Control-Allow-Methods', '❌ Missing')}")
        
    except Exception as e:
        print(f"   ❌ OPTIONS request failed: {e}")
    
    print("\n" + "=" * 60)
    print("📊 CORS TEST RESULTS")
    print("=" * 60)
    print("✅ If all endpoints show 'Access-Control-Allow-Origin: *'")
    print("✅ Frontend should be able to access the API")
    print("❌ If CORS headers are missing, there's a configuration issue")

if __name__ == "__main__":
    test_cors_headers()
