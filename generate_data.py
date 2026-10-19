"""Builds data.csv: hand-written chat sentences + topic questions made from templates.
Run: python generate_data.py"""
import pandas as pd

# Part 1: hand-written sentences (small talk and questions about the bot)
hand = {'bot_identity': ['who are you', 'what is your name', 'what are you', 'tell me about yourself', 'are you a robot', 'are you human', 'who made you', 'who created you', 'introduce yourself', 'what can you do', 'are you an ai'],
    'courses': ['what courses are available', 'which subjects do you offer', 'tell me about the syllabus', 'list the courses', 'what can i study here', 'show me the subjects', 'which courses do you have', 'what do you teach', 'tell me about your courses', 'are there any ai courses'],
    'goodbye': ['bye', 'goodbye', 'see you later', 'talk to you soon', 'see you', 'bye bye', 'i have to go now', 'catch you later', 'have a nice day', 'good night', 'i am leaving', 'take care', 'see you tomorrow', 'gotta go', 'farewell'],
    'greeting': ['hi', 'hello', 'hey', 'hello there', 'good morning', 'good evening', 'hey there', 'hi bot', 'good afternoon', 'howdy', 'hiya', 'greetings', 'hello bot', 'hey buddy', 'hi there'],
    'help': ['help', 'i need help', 'can you help me', 'what can i ask you', 'how do i use you', 'give me some examples', 'what topics do you know', 'show me the menu', 'what questions can i ask', 'guide me'],
    'how_are_you': ['how are you', 'how are you doing', 'how is it going', 'whats up', 'how do you do', 'are you fine', 'how are you today', 'hows everything', 'are you okay', 'how have you been'],
    'project_info': ['how does this chatbot work', 'how were you built', 'what algorithm do you use', 'explain this project', 'what dataset did you use', 'how were you trained', 'what is tf idf', 'what is the accuracy of this chatbot', 'which model do you use', 'what is an intent'],
    'thanks': ['thank you', 'thanks a lot', 'that was helpful', 'thanks', 'many thanks', 'thank you so much', 'great thanks', 'i appreciate it', 'that helps thanks', 'thanks for the help', 'awesome thanks', 'nice answer', 'cool thank you', 'perfect thanks', 'you are great']}

# Part 2: topic terms. Each term is turned into several question styles.
topics = {
"ai_info": ["artificial intelligence", "ai", "difference between ai and ml", "ai vs machine learning vs deep learning"],
"ml_info": ["machine learning", "ml", "machine learning in simple words", "how machines learn"],
"dl_info": ["deep learning", "neural network", "neural networks", "cnn", "artificial neuron", "layers in a neural network"],
"supervised": ["supervised learning", "classification", "regression", "linear regression", "multiple linear regression", "logistic regression", "knn", "k nearest neighbors", "decision tree", "random forest"],
"unsupervised": ["unsupervised learning", "clustering", "k means", "kmeans clustering", "hierarchical clustering", "pca", "dimensionality reduction", "anomaly detection", "reinforcement learning"],
"workflow": ["machine learning workflow", "ml pipeline", "model training", "data preprocessing", "model evaluation", "model deployment", "steps of a machine learning project", "data collection"],
"metrics": ["accuracy", "precision", "recall", "f1 score", "confusion matrix", "cross validation", "evaluation metrics", "precision and recall"],
"data_prep": ["dataset", "data cleaning", "missing values", "feature scaling", "normalization", "standardization", "feature selection", "train test split", "eda", "exploratory data analysis", "heat map", "histogram", "scatter plot", "correlation"],
"python_libs": ["numpy", "pandas", "matplotlib", "scikit learn", "sklearn", "google colab", "jupyter notebook", "anaconda", "python libraries for ml"],
"applications": ["ml in healthcare", "ml in iot", "ml in signal processing", "ai in telecommunication", "ai in robotics", "ai in agriculture", "ml in industrial automation", "applications of machine learning", "ai in smart manufacturing", "ml in smart communication systems"],
"trends": ["generative ai", "edge ai", "tinyml", "aiot", "explainable ai", "xai", "ai in 5g", "ai in 6g", "ai assistants", "future of ai"],
"api_info": ["an api", "an ai api", "cloud ai", "prompt engineering", "a prompt", "gemini", "a large language model", "llm", "chatgpt", "generative ai tools"],
"ethics": ["responsible ai", "ai ethics", "bias in ai", "dataset bias", "fairness in ai", "ai safety", "risks of ai", "ethical issues in ai"],
}
templates = ["what is {t}", "explain {t}", "tell me about {t}", "define {t}", "{t} meaning", "can you explain {t}"]

rows = []
for intent, sents in hand.items():
    rows += [{"text": s, "intent": intent} for s in sents]
for intent, terms in topics.items():
    for t in terms:
        for tpl in templates:
            rows.append({"text": tpl.format(t=t), "intent": intent})

df = pd.DataFrame(rows).drop_duplicates()
df.to_csv("data.csv", index=False)
print("data.csv created:", df.shape, "| intents:", df["intent"].nunique())
