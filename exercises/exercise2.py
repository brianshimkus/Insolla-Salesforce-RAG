# exercise2.py
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
    print(ask("Write a one-sentence tagline for a coffee shop.", temperature=0.0))
    print(ask("Write a one-sentence tagline for a coffee shop.", temperature=1.5))