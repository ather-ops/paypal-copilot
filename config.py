
import os
import streamlit as st
from dotenv import load_dotenv

# Load local .env when available
load_dotenv()

def get_setting(name, default=None):
    """Read from environment variables or Streamlit secrets."""

    value = os.getenv(name)

    if value:
        return value

    try:
        value = st.secrets.get(name, default)
        return value
    except Exception:
        return default


# PayPal configuration
PAYPAL_CLIENT_ID = get_setting("PAYPAL_CLIENT_ID")
PAYPAL_CLIENT_SECRET = get_setting("PAYPAL_CLIENT_SECRET")

PAYPAL_BASE_URL = get_setting(
    "PAYPAL_BASE_URL",
    "https://api-m.sandbox.paypal.com"
)

# Groq configuration
GROQ_API_KEY = get_setting("GROQ_API_KEY")
GROQ_MODEL = get_setting("GROQ_MODEL")

# Validate required credentials
required_settings = {
    "PAYPAL_CLIENT_ID": PAYPAL_CLIENT_ID,
    "PAYPAL_CLIENT_SECRET": PAYPAL_CLIENT_SECRET,
    "GROQ_API_KEY": GROQ_API_KEY,
    "GROQ_MODEL": GROQ_MODEL,
}

missing = [
    name
    for name, value in required_settings.items()
    if not value
]

if missing:
    raise ValueError(
        f"Missing required configuration: {', '.join(missing)}"
    )
