# therapist_ai.py

from mistralai import Mistral
import requests
import numpy as np
import faiss
import os
from sentence_transformers import SentenceTransformer
from getpass import getpass
import fitz
import uuid
from crisis import contains_crisis_keywords, SAFETY_MESSAGE
from logger import log_chat
from transformers import AutoTokenizer

from dotenv import load_dotenv
load_dotenv()



# 1. Therapist prefix
THERAPIST_PREFIX = "You are a compassionate therapist who speaks in a calm and understanding tone."

# 2. Mistral LLM API key
api_key = os.getenv("MISTRAL_API_KEY")
client = Mistral(api_key=api_key)

# 3. Tokenizer 
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")  

# 4. Extract text from 'books' folder
def extract_text_from_folder(folder_path):
    all_text = ""
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            try:
                doc = fitz.open(pdf_path)
                for page in doc:
                    all_text += page.get_text()
            except Exception as e:
                print(f"Error reading {pdf_path}: {e}")
    return all_text

text = extract_text_from_folder("books")
print(text[:500])

# 5. Split into chunks
chunk_size = 2048
chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
print(f"Total chunks: {len(chunks)}")

# 6. Generate sentence-transformer embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')
text_embeddings = model.encode(chunks, show_progress_bar=True, convert_to_numpy=True).astype('float32')

# 7. Load into FAISS vector DB
d = text_embeddings.shape[1]
index = faiss.IndexFlatL2(d)
index.add(text_embeddings)

# 8. Run Mistral for final answer
def run_mistral(user_message, model="mistral-large-latest"):
    messages = [{"role": "user", "content": user_message}]
    chat_response = client.chat.complete(
        model=model,
        messages=messages
    )
    return chat_response.choices[0].message.content

# 9. Main chat runner
def run_chat(question: str) -> str:
    question_embeddings = model.encode([question]).astype('float32')
    D, I = index.search(question_embeddings, k=2)
    retrieved_chunk = [chunks[i] for i in I[0]]

    context = "\n".join(retrieved_chunk)
    prompt = f"""
{THERAPIST_PREFIX}
Context information is below.
---------------------
{context}
---------------------
Given the context information and not prior knowledge, answer the query.
Query: {question}
Answer:
"""

    answer = run_mistral(prompt)
    is_crisis = contains_crisis_keywords(question)

    if is_crisis:
        answer = SAFETY_MESSAGE + "\n" + answer

    session_id = str(uuid.uuid4())
    log_chat(session_id=session_id, query=question, response=answer, is_crisis=is_crisis)

    return answer

# 10.Interactive call
if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = run_chat(user_input)
        print("Therapist:", response)
