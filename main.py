import os

def evaluate_readme():
    readme_path = "README.md"
    
    if not os.path.exists(readme_path):
        print(f"Error: {readme_path} not found.")
        return

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read().lower()

    # فحص الأقسام الأساسية في ملف الـ README
    checks = {
        "Project Title": "#" in content,
        "Description": "description" in content or "about" in content,
        "Installation": "install" in content or "setup" in content,
        "Usage": "usage" in content or "how to use" in content,
        "Features": "feature" in content,
        "Contributing": "contributing" in content,
        "License": "license" in content
    }

    score = sum(1 for passed in checks.values() if passed)
    total = len(checks)
    percentage = (score / total) * 100

    print("=== ReadMeRank Automated Audit ===")
    print(f"Overall Score: {percentage:.1f}/100")
    print("Detailed Checks:")

    missing_sections = []
    for section, passed in checks.items():
        status = "✅ Passed" if passed else "❌ Missing"
        print(f"- {section}: {status}")
        if not passed:
            missing_sections.append(section)

    print("\n🤖 Smart AI-Powered Recommendations:")
    
    if missing_sections:
        print(f"Your project README scored {percentage:.1f}/100.")
        print(f"To make your project stand out and attract more users and contributors, please add the following missing sections: {', '.join(missing_sections)}.")
        print("💡 Tip: A great README should clearly explain what the project does, how to install it, and how to use it with clear examples.")
    else:
        print("🎉 Outstanding! Your README includes all essential sections and looks professional.")

if __name__ == "__main__":
    evaluate_readme()
  
