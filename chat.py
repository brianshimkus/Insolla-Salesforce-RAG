from rag import answer

print("Salesforce RAG — ask about your org (Ctrl+C to quit)")
while True:
    q = input("\nYou: ")
    print("\n" + answer(q))
