

theory Isabelleproof
imports Main
begin

locale group =
  fixes mul (infixl "\<otimes>" 70)
    and e :: "'a"
    and inv :: "'a => 'a"
  assumes assoc: "(x \<otimes> y) \<otimes> z = x \<otimes> (y \<otimes> z)"
    and left_neutral: "e \<otimes> x = x"
    and left_inverse: "inv x \<otimes> x = e"
begin

lemma identity_unique:
  assumes neutral_e': "\<forall>x. e' \<otimes> x = x"
  assumes neutral_e:  "\<forall>x. e \<otimes> x = x"
  shows "e' = e"
proof -
  have "e' = e' \<otimes> e" using neutral_e[rule_format] by simp
  also have "... = e" using neutral_e'[rule_format] by simp
  finally show ?thesis .
qed

end

end



