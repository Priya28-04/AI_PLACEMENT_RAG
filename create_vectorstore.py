import os

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

print("=" * 60)
print("🚀 AI Placement Preparation Assistant")
print("Creating FAISS Vector Database...")
print("=" * 60)

# -------------------------------------------------------
# Step 1: Load PDFs
# -------------------------------------------------------

print("\n📂 Loading PDF files...\n")

loader = DirectoryLoader(
    "data/pdfs",
    glob="*.pdf",
    loader_cls=PyPDFLoader,
    show_progress=True
)

documents = loader.load()

print(f"\n✅ Total Pages Loaded : {len(documents)}")

# -------------------------------------------------------
# Step 2: Add Metadata
# -------------------------------------------------------

print("\n📑 Adding metadata...\n")

for doc in documents:

    filename = os.path.basename(doc.metadata["source"])

    subject = filename.replace(".pdf", "").upper()

    doc.metadata["subject"] = subject

print("✅ Metadata Added")

# -------------------------------------------------------
# Step 3: Split Documents
# -------------------------------------------------------

print("\n✂ Splitting documents into chunks...\n")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = text_splitter.split_documents(documents)

print(f"✅ Total Chunks Created : {len(chunks)}")

# -------------------------------------------------------
# Step 4: Load Embedding Model
# -------------------------------------------------------

print("\n🧠 Loading HuggingFace Embedding Model...\n")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("✅ Embedding Model Loaded")

# -------------------------------------------------------
# Step 5: Create FAISS Vector Store
# -------------------------------------------------------

print("\n⚡ Creating FAISS Index...\n")

vectorstore = FAISS.from_documents(
    chunks,
    embeddings
)

# -------------------------------------------------------
# Step 6: Save Vector Store
# -------------------------------------------------------

vectorstore.save_local("faiss_index")

print("\n" + "=" * 60)
print("🎉 FAISS Vector Database Created Successfully!")
print("=" * 60)

print("\nSaved Location : ./faiss_index")

print("\nFiles Created:")

print("✔ index.faiss")
print("✔ index.pkl")

print("\nReady to Run:")
print("streamlit run app.py")