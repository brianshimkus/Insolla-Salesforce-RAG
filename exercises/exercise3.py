# exercise3.py
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

def ask(question: str, temperature: float = 0.7) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a concise assistant."},
            {"role": "user", "content": question},
        ],
        temperature=temperature,
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    with open("exercises/questions.txt") as f:
        questions = [line.strip() for line in f]

    results = []
    for question in questions:
        answer = ask(question)
        results.append({"question": question, "answer": answer})

    with open("exercises/answers.json", "w") as f:
        json.dump(results, f, indent=2)  # TODO: what's being written?