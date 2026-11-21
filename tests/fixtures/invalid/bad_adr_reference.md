---
audience: test
purpose: exercise FAIL for a reference to a non-existent ADR number
required_sections: [Body]
authoritative_sources: [AGENTS.md]
acceptance_criteria:
  - fails because decisions/9999-does-not-exist.md is not a real ADR in this repository
---

# Bad ADR reference fixture

## Body

See [a nonexistent decision](../../../decisions/9999-does-not-exist.md).
Per contract rule 7, the validator must report FAIL naming the bad ADR
number, since this path resolves into `decisions/` but no such file
exists.
