import streamlit as st
import requests

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="ReadmeRank | GitHub README Auditor",
    page_icon="📊",
    layout="wide"
)

# عنوان واقعي واحترافي يبرز قوة الأداة بدون مبالغة
st.title("ReadmeRank | GitHub README Auditor")
st.write("أداة تحليل وتقييم جودة ملفات README للمشاريع البرمجية لضمان توثيق احترافي ومنظم.")

# 2. طريقة الإدخال بنصوص سليمة وواضحة
st.markdown("---")
input_method = st.radio(
    "اختر مصدر ملف README للتحليل:", 
    ["رابط مستودع GitHub", "رفع ملف Markdown من الجهاز"]
)

readme_content = ""
analysis_triggered = False

if input_method == "رابط مستودع GitHub":
    repo_input = st.text_input("أدخل رابط المستودع (مثال: owner/repo أو الرابط الكامل):", placeholder="https://github.com/torvalds/linux")
    if st.button("فحص المستودع", type="primary"):
        if not repo_input:
            st.warning("الرجاء إدخال رابط صحيح.")
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
                    st.success("تم جلب ملف README بنجاح من المستودع.")
                    analysis_triggered = True
                else:
                    st.error("لم يتم العثور على ملف README.md في هذا المستودع (تأكد أن المستودع عام).")
            else:
                st.error("صيغة الرابط غير صحيحة.")

else:
    uploaded_file = st.file_uploader("اختر ملف Markdown (.md) من جهازك:", type=["md", "txt"])
    if st.button("فحص الملف", type="primary"):
        if uploaded_file is not None:
            readme_content = uploaded_file.getvalue().decode("utf-8")
            st.success("تم رفع وفحص الملف بنجاح.")
            analysis_triggered = True
        else:
            st.warning("الرجاء تحديد ملف أولاً.")

# 3. التحليل والفحص
if analysis_triggered and readme_content:
    st.markdown("---")
    st.subheader("تقرير تحليل وتقییم التوثيق")

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
        st.metric(label="التقييم الكلي", value=f"{score}/100")
    with col2:
        if score >= 80:
            st.success("مستوى التوثيق: ممتاز")
        elif score >= 50:
            st.warning("مستوى التوثيق: جيد، يحتاج تحسينات")
        else:
            st.error("مستوى التوثيق: ضعيف")
    with col3:
        word_count = len(readme_content.split())
        st.metric(label="عدد الكلمات", value=word_count)

    st.markdown("### تفاصيل الأقسام الأساسية:")
    
    sections_status = [
        ("التثبيت (Installation)", has_install, "يوضح كيفية إعداد وتشغيل المشروع."),
        ("الاستخدام (Usage)", has_usage, "يشرح طريقة الاستفادة من المشروع وأمثلة الاستخدام."),
        ("المميزات (Features)", has_features, "يستعرض الخصائص والمواصفات البارزة."),
        ("المساهمة (Contributing)", has_contributing, "يرشد المطورين لطريقة المشاركة في التطوير."),
        ("الترخيص (License)", has_license, "يوضح حقوق الملكية وشروط الاستخدام."),
        ("الشارات (Badges)", has_badges, "يعرض حالة البناء والإصدارات بصرياً."),
        ("صور العرض (Screenshots / Demo)", has_screenshots, "يقدم نظرة بصریة أو عروض توضيحية للمشروع.")
    ]

    for name, exists, desc in sections_status:
        if exists:
            st.markdown(f"- **{name}**: متوفر ✅ — *{desc}*")
        else:
            st.markdown(f"- **{name}**: غير متوفر ❌ — *{desc}*")

    if score < 80:
        st.markdown("---")
        st.subheader("توصيات التحسين:")
        if not has_install: st.info("• يُفضل إضافة قسم للتثبيت (Installation) بخطوات واضحة.")
        if not has_usage: st.info("• يُفضل إضافة قسم للاستخدام (Usage) يوضح كيفية تطبيق الكود.")
        if not has_contributing: st.info("• يُفضل إضافة قسم للمساهمة (Contributing) لتنظيم مشاركة المبرمجين.")
        if not has_license: st.info("• يُفضل توضيح رخصة المشروع (License) لحفظ الحقوق.")

        template_text = (
            "# Project Name\n"
            "> وصف موجز ومباشر للمشروع.\n\n"
            "## Features\n"
            "- ميزة 1\n"
            "- ميزة 2\n\n"
            "## Installation\n"
            "```bash\n"
            "git clone [https://github.com/username/repo.git](https://github.com/username/repo.git)\n"
            "```\n\n"
            "## Usage\n"
            "أضف أمثلة الاستخدام هنا.\n\n"
            "## Contributing\n"
            "تعليمات المساهمة في المشروع.\n\n"
            "## License\n"
            "MIT License"
        )

        with st.expander("عرض قالب README قياسي مقترح للنسخ"):
            st.code(template_text, language="markdown")

