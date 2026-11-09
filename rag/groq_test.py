
from tools.groq_client import generate_response

messages = [
    {
        "role": "system",
        "content": "You are PayPal Copilot, an assistant that helps merchants understand payment disputes."
    },
    {
        "role": "user",
        "content": "What is an Item Not Received dispute?"
    }
]

response = generate_response(messages)

print(response)
print("Done all works perfectly👍")
