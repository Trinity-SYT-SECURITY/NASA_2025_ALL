#!/usr/bin/env python3
"""
測試總覽腳本
運行所有測試並生成報告
"""

import subprocess
import sys
import os
from pathlib import Path

def run_test(test_file, description):
    """運行單個測試並報告結果"""
    print(f"\n🔍 {description}")
    print("=" * 50)

    try:
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            print("✅ 測試通過")
            return True, result.stdout
        else:
            print("❌ 測試失敗")
            print(f"錯誤輸出:\n{result.stderr}")
            return False, result.stderr

    except subprocess.TimeoutExpired:
        print("❌ 測試超時")
        return False, "Test timed out"
    except Exception as e:
        print(f"❌ 測試錯誤: {e}")
        return False, str(e)

def main():
    print("🌌 Exoplanet AI Platform - 完整測試套件")
    print("=" * 60)

    # 獲取測試目錄
    test_dir = Path(__file__).parent

    # 定義測試套件
    test_suite = [
        ("test_ml_training_analysis.py", "ML 訓練結果分析"),
        ("test_backend_api.py", "後端 API 測試"),
        ("test_docker_final.py", "Docker 部署測試"),
        ("fix_ml_model.py", "ML 模型修復測試"),
    ]

    results = []
    total_passed = 0

    for test_file, description in test_suite:
        test_path = test_dir / test_file
        if test_path.exists():
            success, output = run_test(str(test_path), description)
            results.append((test_file, success, description))
            if success:
                total_passed += 1
        else:
            print(f"\n⚠️ 測試文件不存在: {test_file}")
            results.append((test_file, False, description))

    # 生成測試報告
    print(f"\n📊 測試報告總結")
    print("=" * 60)

    total_tests = len(results)
    passed_tests = sum(1 for _, success, _ in results if success)

    print(f"總測試數: {total_tests}")
    print(f"通過測試: {passed_tests}")
    print(f"失敗測試: {total_tests - passed_tests}")
    print(f"成功率: {(passed_tests/total_tests)*100:.1f}%".1f"    # 詳細結果
    print("
詳細結果:"    for test_file, success, description in results:
        status = "✅" if success else "❌"
        print(f"  {status} {description}")

        if not success:
            print(f"    文件: {test_file}")

    # 最終判斷
    if passed_tests == total_tests:
        print("
🎉 所有測試通過！平台準備就緒。"        return 0
    else:
        print("
⚠️ 部分測試失敗，需要修復。"        return 1

if __name__ == "__main__":
    sys.exit(main())
