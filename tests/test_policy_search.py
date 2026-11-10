
from tools.policy_search import search_paypal_policy


def test_paypal_policy_search():
    result = search_paypal_policy(
        query="What evidence is required for an Item Not Received dispute?"
    )

    assert isinstance(result, str)
    assert len(result.strip()) > 0
    assert "No relevant policy information was found" not in result

    print("\nRetrieved PayPal Policy:\n")
    print(result)
