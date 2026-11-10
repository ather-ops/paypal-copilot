
from agent.agent import run_agent


def test_paypal_copilot_agent():
    question = """
    Analyze a PayPal Sandbox dispute.

    1. Use get_paypal_disputes to retrieve the available disputes.
    2. Select one dispute and use get_paypal_dispute_details
       to retrieve its complete details.
    3. Use search_paypal_policy to find relevant dispute
       policies and evidence requirements.
    4. Analyze the case and provide a recommendation.

    Include:
    - Dispute Summary
    - Relevant Policy
    - Evidence Assessment
    - Recommended Decision
    - Reasoning
    - Next Steps
    - Risk Level

    Do not invent evidence or policy requirements.
    Do not submit evidence, issue refunds, or perform
    any action on the PayPal account.
    """

    response = run_agent(question)

    assert isinstance(response, str)
    assert len(response.strip()) > 0

    print("\n PAYPAL COPILOT FINAL ANALYS \n")
    print(response)
