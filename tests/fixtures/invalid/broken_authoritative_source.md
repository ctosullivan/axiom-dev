---
audience: test
purpose: exercise FAIL for an authoritative_sources entry that does not resolve
required_sections: [Body]
authoritative_sources: [this-file-does-not-exist.md]
acceptance_criteria:
  - fails because the authoritative source path does not resolve relative to the repository root
---

# Broken authoritative source fixture

## Body

Per contract rule 5, the validator must report FAIL naming the
unresolvable path.
