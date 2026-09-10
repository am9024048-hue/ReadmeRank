import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(
    page_title="ReadmeRank Pro",
    page_icon="🚀",
    layout="centered"
)

# تصميم وتنسيق إضافي (CSS) لجعل الواجهة احترافية جداً
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #FF4B4B;
    }
    .stAlert {
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🚀 ReadmeRank Pro</h1>", unsafe_allow_html=Platform := None)
st.write("<p style='text-align: center;'>الأداة الاحترافية الأولى لتقييم، تحليل، وترقية ملفات الـ README للمطورين بمساعدة الذكاء الاصطناعي.</p>", unsafe_allow_html=True)

# الشريط الجانبي للإعدادات المتقدمة
st.sidebar.header("⚙️ لوحة تحكم المطور")

# جلب المفتاح تلقائياً أو طلبه
api_key = ""
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.sidebar.success("تم تحميل مفتاح الـ API من الأسرار بنجاح! ✅")
except Exception:
    pass

if not api_key:
    api_key = st.sidebar.text_input(
        "أدخل مفتاح Google Gemini API:", 
        type="password",
        help="احصل على المفتاح من Google AI Studio"
    )
    if not api_key:
        st.sidebar.warning("⚠️ أدخل المفتاح هنا أو في إعدادات المنصة (Secrets).")

st.sidebar.markdown("---")
analysis_mode = st.sidebar.selectbox(
    "🎯 مستوى التحليل المطلوبة:",
    ["تحليل شامل واحترافي (Detailed)", "تحليل سريع ومباشر (Quick)"]
)

# مساحة إدخال الـ README
st.markdown("### 📝 محتوى ملف الـ README")
readme_text = st.text_area(
    "ضع محتوى ملف الـ README هنا للتحليل:", 
    height=280, 
    placeholder="# اسم المشروع\n\nوصف المشروع ومميزاته هنا..."
)

# عرض عدد الكلمات لمساعدة المطور
if readme_text:
    words_count = len(readme_text.split())
    st.caption(f"📊 عدد كلمات الملف الحالي: {words_count} كلمة")

# زر الفحص والتقييم
if st.button("🚀 ابدأ الفحص والتحليل الذكي", type="primary", use_container_width=True):
    if not api_key:
        st.error("❌ عذراً، يجب إدخال مفتاح Gemini API في الشريط الجانبي أو إعدادات المنصة أولاً.")
    elif not readme_text.strip():
        st.error("❌ الرجاء إدخال محتوى ملف الـ README للقيام بالتحليل.")
    else:
        with st.spinner("🤖 جاري فحص الهيكل، الأكواد، الروابط، وتقديم استراتيجيات التحسين للمطور... برجاء الانتظار"):
            try:
                genai.configure(api_key=api_key)
                
                # تخصيص البرومبت حسب الوضع المختار
                depth_instruction = "قدم تقييماً عميقاً ومفصلاً جداً مع أمثلة برمجية" if "شامل" in analysis_mode else "قدم تقييماً سريعاً ومباشراً لأهم النقاط"
                
                prompt = f"""
                قم بتحليل ملف الـ README التالي للمطورين بصفتك خبير هندسة برمجيات وخبير توثيق مشاريع مفتوحة الصור (Open Source).
                اتبع المعايير الآتية بدقة:
                1. النتيجة الإجمالية (Readme Score) من 100 مع تحديد تصنيف المشروع (مبتدئ، متوسط، احترافي عالمي).
                2. تقييم ووضوح خطوات التثبيت (Installation) والاستخدام (Usage).
                3. تحليل الأقسام المفقودة والحرجة (مثل: طريقة المساهمة، التراخيص، شارة البناء، أمثلة حية).
                4. {depth_instruction}.
                5. أهم 3-5 تحسينات فورية مقترحة مع كتابة الأكواد أو العناوين المقترحة لتعديلها مباشرة.
                
                محتوى الـ README المطلوب تحليله:
                {readme_text}
                """
                
                # استدعاء الموديل (Gemini 1.5 Flash الأسرع والأدق)
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                
                st.success("🎉 تم إنجاز التحليل بنجاح وبتفوق!")
                st.markdown("---")
                
                # عرض النتيجة
                st.markdown(response.text)
                
                # زر لتصدير التقرير أو نسخه
                st.markdown("---")
                st.download_button(
                    label="📥 تحميل تقرير التحليل كملف Markdown",
                    data=response.text,
                    file_name="ReadmeRank_Report.md",
                    mime="text/markdown"
                )
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال بنظام الذكاء الاصطناعي: {e}")
                
