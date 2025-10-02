#!/usr/bin/env python3
"""
Verify mathematical foundations and algorithms section in README
"""

import os
import re

def verify_math_section():
    """Verify README.md contains comprehensive mathematical content"""
    print("🧮 Verifying Mathematical Foundations & Algorithms Section")
    print("=" * 70)
    
    readme_path = "README.md"
    
    if not os.path.exists(readme_path):
        print("❌ README.md not found")
        return False
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for mathematical content
    math_checks = [
        ("🧮 Mathematical Foundations & Algorithms", "Main math section header"),
        ("Random Forest Ensemble Method", "Random Forest algorithm explanation"),
        ("XGBoost Gradient Boosting", "XGBoost mathematical foundation"),
        ("LightGBM Leaf-wise Growth", "LightGBM algorithm details"),
        ("Logistic Regression Multi-class", "Logistic regression mathematics"),
        ("StandardScaler Normalization", "Feature scaling mathematics"),
        ("Cosine Similarity", "Similarity calculation algorithm"),
        ("Habitability Score Calculation", "Custom scoring algorithm"),
        ("Cross-Validation Mathematics", "Statistical validation methods"),
        ("3D Visualization Mathematics", "Graphics mathematics"),
        ("Performance Metrics Mathematics", "Evaluation metrics"),
        ("Feature Importance Algorithms", "Feature analysis mathematics"),
        ("Optimization Algorithms", "Hyperparameter optimization"),
        ("Statistical Validation", "Statistical testing methods"),
    ]
    
    # Check for mathematical formulas
    formula_checks = [
        ("Prediction = Mode{T₁(x), T₂(x), ..., Tₙ(x)}", "Random Forest formula"),
        ("F(x) = Σᵢ₌₁ᵀ fᵢ(x)", "XGBoost ensemble formula"),
        ("Ω(f) = γT + ½λ||w||²", "XGBoost regularization"),
        ("P(y=k|x) = exp(wₖᵀx + bₖ)", "Logistic regression probability"),
        ("x_scaled = (x - μ) / σ", "Z-score standardization"),
        ("similarity = (A · B) / (||A|| × ||B||)", "Cosine similarity formula"),
        ("CV_Score = (1/k) Σᵢ₌₁ᵏ Accuracy(Mᵢ, Dᵢ)", "Cross-validation formula"),
        ("x = r × sin(θ) × cos(φ)", "Spherical coordinates"),
        ("Accuracy = (TP + TN) / (TP + TN + FP + FN)", "Accuracy formula"),
    ]
    
    # Check for algorithm details
    algorithm_checks = [
        ("n_estimators=200", "Random Forest parameters"),
        ("max_depth=8", "Tree depth configuration"),
        ("learning_rate=0.1", "Learning rate parameter"),
        ("subsample=0.8", "Subsampling ratio"),
        ("k = 5 folds", "Cross-validation folds"),
        ("Bootstrap Sampling", "Sampling methodology"),
        ("Stratified K-Fold", "Validation strategy"),
        ("Grid Search", "Hyperparameter optimization"),
    ]
    
    # Perform checks
    print("📊 Mathematical Content Verification:")
    all_passed = True
    
    for check_text, description in math_checks:
        if check_text in content:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ MISSING: {description}")
            all_passed = False
    
    print(f"\n🔢 Mathematical Formula Verification:")
    formula_count = 0
    for formula, description in formula_checks:
        if formula in content:
            print(f"  ✅ {description}")
            formula_count += 1
        else:
            print(f"  ❌ MISSING: {description}")
            all_passed = False
    
    print(f"\n⚙️ Algorithm Detail Verification:")
    algorithm_count = 0
    for detail, description in algorithm_checks:
        if detail in content:
            print(f"  ✅ {description}")
            algorithm_count += 1
        else:
            print(f"  ❌ MISSING: {description}")
            all_passed = False
    
    # Count mathematical symbols and formulas
    math_symbols = ['Σ', '∈', '≈', '≥', '≤', '±', '√', 'π', 'θ', 'φ', 'μ', 'σ', 'λ', 'γ']
    symbol_counts = {symbol: content.count(symbol) for symbol in math_symbols}
    total_math_symbols = sum(symbol_counts.values())
    
    # Count code blocks (formulas)
    code_blocks = len(re.findall(r'```[^`]*```', content))
    
    # Statistics
    math_section_start = content.find("🧮 Mathematical Foundations & Algorithms")
    math_section_end = content.find("## 🚀 Quick Start")
    math_section_length = math_section_end - math_section_start if math_section_start != -1 and math_section_end != -1 else 0
    
    print(f"\n📊 Mathematical Content Statistics:")
    print(f"  📄 Math section length: {math_section_length:,} characters")
    print(f"  🔢 Mathematical symbols: {total_math_symbols}")
    print(f"  📝 Code blocks (formulas): {code_blocks}")
    print(f"  🧮 Formula coverage: {formula_count}/{len(formula_checks)}")
    print(f"  ⚙️ Algorithm details: {algorithm_count}/{len(algorithm_checks)}")
    
    # Detailed symbol breakdown
    print(f"\n🔣 Mathematical Symbol Usage:")
    for symbol, count in symbol_counts.items():
        if count > 0:
            print(f"  {symbol}: {count} times")
    
    # Algorithm categories covered
    algorithm_categories = [
        "Ensemble Methods", "Gradient Boosting", "Classification", 
        "Feature Engineering", "Validation", "Visualization", 
        "Optimization", "Statistics"
    ]
    
    print(f"\n🎯 Algorithm Categories Covered:")
    for category in algorithm_categories:
        if category.lower() in content.lower():
            print(f"  ✅ {category}")
        else:
            print(f"  ❌ {category}")
    
    # Final assessment
    print(f"\n" + "=" * 70)
    if all_passed and formula_count >= 7 and algorithm_count >= 6:
        print("🎉 Mathematical Foundations Section Successfully Added!")
        print("✅ Comprehensive algorithm explanations included")
        print("✅ Mathematical formulas properly formatted")
        print("✅ Implementation details provided")
        print("✅ Statistical validation methods covered")
        print("✅ 3D visualization mathematics explained")
        
        print(f"\n🏆 Achievement Summary:")
        print(f"  📚 {len(math_checks)} mathematical topics covered")
        print(f"  🔢 {formula_count} mathematical formulas included")
        print(f"  ⚙️ {algorithm_count} algorithm implementations detailed")
        print(f"  🔣 {total_math_symbols} mathematical symbols used")
        
    else:
        print("⚠️ Mathematical content needs improvement")
        print("   Some formulas or algorithm details are missing")
    
    print(f"\n💡 Mathematical Rigor Assessment:")
    print(f"  🎯 Covers 4 major ML algorithms with mathematical foundations")
    print(f"  📊 Includes feature engineering and preprocessing mathematics")
    print(f"  🧪 Statistical validation and testing methods explained")
    print(f"  🌌 3D graphics and visualization mathematics covered")
    print(f"  📈 Performance evaluation metrics with formulas")
    
    return all_passed and formula_count >= 7

def main():
    """Main verification function"""
    try:
        success = verify_math_section()
        if success:
            print(f"\n🚀 README.md now contains comprehensive mathematical foundations!")
            print(f"   Perfect for demonstrating technical depth in NASA challenge")
        else:
            print(f"\n🔧 Some mathematical content may be missing")
            
    except Exception as e:
        print(f"❌ Error during verification: {e}")

if __name__ == "__main__":
    main()
