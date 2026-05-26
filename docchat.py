import os
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import tempfile

load_dotenv()

st.title("📄 DocChat")
st.write("Upload a PDF and chat with it using AI")

# --- File uploader ---
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    # Save uploaded file to a temp location (PyPDFLoader needs a file path)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    # Process the PDF (only once — store in session_state)
    if "vectorstore" not in st.session_state:
        with st.spinner("Processing document..."):
            loader = PyPDFLoader(tmp_path)
            pages = loader.load()

            splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            chunks = splitter.split_documents(pages)

            embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            st.session_state.vectorstore = Chroma.from_documents(chunks, embeddings)

        st.success(f"Document processed! Split into {len(chunks)} chunks. Ask me anything.")
    
# --- Initialize chat history and LLM ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "llm" not in st.session_state:
    st.session_state.llm = ChatGroq(
        model="openai/gpt-oss-20b",
        api_key=os.getenv("GROQ_API_KEY")
    )

# --- Display existing chat history ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- Chat input ---
user_question = st.chat_input("Ask about your document...")

if user_question:
    # Show user message
    with st.chat_message("user"):
        st.write(user_question)
    st.session_state.messages.append({"role": "user", "content": user_question})

    # Generate answer with RAG
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # 1. Retrieve relevant chunks
            relevant = st.session_state.vectorstore.similarity_search(user_question, k=5)
            context = "\n\n".join(chunk.page_content for chunk in relevant)

            # 2. Build prompt
            prompt = f"""Answer using ONLY the context below. If the answer isn't in the context, say "I don't have that information in the document."

Context:
{context}

Question: {user_question}

Answer:"""

            # 3. Get answer
            answer = st.session_state.llm.invoke(prompt).content
            st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})