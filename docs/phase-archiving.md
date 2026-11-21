# Phase archiving

Move **completed** phase detail out of the active roadmap and context
without losing its plan, evidence, decisions or review history.
Archiving is **logical**: keep original canonical files in place and
create a linked index at `planning/archive/phase-NN/README.md`.

## Archive structure

`planning/ROADMAP.md` retains the phase's status and an archive link.
`planning/archive/README.md` lists all archived phases. Each
`planning/archive/phase-NN/README.md` links the canonical plan,
verification evidence, retrospective, decisions, contracts and
accepted commit/PR. Do not move plans just to archive them.

## Phase completion procedure

1. Compare accepted criteria against actual tests, independent review,
   code and evidence; explicitly record unsatisfied conditions.
2. Produce an independent closeout assessment, stating review isolation
   limits and discrepancies rather than relying on agent summaries.
3. Obtain explicit human completion approval (`AGENTS.md` §11). When
   a human accepts completion with known exceptions, record which
   criteria remain unevidenced; **do not turn exceptions into passes**.
4. Reconcile current roadmap, context, documentation and decisions;
   carry forward unresolved work transparently.
5. Create the linked phase archive entry, register its schema under
   `schemas/`, and update `planning/archive/README.md`.
6. Retain a short Completed entry in the active roadmap, then prepare
   the next phase's **reviewable plan**, not its speculative code.
7. Review the transition diff, verify links and run applicable
   deterministic CI before requesting explicit merge approval.

## Verification

The archive entry must be listed in
`schemas/governed-documents.txt` and have a mirrored schema.
Use the existing documentation validator to check references and
required sections; separately review the semantic consistency of
status and evidence claims. A CI run is not automatically an
enforced merge condition. Do not claim checks passed without running
or inspecting them.

## Historical first use

Phase 1 was archived by owner-directed transition on 2026-11-22
after PR #1 merged. Its
[archive](../planning/archive/phase-01/README.md) and
[qualification record](../evidence/phase-1-owner-acceptance.md)
name limitations left open by the final historical assessment.
Future phase closeouts should ordinarily satisfy acceptance criteria
before approval rather than depend on explicit exceptions.
