# PayPal sandbox setup (do this once, about 45 minutes)

Goal: a merchant account, a buyer account, API credentials, and 3 open test disputes.

## 1. Developer account and sandbox
1. Go to developer.paypal.com and log in (or sign up). Signing up creates your sandbox automatically, with a default **business** account (merchant) and a default **personal** account (buyer).
2. Flip the toggle at the top right to **Sandbox**, not Live.
3. Open **Testing tools > Sandbox accounts**. For each account use the three-dot menu > **View/Edit account** to see its email and generated password. Save both in a password manager. These are not your real PayPal logins.
4. Check the account **country**. Prefer **United States** so it matches the US Seller Protection policy in the knowledge base. If it is not, click **Create account** and make a new US business and a new US personal account.

## 2. REST app and credentials
1. Open **Apps & Credentials**, make sure **Sandbox** is selected.
2. Use the default app, or **Create App** (type: Merchant).
3. Copy the **Client ID** and **Secret** into your local `.env` (see `.env.example`). Never paste them into chat, a commit or a screenshot.
4. Note which sandbox business account the app belongs to. The API acts as that account, so the disputes must be on that same merchant.

## 3. Token test (proves the credentials work)
POST to `https://api-m.sandbox.paypal.com/v1/oauth2/token` with HTTP basic auth (client ID as user, secret as password) and the form field `grant_type=client_credentials`. A good reply contains `access_token` and `expires_in`. Tokens expire, so your code must cache and refresh them.

## 4. Make 3 test payments (as the buyer)
1. Use a **separate browser profile or private window** for each account. Never mix with a real PayPal session.
2. Sign in at sandbox.paypal.com with the **personal** account.
3. Send money to the **business** account's email. Choose **paying for goods or services** (friends and family payments are not protected and make poor test cases).
4. Make three payments, for example $120, $64.50 and $310 (the amounts used in `orders.csv`).
5. Open each payment in recent activity and copy its **Transaction ID**. Paste them into `data/orders.csv` in place of the `REPLACE_WITH_SANDBOX_TXN_ID_*` values.

## 5. Create 3 disputes (as the buyer, in the website)
1. Still as the personal account, open the **Resolution Center**.
2. Report a problem on each transaction: one **item not received**, one **not as described**, one **unauthorized**.
3. Wait a few minutes. PayPal's test guide says actions can take a little while to become available.
4. In the other browser profile, sign in as the **business** account and open its Resolution Center. You should see the 3 disputes. Dispute IDs look like `PP-D-12345`.

Why the website and not the API? Creating disputes through the API as a buyer needs a special permission scope that PayPal normally adds through an account manager, plus a signed buyer token. That is a risky detour for a hackathon. The website route needs none of it.

## 6. API check (Thursday)
With the app's token, list disputes (`GET /v1/customer/disputes`). You should see 3 items. Open one with show dispute details and confirm you see `reason`, `status`, `dispute_life_cycle_stage` and `seller_response_due_date`. If the list is empty, the app and the business account you used to receive payments are probably different.

## Gotchas
- **Evidence types in the sandbox:** PayPal's test guide uses PROOF_OF_FULFILLMENT with tracking info for item-not-received cases and OTHER with notes for general cases. Try PROOF_OF_FULFILLMENT first, fall back to OTHER.
- **Stage matters:** evidence only works while status is WAITING_FOR_SELLER_RESPONSE. If the dispute is still OPEN, wait, or use the sandbox-only status update described in PayPal's test guide.
- **Sandbox helpers:** the test guide documents sandbox-only calls to settle a dispute (outcome BUYER_FAVOR or SELLER_FAVOR) and to change a dispute reason. A buyer email containing `allowappeal` enables the appeal flow. The path value `ERRDIS015` simulates a forbidden error.
- **Sandbox is sometimes slow or flaky.** If something fails, wait and retry before debugging your code.
- **Do not commit** screenshots that show secrets, or real emails.

## Other accounts to have ready
- Groq API key, and confirm the model you pick supports tool calling.
- Hugging Face model download: run the embedding model once on Thursday so Saturday does not wait on a download.
- GitHub account connected to Streamlit Community Cloud.
- Devpost: registered for the hackathon, rules read (deadline, video length, repo and license requirements).
