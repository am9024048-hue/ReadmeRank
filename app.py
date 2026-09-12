import re
import requests
import streamlit as st

st.set_page_config(
    page_title="ReadmeRank | Free Edition", page_icon="🚀", layout="centered"
)

st.markdown(
    """
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.7rem;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #ff2b2b;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    "<h1 style='text-align: center; color: #ff4b4b;'>ReadmeRank <span"
    " style='font-size: 16px; color: #8b949e;'>Free Edition</span></h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center;'>المنصة المجانية للتحليل الهيكلي والتقييم"
    " الفوري لملفات الـ README.</p>",
    unsafe_allow_html=True,
)

st.write("---")

input_mode = st.radio(
    "اختر طريقة إدخال الـ README:",
    ("سحب برابط جيت هب (GitHub URL)", "إدخال نصي مباشر 📝"),
)

readme_content = ""

if "سحب" in input_mode:
  repo_input = st.text_input(
      "أدخل رابط مستودع جيت هب أو اسم المستودع (مثال: psf/requests):",
      placeholder="owner/repo or https://github.com/owner/repo",
  )
  if repo_input:
    clean_repo = repo_input.strip()
    if "github.com/" in clean_repo:
      clean_repo = clean_repo.split("github.com/")[-1]
    if clean_repo.endswith("/"):
      clean_repo = clean_repo[:-1]

    api_url = f"https://api.github.com/repos/{clean_repo}/readme"
    headers = {"Accept": "application/vnd.github.v3.raw"}
    try:
      response = requests.get(api_url, headers=headers)
      if response.status_code == 200:
        readme_content = response.text
        st.success("تم سحب ملف الـ README بنجاح وجاهز للتحليل الفوري!")
      else:
        st.error(
            "تعذر العثور على ملف README في هذا المستودع. تأكد من صحة الرابط أو"
            " جرب الإدخال المباشر."
        )
    except Exception as e:
      st.error(f"حدث خطأ أثناء الاتصال: {e}")
else:
  readme_content = st.text_area(
      "الصق محتوى ملف الـ README هنا:", height=200, placeholder="# مشروعك هنا..."
  )

st.write("")

if st.button("🚀 ابدأ الفحص الهيكلي الشامل"):
  if not readme_content.strip():
    st.warning("الرجاء إدخال رابط صالح أو كتابة محتوى للتحليل أولاً.")
  else:
    with st.spinner("⚡ جاري فحص هيكل الملف وتقييم الأقسام..."):
      text_lower = readme_content.lower()

      has_installation = any(
          k in text_lower
          for k in [
              "installation",
              "install",
              "getting started",
              "تثبيت",
              "البدء",
          ]
      )
      has_usage = any(
          k in text_lower for k in ["usage", "how to use", "examples", "استخدام"]
      )
      has_license = any(
          k in text_lower for k in ["license", "licence", "ترخيص", "رخصة"]
      )
      has_contributing = any(
          k in text_lower for k in ["contributing", "contribute", "المساهمة"]
      )
      has_badges = "[![" in readme_content or "<img" in readme_content

      score = 40
      if has_installation:
        score += 20
      if has_usage:
        score += 20
      if has_license:
        score += 10
      if has_contributing:
        score += 5
      if has_badges:
        score += 5

      word_count = len(readme_content.split())

      st.write("---")
      st.subheader("📊 تقرير التحليل الهيكلي والتقييم:")

      col1, col2, col3 = st.columns(3)
      with col1:
        st.metric(label="التقييم العام", value=f"{score} / 100")
      with col2:
        st.metric(label="عدد الكلمات", value=word_count)
      with col3:
        status_text = "ممتاز" if score >= 80 else "مقبول" if score >= 60 else "ضعيف"
        st.metric(label="حالة التوثيق", value=status_text)

      st.write("### 🔍 تقييم الأقسام الأساسية:")
      st.markdown(
          f"- **قسم التثبيت (Installation):** {'✅ متوفر' if has_installation"
          ' else '❌ غير متوفر'}"
      )
      st.markdown(
          f"- **قسم الاستخدام والأمثلة (Usage):** {'✅ متوفر' if has_usage else"
          ' ❌ غير متوفر'}"
      )
      st.markdown(
          f"- **شروط الترخيص (License):** {'✅ متوفر' if has_license else"
          ' ❌ غير متوفر'}"
      )
      st.markdown(
          f"- **دليل المساهمة (Contributing):** {'✅ متوفر' if has_contributing"
          ' else '⚠️ غير متوفر'}"
      )
      st.markdown(
          f"- **الشارات (Badges):** {'✅ توجد شارات' if has_badges else"
          ' ⚠️ لا توجد شارات'}"
      )

      st.write("### 💡 توصيات سريعة لتحسين المشروع:")
      if score < 80:
        st.info(
            "💡 احرص على إضافة الأقسام المفقودة وتوضيح أمثلة برمجية سريعة في"
            " بدايته."
        )
      else:
        st.success("🌟 ملف الـ README الخاص بك منظم واحترافي!")

      st.write("---")
      st.info(
          "🔒 **هل تريد تحليلاً أعمق بالذكاء الاصطناعي؟** ترقبوا قريباً إطلاق"
          " النسخة المدفوعة (PRO)!"
)

