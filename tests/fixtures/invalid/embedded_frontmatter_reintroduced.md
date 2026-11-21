---
audience: test fixture
purpose: exercise contract revision rule 7 — accidental reintroduction of embedded front-matter must FAIL, never be silently parsed as the schema
required_sections: [Body]
authoritative_sources: [AGENTS.md]
acceptance_criteria:
  - this fixture deliberately reintroduces the superseded front-matter convention
---

# Embedded front-matter reintroduced fixture

## Body

This document still starts with an old-style `---`-delimited front-matter
block even though a companion `.schema.yaml` file is the current
convention (`decisions/0006`). The validator must FAIL this document,
naming the reintroduction, rather than parsing the block above as if it
were still a valid schema.
