import streamlit as st
import openai

st.set_page_config(page_title="Find Your Sport", layout="centered")

# Title
st.markdown("## 🏅 Find Your Sport")
st.markdown("Answer a few quick questions to discover the sport that fits you best.")

# Load API Key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Language selection
language = st.radio("Choose your language:", ["English", "العربية"])

# Questions (simple + short)
questions_en = [
    "Do you enjoy being alone or with others?",
    "Do you prefer calm or intense experiences?",
    "What motivates you more: fun, challenge, or mastery?",
    "How do you express yourself physically?",
    "What kind of risk are you okay with?"
]

questions_ar = [
    "هل تفضل أن تكون وحدك أم مع الآخرين؟",
    "هل تفضل التجارب الهادئة أم المكثفة؟",
    "ما الذي يحفزك أكثر: المرح، التحدي، أم الإتقان؟",
    "كيف تعبر عن نفسك جسديًا؟",
    "ما نوع المخاطرة التي تتقبلها؟"
]

questions = questions_en if language == "English" else questions_ar

answers = []
for q in questions:
    answer = st.text_input(q)
    answers.append(answer)

# When all answered
if all(answers):
    joined = "\n".join([f"{q} {a}" for q, a in zip(questions, answers)])

    with st.spinner("Thinking..."):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You're a sport matchmaker who finds the perfect sport for each person based on personality and preferences. Be bold, creative, and concise."},
                {"role": "user", "content": f"My preferences:\n{joined}\nWhat is the perfect sport for me and why?"}
            ],
            temperature=0.9,
            max_tokens=300
        )

        result = response.choices[0].message.content
        st.markdown("### 🎯 Your Sport Recommendation:")
        st.success(result)

        # Share buttons
        st.markdown("#### 🔗 Share this result:")
        st.code(result, language="markdown")
        st.button("📋 Copy Recommendation")
        st.markdown("[📨 Send to a Friend on WhatsApp](https://wa.me/?text=" + result.replace(" ", "%20") + ")")
