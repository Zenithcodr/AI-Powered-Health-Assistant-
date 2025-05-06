import streamlit as st
from transformers import pipeline
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')


# Load a pre-trained Hugging Face model
chatbot = pipeline("text-generation", model="emilyalsentzer/Bio_ClinicalBERT")

# Define healthcare-specific response logic (or use a model to generate responses)
def healthcare_chatbot(user_input):
    user_input_lower = user_input.lower().strip()
    if not user_input_lower:
        return "Please enter a valid question."
    if "symptom" in user_input_lower:
        return "It seems like you're experiencing symptoms. Please consult a doctor for accurate advice."
    elif "appointment" in user_input_lower:
        return "Would you like me to schedule an appointment with a doctor?"
    elif "medication" in user_input_lower or "medicine" in user_input_lower:
        return "It's important to take your prescribed medications regularly. If you have concerns, consult your doctor."
    elif "emergency" in user_input_lower:
        return "If this is a medical emergency, please call your local emergency number immediately."
    elif "diet" in user_input_lower or "nutrition" in user_input_lower:
        return "A balanced diet is important for good health. Would you like tips on healthy eating?"
    elif "exercise" in user_input_lower or "fitness" in user_input_lower:
        return "Regular exercise can improve your overall health. Would you like some exercise recommendations?"
    elif "mental health" in user_input_lower or "stress" in user_input_lower:
        return "Mental health is important. If you're feeling stressed or anxious, consider talking to a professional."
    else:
        try:
            response = chatbot(user_input, max_length=100, num_return_sequences=1)
            return response[0]['generated_text'].strip()
        except Exception as e:
            return f"Sorry, I couldn't process your request due to an error: {str(e)}"

# Streamlit web app interface
def main():
    st.title("Healthcare Assistant Chatbot")
    st.markdown(
        "<span style='color:red'><b>Disclaimer:</b> This chatbot is for informational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment.</span>", unsafe_allow_html=True)
    user_input = st.text_input("How can I assist you today?", "")
    if st.button("Submit"):
        if user_input:
            st.write("User: ", user_input)
            response = healthcare_chatbot(user_input)
            st.write("Healthcare Assistant: ", response)
        else:
            st.write("Please enter a query.")

if __name__ == "__main__":
    main()
