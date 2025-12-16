import json
from api import *

class FormalizationAgent:
    def __init__(self, natural_language_text, formal_language, personalized_examples, model="deepseek-r1:14b"):
        self.natural_language_text = natural_language_text
        self.formal_language = formal_language
        self.personalized_examples = personalized_examples
        self.model = model
        
    def translate(self):

        # start ai
        prompt = f"""
        You are a highly specialized Formalization Engine. Your task is to translate a mathematical STATEMENT or PROOF from natural language into valid, compilable Isabelle/HOL code.

        You **MUST** strictly adhere to the following Universal Formalization Rules:

        ### I. SYNTAX & ENCODING (CRITICAL)
        1.  **ASCII Only:** Do not use Unicode symbols. Use ASCII equivalents to prevent parsing errors:
            - Use `=>` instead of `⇒`.
            - Use `!!` instead of `⋀` (for universal quantifiers).
            - Use `_` or `ALL` / `EX` for quantifiers.
            - Use `"` (straight quotes) strictly. Never use smart quotes.
        2.  **Assumption Naming:**
            - **NEVER** put names in parentheses after the formula (e.g., `assumes "P" (name)` is FORBIDDEN).
            - **ALWAYS** put the name before the formula with a colon.
            - **Correct Format:** `assumes name: "formula"`
            - **Multiple Assumptions:** Use `and` to separate named assumptions clearly.
            Example: 
            `assumes left: "..." and right: "..."`

        ### II. TYPE SYSTEM & OPERATORS
        1.  **Abstract Algebra Rule:** Raw type variables (e.g., `'a`) do not have arithmetic operators defined.
            - **Bad:** `fixes x :: 'a` ... `x * y` (Undefined operator error).
            - **Option A (Explicit Functions):** Define the operator explicitly: `fixes mult :: "'a => 'a => 'a"`.
            - **Option B (Type Classes):** Restrict the type: `fixes x :: "'a::group"`.
        2.  **Set vs. Type Logic:** - If you fix a set `G :: 'a set`, do not use global quantifiers `!!x` unless you restrict x to G (e.g., `!!x. x : G ==> ...`).
            - Prefer reasoning about the whole type (`fixes x :: 'a`) if the problem allows it.

        ### III. LOGIC & CORRECTNESS
        1.  **Completeness:** Do not reference variables in the `shows` statement that are not defined in `fixes` or `assumes`. If you prove `e = f`, both `e` and `f` must be defined and constrained.
        2.  **Logical Flow:** - Ensure logical transitivity. In a calculation chain (`also have`), the RHS of the previous step must structurally match the LHS of the next step.
            - Verify assumptions: Do not use a "right identity" assumption to simplify a "left identity" position.

        ### IV. PROOF STYLE (ISAR)
        1.  **Structure:** Always use the structured Isar proof style:
            ```isabelle
            proof -
            have "term1 = term2" using rule_name by simp
            also have "... = term3" using other_rule by simp
            finally show ?thesis .
            qed
            ```
        2.  **Witnesses:** When proving existence, use `obtain ... where ...` immediately.
        3.  **Simplicity:** Prefer `simp`, `auto`, or `blast` for standard steps. Avoid obscure tactics unless necessary.

        ### V. DOMAIN SPECIFIC (NUMBER THEORY)
        *Only apply these if the problem involves Integers/Naturals:*
        - Use `dvd` for divisibility.
        - Use `even` for parity.
        - Simplify expressions like `m*(a*k) + n*(a*l)` using `simp add: distrib_left distrib_right`.

        ### VI. SIMP METHOD SYNTAX
        - NEVER use square brackets with simp (e.g., `by simp [rule]` is INVALID).
        - ALWAYS use parentheses and `add:` (e.g., `by (simp add: rule1 rule2)`).
        - Do NOT hallucinate lemma names like `mul_add` or `dvd_iff_...`.
        - Use `algebra_simps` to handle distributivity and commutativity for rings/integers.

        ---
        **OUTPUT INSTRUCTION:**
        Respond **ONLY** with the raw Isabelle/HOL code block. No explanations, no Markdown wrappers outside the code block, no comments about the process.

        --- PERSONALIZED EXAMPLES TO FOLLOW ---
        Example 1:
        theory Scratch
        imports Main
        begin

        theorem square_of_product:
        fixes a b :: 'a
            and mult :: "'a => 'a => 'a"
        assumes assoc: "!!x y z. mult (mult x y) z = mult x (mult y z)"
            and comm:  "!!x y. mult x y = mult y x"
        shows "mult (mult a b) (mult a b) = mult (mult a a) (mult b b)"
        proof -
        have "mult (mult a b) (mult a b) = mult a (mult b (mult a b))"
            using assoc by simp

        also have "... = mult a (mult (mult b a) b)"
            using assoc by simp

        also have "... = mult a (mult (mult a b) b)"
            using comm by simp

        also have "... = mult (mult a a) (mult b b)"
            using assoc by simp

        finally show "mult (mult a b) (mult a b) = mult (mult a a) (mult b b)" .
        qed

        end

        Example 2:
        theory Scratch
        imports Main
        begin

        lemma double_negation: "~~P \<longleftrightarrow> P"
        proof
        assume "~~P"
        then show P
            by blast
        next
        assume P
        then show "~~P"
            by blast
        qed

        fun add_one :: "nat \<Rightarrow> nat" where
        "add_one x = x + 1"

        theorem add_one_gt_zero: "add_one x > 0"
        by simp

        end

        Example 3:
        theory Scratch
        imports Complex_Main
        begin

        lemma "sqrt 2 + sqrt 3 < sqrt 10"
        proof -
        have "(sqrt 2 + sqrt 3)^2 < (sqrt 10)^2"
        proof (simp add: algebra_simps eval_nat_numeral)
            have "(2 * (sqrt 2 * sqrt 3))^2 < 5 ^ 2"
            by (simp add: algebra_simps eval_nat_numeral)
            then show "2 * (sqrt 2 * sqrt 3) < 5"
            by (smt (verit, best) power_mono)
        qed
        then show ?thesis
            by (simp add: real_less_rsqrt)
        qed

        end

        Example 4:
        theory Scratch
        imports Complex_Main
        begin

        theorem sum_of_two_evens_is_even:
        fixes a b :: int
        assumes "even a" "even b"
        shows "even (a + b)"
        proof -
        from assms obtain k where hk: "a = 2*k" using dvdE by blast
        from assms obtain l where hl: "b = 2*l" using dvdE by blast
        have "a + b = 2*(k + l)" using hk hl by simp
        hence "2 dvd (a + b)" by simp
        thus ?thesis by simp
        qed

        end

        Example 5:
        theory Scratch
        imports Main
        begin

        theorem divides_linear_combination:
        fixes a b c m n :: int
        assumes "a dvd b" "a dvd c"
        shows   "a dvd (m * b + n * c)"
        proof -
        from assms obtain k where hk: "b = a * k" by (elim dvdE)
        from assms obtain l where hl: "c = a * l" by (elim dvdE)

        have "m * b + n * c = a * (m * k + n * l)"
            using hk hl by (simp add: distrib_left distrib_right)

        then show ?thesis by (simp add: dvdI)
        qed

        end

        Example 6:
        theory Scratch
        imports Main
        begin

        theorem inverse_of_inverse:
        fixes a e :: 'a
            and mult :: "'a => 'a => 'a"
            and inv :: "'a => 'a"
        assumes assoc: "!!x y z. mult (mult x y) z = mult x (mult y z)"
            and left_id: "!!x. mult e x = x"
            and right_id: "!!x. mult x e = x"
            and left_inv: "!!x. mult (inv x) x = e"
            and right_inv: "!!x. mult x (inv x) = e"
        shows "inv (inv a) = a"
        proof -
        have "inv (inv a) = mult e (inv (inv a))"
            using left_id by simp
        also have "... = mult (mult a (inv a)) (inv (inv a))"
            using right_inv by simp
        also have "... = mult a (mult (inv a) (inv (inv a)))"
            using assoc by simp
        also have "... = mult a e"
            using right_inv by simp
        also have "... = a"
            using right_id by simp
        finally show ?thesis .
        qed

        end

        --- END OF EXAMPLES ---

        NOW, TRANSLATE THE FOLLOWING TEXT INTO ISABELLE/HOL. 

        Input Text:
        {self.natural_language_text}

        """

        # end ai

        #############################################################################

        # start ai
        older_prompt = f"""
        You are a highly specialized Formalization Engine. Your task is to translate a mathematical STATEMENT or PROOF
        from natural language into the target formal language (Isabelle/HOL).

        You **MUST** strictly adhere to the following rules:

        1. **Use Context:** Follow the provided examples exactly for syntax, terminology, and proof style.
        2. **Target Language:** Output must be valid Isabelle/HOL code that compiles with the Isabelle system.
        3. **Correct Syntax:**
        - Use `dvd` for divisibility (do NOT use Unicode symbols like ∣). 
        - Use `even` for divisibility by 2. 
        - Extract witnesses for divisibility using `obtain ... where ... by (elim dvdE)`.
        - Use `simp` or `blast` for simplifications. Do not use `ring`, `algebra_simps`, or `even_def`.
        - Declare variables using `fixes` and theorem statements using `assumes` / `shows`.
        - Use `simp add: distrib_left distrib_right` to simplify expressions of the form m*(a*k) + n*(a*l).
        - Ensure all proofs compile in Main without extra libraries like HOL-Algebra, Group or frameworks. 
        - Always write proofs in the style:
            fix variables
            assume properties (e.g., a * e = a)
            use have ... by simp
            then show ?thesis by simp
        4. **Proof Style:**
        - Proofs must be **complete, correct, and idiomatic Isabelle/HOL**.
        - Combine simple arithmetic or logical steps in a **single `simp` or `also ... finally` chain**.
        - Extract each witness (`k`, `l`, etc.) **exactly once** and reuse.
        - Avoid repetition of trivial simplifications.
        - Extract each witness (k, l, etc.) exactly once using 'obtain ... where ... by (elim dvdE)' and reuse them.
        - Keep proofs minimal, idiomatic, and fully compatible with Main.
        5. **Output Format:**
        - Respond **ONLY** with raw Isabelle/HOL code.
        - Do **not** include explanations, Markdown, JSON, or comments.
        6. **Guidelines for writing valid Isabelle/HOL code:**
        - Define Operators Explicitly: Do not use infix operators like * or + on raw type variables (e.g., fixes x :: 'a). 
        Raw types do not have arithmetic defined. Instead, explicitely fix a function (e.g., fixes mult :: "'a => 'a => 'a") 
        or use type classes (e.g., fixes x :: "'a::group").
        - Named Assumptions: Never use indexed references like assms(1) or assms(2). Always assign descriptive names to your 
        assumptions (e.g., assumes right_inv: "...") and reference them by these names.
        - Logical Consistency: Verify which assumption justifies a step. For example, to prove e = e * f, you must use 
        the assumption that f is a right identity, not that e is a right identity.
        - Syntax Safety: Avoid using -- for comments inside proof blocks as it can lead to parsing errors. Use (* comment *) for safety.
        - Step-by-Step Chains: When using also have, ensure the term on the right side of the previous equation matches the left side of 
        the current one conceptually (transitivity).
        - Correct Assumption Naming: Never place assumption names in parentheses after the formula (e.g., assumes "P" (name) is invalid). 
        Always place the name before the formula, followed by a colon (e.g., assumes name: "P").
        - Unused Fixed Variables: You defined fixes G :: "'a set" but used !!x. (universal quantifier over the entire type 'a) instead of 
        restricting x to G (e.g., !!x. x ∈ G ⟹ ...). If you intend to prove algebraic properties on types, do not fix a set G unless you actually restrict quantifiers to it.
        - Syntax Flow: In assumes blocks, the structure must be assumes label1: "prop1" and label2: "prop2". Breaking this structure causes "Outer syntax errors".

        --- EXAMPLES OF CORRECT OUTPUT ---
        Example 1:
        theory Scratch
        imports Main
        begin

        theorem square_of_product:
        fixes a b :: 'a
            and mult :: "'a => 'a => 'a"
        assumes assoc: "!!x y z. mult (mult x y) z = mult x (mult y z)"
            and comm:  "!!x y. mult x y = mult y x"
        shows "mult (mult a b) (mult a b) = mult (mult a a) (mult b b)"
        proof -
        have "mult (mult a b) (mult a b) = mult a (mult b (mult a b))"
            using assoc by simp

        also have "... = mult a (mult (mult b a) b)"
            using assoc by simp

        also have "... = mult a (mult (mult a b) b)"
            using comm by simp

        also have "... = mult (mult a a) (mult b b)"
            using assoc by simp

        finally show "mult (mult a b) (mult a b) = mult (mult a a) (mult b b)" .
        qed

        end

        Example 2:
        theory Scratch
        imports Main
        begin

        lemma double_negation: "~~P \<longleftrightarrow> P"
        proof
        assume "~~P"
        then show P
            by blast
        next
        assume P
        then show "~~P"
            by blast
        qed

        fun add_one :: "nat \<Rightarrow> nat" where
        "add_one x = x + 1"

        theorem add_one_gt_zero: "add_one x > 0"
        by simp

        end

        Example 3:
        theory Scratch
        imports Complex_Main
        begin

        lemma "sqrt 2 + sqrt 3 < sqrt 10"
        proof -
        have "(sqrt 2 + sqrt 3)^2 < (sqrt 10)^2"
        proof (simp add: algebra_simps eval_nat_numeral)
            have "(2 * (sqrt 2 * sqrt 3))^2 < 5 ^ 2"
            by (simp add: algebra_simps eval_nat_numeral)
            then show "2 * (sqrt 2 * sqrt 3) < 5"
            by (smt (verit, best) power_mono)
        qed
        then show ?thesis
            by (simp add: real_less_rsqrt)
        qed

        end

        Example 4:
        theory Scratch
        imports Complex_Main
        begin

        theorem sum_of_two_evens_is_even:
        fixes a b :: int
        assumes "even a" "even b"
        shows "even (a + b)"
        proof -
        from assms obtain k where hk: "a = 2*k" using dvdE by blast
        from assms obtain l where hl: "b = 2*l" using dvdE by blast
        have "a + b = 2*(k + l)" using hk hl by simp
        hence "2 dvd (a + b)" by simp
        thus ?thesis by simp
        qed

        end

        Example 5:
        theory Scratch
        imports Main
        begin

        theorem divides_linear_combination:
        fixes a b c m n :: int
        assumes "a dvd b" "a dvd c"
        shows   "a dvd (m * b + n * c)"
        proof -
        from assms obtain k where hk: "b = a * k" by (elim dvdE)
        from assms obtain l where hl: "c = a * l" by (elim dvdE)

        have "m * b + n * c = a * (m * k + n * l)"
            using hk hl by (simp add: distrib_left distrib_right)

        then show ?thesis by (simp add: dvdI)
        qed

        end

        Example 6:
        theory Scratch
        imports Main
        begin

        theorem inverse_of_inverse:
        fixes a e :: 'a
            and mult :: "'a => 'a => 'a"
            and inv :: "'a => 'a"
        assumes assoc: "!!x y z. mult (mult x y) z = mult x (mult y z)"
            and left_id: "!!x. mult e x = x"
            and right_id: "!!x. mult x e = x"
            and left_inv: "!!x. mult (inv x) x = e"
            and right_inv: "!!x. mult x (inv x) = e"
        shows "inv (inv a) = a"
        proof -
        have "inv (inv a) = mult e (inv (inv a))"
            using left_id by simp
        also have "... = mult (mult a (inv a)) (inv (inv a))"
            using right_inv by simp
        also have "... = mult a (mult (inv a) (inv (inv a)))"
            using assoc by simp
        also have "... = mult a e"
            using right_inv by simp
        also have "... = a"
            using right_id by simp
        finally show ?thesis .
        qed

        end

        --- TEXT TO TRANSLATE ---
        {self.natural_language_text}

        --- TARGET FORMAL LANGUAGE ---
        {self.formal_language}

        --- RAW FORMAL CODE OUTPUT ---

        """

        # end ai

        formal_language_text = ask(prompt, model=self.model)

        return formal_language_text