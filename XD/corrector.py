import json
from api import *

class CorrectionAgent:
    def __init__(self, failed_isabelle_code, verification_log ,model="deepseek-r1:14b"):
        self.model = model
        self.failed_isabelle_code = failed_isabelle_code
        self.verification_log = verification_log
        
    def doStuff(self):

        # start ai
        prompt = f"""
You are an **Isabelle/HOL Proof Repair and Correction Engine**.

You receive:
1. A complete Isabelle theory that FAILED to verify
2. The exact output of Isabelle's verifier (error log)

Your task is to **correct the Isabelle proof so that it compiles successfully**,
while preserving the original proof idea as much as possible.

==================================================================
INPUTS
==================================================================

Input A — FAILED ISABELLE THEORY:
{self.failed_isabelle_code}

Input B — VERIFICATION OUTPUT:
{self.verification_log}

==================================================================
GLOBAL OBJECTIVE
==================================================================

Produce a **corrected Isabelle/HOL theory** that:

• compiles without errors
• respects Isabelle syntax and typing rules
• does NOT introduce unjustified assumptions
• preserves the intended mathematical meaning
• minimally modifies the original proof

==================================================================
ERROR ANALYSIS RULES (MANDATORY)
==================================================================

1. **Read the Error Message Literally**
   - Identify:
     - the failed proof step
     - the lemma or assumption Isabelle tried to apply
     - the exact goal at failure

2. **Do NOT Guess**
   - Only use assumptions that actually match the goal syntactically
   - If `simp` fails, check:
     - orientation of equations
     - argument positions
     - missing assumptions

3. **Identity Directionality (CRITICAL)**
   - If the assumption is:
     `!!x. mult x e = x`
     it can ONLY rewrite terms of the form:
     `mult ?x e`
   - It CANNOT rewrite:
     `mult e ?x`
   - If the proof misuses identity direction, you MUST fix the proof order.

4. **No Implicit Properties**
   - Do NOT use:
     - commutativity
     - associativity
     - inverse laws
   unless they are explicitly assumed AND required.

==================================================================
ALLOWED REPAIR OPERATIONS
==================================================================

You MAY:
✔ reorder proof steps  
✔ replace `simp` with explicit `have` steps  
✔ introduce intermediate equalities  
✔ rename assumptions for clarity  
✔ add missing assumptions ONLY if logically required  

You MAY NOT:
✘ change the theorem statement unless absolutely necessary  
✘ weaken or remove assumptions to make proof easier  
✘ use automation to hide logical errors  

==================================================================
PROOF STYLE REQUIREMENTS
==================================================================

• Use structured Isar proof (`proof - ... qed`)
• Prefer explicit `have`, `also have`, `finally`
• Avoid `auto`, `blast`, `smt` unless unavoidable
• Avoid rewriting chains that violate logical flow

==================================================================
COMMON FAILURE PATTERNS TO FIX
==================================================================

1. **Wrong Identity Used**
   Example error:
   Goal: `e = mult e f`
   Attempted rule: `mult ?x e = ?x`

   Correct fix:
   - Either use `left_id`
   - Or change the equality direction

2. **Unconstrained Variable**
   - Introduce `fixes` or assumptions

3. **Unused Assumptions**
   - If `inv` or inverse laws are unused, consider removing them

==================================================================
OUTPUT FORMAT (STRICT)
==================================================================

• Output ONLY the corrected Isabelle theory
• NO explanations
• NO Markdown
• NO comments
• Preserve original formatting as much as possible

YOUR OUTPUT MUST BEGIN WITH "theory Scratch' AND MUST END WITH 'end'. 
THIS IS CRUCIAL, CRUCIAL, CRUCIAL!!!

EXAMPLE ISABELLE CODE:
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

==================================================================
TASK
==================================================================

Analyze the verification failure and produce a corrected Isabelle/HOL theory
that passes verification.

        """

        # end ai

        #############################################################################

        corrected_proof = ask(prompt, model=self.model, thinking=False)

        return corrected_proof