import os
from dotenv import load_dotenv

# Load variables from the .env file in the root
load_dotenv()

PAYPAL_BASE_URL = os.getenv("PAYPAL_BASE_URL")
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

missing = []
if not PAYPAL_BASE_URL: missing.append("PAYPAL_BASE_URL")
if not PAYPAL_CLIENT_ID: missing.append("PAYPAL_CLIENT_ID")
if not PAYPAL_CLIENT_SECRET: missing.append("PAYPAL_CLIENT_SECRET")

if missing:
    raise ValueError(f"Missing required environment variables in .env: {', '.join(missing)}")
