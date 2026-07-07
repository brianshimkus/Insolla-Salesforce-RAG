from dotenv import load_dotenv
import os

load_dotenv()
print("OpenAI key loaded:", bool(os.getenv("OPENAI_API_KEY")))
print("Pinecone key loaded:", bool(os.getenv("PINECONE_API_KEY")))
