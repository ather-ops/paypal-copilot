import json
import os
import requests
from config import PAYPAL_BASE_URL
from tools.paypal_auth import get_paypal_access_token

def fetch_dispute_details(dispute_id: str):
    token = get_paypal_access_token()
    url = f"{PAYPAL_BASE_URL}/v1/customer/disputes/{dispute_id}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    print(f"[DISPUTE DETAILS] Fetching details for dispute ID: {dispute_id}...")
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch dispute details ({response.status_code}): {response.text}")

    data = response.json()

    os.makedirs("docs/samples", exist_ok=True)
    filename = f"docs/samples/dispute_details_{dispute_id}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"[DISPUTE DETAILS] Saved details to {filename}")
    return data

