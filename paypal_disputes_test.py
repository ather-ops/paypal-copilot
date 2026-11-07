import json
import os
import requests
from config import PAYPAL_BASE_URL
from tools.paypal_auth import get_paypal_access_token

def fetch_disputes():
    token = get_paypal_access_token()
    url = f"{PAYPAL_BASE_URL}/v1/customer/disputes"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    print("[DISPUTES] Fetching open disputes from PayPal Sandbox...")
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch disputes ({response.status_code}): {response.text}")

    data = response.json()

    os.makedirs("docs/samples", exist_ok=True)
    with open("docs/samples/list_disputes.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print("[DISPUTES] Saved raw response to docs/samples/list_disputes.json")
    return data
if __name__ == "__main__":
    try:
        disputes = fetch_disputes()
        print(f"\nSuccess! Retrieved disputes data.")
    except Exception as e:
        print(f"\nError: {e}")
