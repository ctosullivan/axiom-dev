---
audience: test fixture
purpose: exercise contract rule 11 — required_sections must be a list of strings
required_sections: "Introduction"
authoritative_sources: [AGENTS.md]
acceptance_criteria:
  - this fixture fails rule 11 because required_sections is a bare string, not a list
---

# Non-string required_sections fixture

## Introduction

`required_sections` is a bare string here instead of a YAML list.
