# PayPal Dispute Knowledge Base

Original summaries of public PayPal documentation, accessed 4 Nov 2026. Not official PayPal text. US Seller Protection policy used throughout. Entries of type `guidance` are the project builder's heuristics, not PayPal rules.


## PART A - HOW PAYPAL DISPUTES WORK


### A1. Two ways to handle PayPal disputes

`ID: A1 | TYPE: overview | REASON: all`  
Source: PayPal Disputes overview - developer.paypal.com/platforms/disputes/overview


Merchants can handle a PayPal dispute in two ways. The Resolution Center is a ready-made web interface that needs no technical integration. The Disputes API lets software list disputes, read their details and respond programmatically. Both follow the same structured dispute lifecycle, from the buyer's submission to a final resolution, which is meant to reduce ambiguity and speed up decisions.

In a direct merchant integration the merchant carries the financial liability for disputes and chargebacks that are decided against them. Disputes can also begin when a bank asks PayPal to reverse a payment, for example an ACH return.

### A2. Dispute lifecycle stages

`ID: A2 | TYPE: api | REASON: all`  
Source: Use the Disputes API - developer.paypal.com/platforms/disputes/handle-disputes/use-disputes-api ; Simulate test scenarios (sandbox) - docs.paypal.ai/growth/disputes/test-go-live


The field dispute_life_cycle_stage shows how far a dispute has progressed. The possible values are INQUIRY, CHARGEBACK, PRE_ARBITRATION and ARBITRATION.
- INQUIRY: the first stage for item-not-received and not-as-described cases. Buyer and merchant try to settle directly, without a ruling from PayPal.
- CHARGEBACK (the claim stage): PayPal reviews evidence and decides. An inquiry moves here when it is escalated to a claim. Some disputes start here directly, such as unauthorized-transaction claims, transaction-error reasons, and item-not-received or not-as-described cases when the merchant has opted out of the inquiry stage.
- PRE_ARBITRATION: reached when a party appeals a decision. The status shows UNDER_REVIEW while PayPal looks at the appeal.
- ARBITRATION: the final stage.

What the merchant can do (send a message, make an offer, provide evidence, accept the claim, escalate, appeal) depends on the stage.

### A3. Dispute statuses and who must act

`ID: A3 | TYPE: api | REASON: all`  
Source: Use the Disputes API - developer.paypal.com/platforms/disputes/handle-disputes/use-disputes-api


The field status tells you whose turn it is. OPEN means the dispute was just created and no merchant action is needed yet. WAITING_FOR_SELLER_RESPONSE means the merchant must act, usually by providing evidence or replying. WAITING_FOR_BUYER_RESPONSE means the buyer must act and the merchant has nothing to do. UNDER_REVIEW means PayPal is reviewing; in the claim-type stages the merchant may still add supporting information. RESOLVED means the dispute is closed.

PayPal can ask for more evidence several times during one dispute. Each request puts the dispute back into WAITING_FOR_SELLER_RESPONSE. The dispute leaves that status only after the merchant submits the evidence that was asked for. Sending a message alone may not change the status if PayPal is still waiting for documents.

### A4. Response deadline and allowed actions

`ID: A4 | TYPE: api | REASON: all`  
Source: Use the Disputes API - developer.paypal.com/platforms/disputes/handle-disputes/use-disputes-api


Each dispute carries a field seller_response_due_date, the date and time by which the merchant must respond. If the merchant does not respond in time, the dispute can close automatically in the customer's favor. Seller Protection also depends on responding to PayPal's requests within the time requested.

Before acting, read the dispute details. The links list (HATEOAS links) and the allowed_response_options object show which actions are available right now, for example provide evidence, accept claim, make offer, send message, escalate or acknowledge a returned item. If an action is not listed, it cannot be used at that moment.

### A5. Important fields in the dispute details response

`ID: A5 | TYPE: api | REASON: all`  
Source: Use the Disputes API - developer.paypal.com/platforms/disputes/handle-disputes/use-disputes-api

