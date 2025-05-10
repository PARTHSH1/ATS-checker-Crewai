# ATS-Checker (Powered by CrewAI + GROQ)

📄🔍 **ATS-Checker** is an intelligent resume analyzer that checks your resume against any job description URL and scores how well your resume aligns with it using keyword extraction, similarity scoring, and multidimensional analysis.

---

## 🚀 Features

- Accepts resumes in **PDF**, **HTML**, and **DOCX** formats  
- Analyzes job descriptions from any **job URL**
- Uses **GROQ LLM** for advanced NLP and CrewAI agents for automation
- Performs:
  - Keyword extraction
  - Similarity scoring
  - Multidimensional alignment analysis
- Outputs a **match report** with actionable suggestions

---

## 🛠️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ATS-checker-crewai.git
   cd ATS-checker-crewai
2. **Install the dependencies**
   ```bash
   pip install -r requirements.txt
3. **Set your GROQ API key**
   ```bash
   Create a .env file in the root directory with the following:
4. **Run the program**
   ```bash
    python main.py
🧠 How It Works
Parses and preprocesses the uploaded resume and job description.
Extracts relevant keywords using the GROQ LLM.
Compares the documents using:
✅ Cosine similarity
✅ Semantic similarity
✅ Domain-specific keyword overlap
Generates a comprehensive match score with detailed feedback and improvement tips.
