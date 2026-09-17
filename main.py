import os
import sys

def evaluate_readme():
    readme_path = "README.md"
    
    if not os.path.exists(readme_path):
        print("Error: README.md not found in the repository!")
        sys.exit(1)
        
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # المعايير الأساسية الـ 7 (فحص سريع لوجود الأقسام أو الكلمات المفتاحية)
    checks = {
        "Project Title": "#" in content,
        "Description": "Description" in content or "about" in content.lower() or len(content) > 100,
        "Installation": "install" in content.lower() or "setup" in content.lower(),
        "Usage": "usage" in content.lower() or "how to" in content.lower(),
        "Features": "feature" in content.lower() or "مميزات" in content,
        "Contributing": "contributing" in content.lower(),
        "License": "license" in content.lower()
    }
    
    score = sum(1 for passed in checks.values() if passed) * (100 / 7)
    
    print("=== ReadmeRank Automated Audit ===")
    print(f"Overall Score: {score:.1f}/100\n")
    print("Detailed Checks:")
    for section, passed in checks.items():
    status = "✅ Passed" if found else "❌ Missing"
    
        print(f"- {section}: {status}")
        
    if score < 50:
        print("\nRecommendation: Your README needs significant improvement to attract developers.")
    else:
        print("\nRecommendation: Great job! Your README looks solid.")

if __name__ == "__main__":
    evaluate_readme()
  
