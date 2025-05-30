from flask import Flask, render_template, request, session, redirect, url_for
from serpapi import GoogleSearch
import random
import os
from docx import Document
from difflib import SequenceMatcher
import requests
from bs4 import BeautifulSoup
import re
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.secret_key = os.getenv('ogog', 'fallback_secret_key')  # Load secret key from .env or fallback to a default key

# SerpAPI key from .env file
API_KEY = os.getenv('API_KEY')


def read_file_content(file_path, filename):
    if filename.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    elif filename.endswith(".docx"):
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return None


def extract_random_phrases(content, num_phrases=40, phrase_length=40):
    words = content.split()
    total_words = len(words)
    if total_words < phrase_length * num_phrases:
        num_phrases = total_words // phrase_length
        phrase_length = 1

    phrases = set()
    while len(phrases) < num_phrases:
        start_idx = random.randint(0, len(words) - phrase_length)
        phrase = ' '.join(words[start_idx:start_idx + phrase_length])
        phrases.add(phrase)

    return list(phrases)


def get_top_google_results(phrase, num_results=3):
    if not API_KEY:
        raise ValueError("API_KEY is missing in environment variables.")

    # SerpAPI seeetupp
    params = {
        "q": phrase,
        "api_key": API_KEY,
        "num": num_results
    }

    search = GoogleSearch(params)
    results = search.get_dict()


    links = []
    for result in results.get("organic_results", []):
        links.append(result.get("link"))

        if len(links) >= num_results:
            break

    return links


def scrape_page_text(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text(separator=' ', strip=True)
        return text
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""


def calculate_total_percentage(phrase_links):
    all_scores = []
    for links in phrase_links:
        if links:
            max_match = max(link["match"] for link in links['links'])
            all_scores.append(max_match)
    if not all_scores:
        return 0
    return round(sum(all_scores) / len(all_scores), 2)


def get_match_percentage(phrase, page_text):
    if not page_text:
        return 0.0

    phrase = phrase.lower().strip()
    sentences = re.split(r'[.!?]', page_text.lower())  # Split into sentences

    max_ratio = 0
    for sentence in sentences:
        matcher = SequenceMatcher(None, phrase, sentence.strip())
        ratio = matcher.quick_ratio()
        max_ratio = max(max_ratio, ratio)

    return round(max_ratio * 100, 2)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/result")
def result():

    phrase_links = session.get('phrase_links', [])
    total_percentage = calculate_total_percentage(phrase_links)
    return render_template("result.html", filename=session.get('filename', ''), phrase_links=phrase_links, total_percentage=total_percentage)


@app.route("/upload", methods=["POST"])
def upload_file():
    uploaded_file = request.files["file"]

    if uploaded_file.filename == "":
        return "No file selected."


    if not (uploaded_file.filename.endswith(".txt") or uploaded_file.filename.endswith(".docx")):
        return "Unsupported file type. Please upload a .txt or .docx file."

    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
    uploaded_file.save(file_path)

    content = read_file_content(file_path, uploaded_file.filename)
    if not content:
        return "Unsupported file type."

    phrases = extract_random_phrases(content, num_phrases=5)

    phrase_links = []

    for phrase in phrases:
        links = get_top_google_results(phrase)
        enriched_links = []

        for link in links:
            page_text = scrape_page_text(link)
            match_percent = get_match_percentage(phrase, page_text)
            enriched_links.append({"url": link, "match": match_percent})

        phrase_links.append({"phrase": phrase, "links": enriched_links})


    session['phrase_links'] = phrase_links
    session['filename'] = uploaded_file.filename

    # Redirect to the result page
    return redirect(url_for('result'))


if __name__ == "__main__":
    app.run(debug=True)

# Using RE no NLP:wq
#changed