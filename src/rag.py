import os
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

def get_chroma_vectorstore(persist_directory="chroma_db_v2", policies_dir="data/policies"):
    embeddings = OpenAIEmbeddings()
    
    if os.path.exists(persist_directory) and os.listdir(persist_directory):
        print("Loading existing Chroma vectorstore.")
        return Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    
    print("Ingesting policy documents into Chroma...")
    loader = DirectoryLoader(policies_dir, glob="*.md", loader_cls=TextLoader)
    documents = loader.load()
    
    # We use size=1000 and overlap=200. Policies are not extremely long, but this ensures rules and their immediate caveats stay together.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200,
        separators=["\n# ", "\n## ", "\n- ", "\n", " ", ""]
    )
    
    split_docs = text_splitter.split_documents(documents)
    
    # Inject chunk ID into metadata for strict citation tracking
    for i, doc in enumerate(split_docs):
        doc.metadata["chunk_id"] = f"chunk_{i}"
        doc.metadata["doc_title"] = os.path.basename(doc.metadata.get("source", "Unknown"))
        
    vectorstore = Chroma.from_documents(
        documents=split_docs, 
        embedding=embeddings, 
        persist_directory=persist_directory
    )
    
    return vectorstore

def format_citations(docs):
    formatted = []
    citations_metadata = []
    for doc in docs:
        doc_title = doc.metadata.get("doc_title", "Unknown")
        chunk_id = doc.metadata.get("chunk_id", "Unknown")
        snippet = f"--- SOURCE: {doc_title} (ID: {chunk_id}) ---\n{doc.page_content}\n"
        formatted.append(snippet)
        citations_metadata.append({"doc": doc_title, "chunk_id": chunk_id, "content": doc.page_content})
    return "\n".join(formatted), citations_metadata

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    vectorstore = get_chroma_vectorstore()
    print(f"Vectorstore ready. Collection count: {vectorstore._collection.count()}")
