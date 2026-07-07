import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()

store = PineconeVectorStore(
    index_name="insolla-salesforce-rag",
    embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
)

results = store.similarity_search("high priority cases about billing", k=3)
for r in results:
    print("—", r.page_content[:120])
