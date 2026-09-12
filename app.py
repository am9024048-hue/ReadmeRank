import streamlit as st
from openai import OpenAI
import requests

st.set_page_config(page_title="ReadmeRank", page_icon="🚀", layout="centered")

st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🚀 ReadmeRank</h1>", unsafe_allow_html=True)
st.write("<p style='text-align: center;'>النسخة الاحترافية لتحليل الـ README بأسرع ذكاء اصطناعي (Groq).</p>", unsafe_allow_html=True)

# سحب مفتاح Groq أوتوماتيكياً من إعدادات الأمان في Streamlit Cloud
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    groq_api_key = ""

input_method = st.radio("اختر طريقة إدخال الـ README:", ["🔗 سحب برابط جيت هب (GitHub URL)", "📝 إدخال نصي مباشر"])

readme_text = ""

if "سحب برابط جيت هب" in input_method:
    repo_input = st.text_input("أدخل رابط مستودع جيت هب أو اسم المستودع (مثال: psf/requests):")
    if repo_input:
        with st.spinner("🔄 جاري سحب ملف الـ README..."):
            try:
                clean_input = repo_input.strip().rstrip("/")
                if "github.com" in clean_input:
                    parts = clean_input.split("github.com/")[-1].split("/")
                else:
                    parts = clean_input.split("/")
                
                if len(parts) >= 2:
                    owner, repo = parts[0], parts[1]
                    raw_urls = [
                        f"https://raw.githubusercontent.com/{owner}/{repo}/main/README.md",
                        f"https://raw.githubusercontent.com/{owner}/{repo}/master/README.md"
                    ]
                    fetched = False
                    for url in raw_urls:
                        res = requests.get(url)
                        if res.status_code == 200:
                            readme_text = res.text
                            fetched = True
                            break
                    if fetched:
                        st.success("✅ تم سحب ملف الـ README بنجاح!")
                    else:
                        st.error("❌ لم يتم العثور على ملف README.md في المستودع العام.")
                else:
                    st.error("❌ صيغة الرابط أو اسم المستودع غير صحيحة.")
            except Exception as e:
                st.error(f"حدث خطأ أثناء السحب: {e}")
else:
    readme_text = st.text_area("محتوى ملف الـ README:", height=250, placeholder="# اسم المشروع...")

if readme_text:
    st.caption(f"📊 عدد كلمات الملف: {len(readme_text.split())} كلمة")

if st.button("🚀 ابدأ الفحص والتحليل الشامل", type="primary", use_container_width=True):
    if not groq_api_key:
        st.error("❌ مفتاح Groq API غير موجود في إعدادات Secrets الخاصة بـ Streamlit. برجاء إضافته أولاً.")
    elif not readme_text.strip():
        st.error("❌ الرجاء إدخال أو سحب محتوى الـ README أولاً.")
    else:
        with st.spinner("🤖 جاري التحليل بسرعة البرق عبر Groq..."):
            try:
                client = OpenAI(
                    base_url="https://api.groq.com/openai/v1",
                    api_key=groq_api_key
                )
                
                prompt = f"""
                قم بتحليل ملف الـ README التالي للمطورين واعطني تقييماً مفصلاً:
                1. النتيجة الإجمالية من 100.
                2. تقييم خطوات التثبيت والاستخدام.
                3. الأقسام المفقودة.
                4. أهم التحسينات الفورية.
                
                محتوى الملف:
                {readme_text}
                """
                
                response = client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=[
                        {"role": "system", "content": "أنت مساعد ذكاء اصطناعي محترف في تقييم ومراجعة مشاريع البرمجيات وملفات الـ README."},
                        {"role": "user", "content": prompt}
                    ]
                )
                
                result_text = response.choices[0].message.content
                
                if result_text:
                    st.success("🎉 تم إنجاز التحليل بنجاح وبسرعة فائقة!")
                    st.markdown("---")
                    st.markdown(result_text)
                else:
                    st.error("❌ لم يتم استلام رد من النموذج.")
                    
            except Exception as e:
                st.error(f"حدث خطأ أثناء التحليل: {e}")

