
from tools.paypal_auth import get_paypal_access_token


def test_paypal_access_token():
    token = get_paypal_access_token()

    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0
