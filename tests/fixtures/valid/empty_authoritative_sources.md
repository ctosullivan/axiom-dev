---
audience: test fixture
purpose: exercise contract rule 14 — authoritative_sources may legitimately be an empty list
required_sections: [Introduction]
authoritative_sources: []
acceptance_criteria:
  - this fixture passes despite an empty authoritative_sources list, because it has no internal authoritative dependencies
---

# Empty authoritative_sources fixture

## Introduction

This document legitimately cites no other repository file as an
authoritative source — an empty list is the honest statement of that,
not an omission.
