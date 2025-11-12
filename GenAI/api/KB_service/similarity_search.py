from KB_service.embedding import generate_embeddings
from KB_service.dbService import create_connection


def similarity_search(user_prompt, top_k=3):
    embedding_obj = generate_embeddings(user_prompt)
    user_prompt_embeded = embedding_obj
    conn = create_connection()
    cursor = conn.cursor()
    query = f"SELECT chunk from embeddings_store order by embedding <=> %s::vector limit {top_k}"
    cursor.execute(query, (user_prompt_embeded,))
    data = cursor.fetchall()
    return data

if __name__ == "__main__":
    user_prompt = "what is happen in the nfity bank today?"
    
    print(similarity_search(user_prompt))