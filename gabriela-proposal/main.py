import json
from translator import FormalizationAgent
from api import *

def main():
    
    # start ai
    NATURAL_STATEMENT = """
    Theorem.
    Let (G, *) be a group. The identity element in G is unique.

    Proof.
    Assume e and f are both identity elements in G. We show that e = f by creating a chain of equalities centered around the term (e * f).

    1. Start with e. Since f is an identity element (specifically a right identity), multiplying by f does not change the value:
    e = e * f

    2. Now consider the term (e * f). Since e is an identity element (specifically a left identity), multiplying by e does not change the value:
    e * f = f

    3. By chaining these two observations together, we get:
    e = e * f = f

    Therefore, e = f. ■

    """
    # end ai

    FORMAL_LANGUAGE = "Isabelle"
    MODEL = "deepseek-r1:14b"
    personalized_examples = ""
    
    formalization_agent = FormalizationAgent(
        natural_language_text=NATURAL_STATEMENT,
        formal_language=FORMAL_LANGUAGE,
        personalized_examples=personalized_examples,
        model=MODEL
    )

    formal_code = formalization_agent.translate()
    
    print(f"Natural statement: {NATURAL_STATEMENT}")
    print(f"Formal language: {FORMAL_LANGUAGE}")
    print(f"**{formal_code}**")


if __name__ == "__main__":
    main()
