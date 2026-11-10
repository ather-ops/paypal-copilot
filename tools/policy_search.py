from functools import lru_cache
from smolagents import tool
from rag.retriever import PayPalRetriever


@lru_cache(maxsize=1)
def get_retriever():
    return PayPalRetriever()


@tool
def search_paypal_policy(query: str) -> str:
    """
    Search official PayPal dispute policy documents.

    Use for dispute reasons, seller protection, evidence requirements,
    response deadlines, and dispute procedures.

    Args:
        query: Specific question about PayPal dispute policies.
    """
    results = get_retriever().retrieve(
        query=query,
        top_k=5,
        document_type="knowledge_base"
    )

    if not results:
        return (
            "No relevant policy information was found. "
            "Do not invent policy guidance."
        )

    formatted_results = []

    for number, result in enumerate(results, start=1):
        metadata = result["metadata"]

        formatted_results.append(
            f"""
POLICY RESULT {number}
Source: {metadata.get('source', 'Unknown')}
Page: {metadata.get('page', 'Unknown')}
Policy IDs: {metadata.get('policy_ids', [])}
Similarity: {result['score']:.4f}

Policy Text:
{result['text']}
"""
        )

    return "\n".join(formatted_results)
