import os
import requests
import json

# قراءة توكن جيت هب المتاح تلقائياً في البيئة
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
# استخدام نموذج ذكاء اصطناعي قوي من GitHub Models
API_URL = "https://models.inference.ai.azure.com/chat/completions"

def generate_marketing_content():
    if not GITHUB_TOKEN:
        print("Error: GITHUB_TOKEN is not available.")
        return

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json"
    }

    prompt = """
    أنت مدير تسويق إلكتروني محترف وخبير في نمو البرمجيات ومشاريع الـ Open Source.
    لدينا أداة برمجية جديدة ومميزة لتطوير وفحص ملفات الـ README لزيادة احترافية المشاريع.
    قم بتوليد حزمة تسويقية احترافية تشمل:
    1. منشور (Post) جذاب ومحترف لمنصة LinkedIn يشرح أهمية الأداة وكيف تساعد المطورين.
    2. تغريدة (Tweet/Thread) حماسية وسريعة لمنصة X.
    3. قائمة بأفضل الهاشتاجات (Hashtags) والكلمات الدلالية التي تجلب أعلى مشاهدات وتفاعل.
    اجعل المحتوى باللغة العربية الفصحى وبأسلوب تسويقي مشوق ومحترف.
    """

    payload = {
        "model": "gpt-4o",  # أو النموذج المتاح في GitHub Models
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
            
            # حفظ المحتوى المولد في ملف نصي عشان الـ Workflow يستخدمه لاحقاً
            with open("marketing_output.md", "w", encoding="utf-8") as f:
                f.write(content)
            print("\nSuccessfully generated and saved marketing content!")
        else:
            print(f"Failed to generate content: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    generate_marketing_content()
  
