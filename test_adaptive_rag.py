
from adaptive_rag import adaptive_ask

questions = [
    "What are classification algorithms in AI?",
    "How does AI classify things?",
    "What is the capital of France?"
]

for question in questions:
    print("\n" + "=" * 55)
    print("Question:", question)

    result = adaptive_ask(question)

    print("\nAnswer:")
    print(result["answer"])

    print("\nRetrieval attempts:",
          result["retrieval_attempts"])

    print("Relevant context found:",
          result["relevant_context_found"])

    if result["rewritten_query"]:
        print("Rewritten query:",
              result["rewritten_query"])

    print("Sources:")
    for source in result["sources"]:
        print(f"{source['source']} - Page {source['page']}")
