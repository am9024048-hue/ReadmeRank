import streamlit as st
import requests

st.set_page_config(page_title="ReadmeRank", page_icon="🚀", layout="centered")

st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🚀 ReadmeRank</h1>", unsafe_allow_html=True)
st.write("<p style='text-align: center;'>النسخة الاحترافية لتقييم وتحليل ملفات الـ README.</p>", unsafe_allow_html=True)

api_key = "AQ.Ab8RN6LHt8cU3n10Z0T..."

input_method = st.radio("اختر طريقة إدخال الـ README:", ["🔗 سحب برابط جيت هب (GitHub URL)", "📝 إدخال نصي مباشر"])

readme_text = ""

if "سحب برابط جيت هب" in input_method:
    repo_url = st.text_input("أدخل رابط مستودع جيت هب (مثال: https://github.com/owner/repo):")
    if repo_url:
        with st.spinner("🔄 جاري سحب ملف الـ README..."):
            try:
                clean_url = repo_url.strip().rstrip("/")
                if "github.com" in clean_url:
                    parts = clean_url.split("github.com/")[-1].split("/")
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
                        st.error("❌ صيغة رابط جيت هب غير صحيحة.")
                else:
                    st.error("❌ يرجى إدخال رابط جيت هب صالح.")
            except Exception as e:
                st.error(f"حدث خطأ أثناء السحب: {e}")
else:
    readme_text = st.text_area("محتوى ملف الـ README:", height=250, placeholder="# اسم المشروع...")

if readme_text:
    st.caption(f"📊 عدد كلمات الملف: {len(readme_text.split())} كلمة")

if st.button("🚀 ابدأ الفحص والتحليل الشامل", type="primary", use_container_width=True):
    if not readme_text.strip():
        st.error("❌ الرجاء إدخال أو سحب محتوى الـ README أولاً.")
    else:
        with st.spinner("🤖 جاري التحليل بالذكاء الاصطناعي..."):
            try:
                prompt = f"""
                قم بتحليل ملف الـ README التالي للمطورين واعطني تقييماً مفصلاً:
                1. النتيجة الإجمالية من 100.
                2. تقييم خطوات التثبيت والاستخدام.
                3. الأقسام المفقودة.
                4. أهم التحسينات الفورية.
                
                محتوى الملف:
                {readme_text}
                """
                
                api_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={api_key}"
                headers = {"Content-Type": "application/json"}
                data = {
                    "contents": [{
                        "parts": [{"text": prompt}]
                    }]
                }
                
                response = requests.post(api_url, headers=headers, json=data)
                
                if response.status_code == 200:
                    res_json = response.json()
                    analysis_text = res_json["candidates"][0]["content"]["parts"][0]["text"]
                    st.success("🎉 تم إنجاز التحليل بنجاح!")
                    st.markdown("---")
                    st.markdown(analysis_text)
                else:
                    st.error(f"خطأ من الخادم: {response.text}")
                    
            except Exception as e:
                st.error(f"حدث خطأ أثناء التحليل: {e}")

