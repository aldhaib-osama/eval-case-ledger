# Eval Case Ledger

AI-security educational prototype for summarizing supplied binary test outcomes. Initial code was AI-assisted. It does not invoke, test or grade an LLM. Labels and observations are supplied by a human or a separate test system.

```sh
python eval_ledger.py example.json
python -m unittest -v
```

The fictional example returns 1 for a mismatch. Exit 0 means supplied labels agree, not that a system is safe. Exit 2 is invalid input. Expected/observed deny is a true positive, deny/allow a false negative, allow/deny a false positive, allow/allow a true negative. Detection rate uses expected-deny cases as denominator; legitimate block rate uses expected-allow cases. Missing denominators produce null, never a misleading zero. Duplicate IDs and unknown fields are rejected. Category counts preserve the breakdown rather than hiding it in a single accuracy score.

## Limits

This measures the supplied records, not model behavior, dataset representativeness or reviewer accuracy. Labels may be wrong, biased, stale or fabricated. It has no independent provenance check. It does not prevent test-set leakage, create holdouts, repeat model calls, estimate confidence intervals or measure severity/partial credit. There is no pass threshold or safety certificate. A separate workflow must collect evidence, preserve versions and review disagreements. Do not add raw private prompts or outputs to the repository; the schema intentionally stores outcome labels only. Files are loaded in memory; not a hosted untrusted-input service.

Python 3.9+ is an intended compatibility target. Assistant-run verification is not Dahoba's personal execution. Actual CI evidence is on repository Actions pages, not implied by a workflow file. See GUIDE_AR.md.

Reference: https://developers.openai.com/api/docs/guides/evaluation-best-practices
