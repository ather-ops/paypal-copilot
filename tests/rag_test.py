
from rag.retriever import retriever

results = retriever.retrieve(
    query="What evidence should a seller provide for an item not received dispute?",
    top_k=5
)

for i, result in enumerate(results, start=1):
    print(f"\nResult {i}")
    print("Score:", round(result["score"], 4))
    print("Source:", result["metadata"]["source"])
    print("Page:", result["metadata"].get("page"))
    print("Policy IDs:", result["metadata"].get("policy_ids"))
    print("Text:", result["text"][:500])
