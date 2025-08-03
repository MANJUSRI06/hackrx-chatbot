from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

def create_vector_store(chunks):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = FAISS.from_documents(chunks, embeddings)
    retriever = vectordb.as_retriever(search_type="similarity", k=5)
    return vectordb, retriever

def retrieve_relevant_chunks(question, retriever):
    return retriever.get_relevant_documents(question)
