import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
import joblib
import os

# Example dataset for demonstration
data = {
    'text': [
        "What is my account balance?",
        "I want to dispute a transaction.",
        "How can I apply for a loan?",
        "Show my last five transactions.",
        "Report a lost credit card."
    ],
    'intent': [
        "balance_inquiry",
        "transaction_dispute",
        "loan_information",
        "transaction_history",
        "card_report"
    ]
}
df = pd.DataFrame(data)

# Vectorize the text
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['text'])
y = df['intent']

# Train the intent classifier
clf = LinearSVC()
clf.fit(X, y)

# Save the models
os.makedirs('models', exist_ok=True)
joblib.dump(clf, 'models/intent_model.pkl')
joblib.dump(vectorizer, 'models/vectorizer.pkl')

print("Models saved successfully in the 'models/' directory.")