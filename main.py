import os
import requests

# ========================================================
# دالة الاتصال بـ GitHub Models (مع التعديل الصحيح للرابط)
# ========================================================
def call_github_model(prompt_text):
        url = "https://models.inference.ai.azure.com/chat/completions"
    
    
    github_token = os.environ.get("GITHUB_TOKEN")
    
    if not github_token:
        print("Warning: GITHUB_TOKEN not found.")
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
                "content": "You are an expert developer and technical writer. Your task is to provide brief, professional, and actionable recommendations to improve project README files."
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
            return f"AI Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"AI Connection Error: {str(e)}"

# ========================================================
# الكود الأساسي لأداتك مضافاً إليه الذكاء الاصطناعي
# ========================================================
def evaluate_readme():
    readme_path = "README.md"
    
    if not os.path.exists(readme_path):
        print(f"Error: {readme_path} not found.")
        return

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read().lower()

    # فحص الأقسام أو الكلمات المفتاحية
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

    # لإعطاء توصيات ذكية واحترافية بناء على النتيجة
    print("\n🤖 AI-Powered Recommendations:")
    
    prompt = f"""
My project README scored {percentage:.1f}/100 in an automated audit.
The missing sections are: {', '.join(missing_sections) if missing_sections else 'None'}.
Write a brief, engaging, and professional set of recommendations to improve this README and make the project stand out.
"""

    ai_recommendation = call_github_model(prompt)
    if ai_recommendation:
        print(ai_recommendation)
    else:
        if score < 50:
            print("Your README needs significant improvements to attract contributors and users.")
        else:
            print("Great job! Your README is solid, but adding the missing sections will make it even better.")

if __name__ == "__main__":
    evaluate_readme()
  
