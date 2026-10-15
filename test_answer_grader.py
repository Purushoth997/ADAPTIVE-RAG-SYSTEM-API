
from answer_grader import grade_answer

question = "How does AI classify things?"

context = """
In Classification Algorithms, the AI machine uses supervised
learning and defines the rules with a training set. When given
new objects, it classifies them according to the rules defined
previously.
"""

tests = [
    {
        "name": "Supported answer",
        "answer": (
            "AI uses supervised learning and a training set "
            "to define rules, then classifies new objects "
            "using those rules."
        ),
        "expected": True
    },
    {
        "name": "Unsupported answer",
        "answer": (
            "AI classifies objects using a database of country "
            "capitals and geographic locations."
        ),
        "expected": False
    }
]

passed = 0

for test in tests:
    print("\n" + "=" * 45)
    print(test["name"])

    result = grade_answer(
        question,
        context,
        test["answer"]
    )

    actual = result["supported"]
    expected = test["expected"]

    print("Actual:", actual)
    print("Expected:", expected)
    print("Reason:", result["reason"])

    if actual == expected:
        print("Test result: PASS")
        passed += 1
    else:
        print("Test result: FAIL")

print("\n" + "=" * 45)
print(f"Tests passed: {passed}/{len(tests)}")
