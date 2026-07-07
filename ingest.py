import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from documents import load_documents

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = "insolla-salesforce-rag"

if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=1536,  # matches text-embedding-3-small
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
store = PineconeVectorStore(index_name=index_name, embedding=embeddings)

docs = load_documents()
store.add_texts(docs)
print(f"Embedded and stored {len(docs)} documents.")
