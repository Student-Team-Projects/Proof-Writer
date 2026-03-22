# Proof-Writer
Proof-writer is an LLM-powered application that generates mathematical proofs. Its key feature is that proofs are first written in Isabelle/HOL and only then translated to natural language.

The program requires an LLM and Isabelle/HOL. Providing a (even small) set of example formal proofs significantly improves results.

## Usage

You can run the program with 
```
python3 ProofWriter.py 
```

### Flags 

#### Main options
`--input` - Path to the file containing a theorem to prove \
`--output` - Path to the file where the proof will be saved \
`--log` - Logging level: debug or info

#### Agent configuration
`--generator_attempts` - Number of attempts for the proof generator agent \
`--verifier_attempts` - Number of attempts for the verifier agent \
`--main_attempts` - Number of attempts for the main agent 

`--examples` - JSON dictionary specifying the number of random examples from each math field to include in the formalizer prompt (e.g. '{"algebra": 3, "number_theory": 1}' or '{"all": 5}')

### Example commands

```
python3 ProofWriter.py --input /home/user/Desktop/theorem.txt --log debug --examples '{"algebra": 3, "number_theory": 1}'
```

```
python3 ProofWriter.py --log info --generator_attempts 7
```
