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
    st.warning("Please enter a valid repository URL first.")
  else:
    try:
      # استخراج اسم المستخدم والمستودع من الرابط
      clean_url = repo_url.rstrip("/")
      parts = clean_url.split("/")
      if len(parts) < 2:
        st.error("Invalid URL. Please check the repository link.")
      else:
        owner = parts[-2]
        repo = parts[-1]

        # جلب ملف الـ README من GitHub API
        api_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
        headers = {"Accept": "application/vnd.github.v3+json"}

        with st.spinner("Analyzing repository structure..."):
          response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
          readme_data = response.json()
          content_download_url = readme_data.get("download_url")

          # تحميل محتوى الـ README
          content_response = requests.get(content_download_url)
          readme_content = content_response.text

          # --- التحليل الهيكلي ---
          st.success("README file found successfully!")

          # فحص الأقسام الأساسية
          has_installation = "installation" in readme_content.lower()
          has_usage = "usage" in readme_content.lower()
          has_contributing = "contributing" in readme_content.lower()
          has_badges = "[![" in readme_content or "<img" in readme_content

          # حساب التقييم
          score = 50
          if has_installation:
            score += 20
          if has_usage:
            score += 20
          if has_contributing:
            score += 5
          if has_badges:
            score += 5

          # تحديد التقدير
          if score >= 90:
            grade = "A"
            status_color = "🟢 Excellent"
          elif score >= 75:
            grade = "B"
            status_color = "🟡 Very Good"
          elif score >= 60:
            grade = "C"
            status_color = "🟠 Good"
          else:
            grade = "D"
            status_color = "🔴 Needs Improvement"

          # عرض النتائج
          st.markdown("### 📊 Structural Analysis Report")
          st.metric(label="Overall Score", value=f"{score}/100")
          st.write(f"**Status:** {status_color}")

          st.markdown("#### Section Breakdown:")
          st.markdown(f"- Installation: {'✅ Found' : '⚠️ Missing' if not has_installation else '✅ Found'}") # simplified check below
          st.markdown(f"- Installation: {'✅ Found' if has_installation else '⚠️ Missing'}")
          st.markdown(f"- Usage: {'✅ Found' if has_usage else '⚠️ Missing'}")
          st.markdown(f"- Contributing: {'✅ Found' if has_contributing else '⚠️ Missing'}")
          st.markdown(f"- Badges: {'✅ Found' if has_badges else '⚠️ Missing'}")

          # --- قسم التشويق للنسخة PRO ---
          st.markdown("---")
          st.info("🤖 Want deeper AI-powered suggestions? (PRO version coming soon!)")

          # --- ميزة الشارات الفيروسية (Viral Badges) برابطك الحقيقي ---
          st.markdown("---")
          st.subheader("🚀 Show off your ReadmeRank!")
          st.write("Get your project score badge and add it to your README file:")

          badge_url = f"https://img.shields.io/badge/ReadmeRank-{grade}-blue?style=flat-square&logo=github"
          st.markdown(f"<img src='{badge_url}' alt='ReadmeRank Badge'/>", unsafe_allow_html=True)

          app_public_url = "https://readmerank.streamlit.app"
          badge_markdown = f"[![ReadmeRank]({badge_url})]({app_public_url})"
          
          st.code(badge_markdown, language="markdown")
          st.caption("💡 Copy the code above and paste it into your repository's README file!")

        else:
          st.error("Sorry, no README file was found in this repository, or the link is invalid / private.")
    except Exception as e:
      st.error(f"An error occurred while fetching data: {e}")

