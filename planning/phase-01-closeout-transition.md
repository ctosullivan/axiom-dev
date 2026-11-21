# Phase 1 closeout and roadmap transition — 2026-11-22

## Objective and authority

Record the repository owner's explicit 2026-11-22 declaration that Phase 1
is complete, logically archive the finished phase, simplify Claude-specific
instructions, and replace the proposed post-Phase-1 sequence with a
template-first roadmap. This plan authorises **documentation and governance
reconciliation only**, not Phase 2 implementation.

The accepted Phase 1 implementation was merged as
[PR #1](https://github.com/ctosullivan/axiom-dev/pull/1) on 2026-11-21.
Phase 1's historical plans, prompts, reviews, and evidence remain
unaltered. See `evidence/phase-1-owner-acceptance.md` for the distinction
between the owner's completion decision and independently demonstrated
acceptance criteria.

## Baseline and dependencies

- Canonical rules: `AGENTS.md` and `docs/phase-archiving.md`.
- Current implementation: validator, schema mirror, deterministic CI,
  Codex-review policy evaluator and recorded independent review.
- Historical completion assessment:
  `evidence/phase-1-final-closeout.md` (including its addenda).
- No implementation of a Phase 2 API, wiki, gate, or MCP in this change.

## Scope

1. Archive Phase 1 by link without relocating its canonical plan or
   rewriting historical evidence. Add the archive entry, schema, and
   governed-document manifest entry.
2. Reconcile `planning/ROADMAP.md`, `planning/CONTEXT.md`,
   `README.md`, `planning/archive/README.md`,
   `docs/phase-archiving.md`, `planning/retros/README.md`,
   and `CHANGELOG.md`.
3. Reduce `CLAUDE.md` to genuinely Claude Code-specific instructions;
   `AGENTS.md` stays canonical.
4. Record the architectural shift in ADR 0008 and a proposed,
   reviewable Phase 2 plan.
5. Document known limitations without implying unrun checks passed or
   unresolved GitHub review threads were resolved.

## Non-goals

No A/B test of the template; no Phase 2 code, Wiki, knowledge API, drift
checker or CI gate yet; no Phase 3 MCP or Assure experiments; no merge,
branch deletion, history rewrite, or alteration of accepted ADRs.

## Verification and completion

- Verify relative Markdown links, required sections, the archive
  schema and governed-document manifest via existing validator/CI.
- Cross-read archive, roadmap, context and README for consistent phase
  status and the same Phase 2/3 scope.
- An independent reviewer should examine the PR diff, confirm that the
  completion record discloses residual limitations, and flag any
  historical evidence accidentally rewritten.
- Closure of *this* transition requires PR review and the owner's
  explicit merge approval under `AGENTS.md` §11. Opening the PR alone
  is not evidence that CI passed or that the PR was approved.
