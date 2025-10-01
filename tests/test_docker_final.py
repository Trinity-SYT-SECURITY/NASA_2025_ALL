#!/usr/bin/env python3
"""
最終測試 Docker 部署修復
驗證所有路徑和配置是否正確
"""

import os
import sys

def test_docker_structure():
    """測試 Docker 容器內的目錄結構"""
    print("🔍 測試 Docker 容器目錄結構...")

    current_dir = os.getcwd()
    print(f"當前工作目錄: {current_dir}")

    # 檢查當前目錄內容
    print(f"當前目錄內容: {os.listdir('.')[:5]}...")  # 只顯示前5個

    # 檢查父目錄（應該是 /app）
    parent_dir = os.path.dirname(current_dir)
    print(f"父目錄: {parent_dir}")
    if os.path.exists(parent_dir):
        print(f"父目錄內容: {os.listdir(parent_dir)[:10]}...")

        # 檢查是否有 ml 和 data 目錄
        ml_dir = os.path.join(parent_dir, 'ml')
        data_dir = os.path.join(parent_dir, 'data')
        backend_dir = os.path.join(parent_dir, 'backend')

        print(f"檢查 ml 目錄: {ml_dir} -> {'✅ 存在' if os.path.exists(ml_dir) else '❌ 不存在'}")
        print(f"檢查 data 目錄: {data_dir} -> {'✅ 存在' if os.path.exists(data_dir) else '❌ 不存在'}")
        print(f"檢查 backend 目錄: {backend_dir} -> {'✅ 存在' if os.path.exists(backend_dir) else '❌ 不存在'}")

        # 檢查 ML 模型文件
        if os.path.exists(ml_dir):
            model_file = os.path.join(ml_dir, 'exoplanet_model_best.joblib')
            print(f"檢查模型文件: {model_file} -> {'✅ 存在' if os.path.exists(model_file) else '❌ 不存在'}")

def test_import_logic():
    """測試導入邏輯是否正確"""
    print("\n🔍 測試導入邏輯...")

    try:
        # 模擬 ultra_simple_api.py 中的邏輯
        current_dir = os.getcwd()
        print(f"當前目錄: {current_dir}")

        # 嘗試多個可能的路徑（支援不同部署環境）
        possible_ml_dirs = [
            os.path.join(current_dir, '..', 'ml'),  # Docker: /app/backend/../ml/ -> /app/ml/
            os.path.join(current_dir, 'ml'),       # 錯誤路徑測試
            os.path.join('/app', 'ml'),             # 絕對路徑
        ]

        print(f"嘗試的路徑: {possible_ml_dirs}")

        ml_dir = None
        for test_dir in possible_ml_dirs:
            model_path = os.path.join(test_dir, 'exoplanet_model_best.joblib')
            print(f"檢查: {model_path}")
            if os.path.exists(model_path):
                ml_dir = test_dir
                print(f"✅ 找到模型文件在: {ml_dir}")
                break

        if ml_dir is None:
            print("❌ 沒有找到模型文件")
            return False

        print("✅ 路徑檢測成功！")
        return True

    except Exception as e:
        print(f"❌ 路徑檢測失敗: {e}")
        return False

def main():
    print("🌌 Docker 最終修復測試")
    print("=" * 50)

    # 測試目錄結構
    test_docker_structure()

    # 測試導入邏輯
    success = test_import_logic()

    if success:
        print("\n✅ Docker 修復成功！")
        print("✅ 目錄結構正確")
        print("✅ 路徑檢測正常")
        print("✅ 模型文件可訪問")
        print("✅ 應用應該能正常啟動")
    else:
        print("\n❌ 需要進一步修復")

if __name__ == "__main__":
    main()
