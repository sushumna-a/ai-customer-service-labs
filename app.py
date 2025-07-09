import json
from flask import Flask, render_template, request, jsonify
import joblib
import spacy
import os

# Load models
intent_model = joblib.load(os.path.join('models', 'intent_model.pkl'))
vectorizer = joblib.load(os.path.join('models', 'vectorizer.pkl'))
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)

# Load FAQs from JSON file at startup
with open('faqs.json', encoding='utf-8') as f:
    faq_list = json.load(f)

def extract_entities(text):
    doc = nlp(text)
    return [{'text': ent.text, 'label': ent.label_} for ent in doc.ents]

@app.route('/')
def home():
    return render_template('index.html', faqs=faq_list)

@app.route('/faq/<int:faq_id>')
def faq_detail(faq_id):
    faq = next((f for f in faq_list if f['id'] == faq_id), None)
    if not faq:
        return "FAQ not found", 404
    return render_template('faq_detail.html', faq=faq)

@app.route('/predict', methods=['POST'])
def predict():
    user_query = request.json['query']
    X = vectorizer.transform([user_query])
    intent = intent_model.predict(X)[0]
    entities = extract_entities(user_query)
    return jsonify({'intent': intent, 'entities': entities})

if __name__ == '__main__':
    app.run(debug=True)
