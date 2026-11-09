from tools.paypal_disputes_details import fetch_dispute_details

test_id = "PP-R-PRQ-10196889"
try:
    disputes = fetch_dispute_details(test_id)
    print("Ready to fetch disputes deatils")
except Exception as e:
    print(f"Error {e}")
