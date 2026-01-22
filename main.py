import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from rag import build_vector_db

# Load API key
load_dotenv()

# Create AI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create FastAPI app
app = FastAPI()

# Load or build vector database
if not os.path.exists("vector_db"):
    print("Building vector database from knowledge folder...")
    db = build_vector_db()
else:
    print("Loading existing vector database...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.load_local("vector_db", embeddings)

# Request schema
class ChatRequest(BaseModel):
    message: str

# Chat endpoint
@app.post("/chat")
def chat_with_ai(request: ChatRequest):
    # Search knowledge base
    docs = db.similarity_search(request.message, k=3)
    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are an intelligent assistant. Use the context below to answer the question.

Context:
{context}

Question:
{request.message}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=400
    )

    return {
        "reply": response.choices[0].message.content
    }
