---
audience: test
purpose: [unterminated flow sequence to force a YAML parse error
---

# Bad YAML fixture

Per contract rule 2, the validator must report INVALID_SCHEMA with the
parser's error location, and must not attempt section/link checks when
the front-matter itself can't be parsed.
