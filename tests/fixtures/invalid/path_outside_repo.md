---
audience: test
purpose: exercise FAIL for an authoritative_sources path that resolves outside the repository
required_sections: [Body]
authoritative_sources: [../outside-the-repository.md]
acceptance_criteria:
  - fails because the path resolves above the repository root, regardless of whether anything exists there
---

# Path outside repository fixture

## Body

Added after independent review found that enough `../` segments could
escape the repository and still be reported PASS if the target happened
to exist. This fixture must FAIL regardless of whether
`../outside-the-repository.md` actually exists on disk — the rule is
about the path resolving outside the repository, not about existence.
