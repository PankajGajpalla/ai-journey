from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

documents = [
    "Our company offers a 30-day money-back guarantee on all products. Refunds are processed within 5 business days.",
    "Shipping is free for orders over $50. Standard delivery takes 3-5 business days. Express shipping is available for $15.",
    "Our customer support team is available Monday to Friday, 9 AM to 6 PM. You can reach us via email or live chat.",
    "We offer a premium membership for $99 per year, which includes free express shipping and exclusive discounts.",
    "All electronic products come with a 2-year warranty. Damaged items can be exchanged within 14 days of delivery."
]

# Free local embedding model
print("Loading embedding model (first run downloads ~90MB)...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Embed and store documents
print("Embedding documents...")
vectorstore = Chroma.from_texts(texts=documents, embedding=embeddings)
print("Done!\n")

# Search by meaning
queries = [
    "How long do I have to return something?",
    "When can I talk to a human?",
    "What does the paid plan include?"
]

for query in queries:
    print(f"Query: {query}")
    results = vectorstore.similarity_search(query, k=2)
    for i, doc in enumerate(results, 1):
        print(f"  {i}. {doc.page_content}")
    print()