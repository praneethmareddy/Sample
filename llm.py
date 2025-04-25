from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOllama
from langchain.schema.output_parser import StrOutputParser

# --- Initialize LLM and Prompt ---
llm = ChatOllama(model="llama3")
prompt_template = ChatPromptTemplate.from_template(
    "You are an assistant. Based on the following context:\n{retrieved_context}\n\nChat History:\n{chat_history}\n\nAnswer this:\n{question}"
)
chain = prompt_template | llm | StrOutputParser()

# --- In-memory storage for Q&A ---
qa_history = []  # stores (q, a)

# --- Chat loop ---
print("Ask your questions (type 'exit' to stop):")
while True:
    question = input("Q: ")
    if question.lower() in ['exit', 'quit', 'stop']:
        break

    # Step 1: Retrieve the most similar context using FAISS (assuming db_index is set up)
    context = db_index.similarity_search(question, k=1)

    # Step 2: Get the page content of the most similar document
    retrieved_context = context[0].page_content if context else ""

    # Step 3: Build the chat history (all Q&A pairs so far)
    chat_history = "\n".join([f"Q: {q}\nA: {a}" for q, a in qa_history])

    # Step 4: Get the answer from the LLM using the current question, retrieved context, and chat history
    response = chain.invoke({
        "retrieved_context": retrieved_context,
        "chat_history": chat_history,
        "question": question
    })

    # Step 5: Store the current Q&A pair in history
    qa_history.append((question, response))

    # Step 6: Display the answer
    print(f"A: {response}\n{'-'*50}")
