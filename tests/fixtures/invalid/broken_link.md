---
audience: test
purpose: exercise FAIL for a broken relative Markdown link in the body
required_sections: [Body]
authoritative_sources: [AGENTS.md]
acceptance_criteria:
  - fails because the body link does not resolve relative to this document's own location
---

# Broken link fixture

## Body

See [nowhere](./this-does-not-exist.md). Per contract rule 6, the
validator must report FAIL naming the broken link.
