import os
import requests

# ==========================================
# دالة الاتصال بـ GitHub Models (الذكاء الاصطناعي المجاني)
# ==========================================
def call_github_model(prompt_text):
    url = "https://models.inference.ai.azure.com/chat/completions"
    github_token = os.environ.get("GITHUB_TOKEN")
    
    if not github_token:
        print("Warning: GITHUB_TOKEN is missing. AI recommendations will be skipped.")
        return None
    
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "You are an expert open-source developer and technical writer. Provide short, encouraging, and highly professional recommendations to improve a project's README."
            },
            {
                "role": "user",
                "content": prompt_text
            }
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"AI Error: {response.status_code}"
    except Exception as e:
        return f"AI Connection Error: {str(e)}"


# ==========================================
# الكود الأساسي لأداتك مضافاً إليه الذكاء الاصطناعي
# ==========================================
def evaluate_readme():
    readme_path = "README.md"

    if not os.path.exists(readme_path):
        print(f"Error: {readme_path} not found!")
        return

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # فحص الأقسام أو الكلمات المفتاحية
    checks = {
        "Project Title": "#" in content,
        "Description": "description" in content.lower(),
        "Installation": "install" in content.lower(),
        "Usage": "usage" in content.lower(),
        "Features": "feature" in content.lower(),
        "Contributing": "contributing" in content.lower(),
        "License": "license" in content.lower()
    }

    score = sum(1 for passed in checks.values() if passed) * (100 / len(checks))

    print("=== ReadMeRank Automated Audit ===")
    print(f"Overall Score: {score:.1f}/100")
    print("Detailed Checks:")

    missing_sections = []
    for section, passed in checks.items():
        status = "✅ Passed" if passed else "❌ Missing"
        print(f"- {section}: {status}")
        if not passed:
            missing_sections.append(section)

    # استخدام الذكاء الاصطناعي لإعطاء توصيات ذكية واحترافية بناءً على النتيجة
    print("\n🤖 AI-Powered Recommendations:")
    
    prompt = f"""
    My project README scored {score:.1f}/100 on ReadMeRank.
    The missing sections are: {', '.join(missing_sections) if missing_sections else 'None'}.
    Write a brief, engaging, and professional recommendation encouraging the developer to fix these missing parts to attract more stars and users.
    """
    
    ai_recommendation = call_github_model(prompt)
    if ai_recommendation:
        print(ai_recommendation)
    else:
        if score < 50:
            print("Your README needs significant improvements to attract more users.")
        else:
            print("Great job! Your README looks solid.")


if __name__ == "__main__":
    evaluate_readme()
  
