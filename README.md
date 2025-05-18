# Plagiarism Checker 

A simple Flask-based web application to check plagiarism in uploaded text or Word documents. (with NLP) 
The app extracts sentences from the document, searches Google using SerpAPI for similar content online, and calculates similarity scores to provide a plagiarism percentage.

(This project is still in development)

---

## Features

- Upload `.txt` or `.docx` files for plagiarism analysis.
- Extracts multiple random sentences from the uploaded document.
- Searches for similar content on Google via SerpAPI.
- Calculates similarity scores using spaCy’s language model.
- Displays detailed similarity results and overall plagiarism percentage.
- User-friendly interface with status messages.

---

## How It Works

- The uploaded file is read and parsed into text.

- Sentences are tokenized and a random sample of 5 sentences is selected.

- Each sentence is searched on Google via SerpAPI to find top 3 related web pages.

- Text is fetched from those pages and compared with the sentence using spaCy’s similarity method.

- Results for each phrase with URLs and similarity percentages are shown.

- An overall plagiarism percentage is calculated based on weighted scores.

---

## Notes
- The app requires a working internet connection to query Google via SerpAPI and fetch webpage content.

- The SerpAPI free tier has limited usage; consider this when testing.

- Processing time may vary depending on file size and network speed.

- .idea/ and other IDE-specific files are ignored via .gitignore.
  
- IMP : main.py file contains the same functionalities but instead of NLP it uses regex library (less accurate). If you want to use this version instead of NLP, you'd have to make some changes else, this file can be deleted or ignored. 

---

## Folder Structure

<pre>```
  Plagiarism-Checker/
  │
  ├── templates/ # HTML templates (index.html, result.html)
  ├── static/ # (Optional) CSS, JS, images for UI styling
  ├── .gitignore # Git ignore file (.idea, pycache, etc.)
  ├── nlpmain.py # Main Flask app code
  ├── requirements.txt # Python dependencies
  ├── README.md # This file
  └── .env # Environment variables (API keys)
```</pre>

---

### Prerequisites

- Python 3.7 or newer
- pip (Python package installer)
- A free [SerpAPI](https://serpapi.com/) account and API key (for Google search)

---

### Installation

1. **Clone the repository**

     ```bash
     git clone https://github.com/LEADisDEAD/Plagiarism-Checker.git
     cd Plagiarism-Checker
     
2. **Create a virtual environment (recommended)**

    ```bash
    python -m venv .venv
    source .venv/bin/activate     # On Linux/macOS
    .venv\Scripts\activate        # On Windows PowerShell
    ```

3. **Install dependencies**

    ```bash
     pip install -r requirements.txt
    ```
    
4. **Set up environment variables**

    Create a .env file in the root directory with the following content:

    ```API_KEY=your_serpapi_key_here
    Replace your_serpapi_key_here with your actual SerpAPI key.
    ```
    
5. **Download spaCy English model**

    ```bash
    python -m spacy download en_core_web_sm
    ```    
---

## Contributing
Contributions, issues, and feature requests are welcome!
Feel free to fork the repository and submit pull requests.

---

## Author

### Prathmesh Manoj Bajpai
LinkedIn: (https://www.linkedin.com/in/prathmesh-bajpai-8429652aa/)

### Aditi Ritesh Dixit 
LinkedIn: (https://www.linkedin.com/in/aditi-dixit-895b551b5/)



