from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOllama
from langchain.schema.output_parser import StrOutputParser
import faiss
import numpy as np

# --- Initialize LLM and Prompt ---
llm = ChatOllama(model="llama3")
prompt_template = ChatPromptTemplate.from_template(
    "You are an assistant. Based on similar questions and context:\n\n{retrieved_context}\n\nChat History:\n{chat_history}\n\nAnswer this:\n{question}"
)
chain = prompt_template | llm | StrOutputParser()

# --- FAISS setup for context retrieval ---
# Assuming you've already created an index
# db_index: FAISS index object for your stored embeddings
# You can use a pre-built FAISS index or create one from your document embeddings

# --- In-memory storage for Q&A ---
qa_history = []          # stores (q, a)

# --- Chat loop ---
print("Ask your questions (type 'exit' to stop):")
while True:
    question = input("Q: ")
    if question.lower() in ['exit', 'quit', 'stop']:
        break

    # Step 1: Embed current question using your embedding model (e.g., sentence-transformers)
    q_embed = embed_model.encode(question, convert_to_tensor=False)
    q_embed = np.array(q_embed).astype("float32")  # Convert to numpy for FAISS

    # Step 2: Retrieve the most similar context using FAISS
    k = 1  # Retrieve top 1 similar context
    _, indices = db_index.search(q_embed.reshape(1, -1), k)  # FAISS search for similarity
    
    # Step 3: Get the most similar Q&A pairs from the index (retrieved context)
    retrieved_context = ""
    for idx in indices[0]:
        if idx != -1:  # If there's a valid index
            retrieved_context += f"Q: {qa_history[idx][0]}\nA: {qa_history[idx][1]}\n"

    # Step 4: Build chat history
    chat_history = "\n".join([f"Q: {q}\nA: {a}" for q, a in qa_history])

    # Step 5: Get the answer from the LLM using the current question, retrieved context, and chat history
    response = chain.invoke({
        "retrieved_context": retrieved_context,
        "chat_history": chat_history,
        "question": question
    })

    # Step 6: Store the current Q&A pair and its embedding in history
    qa_history.append((question, response))

    # Step 7: Display the answer
    print(f"A: {response}\n{'-'*50}")
