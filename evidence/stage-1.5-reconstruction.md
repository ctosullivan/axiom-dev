---
audience: whoever assesses Phase 1 closeout or extends the validator's documentation later
purpose: record the Stage 1.5 independent documentation reconstruction exercise and its findings/dispositions
required_sections: [Permitted evidence boundary, Reconstruction summary, Comparison findings and dispositions, Isolation honesty note]
authoritative_sources: [docs/axiom-validator.md, contracts/documentation-schema-validator.md, planning/phase-01-foundation.md]
acceptance_criteria:
  - the permitted-evidence boundary is stated explicitly, with the actual files the agent read recorded as an audit trail, not assumed
  - every finding has a disposition (fixed, or explicitly accepted with reasoning)
---

# Stage 1.5: independent documentation reconstruction

Per `planning/phase-01-foundation.md` §4 Stage 1.5 and the "no synthetic
substitute" rule (§2): this reconstruction was run against the real,
already-built validator component — not a constructed exercise built to
pass.

## Permitted evidence boundary

The reconstructing agent was instructed to read, for its blind
reconstruction phase, only: `src/axiom_validator/*.py`, `tests/` (test
file + all fixtures), `contracts/documentation-schema-validator.md`,
`evidence/stage-1.4-baseline.md`, `evidence/stage-1.4-refactor.md`,
`requirements.txt` — explicitly excluding `docs/`, `planning/`,
`decisions/`, `README.md`, `AGENTS.md`, and git history, to prevent
copying or anchoring on the human-facing explanation it would later be
compared against.

**Isolation level: best-effort, not mechanical** (per `docs/agent-isolation.md`'s
taxonomy) — nothing technically prevented the agent from reading
excluded files; it was asked not to, and it reported which files it
actually read as its own audit trail. That self-report is not a
substitute for mechanical enforcement, and is named as such here rather
than presented as stronger than it is. The reported file list (20 files,
all within the permitted set, none outside it) is consistent with the
instruction having been followed, but this project has no independent
way to confirm the agent didn't glance elsewhere and simply not mention
it.

## Reconstruction summary

From the permitted evidence alone, the agent correctly reconstructed:
the validator's purpose and all four main behaviours (SKIPPED/INVALID_SCHEMA/PASS/FAIL
semantics, the five required schema fields, the section/source/link
checks, the ADR-specific error case); the real module architecture
(`parsing.py`/`rules.py`/`reporting.py`/`__init__.py`/`__main__.py` and
each one's actual responsibility, matching the real code); correct CLI
and programmatic usage, including a detail — `README.md` validating to
`PASS` — it verified against the actual test file rather than assuming;
and the real, documented limitations (schema-enforcement scope,
semantic-check scope, the `§`-only bare-path limitation, the
wrong-slug-vs-wrong-number ADR limitation).

## Comparison findings and dispositions

**GAP (accepted, no action) — the reconstruction couldn't verify
`docs/axiom-validator.md`'s opening provenance claim** ("found missing
during Stage 1.4→1.5 reconciliation," citing `AGENTS.md` §7) because
that file and `AGENTS.md` were outside the permitted evidence by design.
**Disposition: no fix needed** — the claim is true (this document's own
earlier revision history and `evidence/phase-1-log.md`'s "Pre-Stage-1.5
reconciliation gap" entry confirm it), and it is correctly placed —
provenance about the *documentation itself* is exactly the kind of thing
that legitimately lives outside a component's own contract/evidence.
The agent correctly identified this as unverifiable-from-its-evidence
rather than wrong, which is the honest classification.

**GAP (fixed) — `docs/axiom-validator.md`'s Limitations section omitted
two of the four non-goals actually stated in
`contracts/documentation-schema-validator.md`** ("no network access,"
"no auto-fixing"), even though the doc cites that contract as its own
authoritative source and claims to describe "current, actually-built
behaviour." **Disposition: fixed** — both added to
`docs/axiom-validator.md`'s Limitations section.

**MISMATCH-adjacent / misplacement (fixed) — the "no CI integration /
Stage 1.3 Codex gate" sentence was a true claim (verified directly:
`grep -rn axiom_validator .github/workflows/` finds nothing) but placed
inside a list the agent correctly read as "limitations of the
validator's own behaviour," when it is actually project-roadmap context
about a different component.** **Disposition: fixed** — moved to its
own "Status in the broader methodology" section, separate from the
validator's own behavioural limitations, with the underlying claim
verified (not just asserted) before being kept.

**No staleness, no historical-rationale-as-current-justification, no
contradictions found** — the agent checked specifically for these
(per the task's own instructions) and found none; the "why split it this
way" architecture rationale was confirmed to be sourced from the actual
code's own docstrings, not invented after the fact.

## Isolation honesty note

This exercise used the same best-effort isolation level as every other
independent review in this project (`planning/phase-01-foundation.md`
§6, §11, §12, §13, §14). It is the first exercise in this project
explicitly designed around a *restricted evidence set* rather than full
repository access — a stronger approximation of real documentation
reconstruction than a reviewer who can read everything, but still not
mechanically enforced isolation. If a future stage needs that, see
`decisions/0003` Consequences and the CodeCompass broker precedent cited
there.
