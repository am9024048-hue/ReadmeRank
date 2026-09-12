import os
import requests
from openai import OpenAI
import streamlit as st

# إعداد الصفحة وتصيمها
st.set_page_config(
    page_title="ReadmeRank", page_icon="🚀", layout="centered"
)

# تخصيص التصميم والستايل (CSS)
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
        padding: 0.6rem;
    }
    .stButton>button:hover {
        background-color: #ff2b2b;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# تهيئة الاتصال بمحرك الذكاء الاصطناعي من السرية (Secrets)
api_key = None
try:
  if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
  pass

if not api_key:
  api_key = os.getenv("GROQ_API_KEY")

# إعداد عميل الاتصال
client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=api_key)

# عنوان التطبيق والوصف النظيف
st.markdown(
    "<h1 style='text-align: center; color: #ff4b4b;'>ReadmeRank</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center;'>النسخة الاحترافية لتحليل ملفات الـ"
    " README بأحدث تقنيات الذكاء الاصطناعي.</p>",
    unsafe_allow_html=True,
)

st.write("---")

# خيارات الإدخال
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
    # تنظيف الرابط لاستخراج صاحب المستودع واسمه
    clean_repo = repo_input.strip()
    if "github.com/" in clean_repo:
      clean_repo = clean_repo.split("github.com/")[-1]
    if clean_repo.endswith("/"):
      clean_repo = clean_repo[:-1]

    # جلب ملف الـ README من جيت هب
    api_url = f"https://api.github.com/repos/{clean_repo}/readme"
    headers = {"Accept": "application/vnd.github.v3.raw"}
    try:
      response = requests.get(api_url, headers=headers)
      if response.status_code == 200:
        readme_content = response.text
        st.success("تم سحب ملف الـ README بنجاح!")
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

# زر الفحص والتحليل
if st.button("🚀 ابدأ الفحص والتحليل الشامل"):
  if not api_key:
    st.error(
        "مفتاح التشغيل غير متوفر. يرجى إضافته في إعدادات المنصة (Secrets)."
    )
  elif not readme_content.strip():
    st.warning("الرجاء إدخال رابط صالح أو كتابة محتوى للتحليل أولاً.")
  else:
    with st.spinner("🤖 جاري الفحص وتحليل البيانات بسرعة البرق..."):
      try:
        # إرسال البيانات للذكاء الاصطناعي للتحليل والتقييم
        prompt = (
            "قم بتحليل وتقییم ملف الـ README التالي الخاص بمشروع برمجى."
            " أعطني تقييماً احترافياً، نقاط القوة، نقاط الضعف، وكيفية تحسينه"
            " لجذب المزيد من المطورين والمشاهدات:\n\n" + readme_content
        )

        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            
            
            messages=[{
                "role": "user",
                "content": prompt,
            }],
            temperature=0.7,
            max_tokens=2048,
        )

        analysis_result = completion.choices[0].message.content

        st.write("---")
        st.subheader("📊 تقرير التحليل الشامل والتقييم:")
        st.markdown(analysis_result)

      except Exception as e:
        st.error(f"حدث خطأ أثناء عملية التحليل: {e}")

