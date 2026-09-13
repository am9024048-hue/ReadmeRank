import streamlit as st
import requests

st.set_page_config(page_title="ReadmeRank", page_icon="📊", layout="centered")

st.title("📊 ReadmeRank")
st.write("Score & optimize your GitHub README files instantly.")

repo_url = st.text_input("GitHub Repository URL", placeholder="https://github.com/username/repository")

if st.button("Analyze README", type="primary"):
    if not repo_url:
        st.warning("Please enter a valid GitHub repository URL.")
    else:
        # تحويل رابط جيت هب إلى رابط جلب ملف الـ README الخام (Raw)
        clean_url = repo_url.strip().rstrip("/")
        if "github.com" in clean_url:
            parts = clean_url.split("github.com/")[-1].split("/")
            if len(parts) >= 2:
                owner, repo = parts[0], parts[1]
                raw_readme_url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/README.md"
            else:
                raw_readme_url = ""
        else:
            raw_readme_url = ""

        try:
            response = requests.get(raw_readme_url)
            # تجربة فرع master إذا لم ينجح فرع main
            if response.status_code != 200 and owner and repo:
                raw_readme_url = f"https://raw.githubusercontent.com/{owner}/{repo}/master/README.md"
                response = requests.get(raw_readme_url)

            if response.status_code == 200:
                readme_content = response.text
                st.success("README file found successfully!")

                st.markdown("---")
                st.subheader("📈 Structural Analysis Report")
                
                # فحص الأقسام الأساسية في الـ README
                content_lower = readme_content.lower()
                has_installation = "install" in content_lower or "installation" in content_lower
                has_usage = "usage" in content_lower or "how to use" in content_lower
                has_features = "feature" in content_lower or "features" in content_lower
                has_license = "license" in content_lower

                # حساب النقاط (Score)
                score = 40  # البداية لو الملف موجود
                if has_installation: score += 20
                if has_usage: score += 20
                if has_features: score += 10
                if has_license: score += 10

                st.markdown(f"### Overall Score")
                st.markdown(f"# **{score}/100**")
                
                status_label = "Good" if score >= 60 else "Needs Improvement"
                st.markdown(f"**Status:** 🟡 {status_label}")

                st.markdown("### Section Breakdown:")

                # عرض حالة الأقسام بطريقة سليمة بدون أخطاء في الـ f-string
                install_msg = "✅ Found" if has_installation else "⚠️ Missing installation section"
                usage_msg = "✅ Found" if has_usage else "⚠️ Missing usage section"
                features_msg = "✅ Found" if has_features else "⚠️ Missing features section"
                license_msg = "✅ Found" if has_license else "⚠️ Missing license section"

                if has_installation and has_usage:
                    st.info(f"{install_msg}\n\n{usage_msg}")
                else:
                    st.error(f"{install_msg}\n\n{usage_msg}\n\n{features_msg}\n\n{license_msg}")

            else:
                st.error("Could not fetch README file. Make sure the repository is public and has a README.md file.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
                   
