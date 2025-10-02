#!/usr/bin/env python3
"""
Verify README.md updates and ML chart integration
"""

import os

def verify_readme_update():
    """Verify README.md has been properly updated"""
    print("📝 Verifying README.md Updates")
    print("=" * 60)
    
    readme_path = "README.md"
    ml_charts_dir = "ml_charts"
    
    # Check README exists
    if not os.path.exists(readme_path):
        print("❌ README.md not found")
        return False
    
    # Read README content
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check key sections
    checks = [
        ("🏆 NASA Space Apps Challenge 2025", "Challenge section updated"),
        ("✅ Challenge Requirements Fulfilled", "Requirements table added"),
        ("🤖 Advanced Machine Learning System", "ML section enhanced"),
        ("![Model Performance Comparison](ml_charts/03_model_performance.png)", "ML charts integrated"),
        ("![Dataset Overview](ml_charts/01_dataset_overview.png)", "Dataset charts included"),
        ("![Feature Importance](ml_charts/05_feature_importance.png)", "Feature importance chart"),
        ("92.4% accuracy", "Updated accuracy metrics"),
        ("Render.com", "Updated deployment info"),
        ("Streamlit", "Streamlit references (should be removed)"),
        ("🏆 Our Comprehensive Challenge Solution", "Challenge solution summary"),
        ("💪 What We Accomplished", "Accomplishments section"),
    ]
    
    results = []
    for check_text, description in checks:
        if check_text in content:
            if "Streamlit" in check_text:
                # This should NOT be found (removed)
                results.append((description, "❌ FOUND (should be removed)", False))
            else:
                results.append((description, "✅ FOUND", True))
        else:
            if "Streamlit" in check_text:
                # This should NOT be found (good)
                results.append((description, "✅ REMOVED", True))
            else:
                results.append((description, "❌ MISSING", False))
    
    # Check ML charts exist
    ml_charts = [
        "01_dataset_overview.png",
        "02_classification_distribution.png", 
        "03_model_performance.png",
        "04_confusion_matrix.png",
        "05_feature_importance.png",
        "06_learning_curves.png",
        "07_roc_curves.png",
        "08_training_progress.png"
    ]
    
    print("📊 ML Charts Verification:")
    chart_results = []
    for chart in ml_charts:
        chart_path = os.path.join(ml_charts_dir, chart)
        if os.path.exists(chart_path):
            chart_results.append((chart, "✅ EXISTS", True))
        else:
            chart_results.append((chart, "❌ MISSING", False))
    
    # Print results
    print("\n📝 README Content Verification:")
    all_good = True
    for desc, status, success in results:
        print(f"  {status} {desc}")
        if not success:
            all_good = False
    
    print(f"\n📊 ML Charts Status:")
    for chart, status, success in chart_results:
        print(f"  {status} {chart}")
        if not success:
            all_good = False
    
    # Summary statistics
    readme_word_count = len(content.split())
    ml_section_start = content.find("🤖 Advanced Machine Learning System")
    ml_section_end = content.find("## 🚀 Quick Start")
    ml_section_length = ml_section_end - ml_section_start if ml_section_start != -1 and ml_section_end != -1 else 0
    
    print(f"\n📊 README Statistics:")
    print(f"  📄 Total word count: {readme_word_count:,} words")
    print(f"  🤖 ML section length: {ml_section_length:,} characters")
    print(f"  📈 Chart references: {content.count('![')}")
    print(f"  🏆 Challenge references: {content.count('challenge')}")
    
    # Final assessment
    print(f"\n" + "=" * 60)
    if all_good:
        print("🎉 README.md successfully updated!")
        print("✅ All ML charts integrated")
        print("✅ Challenge requirements highlighted") 
        print("✅ Streamlit references removed")
        print("✅ Comprehensive documentation complete")
    else:
        print("⚠️ Some issues found - please review above")
    
    print(f"\n💡 Next Steps:")
    print(f"  1. Review the updated README.md")
    print(f"  2. Check all ML charts are displaying correctly")
    print(f"  3. Verify challenge requirements are clearly addressed")
    print(f"  4. Ensure production URLs are accurate")
    
    return all_good

def main():
    """Main verification function"""
    try:
        success = verify_readme_update()
        if success:
            print(f"\n🚀 README.md is ready for the NASA Space Apps Challenge!")
        else:
            print(f"\n🔧 Please address the issues above before submission.")
            
    except Exception as e:
        print(f"❌ Error during verification: {e}")

if __name__ == "__main__":
    main()
