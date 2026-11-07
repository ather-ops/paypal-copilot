import time
import requests
from config import PAYPAL_BASE_URL, PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET

_token_cache = {
    "access_token": None,
    "expires_at": 0
}

def get_paypal_access_token() -> str:
    current_time = time.time()

    if _token_cache["access_token"] and current_time < (_token_cache["expires_at"] - 60):
        print("[AUTH] Using cached PayPal access token.")
        return _token_cache["access_token"]

    print("[AUTH] Requesting new PayPal access token from API...")
    url = f"{PAYPAL_BASE_URL}/v1/oauth2/token"
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en_US"
    }
    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post(url, auth = (PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET), headers=headers, data=data)

    if response.status_code != 200:
        raise Exception(f"Failed to authenticate with PayPal ({response.status_code}): {response.text}")

    token_data = response.json()
    _token_cache["access_token"] = token_data["access_token"]

    _token_cache["expires_at"] = current_time + token_data.get("expires_in", 32400)

    return _token_cache["access_token"]
