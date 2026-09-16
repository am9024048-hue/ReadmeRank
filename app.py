import streamlit as st
import requests

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="ReadmeRank - Pro Auditor",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 ReadmeRank: Pro GitHub README Auditor")
st.write("أداة فحص وتقييم ملفات الـ README لاحتراف مشاريع المصادر المفتوحة ورفع جودتها.")

# 2. طريقة الإدخال
st.markdown("---")
input_method = st.radio("اختر طريقة إدخال ملف الـ README:", ["🔗 رابط مستودع GitHub", "📁 رفع ملف محلي (Markdown)"])

readme_content = ""
analysis_triggered = False

if input_method == "🔗 رابط مستودع GitHub":
    repo_input = st.text_input("أدخل رابط المستودع (مثال: owner/repo أو الرابط الكامل):", placeholder="https://github.com/torvalds/linux")
    if st.button("🔍 فحص المستودع", type="primary"):
        if not repo_input:
            st.warning("⚠️ الرجاء إدخال رابط صحيح.")
        else:
            clean_input = repo_input.strip()
            owner, repo = "", ""
            
            if "github.com" in clean_input:
                parts = [p for p in clean_input.split("/") if p]
                if len(parts) >= 2:
                    owner, repo = parts[-2], parts[-1].replace(".git", "")
            elif "/" in clean_input:
                parts = clean_input.split("/")
                if len(parts) == 2:
                    owner, repo = parts[0].strip(), parts[1].strip()

            if owner and repo:
                raw_urls = [
                    f"https://raw.githubusercontent.com/{owner}/{repo}/main/README.md",
                    f"https://raw.githubusercontent.com/{owner}/{repo}/master/README.md"
                ]
                
                success = False
                for url in raw_urls:
                    response = requests.get(url)
                    if response.status_code == 200:
                        readme_content = response.text
                        success = True
                        break
                
                if success:
                    st.success("✅ تم جلب ملف الـ README بنجاح من المستودع!")
                    analysis_triggered = True
                else:
                    st.error("❌ لم يتم العثور على ملف README.md في هذا المستودع (تأكد أن المستودع عام).")
            else:
                st.error("⚠️ صيغة الرابط غير صحيحة.")

else:
    uploaded_file = st.file_uploader("اختر ملف README.md من جهازك:", type=["md", "txt"])
    if st.button("🔍 فحص الملف المرفوع", type="primary"):
        if uploaded_file is not None:
            readme_content = uploaded_file.getvalue().decode("utf-8")
            st.success("✅ تم رفع وفحص الملف بنجاح!")
            analysis_triggered = True
        else:
            st.warning("⚠️ الرجاء رفع ملف أولاً.")

# 3. التحليل والفحص
if analysis_triggered and readme_content:
    st.markdown("---")
    st.subheader("📊 تقرير الفحص والتحليل الاحترافي")

    content_lower = readme_content.lower()
    
    has_install = any(k in content_lower for k in ["install", "installation", "getting started", "التثبيت"])
    has_usage = any(k in content_lower for k in ["usage", "how to use", "examples", "الاستخدام"])
    has_features = any(k in content_lower for k in ["feature", "features", "highlights", "المميزات"])
    has_contributing = any(k in content_lower for k in ["contribut", "pull request", "المساهمة"])
    has_license = any(k in content_lower for k in ["license", "licence", "الترخيص"])
    has_badges = any(k in content_lower for k in ["[![", "img.shields.io", "badge"])
    has_screenshots = any(k in content_lower for k in ["screenshot", "demo", "preview", "gif", "صورة"])

    score = 0
    if has_install: score += 20
    if has_usage: score += 20
    if has_features: score += 15
    if has_contributing: score += 15
    if has_license: score += 10
    if has_badges: score += 10
    if has_screenshots: score += 10

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="التقييم الكلي (Score)", value=f"{score}/100")
    with col2:
        if score >= 80:
            st.success("الحالة: ممتاز 🌟")
        elif score >= 50:
            st.warning("الحالة: جيد، يحتاج تحسين ⚠️")
        else:
            st.error("الحالة: ضعيف ❌")
    with col3:
        word_count = len(readme_content.split())
        st.metric(label="عدد الكلمات", value=word_count)

    st.markdown("### 📋 تفصيل الأقسام:")
    
    sections_status = [
        ("Installation (التثبيت)", has_install, "يوضح كيفية تشغيل المشروع."),
        ("Usage (الاستخدام)", has_usage, "يشرح طريقة الاستفادة منه."),
        ("Features (المميزات)", has_features, "يبرز نقاط قوة المشروع."),
        ("Contributing (المساهمة)", has_contributing, "يشجع المطورين الآخرين."),
        ("License (الترخيص)", has_license, "يحفظ حقوق الملكية."),
        ("Badges (الشارات)", has_badges, "يمنح مظهراً احترافياً."),
        ("Screenshots / Demo", has_screenshots, "يعرض شكل المشروع بصرياً.")
    ]

    for name, exists, desc in sections_status:
        if exists:
            st.markdown(f"✅ **{name}**: موجود - *{desc}*")
        else:
            st.markdown(f"❌ **{name}**: غير موجود - *{desc}*")

    if score < 80:
        st.markdown("---")
        st.subheader("💡 اقتراحات لتحسين الـ README:")
        if not has_install: st.info("👉 أضف قسم `## Installation`.")
        if not has_usage: st.info("👉 أضف قسم `## Usage`.")
        if not has_contributing: st.info("👉 أضف قسم `## Contributing`.")
        if not has_license: st.info("👉 أضف قسم `## License`.")

        template_text = (
            "# Project Name 🚀\n"
            "> وصف قصير للمشروع.\n\n"
            "## ✨ Features\n"
            "- ميزة 1\n"
            "- ميزة 2\n\n"
            "## 📦 Installation\n"
            "```bash\n"
            "git clone [https://github.com/username/repo.git](https://github.com/username/repo.git)\n"
            "```\n\n"
            "## 🎮 Usage\n"
            "أضف مثال الاستخدام هنا.\n\n"
            "## 🤝 Contributing\n"
            "نرحب بالمساهمات!\n\n"
            "## 📄 License\n"
            "MIT License"
        )

        with st.expander("📝 اضغط هنا لرؤية قالب README جاهز للنسخ"):
            st.code(template_text, language="markdown")

