from flask import Flask, render_template, request, jsonify
import joblib
import spacy

intent_model = joblib.load('models/intent_model.pkl')
vectorizer = joblib.load('models/vectorizer.pkl')
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)

def extract_entities(text):
    doc = nlp(text)
    return [{'text': ent.text, 'label': ent.label_} for ent in doc.ents]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    user_query = request.json['query']
    X = vectorizer.transform([user_query])
    intent = intent_model.predict(X)[0]
    entities = extract_entities(user_query)
    return jsonify({'intent': intent, 'entities': entities})

if __name__ == '__main__':
    app.run(debug=True)