- dispute_id: the unique identifier, used to read details and to respond.
- reason: why the buyer opened the dispute (see PART B).
- status and dispute_life_cycle_stage: whose turn it is and how far the case has progressed.
- seller_response_due_date: the response deadline.
- evidences: the evidence PayPal wants. Items whose source is REQUESTED_FROM_SELLER are the ones the merchant must supply, each with an evidence_type such as PROOF_OF_FULFILLMENT, PROOF_OF_REFUND or OTHER.
- messages and offer: the conversation and any offer already made.
- dispute_outcome: the result once resolved, for example resolved in the buyer's favor or the seller's favor.
- allowed_response_options and links: the actions currently permitted.

## PART B - DISPUTE REASONS AND WHAT EACH NEEDS


### B1. List of dispute reasons

`ID: B1 | TYPE: api | REASON: all`  
Source: Dispute reasons and evidence - developer.paypal.com/disputes/reasons-evidence ; Disputes webhooks - developer.paypal.com/docs/disputes/webhooks


The main reasons are MERCHANDISE_OR_SERVICE_NOT_RECEIVED (the buyer did not receive the item or service; often abbreviated INR), MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED (the item or service differs from what was advertised; often abbreviated SNAD) and UNAUTHORISED (the buyer says they did not authorize the payment).

Transaction-error reasons also exist: CREDIT_NOT_PROCESSED (a promised refund or credit was not issued), DUPLICATE_TRANSACTION, INCORRECT_AMOUNT, PAYMENT_BY_OTHER_MEANS, CANCELED_RECURRING_BILLING, PROBLEM_WITH_REMITTANCE and OTHER.

The reason decides which evidence PayPal expects, so identify it first.

### B2. Item not received (INR): what evidence is needed

`ID: B2 | TYPE: policy | REASON: MERCHANDISE_OR_SERVICE_NOT_RECEIVED`  
Source: Dispute reasons and evidence - developer.paypal.com/disputes/reasons-evidence ; Third-party merchant guidance (Solidgate, Adyen) - supporting items only, not PayPal policy


For INR, PayPal asks for PROOF_OF_FULFILLMENT: proof that the item was shipped and delivered, or that a service or digital product was provided. For physical goods this means the carrier name and a tracking number, and delivery confirmation or a delivery signature where available.

For digital goods, typical proof is a system record showing the product was sent or accessed, such as an email receipt or a download link and access log.

If the merchant already refunded the buyer, PROOF_OF_REFUND with the refund ID is the right evidence type instead.

A strong INR response shows a verifiable tracking number, a delivered status with the delivery date, and a delivery address that matches the address on the PayPal transaction.

### B3. Not as described (SNAD): what evidence is needed

`ID: B3 | TYPE: policy | REASON: MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED`  
Source: Dispute reasons and evidence - developer.paypal.com/disputes/reasons-evidence ; Disputes Integration Guide - developer.paypal.com/docs/disputes/integration-guide ; Third-party merchant guidance (Solidgate, Adyen) - supporting items only, not PayPal policy


In a SNAD dispute the buyer says the item or service differs from the listing, is defective, or lacks promised features. If the merchant has refunded, PayPal accepts PROOF_OF_REFUND with the refund IDs.

Supporting material usually goes under the evidence type OTHER with notes and documents. Useful items include the original listing and product description, photos of what was shipped, communication with the buyer, and the refund or return policy that applied to the sale.

At any stage of the dispute lifecycle, a merchant can ask the buyer to return a SNAD item in exchange for a full refund.

SNAD claims are generally not covered by Seller Protection (see PART D), so the financial risk is higher and a refund or return offer is often the practical outcome.

### B4. Unauthorized transaction: what evidence is needed

`ID: B4 | TYPE: policy | REASON: UNAUTHORISED`  
Source: Dispute reasons and evidence - developer.paypal.com/disputes/reasons-evidence ; PayPal Seller Protection Program (US), updated 26 Jan 2026 - paypal.com/us/legalhub/paypal/seller-protection ; Third-party merchant guidance (Solidgate, Adyen) - supporting items only, not PayPal policy


In an unauthorized claim the buyer says they did not authorize the payment. PayPal asks for PROOF_OF_FULFILLMENT: the carrier name and tracking number showing the goods went out.

Merchants often add order logs, the IP address used for the purchase, and the email addresses involved as supporting evidence.

For Seller Protection, the payment must be marked eligible or partially eligible on the Transaction Details page, and valid proof of shipment must show the item was shipped no later than two days after PayPal told the merchant about the dispute.

### B5. Transaction-error reasons

