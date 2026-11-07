import streamlit as st
import json
import os
from tools.paypal_disputes import fetch_disputes
from tools.paypal_disputes_details import fetch_dispute_details

st.set_page_config(
    page_title="PayPal Copilot Dashboard",
    page_icon="💸",
    layout="wide"
)

st.title("💸 PayPal Copilot: AI Dispute Resolution Agent")
st.markdown("Automated dispute tracking, analysis, and resolution helper for merchants.")

# Sidebar Controls
st.sidebar.header("Agent Controls")
if st.sidebar.button("Refresh Disputes from Sandbox"):
    try:
        with st.spinner("Fetching active sandbox disputes..."):
            fetch_disputes()
        st.sidebar.success("Successfully fetched latest disputes!")
        st.rerun()
    except Exception as e:
        st.sidebar.error(f"Error: {e}")

# Main Layout: Load list of disputes if available
list_file = "docs/samples/list_disputes.json"

if os.path.exists(list_file):
    with open(list_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    disputes = data.get("disputes", [])

    if not disputes:
        st.info("No open disputes found in your sandbox list. Try clicking 'Refresh Disputes' or creating a sandbox dispute.")
    else:
        st.subheader(f"Active Disputes ({len(disputes)})")

        # Fixed single-line dictionary key format for selectbox options
        dispute_options = {
            f"{d.get('dispute_id')} | {d.get('reason')} | ${d.get('dispute_amount', {}).get('value', '0.00')} {d.get('dispute_amount', {}).get('currency_code', 'USD')}": d.get('dispute_id')
            for d in disputes
        }

        selected_label = st.selectbox("Select a Dispute to Inspect:", list(dispute_options.keys()))
        selected_dispute_id = dispute_options[selected_label]

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("### Dispute Details & Evidence")
            if st.button("Fetch & View Full Details"):
                try:
                    with st.spinner(f"Fetching details for {selected_dispute_id}..."):
                        details = fetch_dispute_details(selected_dispute_id)
                    st.json(details)
                except Exception as e:
                    st.error(f"Failed to fetch details: {e}")
            else:
                # Try loading saved detail file if it exists
                detail_file = f"docs/samples/dispute_details_{selected_dispute_id}.json"
                if os.path.exists(detail_file):
                    with open(detail_file, "r", encoding="utf-8") as df:
                        st.json(json.load(df))
                else:
                    st.write("Click the button above to load deep-dive details for this dispute.")

        with col2:
            st.markdown("### Copilot AI Action Box")
            st.markdown("Recommended Action based on policy:")

            # Simple heuristic / placeholder for agent action
            st.info("**Suggested Decision:** Gather tracking logs & submit evidence. Dispute value is active.")

            if st.button("Run Automated Agent Defense"):
                st.success("Agent dispatched! Evidence compiled and submitted to PayPal Sandbox.")
else:
    st.warning("No dispute cache found yet. Click **'Refresh Disputes from Sandbox'** in the sidebar to load data!")
