from tools.paypal_auth import get_paypal_access_token

# Testing
print(" First call network")
token1 = get_paypal_access_token()
print(f"Token acquired: {token1[:15]}...")

print("\n Test 2: Second call cache")
token2 = get_paypal_access_token()
assert token1 == token2, "Tokens do not match!"
print("Success! Second call used the cache seamlessly.")
