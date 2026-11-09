from tools.paypal_tools import (
    get_paypal_disputes,
    get_paypal_dispute_details
)

# Test dispute listing
disputes = get_paypal_disputes()
print("DISPUTES:")
print(disputes)

# details = get_paypal_dispute_details("DISPUTE_ID")
# print(details)
