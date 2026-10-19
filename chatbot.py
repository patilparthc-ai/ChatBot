import os
import pickle
from responses import responses

# ---------- Settings ----------
CONFIDENCE = 0.40          # below this, the ML model is "not sure" -> use API
API_KEY = os.environ.get("GEMINI_API_KEY", "")   # or paste your key here: API_KEY = "xxxx"
# Model names change over time; the bot tries these one by one.
MODELS = ["gemini-3.5-flash", "gemini-2.5-flash", "gemini-2.0-flash"]
# ------------------------------

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

client = None
if API_KEY:
    try:
        from google import genai
        client = genai.Client(api_key=API_KEY)
    except Exception as e:
        print("API setup failed:", e)

def ask_api(question):
    """Send the question to a Generative AI API (used when ML model is not sure)."""
    if client is None:
        return None
    prompt = ("You are a friendly student-project chatbot about AI, ML and general topics. "
              "Answer clearly in 3-4 short sentences.\nQuestion: " + question)
    for name in MODELS:
        try:
            return client.models.generate_content(model=name, contents=prompt).text
        except Exception:
            continue
    return None

def get_reply(text):
    vec = vectorizer.transform([text.lower().strip()])
    probs = model.predict_proba(vec)[0]
    best = probs.max()
    intent = model.classes_[probs.argmax()]
    if best >= CONFIDENCE:
        return "ML model", responses[intent], best
    answer = ask_api(text)
    if answer:
        return "AI API", answer, best
    return "Fallback", ("I'm not sure about that. I know about AI, ML, Python, metrics and more "
                        "(type 'help'). Add an API key to answer any topic."), best

if __name__ == "__main__":
    print("Chatbot ready! Type 'quit' to exit.")
    print("API mode:", "ON" if client else "OFF (no key set)")
    while True:
        user = input("You: ").strip()
        if not user:
            continue
        if user.lower() in ("quit", "exit"):
            print("Bot: Bye!")
            break
        source, reply, conf = get_reply(user)
        print(f"Bot [{source}, confidence {conf:.2f}]: {reply}")
