import pandas as pd
import pickle
import matplotlib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay

# 1. Load data
df = pd.read_csv("data.csv")
print(df.head())
print("Rows:", len(df), "| Intents:", df["intent"].nunique())

# 2. Clean data
df = df.dropna()
df["text"] = df["text"].str.lower().str.strip()

# 3. Text -> numbers (TF-IDF)
vectorizer = TfidfVectorizer(ngram_range=(1, 2))
X = vectorizer.fit_transform(df["text"])
y = df["intent"]

# 4. Train / test split (80% / 20%)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

# 5. Train model
model = LogisticRegression(C=10, max_iter=1000)
model.fit(X_train, y_train)

# 6. Evaluate
pred = model.predict(X_test)
print("\nTest Accuracy:", round(accuracy_score(y_test, pred), 3))
print(classification_report(y_test, pred, zero_division=0))
print("Cross-validation accuracy (5-fold):",
      round(cross_val_score(LogisticRegression(C=10, max_iter=1000), X, y,
                            cv=StratifiedKFold(5, shuffle=True, random_state=42)).mean(), 3))

cm = confusion_matrix(y_test, pred, labels=model.classes_)
fig, ax = plt.subplots(figsize=(10, 10))
ConfusionMatrixDisplay(cm, display_labels=model.classes_).plot(ax=ax, xticks_rotation=90)
plt.tight_layout()
plt.savefig("confusion_matrix.png")
print("Confusion matrix saved as confusion_matrix.png")
plt.show()

# 7. Final model: retrain on ALL data, then save
model.fit(X, y)
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))
print("Model saved!")
