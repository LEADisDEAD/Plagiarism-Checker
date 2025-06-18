# Plagiarism Checker 🔍

A full-stack web application (Flask + React) to check plagiarism in uploaded text or Word documents using Natural Language Processing (NLP).  
It uses **SerpAPI** to search the web and **spaCy** to calculate content similarity.

🚧 _This project is still in development._

---

## 🔧 Features

- Upload `.txt` or `.docx` files for plagiarism analysis.
- Extracts random sentences from the document.
- Google search integration via SerpAPI to find similar content.
- NLP-powered similarity score calculation using **spaCy**.
- Displays individual sentence matches with links and scores.
- Overall plagiarism percentage.
- **Frontend built with React** for a modern UI.

---

## 🧠 How It Works

1. The file is uploaded through the React interface.
2. The Flask backend reads and parses the document.
3. Five random sentences are selected.
4. Each sentence is searched on Google using SerpAPI (top 3 results).
5. Content from those pages is fetched and compared using `spaCy`'s similarity method.
6. Results are displayed in the frontend with links and match scores.
7. Final plagiarism percentage is calculated from all matches.

---

## 🗂 Folder Structure

```
Plagiarism-Checker/
│
├── frontend/             # React frontend
│   ├── public/
│   ├── src/
│   └── ...
│
├── templates/            # Flask HTML templates (for legacy UI)
├── static/               # Static files (CSS, JS, images)
├── nlpmain.py            # Flask backend using NLP
├── main.py               # Alternate version (regex-based)
├── requirements.txt      # Python dependencies
├── .gitignore
├── .env                  # API key (not committed)
└── README.md
```

---

## 🚀 Getting Started

### 📦 Prerequisites

- Python 3.7+
- Node.js + npm (for React frontend)
- pip (Python package manager)
- [SerpAPI](https://serpapi.com/) API key

---

### ⚙️ Backend Setup (Flask)

1. **Clone the repository**

```bash
git clone https://github.com/LEADisDEAD/Plagiarism-Checker.git
cd Plagiarism-Checker
```

2. **Create virtual environment**

```bash
python -m venv .venv
.venv\Scripts\activate       # Windows
# OR
source .venv/bin/activate   # macOS/Linux
```

3. **Install Python dependencies**

```bash
pip install -r requirements.txt
```

4. **Add your SerpAPI key**

Create a `.env` file in the root folder:

```env
API_KEY=your_serpapi_key_here
```

_(Do not share this key publicly or push it to GitHub.)_

5. **Download spaCy model**

```bash
python -m spacy download en_core_web_md
```

---

### 🎨 Frontend Setup (React)

1. **Navigate to frontend folder**

```bash
cd frontend
```

2. **Install dependencies**

```bash
npm install
```

3. **Start the React app**

```bash
npm start
```

4. **Frontend will run at** `http://localhost:3000` and connect to the Flask backend.

---

## 📝 Notes

- Make sure the Flask server is running on port 5000 and CORS is enabled.
- You may need to adjust the proxy in `frontend/package.json` to match your Flask backend:
```json
"proxy": "http://localhost:5000"
```

- `.env` file is required both locally and in deployment (on platforms like Render or Vercel).
- Do **not commit your `.env` file** — it's already ignored via `.gitignore`.

---

## ⚠️ Alternate Backend Option

The `main.py` file has the same core logic but uses basic regex matching instead of NLP (spaCy).  
If you want a lighter and faster version with less accuracy, use this.

---

## 🤝 Contributing

Pull requests, issues, and feature suggestions are welcome!  
Feel free to fork the repo and contribute.

---

## 👩‍💻 Authors

**Prathmesh Manoj Bajpai**  
[LinkedIn](https://www.linkedin.com/in/prathmesh-bajpai-8429652aa/)

**Aditi Ritesh Dixit**  
[LinkedIn](https://www.linkedin.com/in/aditi-dixit-895b551b5/)
