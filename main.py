import os

def evaluate_readme():
    readme_path = "README.md"
    
    if not os.path.exists(readme_path):
        print(f"Error: {readme_path} not found.")
        return

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # فحص سريع لوجود الأقسام أو الكلمات المفتاحية
    checks = {
        "Project Title": "#" in content,
        "Description": "Description" in content or "about" in content.lower(),
        "Installation": "install" in content.lower(),
        "Usage": "usage" in content.lower() or "how to" in content.lower(),
        "Features": "feature" in content.lower() or "highlights" in content.lower(),
        "Contributing": "contributing" in content.lower(),
        "License": "license" in content.lower()
    }

    score = sum(1 for passed in checks.values() if passed) / len(checks) * 100

    print("=== ReadmeRank Automated Audit ===")
    print(f"Overall Score: {score:.1f}/100\n")
    print("Detailed Checks:")
    
    for section, passed in checks.items():
        status = "✅ Passed" if passed else "❌ Missing"
        print(f"- {section}: {status}")

    if score < 50:
        print("\nRecommendation: Your README needs significant improvements!")
    else:
        print("\nRecommendation: Great job! Your README looks solid.")

if __name__ == "__main__":
    evaluate_readme()
  
