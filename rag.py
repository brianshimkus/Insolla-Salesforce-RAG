import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

store = PineconeVectorStore(
    index_name="insolla-salesforce-rag",
    embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
)
retriever = store.as_retriever(search_kwargs={"k": 4})
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = ChatPromptTemplate.from_template(
    """Answer the question using ONLY the context below from our Salesforce org.
If the context doesn't contain the answer, say so — do not guess.

Context:
{context}

Question: {question}

Answer:"""
)


def answer_with_sources(question: str):
    docs = retriever.invoke(question)
    context = "\n\n".join(d.page_content for d in docs)
    chain = prompt | llm
    result = chain.invoke({"context": context, "question": question}).content
    return result, docs


def answer(question: str) -> str:
    return answer_with_sources(question)[0]


if __name__ == "__main__":
    print(answer("Which accounts have open high-priority cases?"))
