import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="ReadmeRank Pro", page_icon="🚀", layout="centered")

st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🚀 ReadmeRank Pro</h1>", unsafe_allow_html=True)
st.write("<p style='text-align: center;'>النسخة النهائية والمحترفة لتقييم وتحليل ملفات الـ README.</p>", unsafe_allow_html=True)

api_key = st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    st.error("❌ مفتاح الـ API غير موجود في إعدادات المنصة (Secrets). يرجى إضافته لتعمل الأداة أوتوماتيكياً.")

readme_text = st.text_area("محتوى ملف الـ README:", height=280, placeholder="# اسم المشروع...")

if readme_text:
    st.caption(f"📊 عدد كلمات الملف: {len(readme_text.split())} كلمة")

if st.button("🚀 ابدأ الفحص والتحليل الشامل", type="primary", use_container_width=True):
    if not api_key:
        st.error("❌ أضف المفتاح في الـ Secrets أولاً.")
    elif not readme_text.strip():
        st.error("❌ الرجاء إدخال محتوى الـ README أولاً.")
    else:
        with st.spinner("🤖 جاري التحليل..."):
            try:
                genai.configure(api_key=api_key)
                prompt = f"""
                قم بتحليل ملف الـ README التالي للمطورين واعطني تقييماً مفصلاً:
                1. النتيجة الإجمالية (Readme Score) من 100.
                2. تقييم خطوات التثبيت والاستخدام.
                3. الأقسام المفقودة.
                4. أهم التحسينات الفورية.

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
                st.error(f"حدث خطأ: {e}")
                        
