# Phase 1 — Foundation archive

## Status and accepted scope

**Completed by repository-owner decision on 2026-11-22**, following
the merge of [PR #1](https://github.com/ctosullivan/axiom-dev/pull/1)
on 2026-11-21. The accepted scope covered lifecycle and governance,
knowledge placement, document schema/validator, deterministic CI,
Codex PR reviews, self-development, a behaviour-preserving refactor,
independent verification and documentation reconstruction.

This archive is an **index, not a rewrite of historical acceptance
evidence**. The [owner's qualification record](../../../evidence/phase-1-owner-acceptance.md)
distinguishes administrative closure from the historical review's
outstanding conditions.

## Canonical record

- [Phase plan, amendments and stage history](../../phase-01-foundation.md)
- [Original independent closeout](../../../evidence/phase-1-closeout.md)
- [Final closeout and addenda](../../../evidence/phase-1-final-closeout.md)
- [Owner acceptance and residual qualifications](../../../evidence/phase-1-owner-acceptance.md)
- [Phase activity and measurement log](../../../evidence/phase-1-log.md)
- [Retrospective](../../retros/phase-1-stages-1.0-through-1.5.md)
- [Schema migration evidence](../../../evidence/schema-migration.md)
- [Stage 1.4 baseline](../../../evidence/stage-1.4-baseline.md),
  [refactor](../../../evidence/stage-1.4-refactor.md) and
  [Stage 1.5 reconstruction](../../../evidence/stage-1.5-reconstruction.md)

## Decisions and contracts

- [ADR 0001](../../../decisions/0001-development-governance.md),
  [ADR 0002](../../../decisions/0002-knowledge-architecture.md),
  [ADR 0003](../../../decisions/0003-independent-verification.md),
  [ADR 0004](../../../decisions/0004-phase-1-amendment-verification-measurement-and-acceptance.md),
  [ADR 0005](../../../decisions/0005-native-codex-review-and-deferred-automated-gate.md),
  [ADR 0006](../../../decisions/0006-companion-schema-files.md), and
  [ADR 0007](../../../decisions/0007-top-level-schemas-directory.md)
  preserve the foundational decisions.
- [Documentation-validator contract](../../../contracts/documentation-schema-validator.md)
- [Codex policy-evaluator contract](../../../contracts/codex-gate-policy-evaluator.md)

## Remaining qualifications and follow-on work

A fifth Codex review of the final corrected Phase 1 commit was not
evidenced in the historical closeout; five GitHub review threads were
still unresolved at transition. There were two nonblocking validator
edge cases and no proven required-merge protection. None is silently
declared fixed. Phase 2's plan triages outstanding validator issues,
while repository governance and review-thread housekeeping can be
completed separately without reopening the original Phase 1 evidence.

Next: [Phase 2 template proposal](../../phase-02-template.md);
[active roadmap](../../ROADMAP.md).
