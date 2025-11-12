from google import genai
from google.genai import types
from dotenv import load_dotenv
#from KB.dbService import create_connection
from KB.dbService import create_connection
import os
import psycopg2
from sentence_transformers import SentenceTransformer  # fallback

load_dotenv()


def generate_embeddings(user_prompt):
    """
    Try to generate embeddings using Google Gemini API.
    If quota is exceeded, fallback to a local embedding model.
    """
    try:
        client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))
        model = os.getenv('EMBEDDINGS_MODEL')  # e.g., "models/text-embedding-004"

        response = client.models.embed_content(
            model=model,
            contents=user_prompt
        )

        return response.embeddings[0].values

    except Exception as e:
        print(f"⚠️ Google API failed: {e}")
        print("⚙️ Falling back to local SentenceTransformer embeddings...")
        # Fallback to local model (no API needed)
        local_model = SentenceTransformer('all-MiniLM-L6-v2')
        return local_model.encode(user_prompt).tolist()



def chunk_text(text, max_length=2000, overlap=400):
    chunks = []
    start =0
    while start < len(text):
        end = min(start + max_length, len(text))
        chunks.append(text[start:end])
        start += max_length - overlap

    return chunks

if __name__ =="__main__":
    with open(r"C:\Users\nates\OneDrive\Desktop\gen ai\GenAI\KB\asset\27-10-2025-ET.txt","r",encoding="utf-8") as f:
        data = f.read()

    chunks = chunk_text(data)
    conn = create_connection()
    cursor = conn.cursor()
    '''DROP TABLE IF EXISTS embeddings_store;

CREATE TABLE embeddings_store (
    id SERIAL PRIMARY KEY,
    chunk TEXT,
    embedding vector(768)  -- ✅ changed from 384 to 768
);'''
    
    ''' cursor.execute(
    "CREATE EXTENSION IF NOT EXISTS vector;")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS embeddings_store (
        id SERIAL PRIMARY KEY,
        chunk TEXT,
        embedding vector(768)
    );
    """)
    conn.commit()'''

    for chunk in chunks:
        emb = generate_embeddings(chunk)
        
        cursor.execute(
            "INSERT INTO embeddings_store (chunk,embedding) VALUES (%s, %s::vector)",
            (chunk, emb)
        )

    conn.commit()
    cursor.close()
    conn.close()
    print(len(chunk))