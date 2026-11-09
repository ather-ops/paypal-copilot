
import os

from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing from .env")

if not GROQ_MODEL:
    raise ValueError("GROQ_MODEL is missing from .env")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)


def generate_response(messages, temperature=0.2, max_tokens=1024):
    """
    Generate a response using the Groq chat completion API.

    Args:
        messages: List of system, user, and assistant messages.
        temperature: Controls response randomness.
        max_tokens: Maximum response length.

    Returns:
        Generated text response.
    """

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return response.choices[0].message.content
