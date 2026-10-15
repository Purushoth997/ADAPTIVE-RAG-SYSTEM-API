
from rag_pipeline import ask_question

question = "What are classification algorithms in AI?"

result = ask_question(question)

print("\nQuestion:")
print(question)

print("\nAnswer:")
print(result["answer"])

print("\nSources:")
for source in result["sources"]:
    print(f"{source['source']} - Page {source['page']}")
