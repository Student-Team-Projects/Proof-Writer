import api as PWapi
import isabelle as Iza
from translator import FormalizationAgent
from corrector import CorrectionAgent

##--------------------------------ISABELLE EXTRACTOR--------------------------------
BEGIN_KEYWORD = "theory Scratch"
END_KEYWORD = "end"

def ExtractIsabelleCode(s):
  start = s.find(BEGIN_KEYWORD)
  if start == -1:
    return ""
  
  end = s.rfind(END_KEYWORD, start + len(BEGIN_KEYWORD))
  if end == -1:
    return ""
  end += len(END_KEYWORD) + 1
  
  return s[start:end].strip()

##--------------------------------STATEMENT--------------------------------
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

""" FORMAL_LANGUAGE = "Isabelle"
MODEL = "deepseek-r1:14b"
personalized_examples = ""

formalization_agent = FormalizationAgent(
    natural_language_text=NATURAL_STATEMENT,
    formal_language=FORMAL_LANGUAGE,
    personalized_examples=personalized_examples,
    model=MODEL
)

formal_code = formalization_agent.translate() """


#--------------------------------------------------------------------------------------



isabelleCode = """theory Scratch
imports Main
begin

theorem unique_identity:
fixes e f :: "'a"
and mult :: "'a => 'a => 'a"
and inv :: "'a => 'a"
assumes assoc: "!!x y z. mult (mult x y) z = mult x (mult y z)"
and left_id: "!!x. mult e x = x"
and right_id: "!!x. mult x e = x"
and left_inv: "!!x. mult (inv x) x = e"
and right_inv: "!!x. mult x (inv x) = e"
shows "e = f"
proof -
have "e = mult e f" using right_id by simp
also have "... = f" using left_id by simp
finally show ?thesis .
qed

end"""
izaVerification = Iza.VerifyCorrectness(isabelleCode)

while(not izaVerification["success"]):
  print("-------------------------------------------------------------------------------------------\n")
  print(izaVerification["stdout"], '\n')
  
  correctnessAgent = CorrectionAgent(
    failed_isabelle_code=isabelleCode,
    verification_log=izaVerification["stdout"]
  )
  
  correctorOut = correctnessAgent.doStuff()
  
  print(correctorOut, '\n')
  
  correctedProof = ExtractIsabelleCode(correctorOut)
  
  print(correctedProof, '\n')
  
  if correctedProof == "":
    
    print("Well...")
    
    formAgent = FormalizationAgent(
      natural_language_text=NATURAL_STATEMENT,
      formal_language="Isabelle",
      personalized_examples=None,
      model="deepseek-r1:14b"
    )
    
    correctedProof = formAgent.translate()
  
  izaVerification = Iza.VerifyCorrectness(correctedProof)
  
  
print("DESPACITO!")