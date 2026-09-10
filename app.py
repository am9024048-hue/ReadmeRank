import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(page_title="ReadmeRank", page_icon="🚀", layout="centered")

st.title("🚀 ReadmeRank - تقييم وتحليل ملفات الـ README")
st.write("أداة ذكية لتقييم وتحسين ملفات الـ README بمساعدة الذكاء الاصطناعي.")

# محاولة جلب المفتاح تلقائياً من أسرار المنصة، ولو مش موجود يظهر في الشريط الجانبي
api_key = ""
try:
    api_key = st.secrets.get("GEMINI_API_KEY", "")
except Exception:
    pass

if not api_key:
    api_key = st.sidebar.text_input("أدخل مفتاح Google Gemini API:", type="password")

# مساحة إدخال الـ README
readme_text = st.text_area("ضع محتوى ملف الـ README هنا:", height=250)

if st.button("🚀 فحص وتقييم README"):
    if not api_key:
        st.error("الرجاء إدخال مفتاح الـ API (سواء في إعدادات المنصة أو الشريط الجانبي) أولاً.")
    elif not readme_text:
        st.error("الرجاء إدخال محتوى الـ README للقيام بالتحليل.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # إعداد البرومبت للتقييم
            prompt = f"""
            قم بتحليل ملف الـ README التالي واعطني تقييماً مفصلاً بناءً على المعايير الآتية:
            1. النتيجة الإجمالية (Readme Score) من 100.
            2. تحليل المعنى والسياق الضمني وهدف المشروع.
            3. شرح الأكواد فحص دعم التقنيات.
            4. الهيكل والأقسام المفقودة والروابط المكتشفة.
            5. أهم 3-5 نقاط تحسينية فورية.
            
            محتوى الـ README:
            {readme_text}
            """
            
            # استدعاء الموديل
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            
            st.success("تم التحليل بنجاح!")
            st.markdown("---")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"حدث خطأ أثناء الاتصال: {e}")
        
