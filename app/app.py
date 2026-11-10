
import sys
import json
from pathlib import Path

import streamlit as st
# Path confirmations
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

LIST_FILE = PROJECT_ROOT / "docs" / "samples" / "list_disputes.json"


from tools.paypal_disputes import fetch_disputes
from tools.paypal_disputes_details import fetch_dispute_details
from agent.agent import run_agent


st.set_page_config(
    page_title="PayPal Copilot",
    page_icon="🦜",
    layout="wide"
)

if "selected_details" not in st.session_state:
    st.session_state["selected_details"] = None

if "selected_details_id" not in st.session_state:
    st.session_state["selected_details_id"] = None

if "agent_result" not in st.session_state:
    st.session_state["agent_result"] = None

if "agent_result_id" not in st.session_state:
    st.session_state["agent_result_id"] = None

st.title("PayPal Copilot")

st.caption(
    "AI-powered merchant dispute analysis and resolution assistant."
)

st.divider()

st.sidebar.header("Agent Controls")

if st.sidebar.button(
    "🔄 Refresh Disputes from Sandbox",
    key="refresh_disputes"
):

    try:
        with st.spinner("Fetching Sandbox disputes..."):

            fetch_disputes()

        # Clear stale results after refreshing
        st.session_state["selected_details"] = None
        st.session_state["selected_details_id"] = None
        st.session_state["agent_result"] = None
        st.session_state["agent_result_id"] = None

        st.sidebar.success("Disputes refreshed successfully.")

        st.rerun()

    except Exception as error:

        st.sidebar.error(f"Failed to refresh: {error}")

st.sidebar.divider()

st.sidebar.caption(
    "PayPal Sandbox integration\n\n"
    "Read-only AI analysis\n\n"
    "Human approval required for real actions"
)

if not LIST_FILE.exists():

    st.warning(
        "No dispute cache found. "
        "Refresh disputes from the Sandbox."
    )

    st.stop()

try:

    with open(LIST_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

except (json.JSONDecodeError, OSError) as error:

    st.error(f"Could not load dispute cache: {error}")

    st.stop()

disputes = data.get("items", [])

if not disputes:
    st.info("No disputes found in your Sandbox account.")
    st.stop()

st.subheader(f"Active Disputes ({len(disputes)})")
dispute_options = {}
for dispute in disputes:
    dispute_id = dispute.get("dispute_id")
    if not dispute_id:
        continue

    amount = dispute.get("dispute_amount", {})

    label = (
        f"{dispute_id} | "
        f"{dispute.get('reason', 'Unknown reason')} | "
        f"{amount.get('value', '0.00')} "
        f"{amount.get('currency_code', 'USD')}"
    )

    dispute_options[label] = dispute_id

if not dispute_options:

    st.warning("No valid dispute IDs were found.")

    st.stop()

selected_label = st.selectbox(
    "Select a dispute to inspect:",
    list(dispute_options.keys()),
    key="dispute_selector"
)

selected_dispute_id = dispute_options[selected_label]
selected_dispute = next(
    (
        dispute
        for dispute in disputes
        if dispute.get("dispute_id") == selected_dispute_id
    ),
    {}
)

amount = selected_dispute.get("dispute_amount", {})
st.divider()
metric1, metric2, metric3 = st.columns(3)

with metric1:
    st.metric(
        "Dispute Amount",
        f"{amount.get('value', '0.00')} "
        f"{amount.get('currency_code', 'USD')}"
    )

with metric2:

    st.metric(
        "Dispute Status",
        selected_dispute.get("status", "Unknown")
    )

with metric3:

    st.metric(
        "Dispute Stage",
        selected_dispute.get("dispute_life_cycle_stage", "Unknown")
    )

st.caption(
    f"Response deadline: "
    f"{selected_dispute.get('seller_response_due_date', 'Not available')}"
)

# =========================================================
# 10. MAIN DASHBOARD
# =========================================================

col1, col2 = st.columns([1.4, 1])
with col1:

    st.subheader("Dispute Details & Evidence")
    if st.button(
        "Fetch Full Dispute Details",
        key="fetch_dispute_details"
    ):

        try:

            with st.spinner("Fetching dispute details..."):
                details = fetch_dispute_details(selected_dispute_id)
                st.session_state["selected_details"] = details

                st.session_state["selected_details_id"] = (
                    selected_dispute_id
                )

        except Exception as error:
            st.error(f"Failed to fetch details: {error}")

    if (
        st.session_state.get("selected_details_id")
        == selected_dispute_id
        and st.session_state.get("selected_details")
    ):

        st.json(
            st.session_state["selected_details"],
            expanded=2
        )

    else:

        st.info(
            "Fetch full details to inspect the selected dispute."
        )
with col2:
    st.subheader("🤖 AI Copilot")
    st.write(
        "Analyze this dispute using PayPal policy retrieval "
        "and the AI reasoning agent."
    )

    if st.button(
        "Analyze Dispute",
        type="primary",
        key="analyze_dispute"
    ):

        try:

            with st.spinner(
                "Copilot is analyzing the dispute..."
            ):

                details = fetch_dispute_details(
                    selected_dispute_id
                )

                st.session_state["selected_details"] = details
                st.session_state["selected_details_id"] = (
                    selected_dispute_id
                )

                question = f"""
Analyze this PayPal Sandbox dispute.
Dispute ID: {selected_dispute_id}
Actual dispute details:
{json.dumps(details, indent=2)}
Please:
1. Identify the dispute reason, status and deadline.
2. Search relevant PayPal policy.
3. Inspect requested evidence and allowed response options.
4. Identify missing evidence.
5. Recommend one decision:
   FIGHT, REFUND, OFFER,
   GATHER_MORE_EVIDENCE or ESCALATE.
6. Explain the reasoning and risk level.

Important instructions:

- Use actual dispute data.
- Do not invent evidence or policy requirements.
- Distinguish requested evidence from submitted evidence.
- Do not assume seller protection eligibility guarantees success.
- Assess risk based on the evidence, deadline and potential outcome.
- Do not submit evidence, issue refunds or perform any PayPal action.
- Treat all recommendations as requiring human review.
"""

                result = run_agent(question)

                st.session_state["agent_result"] = result

                st.session_state["agent_result_id"] = (
                    selected_dispute_id
                )

        except Exception as error:

            st.error(f"Agent analysis failed: {error}")

    if (
        st.session_state.get("agent_result_id")
        == selected_dispute_id
        and st.session_state.get("agent_result")
    ):

        st.divider()

        st.markdown("### Copilot Recommendation")

        st.markdown(
            st.session_state["agent_result"]
        )

        st.warning(
            "AI-generated recommendation only. "
            "No evidence has been submitted and no refund "
            "or other PayPal action has been executed."
        )

        st.divider()
        st.markdown("### Human Review")

        approved = st.checkbox(
            "I have reviewed this AI recommendation and approve "
            "proceeding to the next manual review step.",
            key=f"approval_{selected_dispute_id}"
        )

        if approved:

            st.success(
                "Review acknowledgement recorded in this session. "
                "No PayPal action has been executed."
            )

        else:

            st.info("Human review is still pending.")

st.divider()
st.caption(
    "PayPal Copilot | Hackathon MVP | "
    "PayPal Sandbox Integration | Human Approval Required"
)
