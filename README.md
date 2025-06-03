# 📧 Cold Email Generator

A Generative AI-powered web app that creates personalized cold emails for job applications based on job descriptions, personal bio, projects, and portfolio links.

🔗 **Live Demo:** [coldmail-generator.streamlit.app](https://coldmail-generator.streamlit.app/)  
📂 **GitHub Repo:** [github.com/itz-Pratham/Cold_Email_Generator](https://github.com/itz-Pratham/Cold_Email_Generator)

---

## 🔍 Features

- **Job Parsing from URL:** Extracts job descriptions from company career pages using `LangChain`'s web loader.
- **Context-Aware Email Writing:** Uses an LLM to generate personalized cold emails based on user bio, project experience, and job requirements.
- **Portfolio Matching with Vector Search:** Retrieves relevant project links by matching job-required skills with a user-uploaded portfolio using ChromaDB.
- **Streamlit UI:** Clean interface with toggleable defaults, file uploads, dynamic Markdown output, and downloadable templates.

---

## 🧠 Tech Stack

- **Frontend/UI:** Streamlit
- **Backend/Logic:** Python, LangChain
- **Vector Store:** ChromaDB
- **LLM Integration:** OpenAI-compatible interface
- **Data Handling:** Pandas, custom CSV parser
- **Deployment:** Streamlit Cloud

---

## 🚀 Getting Started

```bash
pip install -r requirements.txt
streamlit run app/main.py
```

Make sure you have your OpenAI API key set in the environment for LLM calls.
