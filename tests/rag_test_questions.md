# RAG test questions

Run each question through retrieval. Pass = the expected entry ID is in the top 3 chunks. Target: at least 17 of 20 pass before moving on. Record results in the last column.

| # | Question | Expected entry | Pass? |
|---|----------|----------------|-------|
| 1 | What are the lifecycle stages of a PayPal dispute? | A2 | |
| 2 | What does WAITING_FOR_SELLER_RESPONSE mean? | A3 | |
| 3 | What happens if the merchant misses the response deadline? | A4 | |
| 4 | Which field tells me how long I have to respond? | A4, A5 | |
| 5 | What evidence does PayPal want for an item not received claim? | B2 | |
| 6 | What proof works for a digital product dispute? | B2, C3 | |
| 7 | What evidence helps in a not as described dispute? | B3 | |
| 8 | Can I ask the buyer to return a not as described item for a full refund? | B3 | |
| 9 | What evidence is needed for an unauthorized transaction? | B4 | |
| 10 | What are the evidence types I can submit? | C1 | |
| 11 | When can I submit evidence and how? | C2 | |
| 12 | What makes tracking proof valid for Seller Protection? | C3, D2 | |
| 13 | What are the basic requirements for Seller Protection? | D2 | |
| 14 | Does Seller Protection cover not as described claims? | D4 | |
| 15 | Are item not received chargebacks filed with the card issuer covered? | D1, D4 | |
| 16 | How fast must I ship after an unauthorized claim notice? | D5 | |
| 17 | What does it mean when I accept a claim? | E3 | |
| 18 | What offer types can I make to a buyer? | E2 | |
| 19 | Can I appeal and how many times? | E5 | |
| 20 | When should the agent recommend refunding instead of fighting? | F1 | |

## Out-of-scope checks (agent must say "no relevant policy found")
- Who won the football match last night?
- What is PayPal's policy on cryptocurrency withdrawals in Brazil?
- Can you guarantee I will win this dispute?
