import streamlit as st
import openai
from deep_translator import GoogleTranslator
import urllib.parse
import base64

# إعداد صفحة التطبيق
st.set_page_config(page_title="Find Your Sport", layout="centered")
openai.api_key = st.secrets["OPENAI_API_KEY"]

# العنوان
st.markdown("""
<h1 style='text-align: center; color: #3F8CFF;'>🏅 Find Your Sport</h1>
<p style='text-align: center;'>رياضة مصممة لشخصيتك باستخدام الذكاء الاصطناعي</p>
""", unsafe_allow_html=True)

# اختيار اللغة
language = st.radio("🌐 اختر لغتك / Choose your language:", ["العربية", "English"])

# الأسئلة
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

# إدخال الأجوبة
st.header("✍️ Answer the Questions")
answers = [st.text_input(q) for q in questions[language]]

# زر التوصية
if st.button("🎯 احصل على رياضتك"):
    if all(answers):
        # ترجمة الإجابات
        answers_en = [
            GoogleTranslator(source='auto', target='en').translate(ans) if language == "العربية" else ans
            for ans in answers
        ]
        formatted = "\n".join([f"Q{i+1}: {a}" for i, a in enumerate(answers_en)])

        # برومبت GPT
        prompt = f"""You are a sport innovation expert AI.
Analyze the user's personality based on the following answers and create a unique sport that matches their identity.
Return your answer in this format:

Personality_Archetype: ...
Identity_Archetype: ...
Recommended_Sport_Name: ...
Sport_Description: ...
Environment: ...
Tools_Needed: ...

Answers:
{formatted}
"""

        # الاتصال بـ GPT
        res = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        output = res.choices[0].message.content.strip()

        # ترجمة الناتج للعربية إذا لزم
        translated_output = GoogleTranslator(source='en', target='ar').translate(output) if language == "العربية" else output

        # عرض التوصية
        st.success("✅ تم التشخيص")
        st.markdown(f"### 🧠 تشخيصك الرياضي:

```
{translated_output}
```")

        # نسخ التوصية
        st.text_area("📋 انسخ نتيجتك أو احفظها:", translated_output, height=250)

        # مشاركة عبر واتساب
        share_text = f"شخصيتي الرياضية هي:\n{translated_output}\nجرب تطلع رياضتك! 👇\nhttps://sport-gpt-app.streamlit.app"
        whatsapp_link = "https://wa.me/?text=" + urllib.parse.quote(share_text)
        st.markdown(f"[📲 شارك مع صديق على واتساب]({whatsapp_link})", unsafe_allow_html=True)

        # توليد رابط دائم (base64)
        encoded = base64.urlsafe_b64encode(translated_output.encode()).decode()
        shareable_link = f"https://sport-gpt-app.streamlit.app/?r={encoded}"
        st.markdown(f"[🔗 رابط نتيجتك الدائم]({shareable_link})", unsafe_allow_html=True)

    else:
        st.warning("❗ جاوب على كل الأسئلة قبل الضغط على الزر.")