`ID: B5 | TYPE: api | REASON: CREDIT_NOT_PROCESSED, DUPLICATE_TRANSACTION, INCORRECT_AMOUNT, PAYMENT_BY_OTHER_MEANS, CANCELED_RECURRING_BILLING, OTHER`  
Source: Simulate test scenarios (sandbox) - docs.paypal.ai/growth/disputes/test-go-live ; Disputes webhooks - developer.paypal.com/docs/disputes/webhooks ; Project builder guidance - not PayPal policy


Disputes for transaction errors usually begin at the CHARGEBACK stage rather than INQUIRY. In practice they are settled by correcting the error, for example issuing the missing refund, or by showing records that prove the charge was correct. Refund IDs go under PROOF_OF_REFUND; other records, such as a billing history, invoice or cancellation log, go under OTHER with notes and documents.

## PART C - EVIDENCE TYPES AND HOW TO SUBMIT


### C1. The three evidence types

`ID: C1 | TYPE: api | REASON: all`  
Source: Dispute reasons and evidence - developer.paypal.com/disputes/reasons-evidence ; Simulate test scenarios (sandbox) - docs.paypal.ai/growth/disputes/test-go-live

- PROOF_OF_FULFILLMENT: shows the goods or service were delivered. Contains tracking information (carrier name and tracking number), or documents such as a delivery signature or a digital delivery record.
- PROOF_OF_REFUND: shows the buyer was refunded. Contains one or more refund IDs.
- OTHER: anything else the case needs. Contains notes and optional documents such as photos or files.

Always match the evidence type to what PayPal requested in the evidences list.

### C2. How a merchant submits evidence

`ID: C2 | TYPE: api | REASON: all`  
Source: Disputes Integration Guide - developer.paypal.com/docs/disputes/integration-guide ; Simulate test scenarios (sandbox) - docs.paypal.ai/growth/disputes/test-go-live


Evidence can be submitted only while the dispute status is WAITING_FOR_SELLER_RESPONSE. First read the dispute details and look for evidence items with source REQUESTED_FROM_SELLER, and confirm that provide evidence appears among the allowed actions.

Then call provide evidence for that dispute ID, sending the evidence type and its information: tracking info for PROOF_OF_FULFILLMENT, refund IDs for PROOF_OF_REFUND, or notes and documents for OTHER. A successful call returns HTTP 200. Read the dispute again to confirm the evidence is recorded.

File uploads have limits on supported file types and sizes; check PayPal's current list before uploading.

### C3. What makes evidence strong

`ID: C3 | TYPE: policy | REASON: all`  
Source: PayPal Seller Protection Program (US), updated 26 Jan 2026 - paypal.com/us/legalhub/paypal/seller-protection


PayPal's proof of shipment needs documentation from a shipping company with an online, verifiable tracking number, the shipment date, and a recipient address that matches the shipping address on the Transaction Details page (at least city and state, city and country, or postal code).

Proof of delivery needs the same, plus the delivery date and a delivered status. The choice of carrier matters: for international shipments the carrier must be able to show delivered status at the correct address, otherwise a Seller Protection claim can be denied.

For digital goods, compelling evidence is a system record showing the date the item was sent and that it was electronically sent to the recipient's address (email, IP and so on) or was received or accessed by the recipient.

## PART D - SELLER PROTECTION (UNITED STATES POLICY)


### D1. What Seller Protection is and when it applies

`ID: D1 | TYPE: policy | REASON: MERCHANDISE_OR_SERVICE_NOT_RECEIVED, UNAUTHORISED`  
Source: PayPal Seller Protection Program (US), updated 26 Jan 2026 - paypal.com/us/legalhub/paypal/seller-protection


Seller Protection is a PayPal program that can let an eligible seller keep the full payment when a buyer disputes it. PayPal alone decides eligibility, based on the program rules and the documents provided. There is no limit on how many payments can be eligible, and the Transaction Details page shows which transactions may qualify.

It may apply when the buyer claims the payment was unauthorized, or that the item was not received. It also may apply when a card payment is reversed because the buyer says they did not authorize it, or when a bank-funded payment is reversed by the buyer's bank.

An item-not-received claim that the buyer files directly with their card issuer as a chargeback is not eligible.

### D2. Basic requirements for Seller Protection

