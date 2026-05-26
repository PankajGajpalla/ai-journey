import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

# --- SETUP PHASE (once) ---
documents = [
    "Our company offers a 30-day money-back guarantee on all products. Refunds are processed within 5 business days.",
    "Shipping is free for orders over $50. Standard delivery takes 3-5 business days. Express shipping is available for $15.",
    "Our customer support team is available Monday to Friday, 9 AM to 6 PM. You can reach us via email or live chat.",
    "We offer a premium membership for $99 per year, which includes free express shipping and exclusive discounts.",
    "All electronic products come with a 2-year warranty. Damaged items can be exchanged within 14 days of delivery."
]

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_texts(texts=documents, embedding=embeddings)
llm = ChatGroq(model="openai/gpt-oss-20b", api_key=os.getenv("GROQ_API_KEY"))


# --- QUERY PHASE (every question) ---
def answer_question(question):
    # 1. Retrieve relevant chunks
    relevant_chunks = vectorstore.similarity_search(question, k=2)

    # 2. Combine chunks into context text
    context = "\n".join(chunk.page_content for chunk in relevant_chunks)

    # 3. Build a prompt with context + question
    prompt = f"""Answer the question using ONLY the context below.
If the answer isn't in the context, say "I don't have that information."

Context:
{context}

Question: {question}

Answer:"""

    # 4. Ask the LLM
    response = llm.invoke(prompt)
    return response.content


# Test it
questions = [
    "How long do I have to return something?",
    "Do you ship internationally?",
    "What's included in the premium plan?",
    "When is support available?"
]

for q in questions:
    print(f"Q: {q}")
    print(f"A: {answer_question(q)}\n")