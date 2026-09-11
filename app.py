import streamlit as st
import google.generativeai as genai
import requests

st.set_page_config(page_title="ReadmeRank Pro", page_icon="🚀", layout="centered")

st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🚀 ReadmeRank Pro</h1>", unsafe_allow_html=True)
st.write("<p style='text-align: center;'>النسخة الاحترافية لتقييم وتحليل ملفات الـ README (يدوياً أو عبر رابط جيت هب).</p>", unsafe_allow_html=True)

# جلب المفتاح من الـ Secrets
api_key = st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    st.error("❌ مفتاح الـ API غير موجود في إعدادات المنصة (Secrets). يرجى إضافته.")

# خيار طريقة الإدخال
input_method = st.radio("اختر طريقة إدخال الـ README:", ["🔗 سحب برابط جيت هب (GitHub URL)", "📝 إدخال نصي مباشر"])

readme_text = ""

if "سحب برابط جيت هب" in input_method:
    repo_url = st.text_input("أدخل رابط مستودع جيت هب (مثال: https://github.com/owner/repo):")
    if repo_url:
        with st.spinner("🔄 جاري سحب ملف الـ README من المستودع..."):
            try:
                # تنظيف الرابط واستخراج صاحب المستودع واسمه
                clean_url = repo_url.strip().rstrip("/")
                if "github.com" in clean_url:
                    parts = clean_url.split("github.com/")[-1].split("/")
                    if len(parts) >= 2:
                        owner, repo = parts[0], parts[1]
                        # محاولة سحب ملف الـ README بأشهر الصيغ
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
                            st.error("❌ لم يتم العثور على ملف README.md في الفرع الرئيسي (main أو master). تأكد أن المستودع عام.")
                    else:
                        st.error("❌ صيغة الرابط غير صحيحة. تأكد أنه رابط مستودع صحيح.")
                else:
                    st.error("❌ يرجى إدخال رابط جيت هب صالح.")
            except Exception as e:
                st.error(f"حدث خطأ أثناء السحب: {e}")
else:
    readme_text = st.text_area("محتوى ملف الـ README:", height=280, placeholder="# اسم المشروع...")

if readme_text:
    st.caption(f"📊 عدد كلمات الملف: {len(readme_text.split())} كلمة")

if st.button("🚀 ابدأ الفحص والتحليل الشامل", type="primary", use_container_width=True):
    if not api_key:
        st.error("❌ أضف المفتاح في الـ Secrets أولاً.")
    elif not readme_text.strip():
        st.error("❌ الرجاء إدخال أو سحب محتوى الـ README أولاً.")
    else:
        with st.spinner("🤖 جاري التحليل بالذكاء الاصطناعي..."):
            try:
                genai.configure(api_key=api_key)
                prompt = f"""
                قم بتحليل ملف الـ README التالي للمطورين واعطني تقييماً مفصلاً:
                1. النتيجة الإجمالية (Readme Score) من 100 مع تحديد المستوى.
                2. تقييم ووضوح خطوات التثبيت والاستخدام.
                3. تحليل الأقسام المفقودة والحرجة.
                4. أهم 3-5 تحسينات فورية مقترحة.
                
                محتوى الملف:
                {readme_text}
                """
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                
                st.success("🎉 تم إنجاز التحليل بنجاح!")
                st.markdown("---")
                st.markdown(response.text)
                
                st.markdown("---")
                st.download_button(
                    label="📥 تحميل تقرير التحليل كملف Markdown",
                    data=response.text,
                    file_name="ReadmeRank_Report.md",
                    mime="text/markdown"
                )
            except Exception as e:
                st.error(f"حدث خطأ أثناء التحليل: {e}")

