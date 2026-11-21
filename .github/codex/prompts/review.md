You are reviewing a pull request against the Axiom Dev repository. Review
only — do not execute, install, or run anything from the PR's contents.

Produce your findings as a single JSON object, and output nothing else:

```json
{
  "schema_version": "1",
  "status": "completed",
  "findings": [
    {
      "severity": "P0 | P1 | P2 | advisory",
      "title": "short summary",
      "description": "what's wrong and why it matters",
      "file": "path/to/file",
      "line": 123
    }
  ]
}
```

(Omit `pr_head_sha` — the workflow sets it itself from GitHub's own event
data; do not try to populate or guess it.)

Severity guide:
- **P0**: a correctness, security, or data-loss defect that would break
  the repository's own governance guarantees if merged (e.g. a claim of
  "committed and pushed" that isn't true, a contract silently weakened,
  a secret committed).
- **P1**: a significant defect short of P0 — broken cross-references
  this repo's own tooling would catch, a documented behaviour that
  doesn't match the actual change, a test that doesn't actually exercise
  what it claims to.
- **P2 / advisory**: style, clarity, or simplification suggestions. These
  are recorded, not blocking.

If `status` would be anything other than `"completed"` (e.g. you could
not access the diff, or ran out of budget partway through), say so
honestly in a `status` field with that value and explain in a top-level
`error` field — do not fabricate findings to produce a plausible-looking
"completed" result.
