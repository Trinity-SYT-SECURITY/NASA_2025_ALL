#!/usr/bin/env python3
"""
簡單測試Streamlit應用程式的API回應
"""

import requests
import json

def test_api():
    url = 'https://appcloudapppy-4s5dd8txmtmq9kedpyebrj.streamlit.app/?endpoint=health'

    try:
        print(f"測試URL: {url}")
        response = requests.get(url, timeout=10)

        print(f"狀態碼: {response.status_code}")
        print(f"內容類型: {response.headers.get('content-type', '')}")

        if response.status_code == 200:
            if 'application/json' in response.headers.get('content-type', ''):
                try:
                    data = response.json()
                    print("✅ 返回JSON格式！")
                    print("回應內容:")
                    print(json.dumps(data, indent=2))
                    return True
                except:
                    print("❌ 不是有效的JSON格式")
                    print("回應預覽:", response.text[:200])
                    return False
            else:
                print("❌ 不是JSON格式")
                print("回應預覽:", response.text[:200])
                return False
        else:
            print(f"❌ HTTP錯誤: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ 請求失敗: {e}")
        return False

if __name__ == "__main__":
    print("🌌 Streamlit API簡單測試")
    print("=" * 40)

    success = test_api()

    if success:
        print("\n🎉 測試通過！Streamlit應用程式可以作為後端使用")
    else:
        print("\n❌ 測試失敗，可能需要重新部署應用程式")
