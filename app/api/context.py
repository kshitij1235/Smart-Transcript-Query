import google.generativeai as genai
from app.config import settings
genai.configure(api_key=settings.GEMINI_API_KEY)
models = genai.list_models()
for model in models:
    print(model.name)
conversation_history = []

def ask_gemini(user_question):
    global conversation_history

    # Build the prompt
    prompt = ""
    for q, a in conversation_history:
        prompt += f"Q: {q}\nA: {a}\n"
    prompt += f"Q: {user_question}\nA:"  # No answer yet

    # Query Gemini
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)

    # Extract answer
    answer = response.text.strip()

    # Save Q&A to history
    conversation_history.append((user_question, answer))

    return answer