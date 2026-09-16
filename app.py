import streamlit as st
import requests

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="ReadmeRank - Pro Auditor",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 ReadmeRank: Pro GitHub README Auditor")
st.write("أداة فحص وتقييم ملفات الـ README لاحتراف مشاريع المตรี (Open Source) ورفع جودتها.")

# 2. طريقة الإدخال (رابط مستودع أو رفع ملف)
st.markdown("---")
input_method = st.radio("اختر طريقة إدخال ملف الـ README:", ["🔗 رابط مستودع GitHub", "📁 رفع ملف محلي (Markdown)"])

readme_content = ""
analysis_triggered = False

if input_method == "🔗 رابط مستودع GitHub":
    repo_input = st.text_input("أدخل رابط المستودع أو اسم المستخدم/المشروع (مثال: username/repo):", placeholder="https://github.com/torvalds/linux")
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
                # محاولة جلب الملف (تغطية الحالتين main و master)
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
                    st.error("❌ لم يتم العثور على ملف README.md في هذا المستودع (تأكد أن المستودع عام وأن الرابط صحيح).")
            else:
                st.error("⚠️ صيغة الرابط غير صحيحة. استخدم: owner/repo أو الرابط الكامل.")

else:
    uploaded_file = st.file_uploader("اختر ملف README.md من جهازك:", type=["md", "txt"])
    if st.button("🔍 فحص الملف المرفوع", type="primary"):
        if uploaded_file is not None:
            readme_content = uploaded_file.getvalue().decode("utf-8")
            st.success("✅ تم رفع وفحص الملف بنجاح!")
            analysis_triggered = True
        else:
            st.warning("⚠️ الرجاء رفع ملف أولاً.")

# 3. عملية التحليل والفحص الشامل
if analysis_triggered and readme_content:
    st.markdown("---")
    st.subheader("📊 تقرير الفحص والتحليل الاحترافي")

    content_lower = readme_content.lower()
    
    # فحص الأقسام والمكونات المتقدمة
    has_install = any(k in content_lower for k in ["install", "installation", "getting started", "طريقة التثبيت", "التثبيت"])
    has_usage = any(k in content_lower for k in ["usage", "how to use", "examples", "استخدام", "كيفية الاستخدام"])
    has_features = any(k in content_lower for k in ["feature", "features", "highlights", "المميزات", "الخصائص"])
    has_contributing = any(k in content_lower for k in ["contribut", "pull request", "المساهمة", "المطورين المشاركين"])
    has_license = any(k in content_lower for k in ["license", "licence", "الترخيص", "رخصة"])
    has_badges = any(k in content_lower for k in ["[![", "img.shields.io", "badge"])
    has_screenshots = any(k in content_lower for k in ["screenshot", "demo", "preview", "gif", "صورة", "عرض"])

    # نظام الأوزان والسكور الذكي (من 100)
    score = 0
    if has_install: score += 20
    if has_usage: score += 20
    if has_features: score += 15
    if has_contributing: score += 15
    if has_license: score += 10
    if has_badges: score += 10
    if has_screenshots: score += 10

    # عرض النتيجة الإجمالية
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="التقييم الكلي (Score)", value=f"{score}/100")
    with col2:
        if score >= 80:
            st.success("الحالة: ممتاز 🌟 (مشروع احترافي)")
        elif score >= 50:
            st.warning("الحالة: جيد، لكن يحتاج تحسينات ⚠️")
        else:
            st.error("الحالة: ضعيف جداً ❌ (يفتقر لأهم الأقسام)")
    with col3:
        word_count = len(readme_content.split())
        st.metric(label="عدد كلمات الـ README", value=word_count)

    # تفاصيل الأقسام مع أيقونات بصرية واضحة
    st.markdown("### 📋 تفصيل الأقسام:")
    
    sections_status = [
        ("Installation (التثبيت)", has_install, "يساعد المستخدمين في معرفة كيفية تشغيل المشروع."),
        ("Usage (الاستخدام والأمثلة)", has_usage, "يشرح للمطور كيف يستفيد من المشروع عملياً."),
        ("Features (المميزات)", has_features, "يبرز قوة المشروع ونقاط تميزه."),
        ("Contributing (المساهمة)", has_contributing, "يشجع المبرمجين الآخرين على المشاركة وتطوير الكود."),
        ("License (الترخيص)", has_license, "يحفظ حقوق الملكية والاستخدام القانوني."),
        ("Badges (الشارات والدروع)", has_badges, "يعطي مظهراً تقنياً واحترافياً للمستودع."),
        ("Screenshots / Demo (الصور والعروض)", has_screenshots, "يوضح شكل المشروع أو مخرجاته بصرياً.")
    ]

    for name, exists, desc in sections_status:
        if exists:
            st.markdown(f"✅ **{name}**: موجود - *{desc}*")
        else:
            st.markdown(f"❌ **{name}**: غير موجود (مفقود) - *{desc}*")

    # اقتراحات ذكية وقالب جاهز لو السكور قليل
    if score < 80:
        st.markdown("---")
        st.subheader("💡 اقتراحات لتحسين الـ README الخاص بك:")
        if not has_install:
            st.info("👉 **نصيحة**: أضف قسم `## Installation` واكتب فيه أوامر التثبيت مثل `pip install` أو `git clone`.")
        if not has_usage:
            st.info("👉 **نصيحة**: أضف قسم `## Usage` مع أمثلة برمجية واضحة وكود تجريبي.")
        if not has_contributing:
            st.info("👉 **نصيحة**: أضف قسم `## Contributing` لتوضيح كيفية استقبال المساهمات الخارجية.")
        if not has_license:
            st.info("👉 **نصيحة**: أضف ملف وذكر رخصة المشروع (مثل MIT License) داخل الـ README.")

        with st.expander("📝 اضغط هنا لرؤية قالب README احترافي جاهز للنسخ"):
            st.code("""# Project Name 🚀
> وصف قصير وقوي للمشروع في سطرين.

## ✨ Features
- مميزة 1
- مميزة 2

## 📦 Installation
```bash
git clone [https://github.com/your-username/your-repo.git](https://github.com/your-username/your-repo.git)
cd your-repo
# قم بتثبيت المتطلبات

