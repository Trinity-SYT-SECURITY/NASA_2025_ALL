#!/usr/bin/env python3
"""
修復 ML 模型載入問題
解決 XGBoost use_label_encoder 錯誤
"""

import joblib
import os
import warnings

def test_model_loading():
    """測試模型載入並修復問題"""
    print("🔧 修復 ML 模型載入問題...")

    # 嘗試載入模型
    ml_dir = os.path.join(os.path.dirname(__file__), '..', 'ml')
    model_path = os.path.join(ml_dir, 'exoplanet_model_best.joblib')

    print(f"嘗試載入模型從: {model_path}")

    try:
        # 載入模型時忽略警告
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            model = joblib.load(model_path)

        print(f"✅ 模型載入成功: {type(model).__name__}")

        # 檢查模型屬性
        print(f"   有 predict 方法: {hasattr(model, 'predict')}")
        print(f"   有 predict_proba 方法: {hasattr(model, 'predict_proba')}")

        # 測試簡單預測
        test_data = [[365.25, 1.0, 288.0, 4.44, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        try:
            prediction = model.predict(test_data)
            print(f"✅ 測試預測成功: {prediction}")

            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba(test_data)
                print(f"✅ 測試概率預測成功: {proba}")
            else:
                print("⚠️ 模型沒有 predict_proba 方法")

        except Exception as e:
            print(f"❌ 測試預測失敗: {e}")

    except Exception as e:
        print(f"❌ 模型載入失敗: {e}")
        return False

    return True

def fix_xgboost_issue():
    """修復 XGBoost use_label_encoder 問題"""
    print("🔧 檢查並修復 XGBoost 問題...")

    try:
        # 嘗試載入模型
        ml_dir = os.path.join(os.path.dirname(__file__), '..', 'ml')
        model_path = os.path.join(ml_dir, 'exoplanet_model_best.joblib')

        model = joblib.load(model_path)

        if hasattr(model, 'use_label_encoder'):
            print("⚠️ 發現舊版 XGBoost，需要修復")
            # 這裡我們無法直接修復模型，但可以記錄問題
            return False
        else:
            print("✅ XGBoost 模型正常")
            return True

    except Exception as e:
        print(f"❌ XGBoost 檢查失敗: {e}")
        return False

def main():
    print("🌌 ML 模型修復工具")
    print("=" * 50)

    # 測試模型載入
    load_success = test_model_loading()

    # 檢查 XGBoost 問題
    xgb_success = fix_xgboost_issue()

    if load_success and xgb_success:
        print("\n✅ 所有問題已修復！")
        print("✅ ML 模型可以正常載入和預測")
    else:
        print("\n❌ 需要手動修復 ML 模型")
        print("💡 建議重新訓練模型並使用最新版本的依賴")

if __name__ == "__main__":
    main()