`ID: D2 | TYPE: policy | REASON: MERCHANDISE_OR_SERVICE_NOT_RECEIVED, UNAUTHORISED`  
Source: PayPal Seller Protection Program (US), updated 26 Jan 2026 - paypal.com/us/legalhub/paypal/seller-protection


All of these must be true:
- The primary address on the seller's PayPal account is in the United States.
- The item is a physical, shippable good (intangible goods have their own rules, and some in-person sales qualify when paid by a PayPal goods-and-services QR code).
- The item was shipped to the address shown on the Transaction Details page. If it is later redirected to a different address, protection is lost. Avoid shipping services arranged by the buyer, because they make valid proof harder to obtain.
- The seller answers PayPal's requests for documents in the time requested, by email or in the Resolution Center.
- For pre-ordered or made-to-order goods, the seller ships within the time promised in the listing; otherwise shipping within 7 days of receiving payment is recommended.
- The seller provides valid proof of shipment or delivery.
- Business sellers using a PayPal checkout product must use its current version and pass the required session information to PayPal at checkout.

For item-not-received claims, valid proof of delivery is required in addition.

### D3. Seller Protection for intangible and digital goods

`ID: D3 | TYPE: policy | REASON: MERCHANDISE_OR_SERVICE_NOT_RECEIVED, UNAUTHORISED`  
Source: PayPal Seller Protection Program (US), updated 26 Jan 2026 - paypal.com/us/legalhub/paypal/seller-protection


Intangible goods and services can qualify if the basic requirements are met and the item was actually delivered with proof of delivery. For unauthorized-transaction claims, PayPal must have marked the intangible transaction as eligible on the Transaction Details page or told the seller so in writing.

Proof for intangible goods is compelling evidence that the item was delivered or the order fulfilled, such as a record of when and where it was electronically sent, or that the buyer accessed it.

### D4. What Seller Protection does not cover

`ID: D4 | TYPE: policy | REASON: all`  
Source: PayPal Seller Protection Program (US), updated 26 Jan 2026 - paypal.com/us/legalhub/paypal/seller-protection


Examples of transactions that are not eligible: real estate; vehicles (bicycles and similar light recreational vehicles excepted); businesses; industrial manufacturing machinery; cash equivalents such as gift cards and prepaid cards; gold; financial products and investments; gambling and games with entry fees and prizes; donations and crowdfunding; payments to government bodies and bill-payment services; personal payments sent as friends and family; payments made through PayPal Payouts; payments to the account and routing number assigned to the business account.

Also not eligible: significantly-not-as-described claims (whether filed with PayPal or the card issuer); item-not-received claims filed directly with the card issuer; physical items delivered in person (unless paid with the PayPal goods-and-services QR code); items sent after PayPal advised not to release them; and anything PayPal determines is prohibited by its user agreement or acceptable use policy.

Guest checkout and standard card payments are not covered for sellers whose accounts are registered in a listed set of countries, mostly in Europe and Asia-Pacific; accounts in other countries remain eligible.

### D5. Unauthorized-claim timing rule

`ID: D5 | TYPE: policy | REASON: UNAUTHORISED`  
Source: PayPal Seller Protection Program (US), updated 26 Jan 2026 - paypal.com/us/legalhub/paypal/seller-protection


For an unauthorized-transaction claim, the proof of shipment must show the item was shipped no later than two days after PayPal notified the seller of the dispute or reversal. For example, if PayPal gives notice on September 1, the shipment must be dated no later than September 3. The payment must also be marked eligible or partially eligible on the Transaction Details page.

### D6. Seller Protection varies by country

`ID: D6 | TYPE: policy | REASON: all`  
Source: PayPal Seller Protection Program (US), updated 26 Jan 2026 - paypal.com/us/legalhub/paypal/seller-protection


The rules summarised in PART D come from PayPal's United States page and require a US primary address. Other countries publish their own versions with different conditions. This knowledge base follows the US policy; a merchant elsewhere should check the policy page for their country before relying on it.

## PART E - WHAT A MERCHANT CAN DO


### E1. Send a message to the buyer

`ID: E1 | TYPE: api | REASON: MERCHANDISE_OR_SERVICE_NOT_RECEIVED, MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED`  
Source: Disputes Integration Guide - developer.paypal.com/docs/disputes/integration-guide ; Simulate test scenarios (sandbox) - docs.paypal.ai/growth/disputes/test-go-live


