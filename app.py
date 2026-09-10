import streamlit as st
from google import genai
import re

st.set_page_config(page_title="README AI Evaluator", page_icon="📝", layout="wide")

st.title("📝 أداة تقييم ملفات README بالذكاء الاصطناعي")
st.write("أدخل نص الـ README للحصول على تقييم شامل وتحليل ذكي.")

with st.sidebar:
    st.header("⚙️ الإعدادات")
    api_key = st.text_input("أدخل Gemini API Key:", type="password")
    st.markdown("[احصل على مفتاح مجاني من Google AI Studio](https://aistudio.google.com/)")

readme_text = st.text_area("إلصق نص README هنا:", height=300)

if st.button("🚀 فحص وتقييم README", type="primary"):
    if not api_key:
        st.error("يرجى إدخال Gemini API Key في الشريط الجانبي أولاً.")
    elif not readme_text.strip():
        st.warning("يرجى إدخال نص الـ README لفحصه.")
    else:
        with st.spinner("جاري التحليل وفحص المكونات والأكواد..."):
            try:
                client = genai.Client(api_key=api_key)
                links_count = len(re.findall(f'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', readme_text))

                prompt = f"""
                أنت خبير في مراجعة وتطوير مشاريع البرمجيات والأكواد.
                قم بتحليل ملف الـ README التالي بدقة وإعطاء تقرير باللغة العربية.

                النص:
                ---
                {readme_text}
                ---

                المطلوب:
                1. النتيجة الإجمالية (Readme Score) من 100.
                2. تحليل المعنى والسياق الضمني وهدف المشروع.
                3. فحص دعم التقنيات (خاصة React) وشرح الأكواد.
                4. فحص الهيكل والأقسام المفقودة والروابط المكتشفة ({links_count}).
                5. أهم 3-5 نقاط تحسينية فورية.
                """

                response = client.models.generate_content(
                    model="gemini-1.5-flash"
                    
                    contents=prompt,
                )

                st.success("تم التحليل بنجاح!")
                st.markdown("---")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال: {e}")
