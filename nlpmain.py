import os
import random
import requests
import nltk
import spacy
from flask import Flask, request, render_template, jsonify
from bs4 import BeautifulSoup
from docx import Document
# from nltk.tokenize import sent_tokenize
from nltk.tokenize import PunktSentenceTokenizer
from dotenv import load_dotenv
from flask_cors import CORS



# PUNKT TOKENIZER NOT THE OTHER ONE

nltk.download('punkt')
tokenizer = PunktSentenceTokenizer()

nlp = spacy.load("en_core_web_md")


app = Flask(__name__)
CORS(app, resources={  
    r"/upload": {
        "origins": ["http://localhost:3000"],
        "methods": ["POST"],
        "allow_headers": ["Content-Type"]
    }
})
load_dotenv()
SERP_API_KEY = os.getenv("API_KEY")


def read_file(file):
    if file.filename.endswith(".txt"):
        return file.read().decode("utf-8")
    elif file.filename.endswith(".docx"):
        doc = Document(file)
        return " ".join([para.text for para in doc.paragraphs])
    else:
        return None
    


def extract_sentences(content, num_sentences=5):
    sentences = tokenizer.tokenize(content)
    if len(sentences) <= num_sentences:
        return sentences
    return random.sample(sentences, num_sentences)


def search_google(phrase):

     if not SERP_API_KEY:
        print("ERROR: Missing SerpAPI key")
        return []

     try:
        response = requests.get(
            "https://serpapi.com/search",
            params={
                "engine": "google",
                "q": phrase[:300],  # Trim long queries
                "api_key": "5c09317f51df2e8f6e9efd1f94fc74be1cb6efc8b296f7f800d3f047c9194fe3",
                "num": 3
            },
            timeout=15
        )
        response.raise_for_status()
        return [result["link"] for result in response.json().get("organic_results", [])]
     except Exception as e:
        print(f"Search failed: {str(e)}")
        return []

def fetch_text_from_url(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text()
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return ""


def calculate_similarity(text1, text2):
    doc1 = nlp(text1)
    doc2 = nlp(text2)
    return doc1.similarity(doc2)


def get_match_percentage(phrase, page_text):
    if not page_text.strip():
        return 0.0

    page_sentences = tokenizer.tokenize(page_text)
    scores = [calculate_similarity(phrase, sent) for sent in page_sentences if sent.strip()]
    if not scores:
        return 0.0
    return round(max(scores) * 100, 2)


def analyze_phrases(content):
    phrases = extract_sentences(content, num_sentences=5)
    results = []

    for phrase in phrases:
        links = search_google(phrase)
        matches = []

        for link in links:
            page_text = fetch_text_from_url(link)
            match = get_match_percentage(phrase, page_text)
            matches.append({"url": link, "match": match})

        results.append({"phrase": phrase, "matches": matches})

    return results


def calculate_total_percentage(results):
    if not results:
        return 0.0
    

    all_scores = []
    for item in results:
        if item.get("matches"):
            weights = [1 / (i + 1) for i in range(len(item["matches"]))]
            scores = [match["match"] for match in item["matches"]]
            weighted_sum = sum(w * s for w, s in zip(weights, scores))
            weight_sum = sum(weights)
            if weight_sum > 0:
                weighted_avg = weighted_sum / weight_sum
                all_scores.append(weighted_avg)
    if all_scores:
        return round(sum(all_scores) / len(all_scores), 2) if all_scores else 0.0
    else:
        return 0.0


@app.route("/", methods=["GET"])
def index():
    # upload page hai
    return {"message": "Plagiarism Checker API is running"}


@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        #handle file upload
        file = request.files.get("file")
        if not file:
            return jsonify({"error": True,
                        "message": "No file uploaded"}),400
    
        
        content = read_file(file)
        if content is None:
            return jsonify({"error": "Unsupported file type"}), 400
    
    
        results = analyze_phrases(content)
        plagiarism_score = calculate_total_percentage(results)

        return jsonify({
            "filename": file.filename,
            "results": results,
            "plagiarism_score": plagiarism_score
        })

    except Exception as e :
        print(f"Upload Error: {str(e)}")
        return jsonify({"error": str(e)}) , 500


if __name__ == "__main__":
    app.run(debug=True)
