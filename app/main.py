from fastapi import FastAPI, Request, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.modules.logic import calculate_score, get_missing_skills, generate_jd, generate_email
import os
import tempfile
import shutil
import fitz
import docx

app = FastAPI(title="Recruitment AI Agent")
templates = Jinja2Templates(directory="app/templates")


def save_temp(upload: UploadFile):
    upload.file.seek(0)  # reset file pointer to start
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(upload.filename)[1]) as tmp:
        shutil.copyfileobj(upload.file, tmp)
        return tmp.name

#Extract text from DOCX
def extract_docx_safe(path: str):
    try:
        doc = docx.Document(path)
        text = "\n".join([p.text for p in doc.paragraphs])
        return text
    except Exception as e:
        return f"[Error reading DOCX: {e}]"

#Extract text from PDF
def extract_pdf_safe(path: str):
    try:
        text = ""
        with fitz.open(path) as pdf:
            for page in pdf:
                text += page.get_text()
        return text      
    except Exception as e:
        return f"[Error reading PDF: {e}]"


# Convert file name to readable candidate name
def clean_name(filename: str):
    base = os.path.splitext(filename)[0]  # remove extension
    return base.replace("_", " ").title()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate-jd", response_class=HTMLResponse)
def gen_jd(request: Request,
           title: str = Form(...),
           years: str = Form(""),
           skills: str = Form(""),
           company: str = Form(""),
           employment: str = Form(""),
           industry: str = Form(""),
           location: str = Form("")):
    data = {"title": title, "years": years, "skills": skills,
            "company": company, "employment": employment,
            "industry": industry, "location": location}
    jd_text = generate_jd(data)
    return templates.TemplateResponse("index.html", {"request": request, "generated_jd": jd_text})


@app.post("/process", response_class=HTMLResponse)
async def process(request: Request,
                  jd_file: UploadFile = None,
                  jd_manual: str = Form(""),
                  skills: str = Form(""),
                  resumes: list[UploadFile] = []):

    # Extract JD text
    jd_text = ""
    if jd_file:
        path = save_temp(jd_file)
        jd_text = extract_pdf_safe(path) if path.endswith(".pdf") else extract_docx_safe(path)
        os.remove(path)
    elif jd_manual:
        jd_text = jd_manual

    skills_list = [s.strip() for s in skills.split(",") if s.strip()]
    results = []

    # Process each resume
    for r in resumes:
        path = save_temp(r)
        res_text = extract_pdf_safe(path) if path.endswith(".pdf") else extract_docx_safe(path)
        os.remove(path)

        score = calculate_score(jd_text, res_text)
        missing = get_missing_skills(jd_text, res_text, skills_list)
        remark = "Strong" if score > 75 else "Average" if score > 50 else "Weak"

        candidate_name = clean_name(r.filename)
        status = "selected" if score == max([score, 0]) else "rejected"

        # Generate professional email
        email = generate_email(
            candidate_name,
            status,
            missing
        )

        results.append({
            "name": candidate_name,
            "score": score,
            "missing": missing,
            "remark": remark,
            "email": email
        })

    # Mark best match
    if results:
        best = max(results, key=lambda x: x["score"])
        for r in results:
            if r["name"] == best["name"]:
                r["remark"] = "Best match ✅"

    return templates.TemplateResponse("results.html", {"request": request, "results": results, "jd": jd_text})

