from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOllama
from langchain.schema.output_parser import StrOutputParser

# Initialize LLM
llm = ChatOllama(model="llama3")

# Initial static context (can be your doc content)
base_context = "This context includes information about network functions and pod resources."

# Store the Q&A history
history = []

# Define a function to build full context with history
def build_context():
    chat_history = "\n".join([f"Q: {q}\nA: {a}" for q, a in history])
    return base_context + "\n\n" + chat_history

# Define prompt template with placeholders
prompt_template = ChatPromptTemplate.from_template(
    "You are an assistant. Based on context:\n{context}\nAnswer the question:\n{question}"
)

# Create chain
chain = prompt_template | llm | StrOutputParser()

# Start loop
print("Ask your questions (type 'exit' to stop):")
while True:
    question = input("Q: ")
    if question.lower() in ['exit', 'quit', 'stop']:
        break

    full_context = build_context()

    # Get answer
    answer = chain.invoke({
        "context": full_context,
        "question": question
    })

    # Show and store result
    print(f"A: {answer}\n{'-'*40}")
    history.append((question, answer))
