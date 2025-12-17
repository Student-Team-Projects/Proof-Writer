import api


#api.ask("Hello?", thinking=False)

models = [
        "gpt-oss:20b",
        "deepseek-r1:14b",
        "phi4:14b"
    ]

prompt = """
Tell an interesting story
"""

result = api.ModelBoost(
    prompt=prompt,
    models=models,
    thinking=True
)

print("Winning model:", result["winning_model"])
print("Votes:", result["votes"])
print("\nBest answer:\n")
print(result["best_answer"])