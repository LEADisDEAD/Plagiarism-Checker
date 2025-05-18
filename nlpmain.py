import os
import random
import requests
import nltk
import spacy
from flask import Flask, request, render_template
from bs4 import BeautifulSoup
from docx import Document
# from nltk.tokenize import sent_tokenize
from nltk.tokenize import PunktSentenceTokenizer
from dotenv import load_dotenv

# PUNKT TOKENIZER NOT THE OTHER ONE

nltk.download('punkt')
tokenizer = PunktSentenceTokenizer()

nlp = spacy.load("en_core_web_sm")

load_dotenv()
app = Flask(__name__)
SERP_API_KEY = os.getenv("API_KEY")


def read_file(file):
    if file.filename.endswith(".txt"):
        return file.read().decode("utf-8")
    elif file.filename.endswith(".docx"):
        doc = Document(file)
        return " ".join([para.text for para in doc.paragraphs])
    return ""


def extract_sentences(content, num_sentences=5):
    sentences = tokenizer.tokenize(content)
    if len(sentences) <= num_sentences:
        return sentences
    return random.sample(sentences, num_sentences)


def search_google(phrase):
    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": phrase,
        "api_key": SERP_API_KEY,
        "num": 3
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        # Extract URLs from organic results if available
        return [result["link"] for result in data.get("organic_results", []) if "link" in result]
    except Exception as e:
        print(f"Error during Google Search: {e}")
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
    phrase_links = []

    for phrase in phrases:
        links = search_google(phrase)
        match_percentages = []

        for link in links:
            page_text = fetch_text_from_url(link)
            match = get_match_percentage(phrase, page_text)
            match_percentages.append({"url": link, "match": match})

        phrase_links.append({"phrase": phrase, "links": match_percentages})

    return phrase_links


def calculate_total_percentage(phrase_links):
    all_scores = []
    for item in phrase_links:
        if item["links"]:
            weights = [1 / (i + 1) for i in range(len(item["links"]))]
            scores = [link["match"] for link in item["links"]]
            weighted_sum = sum(w * s for w, s in zip(weights, scores))
            weight_sum = sum(weights)
            if weight_sum > 0:
                weighted_avg = weighted_sum / weight_sum
                all_scores.append(weighted_avg)
    if all_scores:
        return round(sum(all_scores) / len(all_scores), 2)
    else:
        return 0.0


@app.route("/", methods=["GET"])
def index():
    # upload page hai
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    if not file:
        return render_template("index.html", error="No file uploaded.")

    content = read_file(file)

    if content:
        phrase_links = analyze_phrases(content)
        total_percentage = calculate_total_percentage(phrase_links)
        return render_template("result.html", filename=file.filename, phrase_links=phrase_links,
                               total_percentage=total_percentage)

    return render_template("index.html", error="Failed to read the file.")


if __name__ == "__main__":
    app.run(debug=True)