During the inquiry stage the merchant can message the buyer directly to solve the problem before it escalates. First check that the send message action is available in the dispute's links, then send a note. The messages array in the dispute details then shows the conversation.

### E2. Make an offer

`ID: E2 | TYPE: api | REASON: MERCHANDISE_OR_SERVICE_NOT_RECEIVED, MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED`  
Source: Simulate test scenarios (sandbox) - docs.paypal.ai/growth/disputes/test-go-live


In the inquiry stage a merchant can offer the buyer a resolution, when make offer appears among the allowed actions. Offer types seen in testing: REFUND (money back, for item-not-received cases), REFUND_WITH_RETURN (refund after the buyer returns the item, which needs a return shipping address), REFUND_WITH_REPLACEMENT (a refund plus a replacement item), and REPLACEMENT_WITHOUT_REFUND. An offer that includes money states the amount the seller is willing to refund.

### E3. Accept the claim (refund the buyer)

`ID: E3 | TYPE: api | REASON: all`  
Source: Disputes Integration Guide - developer.paypal.com/docs/disputes/integration-guide ; Simulate test scenarios (sandbox) - docs.paypal.ai/growth/disputes/test-go-live


Accepting a claim means giving up the dispute. It closes in the buyer's favor and PayPal refunds the buyer from the merchant's account. Accept-claim types include REFUND (full), PARTIAL_REFUND (an amount lower than the buyer asked for) and REFUND_WITH_RETURN (the buyer first returns the item to the given address).

If a partial refund is below what the buyer requested, the buyer is asked to agree in the Resolution Center. If it equals or exceeds the request, the case resolves.

### E4. Escalate an inquiry to a claim

`ID: E4 | TYPE: api | REASON: MERCHANDISE_OR_SERVICE_NOT_RECEIVED, MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED`  
Source: Simulate test scenarios (sandbox) - docs.paypal.ai/growth/disputes/test-go-live


If buyer and merchant cannot agree during the inquiry, the case can be escalated to a claim when the escalate action is available. After escalation the lifecycle stage changes from INQUIRY to CHARGEBACK and PayPal reviews the evidence and decides.

### E5. Appeal a decision

`ID: E5 | TYPE: api | REASON: all`  
Source: Disputes Integration Guide - developer.paypal.com/docs/disputes/integration-guide ; Simulate test scenarios (sandbox) - docs.paypal.ai/growth/disputes/test-go-live


If PayPal decides against the merchant, the merchant may be able to appeal when the appeal action is offered. PayPal uses preset rules to decide whether an appeal is allowed, and each party can appeal only once per case. The appeal can carry proof of fulfillment (tracking), proof of refund (refund IDs), or notes and documents under OTHER.

After an appeal the status becomes UNDER_REVIEW and the stage PRE_ARBITRATION. If the seller wins the appeal, PayPal pays the seller; if the seller loses, no money moves and the case closes.

### E6. Acknowledge a returned item

`ID: E6 | TYPE: api | REASON: MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED`  
Source: Disputes Integration Guide - developer.paypal.com/docs/disputes/integration-guide


When a SNAD resolution involves the buyer returning the item, the dispute stays in WAITING_FOR_SELLER_RESPONSE until the merchant confirms receipt of the returned item with the acknowledge returned item action, which becomes available after the buyer uploads return tracking.

## PART F - DECISION GUIDANCE (BUILDER'S HEURISTICS, NOT PAYPAL RULES)


### F1. Fight, refund, offer, or gather more

`ID: F1 | TYPE: guidance | REASON: all`  
Source: Project builder guidance - not PayPal policy


These are practical rules of thumb for the Copilot's recommendations. They are estimates and never guarantee an outcome; PayPal makes the final decision.
- Recommend FIGHT when the reason is item not received or unauthorized AND there is a verifiable tracking number showing delivered, delivered to the address on the PayPal transaction, with a delivery date and ideally a signature, AND the response deadline has not passed. For digital goods, fight when there is a clear record of delivery or access.
- Recommend REFUND (accept the claim) when the evidence is missing or contradicts the seller (delivery to a different address, item returned to sender, no tracking), when a not-as-described claim looks valid, when the amount is small compared with the effort, or when the deadline is nearly over and no evidence exists.
- Recommend OFFER or PARTIAL REFUND when evidence is mixed: the parcel is delayed or in transit, tracking is incomplete, or the problem is minor (a cosmetic defect). A partial refund or replacement can save the relationship and the cost of a loss.
- Recommend GATHER MORE first when a missing document (such as carrier confirmation) could realistically be obtained before the deadline.

