---
audience: test
purpose: exercise FAIL for a required section that is not present
required_sections: [Introduction, NotPresent]
authoritative_sources: [AGENTS.md]
acceptance_criteria:
  - fails because the "NotPresent" heading does not appear anywhere in the body
---

# Missing section fixture

## Introduction

This document has an Introduction heading but no "NotPresent" heading
anywhere. Per contract rule 4, the validator must report FAIL naming
every missing heading.
