
from vector_store import search_chunks
from relevance_checker import check_relevance

questions = [
    "What are classification algorithms in AI?",
    "How does AI classify things?",
    "What is the capital of France?"
]

for question in questions:
    print("\n" + "=" * 50)
    print("Question:", question)

    documents = search_chunks(question, k=4)
    result = check_relevance(question, documents)

    print("Relevant:", result["relevant"])
    print("Score:", result["score"])
    print("Reason:", result["reason"])
