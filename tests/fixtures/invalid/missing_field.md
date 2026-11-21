---
audience: test
purpose: exercise INVALID_SCHEMA for a front-matter missing a required field
required_sections: [Body]
authoritative_sources: [AGENTS.md]
---

# Missing field fixture

## Body

This front-matter is valid YAML but omits `acceptance_criteria`. Per
contract rule 3, the validator must report INVALID_SCHEMA naming the
missing field.
