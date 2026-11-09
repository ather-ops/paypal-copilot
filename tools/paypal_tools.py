
import json
from smolagents import tool

from tools.paypal_disputes import fetch_disputes
from tools.paypal_disputes_details import fetch_dispute_details


@tool
def get_paypal_disputes() -> str:
    """
    Fetch disputes from the PayPal Sandbox account.

    Use this tool when the merchant wants to see their disputes,
    identify disputes requiring action, or inspect dispute statuses.

    Returns:
        A JSON-formatted list of PayPal disputes.
    """
    try:
        data = fetch_disputes()
        return json.dumps(data, indent=2)

    except Exception as error:
        return f"Failed to fetch disputes: {str(error)}"


@tool
def get_paypal_dispute_details(dispute_id: str) -> str:
    """
    Fetch detailed information about a specific PayPal dispute.

    Use this tool to inspect dispute reason, status, evidence requirements,
    response deadlines, and allowed response options.

    Args:
        dispute_id: The PayPal dispute ID.

    Returns:
        JSON-formatted dispute details.
    """
    try:
        data = fetch_dispute_details(dispute_id)
        return json.dumps(data, indent=2)

    except Exception as error:
        return f"Failed to fetch dispute details: {str(error)}"
