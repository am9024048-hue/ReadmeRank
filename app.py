import requests
import streamlit as st

# إعدادات الصفحة
st.set_page_config(
    page_title="ReadmeRank",
    page_icon="🚀",
    layout="centered",
)

st.title("🚀 ReadmeRank")
st.markdown(
    "**A professional SaaS tool to evaluate, score, and optimize GitHub README files with structural analysis and instant feedback.**"
)
st.markdown("---")

# إدخال رابط المستودع
repo_url = st.text_input(
    "GitHub Repository URL",
    placeholder="https://github.com/username/repository",
)

if st.button("Analyze README", type="primary"):
  if not repo_url:
    st.warning("الرجاء إدخال رابط مستودع صحيح أولاً.")
  else:
    try:
      # استخراج اسم المستخدم والمستودع من الرابط
      clean_url = repo_url.rstrip("/")
      parts = clean_url.split("/")
      if len(parts) < 2:
        st.error("رابط غير صالح. يرجى التأكد من الرابط.")
      else:
        owner = parts[-2]
        repo = parts[-1]

        # جلب ملف الـ README من GitHub API
        api_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
        headers = {"Accept": "application/vnd.github.v3+json"}

        with st.spinner("جاري فحص المستودع وتحليل الهيكل..."):
          response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
          readme_data = response.json()
          content_download_url = readme_data.get("download_url")

          # تحميل محتوى الـ README
          content_response = requests.get(content_download_url)
          readme_content = content_response.text

          # --- التحليل الهيكلي البسيط ---
          st.success("تم العثور على ملف الـ README بنجاح!")

          # فحص الأقسام الأساسية
          has_installation = (
              "installation" in readme_content.lower()
              or "التثبيت" in readme_content
          )
          has_usage = "usage" in readme_content.lower() or "الاستخدام" in readme_content
          has_contributing = (
              "contributing" in readme_content.lower()
              or "المساهمة" in readme_content
          )
          has_badges = "[![" in readme_content or "<img" in readme_content

          # حساب تقريبي للنتيجة بناءً على الأقسام الموجودة
          score = 50
          if has_installation:
            score += 20
          if has_usage:
            score += 20
          if has_contributing:
            score += 5
          if has_badges:
            score += 5

          # تحديد التقدير الحرفي (Grade)
          if score >= 90:
            grade = "A"
            status_color = "🟢 ممتاز"
          elif score >= 75:
            grade = "B"
            status_color = "🟡 جيد جداً"
          elif score >= 60:
            grade = "C"
            status_color = "🟠 مقبول"
          else:
            grade = "D"
            status_color = "🔴 يحتاج تحسين"

          # عرض النتائج
          st.markdown("### 📊 تقرير التحليل الهيكلي")
          st.metric(label="التقييم الإجمالي (Score)", value=f"{score}/100")
          st.write(f"**الحالة التقديرية:** {status_color}")

          st.markdown("#### تفاصيل الأقسام:")
          st.markdown(
              f"- تثبيت المشروع (Installation): {'✅ متوفر' if has_installation else '⚠️ غير متوفر'}"
          )
          st.markdown(
              f"- طريقة الاستخدام (Usage): {'✅ متوفر' if has_usage else '⚠️ غير متوفر'}"
          )
          st.markdown(
              f"- دليل المساهمة (Contributing): {'✅ متوفر' if has_contributing else '⚠️ غير متوفر'}"
          )
          st.markdown(
              f"- الشارات (Badges): {'✅ توجد شارات' if has_badges else '⚠️ لا توجد شارات'}"
          )

          # --- قسم التشويق للنسخة PRO ---
          st.markdown("---")
          st.info(
              "🤖 هل تريد تحليلاً أعمق واقترحات بالذكاء الاصطناعي؟ (قريباً إطلاق"
              " النسخة PRO)!"
          )

          # --- ميزة الشارات الفيروسية (Viral Badges) ---
          st.markdown("---")
          st.subheader("🚀 Show off your ReadmeRank!")
          st.write(
              "احصل على شارة تقييم مشروعك وضعها في ملف الـ README الخاص بك:"
          )

          badge_url = f"https://img.shields.io/badge/ReadmeRank-{grade}-blue?style=flat-square&logo=github"
          st.markdown(
              f"<img src='{badge_url}' alt='ReadmeRank Badge'/>",
              unsafe_allow_html=True,
          )

          # ضع رابط تطبيقك الفعلي هنا بدل الـ localhost أو رابط الـ streamlit القديم
          app_public_url = "https://your-streamlit-app-url.streamlit.app"
          badge_markdown = (
              f"[![ReadmeRank]({badge_url})]({app_public_url})"
          )
          st.code(badge_markdown, language="markdown")
          st.caption(
              "💡 انسخ الكود أعلاه والزقه في ملف الـ README بمستودعك لتدعم الأداة"
              " وتظهر تقييمك للجميع!"
          )

        else:
          st.error(
              "عذراً، لم يتم العثور على ملف README في هذا المستودع، أو أن"
              " الرابط غير صحيح / المستودع خاص."
          )
    except Exception as e:
      st.error(f"حدث خطأ أثناء جلب البيانات: {e}")

