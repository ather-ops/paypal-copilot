# Saturday go / no-go (check on Friday night)

All must be true before you start building:
- [ ] Repo is public, starter files pushed, `.env` is ignored
- [ ] Sandbox business and personal accounts both log in
- [ ] OAuth token request succeeds
- [ ] List disputes returns 3 disputes; details call works
- [ ] `orders.csv` has the real sandbox transaction IDs
- [ ] Embedding model already downloaded
- [ ] Groq key works; model tested with two dummy tools
- [ ] Knowledge base PDF skimmed; 3 playbooks at least half drafted
- [ ] Streamlit Cloud is connected to GitHub
- [ ] Devpost registered; deadline noted (check the page: Nov 12 vs 13)

## Session 1: Sat 10pm to Sun 4am
| Time | Goal |
|------|------|
| 10:00-11:00 | Auth helper + list and details tools working |
| 11:00-12:30 | Playbooks finished, ingest knowledge base + playbooks |
| 12:30-12:45 | Break |
| 12:45-2:15 | Chunk, embed, FAISS, RAG tool, run tests/rag_test_questions.md |
| 2:15-3:30 | Order evidence tool over orders.csv |
| 3:30-4:00 | Commit, update TODO.md, stop |

## Session 2: Sun 1pm to 5pm
| Time | Goal |
|------|------|
| 1:00-2:15 | Agent, system prompt, draft evidence tool |
| 2:15-3:00 | Test all 3 disputes in the terminal |
| 3:00-4:45 | Streamlit UI, Approve button, submit called by the UI only |
| 4:45-5:00 | Commit, TODO.md |

Decision rule: if submitting evidence is not working by 4:15pm, switch to the fallback (app outputs a ready-to-submit package).

## Session 3: Sun 7pm to 9pm
Fix bugs, deploy, screenshots, README draft.

## Mon to Wed
Demo video, README polish, submit on **Nov 11**.
