# build_vector_db.py
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

print("Starting...")

#read the logs
try:
    with open("redacted_output.txt", "r", encoding="utf-8") as file:
        sanitized_logs = file.read()
except FileNotFoundError:
    print("Redacted file do not exist")
    exit()

#chunking the logs
document_chunks = [line.strip() for line in sanitized_logs.strip().split("\n") if line.strip()]
print(f"[INFO] Processing {len(document_chunks)} log events...")

# embedding model
print("[INFO] Loading Embedding Engine (all-MiniLM-L6-v2)...")
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

#building the database
print("[INFO] Generating vectors and saving to disk...")
vector_store = Chroma.from_texts(
    texts=document_chunks,
    embedding=embedding_model,
    persist_directory="./acme_chroma_db"  # Saves the DB to this folder
)

print("[SUCCESS] Database successfully built and secured in ./acme_chroma_db")