import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

SYSTEM_PROMPT = (
    "You are a medical guidance assistant for informational guidance only. "
    "Only answer health, symptoms, wellness, medication-safety, and care-navigation questions. "
    "If the user asks non-medical questions, refuse briefly and ask for a health-related query. "
    "You are not a doctor. Give clear and practical advice, suggest when to seek "
    "professional care, and avoid diagnosis certainty. If emergency symptoms are "
    "present (chest pain, severe breathing issues, stroke signs, heavy bleeding, "
    "suicidal intent), immediately advise contacting emergency services."
)


def is_medical_query(user_input: str) -> bool:
    text = user_input.lower()
    medical_terms = {
        "health",
        "medical",
        "doctor",
        "hospital",
        "clinic",
        "symptom",
        "pain",
        "fever",
        "cough",
        "cold",
        "flu",
        "headache",
        "migraine",
        "nausea",
        "vomit",
        "diarrhea",
        "rash",
        "infection",
        "blood pressure",
        "sugar",
        "diabetes",
        "asthma",
        "allergy",
        "medication",
        "medicine",
        "dose",
        "tablet",
        "side effect",
        "prescription",
        "diet",
        "nutrition",
        "exercise",
        "fitness",
        "sleep",
        "mental health",
        "anxiety",
        "depression",
        "stress",
        "therapy",
        "pregnancy",
        "period",
        "injury",
        "wound",
        "emergency",
        "first aid",
        "vaccin",
    }
    return any(term in text for term in medical_terms)


def off_topic_message() -> str:
    return (
        "I am a medical chatbot, so I can only help with health-related questions. "
        "Please ask about symptoms, medicines, diet, mental health, fitness, or when to see a doctor."
    )


def contains_emergency_signal(user_input: str) -> bool:
    text = user_input.lower()
    emergency_terms = [
        "chest pain",
        "can't breathe",
        "cannot breathe",
        "severe bleeding",
        "stroke",
        "heart attack",
        "suicide",
        "kill myself",
        "overdose",
    ]
    return any(term in text for term in emergency_terms)


def emergency_message() -> str:
    return (
        "This may be an emergency. Please call your local emergency number now "
        "or go to the nearest emergency room immediately."
    )


def local_fallback_reply(user_input: str) -> str:
    text = user_input.lower().strip()
    if not text:
        return "Please share your question so I can help."
    if "fever" in text:
        return (
            "For fever, stay hydrated and rest. If fever is high, lasts over 2-3 days, "
            "or comes with severe symptoms, contact a doctor."
        )
    if "headache" in text:
        return (
            "Headaches can happen for many reasons like stress, dehydration, or sleep loss. "
            "If it is severe, sudden, or persistent, seek medical evaluation."
        )
    if "diet" in text or "nutrition" in text:
        return (
            "A balanced plate usually includes vegetables, lean protein, fiber-rich carbs, "
            "healthy fats, and enough water."
        )
    if "exercise" in text or "fitness" in text:
        return (
            "Most adults benefit from regular physical activity, such as brisk walking and "
            "strength work each week, adjusted to personal health conditions."
        )
    return (
        "I can share general health guidance, but this does not replace professional "
        "medical care. If your symptoms are worsening or persistent, please consult a doctor."
    )


def build_mistral_client(api_key: str) -> OpenAI:
    return OpenAI(api_key=api_key, base_url="https://api.mistral.ai/v1")


def get_mistral_api_key() -> str:
    # Keep secret lookup on backend only: Streamlit secrets first, then local .env.
    try:
        secret_key = st.secrets.get("MISTRAL_API_KEY", "")
        if secret_key:
            return secret_key
    except Exception:  # noqa: BLE001
        # No Streamlit secrets file configured, fallback to .env.
        pass
    return os.getenv("MISTRAL_API_KEY", "")


def generate_response(mistral_key: str, mistral_model: str, messages: list[dict[str, str]]) -> str:
    latest_user_message = messages[-1]["content"] if messages else ""

    if messages and not is_medical_query(latest_user_message):
        return off_topic_message()

    if messages and contains_emergency_signal(messages[-1]["content"]):
        return emergency_message()

    if not mistral_key:
        return local_fallback_reply(latest_user_message)

    try:
        client = build_mistral_client(mistral_key)

        completion = client.chat.completions.create(
            model=mistral_model,
            temperature=0.4,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *messages,
            ],
        )
        content = completion.choices[0].message.content
        return content.strip() if content else "I could not generate a response."
    except Exception as exc:  # noqa: BLE001
        return (
            "I could not reach the model provider right now. "
            f"Error: {exc}. Falling back to basic guidance: "
            + local_fallback_reply(latest_user_message)
        )


def init_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []


def sidebar_settings() -> dict[str, str]:
    st.sidebar.header("Model Settings")
    mistral_model = st.sidebar.text_input(
        "Mistral Model",
        value=os.getenv("MISTRAL_MODEL", "mistral-small-latest"),
    )
    api_status = "configured" if get_mistral_api_key() else "missing"
    st.sidebar.caption(f"Mistral API key status: {api_status}")

    if st.sidebar.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    return {
        "mistral_model": mistral_model,
    }


def main() -> None:
    st.set_page_config(page_title="AI Health Assistant", page_icon="stethoscope", layout="wide")
    init_state()

    st.title("AI-Powered Health Assistant")
    st.caption(
        "Informational guidance only. This app does not provide medical diagnosis or treatment."
    )

    settings = sidebar_settings()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_prompt = st.chat_input("Describe your symptoms or ask a health question...")
    if not user_prompt:
        return

    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = generate_response(
                get_mistral_api_key(),
                settings["mistral_model"],
                st.session_state.messages,
            )
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