Label every recommendation with a strength: strong, moderate or weak.

### F2. How to write an evidence note

`ID: F2 | TYPE: guidance | REASON: all`  
Source: Project builder guidance - not PayPal policy


Keep the note short, factual and ordered: (1) one sentence naming the order, amount and dispute reason; (2) the fulfillment facts with dates: order date, ship date, carrier, tracking number, delivery date and status; (3) confirmation that the delivery address matches the PayPal transaction; (4) a list of attached documents; (5) a polite closing request that the case be decided in the seller's favor. Avoid emotion, blame and speculation, and never state facts that the records do not show.

### F3. When to hand the case to a human

`ID: F3 | TYPE: guidance | REASON: all`  
Source: Project builder guidance - not PayPal policy


The agent should tell the merchant to review personally when: the amount is large for the business; the same buyer disputes repeatedly; there are signs of fraud or identity problems; the buyer or merchant mentions legal action; the order records conflict with each other; or the retrieved policy does not clearly cover the situation. In that last case the agent must say it found no relevant policy instead of inventing one.

### F4. Boundaries for the Copilot

`ID: F4 | TYPE: guidance | REASON: all`  
Source: Project builder guidance - not PayPal policy


The Copilot supports decisions; it does not make binding ones. It must cite the sources it used, state when it is unsure, describe its recommendation as an estimate, avoid legal or financial advice, work only with sandbox data in this project, and never submit evidence or accept a claim until the merchant has explicitly approved the action.

## PART G - GLOSSARY


### G1. Glossary of terms

`ID: G1 | TYPE: glossary | REASON: all`  
Source: PayPal Disputes overview - developer.paypal.com/platforms/disputes/overview ; Simulate test scenarios (sandbox) - docs.paypal.ai/growth/disputes/test-go-live

- INR: Item Not Received, the reason MERCHANDISE_OR_SERVICE_NOT_RECEIVED.
- SNAD: Significantly Not As Described, the reason MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED.
- Resolution Center: PayPal's web interface where buyers and sellers handle disputes.
- Claim: the formal stage after an inquiry is escalated; in the API it is the CHARGEBACK stage.
- Chargeback: a reversal started through the buyer's card issuer, or a PayPal claim-stage dispute in API terms.
- Adjudication: PayPal's decision, in the buyer's favor or the seller's favor.
- Appeal: a request to review an unfavorable decision, allowed once per party and only when PayPal's rules permit.
- HATEOAS links: links in an API response that list the actions currently available.
- Webhook: an automatic notification. Dispute events are CUSTOMER.DISPUTE.CREATED, CUSTOMER.DISPUTE.UPDATED and CUSTOMER.DISPUTE.RESOLVED.
- Transaction Details page: the page in a PayPal account showing a payment, its shipping address and Seller Protection eligibility.

## PART H - SOURCES (accessed 4 Nov 2026)

- PayPal Disputes overview: https://developer.paypal.com/platforms/disputes/overview
- Use the Disputes API (lifecycle, statuses, fields): https://developer.paypal.com/platforms/disputes/handle-disputes/use-disputes-api
- Disputes Integration Guide: https://developer.paypal.com/docs/disputes/integration-guide
- Dispute reasons and evidence: https://developer.paypal.com/disputes/reasons-evidence
- Simulate test scenarios (sandbox testing): https://docs.paypal.ai/growth/disputes/test-go-live
- Disputes webhooks: https://developer.paypal.com/docs/disputes/webhooks
- PayPal Seller Protection Program (US): https://www.paypal.com/us/legalhub/paypal/seller-protection
- Solidgate: PayPal chargeback representment guide (third-party): https://solidgate.com/blog/paypal-chargeback-representment-a-guide-to-winning-paypal-disputes/
- Adyen: PayPal chargebacks (third-party): https://docs.adyen.com/risk-management/chargeback-guidelines/paypal-chargebacks
