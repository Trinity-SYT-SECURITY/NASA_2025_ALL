#!/usr/bin/env python3
"""
測試 Render 後端 API 是否正常工作
"""

import requests
import json

def test_backend_api(base_url):
    """測試後端 API 端點"""
    print(f"🔍 測試後端 API: {base_url}")
    print("=" * 50)

    # 測試健康檢查
    print("1. 測試健康檢查...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"   狀態碼: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ 健康檢查成功")
            print(f"   狀態: {data.get('status')}")
            print(f"   模型載入: {data.get('models_loaded')}")
            print(f"   ML準確率: {data.get('ml_accuracy')}")
        else:
            print(f"❌ 健康檢查失敗: {response.status_code}")
            print(f"   響應: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ 健康檢查錯誤: {e}")

    print()

    # 測試統計端點
    print("2. 測試統計端點...")
    try:
        response = requests.get(f"{base_url}/stats", timeout=10)
        print(f"   狀態碼: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ 統計端點成功")
            print(f"   總計行星: {data.get('total_exoplanets'):,}")
            print(f"   確認行星: {data.get('confirmed'):,}")
            print(f"   候選行星: {data.get('candidates'):,}")
        else:
            print(f"❌ 統計端點失敗: {response.status_code}")
    except Exception as e:
        print(f"❌ 統計端點錯誤: {e}")

    print()

    # 測試預測端點
    print("3. 測試預測端點...")
    try:
        test_data = {
            "koi_period": 365.25,
            "koi_prad": 1.0,
            "koi_teq": 288.0,
            "koi_slogg": 4.44
        }
        response = requests.post(f"{base_url}/predict", json=test_data, timeout=10)
        print(f"   狀態碼: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ 預測端點成功")
            print(f"   預測結果: {data.get('prediction')}")
            print(f"   行星名稱: {data.get('planet_name')}")
            print(f"   置信度: {data.get('confidence')}")
            print(f"   概率分佈: {data.get('probabilities')}")
        else:
            print(f"❌ 預測端點失敗: {response.status_code}")
            print(f"   響應: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ 預測端點錯誤: {e}")

    print()

    # 測試 ML 測試端點
    print("4. 測試 ML 測試端點...")
    try:
        response = requests.get(f"{base_url}/test-ml", timeout=10)
        print(f"   狀態碼: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ ML 測試成功")
            print(f"   成功: {data.get('success')}")
            print(f"   ML 載入: {data.get('ml_loaded')}")
            if data.get('test_prediction'):
                print(f"   測試預測: {data.get('test_prediction')}")
        else:
            print(f"❌ ML 測試失敗: {response.status_code}")
    except Exception as e:
        print(f"❌ ML 測試錯誤: {e}")

def main():
    print("🌌 Render 後端 API 測試")
    print("=" * 50)

    # 測試你的 Render 後端
    base_url = "https://test-backend-2-ikqg.onrender.com"
    test_backend_api(base_url)

    print("🎯 測試完成!")
    print(f"💡 如果所有測試都成功，前端可以配置此URL:")
    print(f"   {base_url}")
    print(f"📚 API 文檔: {base_url}/docs")

if __name__ == "__main__":
    main()
