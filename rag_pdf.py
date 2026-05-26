import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from dotenv import load_dotenv

pdf_path = "newresume.pdf"
print("Looking for:", os.path.abspath(pdf_path))
print("Exists?", os.path.exists(pdf_path))

if not os.path.exists(pdf_path):
    print("Not found — check the path above")
    exit()

loader = PyPDFLoader(pdf_path)


load_dotenv()

# --- SETUP: load and process the PDF ---
print("Loading PDF...")
loader = PyPDFLoader("newresume.pdf")   # ← change to your PDF filename
pages = loader.load()
print(f"Loaded {len(pages)} pages")

# Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(pages)
print(f"Split into {len(chunks)} chunks")

# Embed and store
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings)
print("Embedded and stored!\n")

llm = ChatGroq(model="openai/gpt-oss-20b", api_key=os.getenv("GROQ_API_KEY"))


# --- QUERY ---
def answer_question(question):
    relevant = vectorstore.similarity_search(question, k=5)
    context = "\n\n".join(chunk.page_content for chunk in relevant)
    prompt = f"""Answer using ONLY the context below. If not in context, say "I don't have that information."

Context:
{context}

Question: {question}

Answer:"""
    return llm.invoke(prompt).content


# Ask questions about YOUR pdf
while True:
    q = input("\nAsk about the document (or 'quit'): ")
    if q == "quit":
        break
    print(f"\n{answer_question(q)}")


