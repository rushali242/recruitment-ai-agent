# Recruitment AI Agent

## 1. Project Overview
Recruitment AI Agent is a web application that automates the process of analyzing resumes against job descriptions (JD) and generating professional emails. It helps recruiters quickly shortlist candidates, identify missing skills, and send interview or rejection emails.

---

## 2. Features

- **Generate Job Description (JD):** Create a concise job description based on input details like title, skills, experience, company, industry, employment type, and location.
- **Resume Scoring & Ranking:** Compare uploaded resumes against the JD and calculate a match score using TFIDF and cosine similarity.
- **Missing Skills Detection:** Identify missing skills from the candidate's resume.
- **Email Generation:** Automatically generate shortlisting or rejection emails using a text-to-text AI model.
- **Best Match Identification:** Highlight the candidate with the highest matching score as the Best Match.

---

## 3. AI & ML Logic

### Resume Scoring
- Uses **TFIDF Vectorization** + **Cosine Similarity** to compute how closely a resume matches a JD.
- Scores are interpreted as:
  - **>75:** Strong match  
  - **50–75:** Average match  
  - **<50:** Weak match

### Email & JD Generation
- Uses **Google FLAN-T5-large** (`text2text-generation` pipeline) to generate:
  - Short job descriptions from input fields.
  - Polite interview invitation emails.
  - Concise rejection emails.

### Text Preprocessing
- Lowercasing
- Removing special characters
- Lemmatization
- Filtering out short words (<3 characters)

> ⚠️ **Note**: Accuracy is limited as only free/open-source models were used. Paid models like `gpt-3.5-turbo`, `gpt-4`, `Claude`, or Google `Bard API` could significantly improve output quality.

---

## 4. Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/your-username/repo-name.git
cd repo-name
```
2. Create and activate a virtual environment, then install dependencies:
```bash
# Create virtual environment
python -m venv myenv
```
3. Activate the environment:
```bash
# Activate (Windows)
myenv\Scripts\activate

# Activate (Mac/Linux)
source myenv/bin/activate
```
4. Install dependencies:
```bash
# Install all required libraries
pip install -r requirements.txt
```

## 5. Running Locally

1. Start the FastAPI server with:
```bash
uvicorn main:app --reload
```
2. Open a browser and visit : http://127.0.0.1:8000

3. Use the inteface to:
    - Generate a job description
    - Upload JD and resume files
    - View candidate ranking and generated emails


## 6. Example Files

To test the project, include the following sample files in the `testing_files` folder in the repository:

- **Job Description:** `testing_files/JD_DataAnalyst.docx`  
- **Resumes:** `testing_files/David.docx`, `testing_files/James.docx`


## 7. Future Improvements

- **Use advanced AI models:** Leverage paid or more powerful AI models for better text generation accuracy.  
- **Improve resume ranking:** Use semantic embeddings or transformer-based embeddings instead of just TFIDF for more accurate matching.  
- **Add email sending integration:** Automatically send shortlisting or rejection emails to candidates.  
- **Enhance UI/UX:** Improve the user interface and experience for easier candidate evaluation and interaction.