from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline
import re


def preprocess_text(text):
    # Lowercase text
    text = text.lower()
    # Keep alphabets, digits, and spaces (remove everything else)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    # keep words > 3 chars
    text = " ".join([word for word in text.split() if len(word) > 3])
    return text

def calculate_score(jd_text,resume_text):
    jd_text = preprocess_text(jd_text)
    resume_text = preprocess_text(resume_text)

    # TFIDF for word count and weight
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf = vectorizer.fit_transform([jd_text, resume_text])

    # Cosine similarity compares the text and give back the similarity score
    score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]

    return round(score * 100, 2)

def get_missing_skills(jd_text, resume_text, skills):
    return [s for s in skills if s.lower() not in resume_text.lower()]

def generate_jd(data):
    generator = pipeline("text2text-generation", model="google/flan-t5-small")
    prompt = (
        f"Write a short job description for a {data['title']} role "
        f"requiring {data['years']} years of experience in {data['skills']}. "
        f"Company: {data['company']}, Industry: {data['industry']}, "
        f"Employment type: {data['employment']}, Location: {data['location']}."
    )
    output = generator(
        prompt,
        max_length=300,
        min_length=85,
        do_sample=True,
        top_p=0.9,
        temperature=0.8,
        repetition_penalty=3.0,
        num_return_sequences=1
        )
    return output[0]["generated_text"]

def generate_email(name, status, missing_skills=None):
    generator = pipeline("text2text-generation", model="google/flan-t5-small")
    if status == "selected":
        prompt = (
        f"Write a short, professional interview invitation email for the candidate {name}. "
        f"Keep it polite and concise, mentioning the role and asking to confirm availability."
    )
    else:
        prompt = (
            f"Write a rejection email for the candidate {name}. That they are NOT SELECTED."
            f"Explain that they were not selected after careful consideration because they lack some of the key skills."
            f"Encourage them to apply for future opportunities that may better match their profile. "
            f"Limit the response to 3–5 concise sentences, avoiding repetition or placeholders."
        )

    output = generator(
        prompt,
        max_length=120,           # allow longer, complete outputs
        min_length=40,            # ensures some detail
        do_sample=True,           # enables random sampling
        top_p=0.9,                # nucleus sampling for natural diversity
        temperature=0.8,          # controls creativity
        repetition_penalty=3.0,   # discourages repeating phrases
        num_return_sequences=1    # just one clean output
        )

    return output[0]["generated_text"]