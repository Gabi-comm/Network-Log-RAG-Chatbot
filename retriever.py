from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# load embedded model
#we need this to convert the user's plain-text question into math
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

#connecting db on disk
#not using .from_texts() here, we are just connecting
vector_store = Chroma(
    persist_directory="./acme_chroma_db",
    embedding_function=embedding_model
)


def retrieve_corporate_context(user_question):
    "searches the existing ChromaDB for relevant log entries"
    matching_docs = vector_store.similarity_search(query=user_question, k=2)
    context_output = "\n".join([doc.page_content for doc in matching_docs])
    return context_output



if __name__ == "__main__":
    print("\n--- Testing ChromaDB Connection ---")
    test_query = "Find instances where user jdavis triggered a DLP block"
    print(f"Query: {test_query}\n")
    print(f"Result:\n{retrieve_corporate_context(test_query)}")
    print("-----------------------------------\n")