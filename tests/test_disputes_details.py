
from tools.paypal_disputes import fetch_disputes
from tools.paypal_disputes_details import fetch_dispute_details


def test_fetch_dispute_details():
    disputes = fetch_disputes()

    assert isinstance(disputes, dict)
    assert disputes.get("items"), "No disputes available in Sandbox"

    dispute_id = disputes["items"][0]["dispute_id"]

    details = fetch_dispute_details(dispute_id)

    assert isinstance(details, dict)
    assert details.get("dispute_id") == dispute_id

    print(f"Successfully retrieved details for: {dispute_id}")
