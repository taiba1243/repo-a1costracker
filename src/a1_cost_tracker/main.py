										

from dotenv import load_dotenv
from google import genai
from groq import Groq

load_dotenv()

GEMINI_MODEL = "gemini-3.8-flash"
GROQ_MODEL =  "openai/gpt-oss-120b"

gemini_client = genai.Client()
groq_client = Groq()

prices = {
    "input": 0.10,
    "output": 0.40
}

def cost(tokens, price_per_million):
    return tokens * price_per_million / 1_000_000


gemini_resp = gemini_client.models.generate_content(
    model=GEMINI_MODEL,
    contents="Explain tokens in one sentence."
)

print("\n--- GEMINI ---")
print(gemini_resp.text)

gemini_input = gemini_resp.usage_metadata.prompt_token_count
gemini_output = gemini_resp.usage_metadata.candidates_token_count

print("Input tokens:", gemini_input)
print("Output tokens:", gemini_output)

gemini_total = (
    cost(gemini_input, prices["input"])
    + cost(gemini_output, prices["output"])
)

print(f"Gemini cost: ${gemini_total:.6f}")


groq_resp = groq_client.chat.completions.create(
    model=GROQ_MODEL,
    messages=[
        {"role": "user", "content": "Explain tokens in one sentence."}
    ]
)

print("\n--- GROQ ---")
print(groq_resp.choices[0].message.content)

groq_input = groq_resp.usage.prompt_tokens
groq_output = groq_resp.usage.completion_tokens

print("Input tokens:", groq_input)
print("Output tokens:", groq_output)

groq_total = (
    cost(groq_input, prices["input"])
    + cost(groq_output, prices["output"])
)

print(f"Groq cost: ${groq_total:.6f}")