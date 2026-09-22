import os
import requests
import json

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPOSITORY = os.environ.get("GITHUB_REPOSITORY")  # بيجيب اسم المستودع تلقائياً مثل: am9044048-hue/ReadmeRank
API_URL = "https://models.inference.ai.azure.com/chat/completions"

def generate_marketing_content():
    if not GITHUB_TOKEN:
        print("Error: GITHUB_TOKEN is not available.")
        return

    repo_url = f"https://github.com/{REPOSITORY}" if REPOSITORY else "https://github.com"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    أنت مدير تسويق إلكتروني محترف وخبير في نمو البرمجيات ومشاريع الـ Open Source.
    لدينا أداة برمجية جديدة ومميزة لتطوير وفحص ملفات الـ README لزيادة احترافية المشاريع.
    رابط المشروع على جيت هب هو: {repo_url}
    
    قم بتوليد حزمة تسويقية احترافية تشمل:
    1. منشور (Post) جذاب ومحترف لمنصة LinkedIn يشرح أهمية الأداة مع وضع رابط المشروع في نهايته بدقة.
    2. تغريدة (Tweet/Thread) حماسية وسريعة لمنصة X مع وضع الرابط.
    3. قائمة بأفضل الهاشتاجات (Hashtags) والكلمات الدلالية التي تجلب أعلى مشاهدات وتفاعل.
    
    اجعل المحتوى باللغة العربية الفصحى وبأسلوب تسويقي مشوق ومحترف، وتأكد من إدراج رابط المشروع بوضوح في نهاية المنشورات.
    """

    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": "You are an expert AI marketing agent."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            print("=== 🤖 Marketing Agency Generated Content ===")
            print(content)
            
            with open("marketing_output.md", "w", encoding="utf-8") as f:
                f.write(content)
            print("\nSuccessfully generated and saved marketing content with the repository link!")
        else:
            print(f"Failed to generate content: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    generate_marketing_content()
      
