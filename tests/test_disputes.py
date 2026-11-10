
from tools.paypal_disputes import fetch_disputes


def test_fetch_paypal_disputes():
    result = fetch_disputes()

    assert isinstance(result, dict)
    assert "items" in result

    print(f"Retrieved {len(result['items'])} disputes")
