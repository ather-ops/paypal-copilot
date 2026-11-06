# Sources (accessed 4 Nov 2026)

Official pages. Download them locally into `data/raw/` if you want the full text (that folder is git-ignored). Do not commit them.

| # | Title | URL | Used for |
|---|-------|-----|----------|
| 1 | PayPal Disputes overview | https://developer.paypal.com/platforms/disputes/overview | lifecycle, two ways to manage disputes |
| 2 | Use the Disputes API | https://developer.paypal.com/platforms/disputes/handle-disputes/use-disputes-api | stages, statuses, fields |
| 3 | Disputes Integration Guide | https://developer.paypal.com/docs/disputes/integration-guide | list, details, evidence, accept claim |
| 4 | Dispute reasons and evidence | https://developer.paypal.com/disputes/reasons-evidence | reason to evidence mapping |
| 5 | Simulate test scenarios (sandbox) | https://docs.paypal.ai/growth/disputes/test-go-live | how to test every flow |
| 6 | Disputes set-up | https://docs.paypal.ai/growth/disputes/set-up | sandbox accounts, buyer-side credentials |
| 7 | Disputes webhooks | https://developer.paypal.com/docs/disputes/webhooks | reason list, events |
| 8 | PayPal Seller Protection Program (US) | https://www.paypal.com/us/legalhub/paypal/seller-protection | eligibility, proof of delivery |
| 9 | PayPal docs index (all pages) | https://docs.paypal.ai/llms.txt | find any other page |
| 10 | Solidgate PayPal representment guide (third-party) | https://solidgate.com/blog/paypal-chargeback-representment-a-guide-to-winning-paypal-disputes/ | typical supporting evidence only |

## Region choice
This project follows the **United States** Seller Protection policy. Say so in the README.

## Already prepared
`data/knowledge_base/PayPal_Dispute_Knowledge_Base.pdf` (and `.md`): original paraphrased summaries of 1-8 above, 30 self-contained entries with IDs. This is the first RAG corpus. Your own playbooks go in `data/playbooks/`.
