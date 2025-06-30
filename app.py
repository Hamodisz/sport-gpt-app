import streamlit as st
import openai
from deep_translator import GoogleTranslator
import urllib.parse
import base64

# إعداد الواجهة
st.set_page_config(page_title="Find Your Sport", layout="centered")

st.markdown("""
<h1 style='text-align: center; color: #3F8CFF;'>🏅 Find Your Sport</h1>
<p style='text-align: center;'>اكتشف رياضتك المثالية حسب شخصيتك</p>
""", unsafe_allow_html=True)

# تحديد اللغة
language = st.radio("🌐 Choose your language / اختر لغتك:", ["English", "العربية"])

# أسئلة التشخيص
questions = {
    "English": [
        "1. Do you prefer to be alone or with people?",
        "2. What makes you feel focused for a long time?",
        "3. Do you like being the center of attention?",
        "4. How do you react when someone challenges you?",
        "5. What motivates you most? Winning, fun, or improving?",
        "6. Do you like danger or prefer to stay safe?",
        "7. What type of place makes you feel good? (nature, city, closed room...etc)",
        "8. Do you love tools and gear or simple action?",
        "9. If you had a power, what would it be?",
        "10. What kind of game or activity makes you forget time?",
        "11. Do you like competing with others or with yourself?",
        "12. What's more important: strength, speed, or strategy?",
        "13. Do you enjoy solving problems?",
        "14. What do you usually watch on TikTok or YouTube?",
        "15. Would you rather lead a team or act alone?",
        "16. Do you enjoy exploring new places?",
        "17. How do you feel about high places or speed?",
        "18. What kind of challenge makes you excited?",
        "19. Do you enjoy planning or prefer reacting fast?",
        "20. Do you admire athletes, gamers, or adventurers more?"
    ],
    "العربية": [
        "1. تحب تكون لحالك أو مع ناس؟",
        "2. وش الشي اللي يخليك تركز لفترة طويلة؟",
        "3. تحب تكون محط الأنظار؟",
        "4. وش تسوي إذا أحد تحداك؟",
        "5. وش أكثر شي يحفزك؟ الفوز، المتعة، أو التطور؟",
        "6. تحب الأشياء الخطيرة أو تفضل الأمان؟",
        "7. وش نوع المكان اللي يريحك؟ (طبيعة، مدينة، غرفة...الخ)",
        "8. تحب الأدوات والملابس أو الحركات البسيطة؟",
        "9. لو عندك قوة خارقة، وش بتكون؟",
        "10. وش الشي اللي يخليك تنسى الوقت إذا سويته؟",
        "11. تحب تتنافس مع غيرك أو مع نفسك؟",
        "12. الأهم عندك: القوة، السرعة، أو الذكاء؟",
        "13. تستمتع بحل المشاكل؟",
        "14. غالباً وش تشوف على تيك توك أو يوتيوب؟",
        "15. تحب تقود الفريق أو تشتغل لحالك؟",
        "16. تحب تستكشف أماكن جديدة؟",
        "17. وش شعورك تجاه المرتفعات أو السرعة؟",
        "18. وش نوع التحدي اللي يخليك تتحمس؟",
        "19. تحب تخطط ولا تشتغل بسرعة؟",
        "20. تعجبك الرياضيين، ولا اللاعبين، ولا المغامرين أكثر؟"
    ]
}

# استقبال الإجابات
st.header("✍️ Answer the Questions")
answers = [st.text_input(q) for q in questions[language]]

# عند الضغط على زر التوصية
if st.button("🎯 Get Your Sport / احصل على رياضتك"):
    if all(answers):
        answers_en = [GoogleTranslator(source='auto', target='en').translate(a) if language == "العربية" else a for a in answers]
        joined = "\n".join([f"Q{i+1}: {a}" for i, a in enumerate(answers_en)])

        openai.api_key = st.secrets["OPENAI_API_KEY"]

        prompt = f"""You are a sports innovation AI. Based on the user's personality traits and preferences below, invent a unique sport for them. Include:
- Personality Archetype
- Identity Archetype
- Recommended Sport Name
- Description
- Environment
- Tools Needed

User Answers:
{joined}
"""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        result = response.choices[0].message.content.strip()

        if language == "العربية":
            result = GoogleTranslator(source='en', target='ar').translate(result)
            st.markdown("### ✅ تم التشخيص")
        else:
            st.markdown("### ✅ Recommendation Complete")

        st.text_area("📋 Result", result, height=300)

    else:
        st.warning("⛔ Please answer all questions. / جاوب على كل الأسئلة من فضلك.")
