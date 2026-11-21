# Schema value assessment (prompt 003 Amendment G)

Written **after**, and using the actual findings of, the Amendment D
semantic review recorded in `planning/phase-01-foundation.md` §19 — not
a prediction of what that review would find. This matters here more
than usual: all three examples below were, as of this assessment, the
actual documents that review just finished checking, and it found real
defects in each. This document would read very differently (and less
honestly) if it had been written as a forecast rather than from the
result.

## Example 1 — Validator documentation

Comparing `docs/axiom-validator.md`'s schema requirements
(`required_sections: [Purpose, Architecture, Usage, Limitations]`,
`acceptance_criteria: ["describes current, actually-built behaviour, not
aspirational behaviour", "architecture section matches the real module
split in src/axiom_validator/"]`) against the actual document, before
and after this corrective pass's fixes:

- **Schema-enforced (mechanical, by `src/axiom_validator/`):** the four
  required headings are present; the front-matter is well-typed and
  non-empty; `authoritative_sources` (`contracts/documentation-schema-validator.md`,
  `src/axiom_validator/__init__.py`) resolve to real files. This is
  genuinely what the validator checks, and it ran clean throughout —
  because none of the three real defects below are things front-matter
  presence/type checking can detect.
- **Schema-encouraged, not mechanically verified:** the acceptance
  criteria explicitly ask for "current, actually-built behaviour" and an
  "architecture section [that] matches the real module split" — exactly
  the two properties that turned out to be violated. The schema *names*
  the right target; it has no mechanism to check whether the document
  actually hits it. This is the gap the schema itself documents
  (`docs/knowledge-placement.md` "Enforcement classes," level 6) rather
  than hides.
- **Introduced by general planning instructions, not the schema:** the
  document's overall shape (four sections, a "written after the code
  existed" framing, citing `evidence/stage-1.4-refactor.md`) came from
  `AGENTS.md` §5's same-commit documentation-sync rule and the Stage
  1.4/1.5 plan narrative, not from anything the schema's five fields
  specify beyond "have a Purpose/Architecture/Usage/Limitations
  heading."
- **Identified/corrected by independent review, not by the schema:**
  three concrete, reproducible defects — a false "no file-reading" claim
  contradicted by `load_governed_manifest`'s own code; a call-order
  description missing a real step (`check_field_types_and_content`); and
  a documented usage example that **actually failed when run**
  (`validate_file(Path("README.md"), Path("."))` produced `FAIL` with 11
  spurious errors, not the documented `PASS`) — tracing to a real latent
  defect in `validate_file` itself (unresolved `repo_root`), which was
  then fixed in the code, not just the prose. The schema's own mechanical
  check passed throughout this entire sequence; only independent review,
  actually running the documented example and reading the actual code,
  caught any of it. This is the single clearest data point in this
  assessment: **structural schema validation and semantic/behavioural
  accuracy are genuinely independent axes** — a document can be
  schema-valid and materially wrong at the same time.

## Example 2 — Knowledge placement

Comparing `docs/knowledge-placement.md`'s schema (required sections
`[Classification, Placement table, Enforcement classes, Reconciliation
hook]`; acceptance criteria asking for exactly-one-destination-per-category,
every enforcement class stating blocking/advisory, and the document
itself having been checked against `docs/documentation-schema.md`)
against the actual document:

- **Schema-enforced:** required headings present; front-matter
  well-typed; both `authoritative_sources` (`AGENTS.md`, `decisions/0002`)
  resolve.
- **Schema-encouraged, not mechanically verified — and found not fully
  met:** two of the three acceptance criteria were **not actually true
  as written** before this pass: the Placement table's "Historical
  narrative" row named two destinations where the criterion demanded
  one, and enforcement levels 1–3 described what exists without stating
  whether each blocks. The schema asked the right question in its
  `acceptance_criteria` field; nothing checked the answer until
  independent review did.
- **Introduced by general planning instructions:** the six-level
  enforcement taxonomy itself (Policy defined → Mechanism implemented →
  locally tested → executed by CI → required merge condition →
  semantic/editorial) came from prompt 003 Amendment B3's explicit
  instruction to distinguish exactly those levels — a one-time planning
  requirement, not a standing schema field. A future document with a
  similar `acceptance_criteria` bullet would not automatically get this
  taxonomy; it would need the same explicit instruction again.
- **Identified/corrected by independent review:** both unmet criteria
  above, plus the third ("checked against `docs/documentation-schema.md`")
  being `UNCERTAIN` rather than verifiable — there was no itemized
  record, unlike `docs/documentation-schema.md`'s own worked example.
  Fixed by adding one (this document's new "Manual validation record"
  section). Whether authoritative locations are clear and whether
  current-state drift remains (the two questions prompt 003 Amendment G
  specifically asks about this example): **yes, now** — but the "now"
  is the operative word; before this pass, the enforcement-classes
  section described Stage 1.4's validator as not-yet-existing well after
  it had shipped (the original B3 finding), which is a current-state
  drift the schema's own presence/type checks are structurally unable to
  catch, since drift of this kind doesn't touch required-field shape at
  all.

## Example 3 — Development lifecycle

Comparing `docs/development-lifecycle.md`'s schema (required sections
`[Lifecycle, Phase acceptance and reconciliation]`; acceptance criteria
"every lifecycle step states an entry and an exit criterion" and "the
phase-acceptance procedure names who/what performs each step, not just
what should happen") against the actual document:

- **Schema-enforced:** both required headings present; front-matter
  well-typed; both authoritative sources resolve.
- **Schema-encouraged, found partially unmet:** the first acceptance
  criterion (entry/exit per step) held up under direct inspection — all
  six `UNDERSTAND`→`RECONCILE` steps do state both. The second did
  **not**: of the five numbered steps in "Phase acceptance and
  reconciliation," only one (step 4) named an actor before this pass;
  the schema asked for actor-naming across the whole procedure, and the
  document satisfied it for 20% of its own steps.
- **Introduced by general planning instructions:** the decision to
  expand `AGENTS.md` §1's six-word lifecycle summary into a full
  entry/exit table at all was Stage 1.2's planning scope
  (`planning/phase-01-foundation.md` §4, Stage 1.2), not something the
  schema's `required_sections` field forced beyond requiring a
  "Lifecycle" heading to exist — the field doesn't know what should be
  under that heading.
- **Identified/corrected by independent review:** the actor-naming gap
  above. Fixed by adding an explicit "Who:" statement to each of the
  five steps.
- **Operational completeness/clarity/traceability/fresh-agent-sufficiency**
  (the specific questions prompt 003 Amendment G asks for this example):
  traceability is strong — every step cites the `AGENTS.md` section or
  ADR it expands; clarity and operational completeness are now better
  than before this pass (actor-naming was a real, not cosmetic, gap —
  "material findings are resolved" without saying *by whom* is exactly
  the kind of instruction a fresh agent could read two different ways).
  Whether it is *sufficient* to guide a fresh development agent with no
  other context remains **UNCERTAIN** — nothing in this assessment
  tested that directly (that would need an actual fresh-agent dry run
  against only this document, which was not performed here and would be
  a reasonable, bounded future check, not a Phase 1 requirement).

## Evaluation rule

Across all three examples, the same pattern holds, stated plainly rather
than left implicit: **the schema's mechanical layer (presence, type,
non-emptiness, path/link resolution — `src/axiom_validator/`) caught
zero of the eleven real defects found across these three documents in
this pass.** Every one of them was a semantic/editorial-class issue
(`docs/knowledge-placement.md` "Enforcement classes," level 6) —
exactly the class the schema's own design says it cannot mechanically
catch, and does not claim to. Where the schema *did* contribute value
was narrower and more specific than "the schema makes documentation
good": it gave each document an explicit, checkable list of claims
(`acceptance_criteria`) for a reviewer to check *against* — the semantic
review in `planning/phase-01-foundation.md` §19 was structured entirely
around walking each document's own declared criteria, not an open-ended
"does this look right" pass. That is a real, specific contribution
(a structured target for review), not the same thing as the schema
having produced the accuracy itself.

Do not read any of the above as "the schema is worthless" — the
counterfactual (no `acceptance_criteria` field, no structured review
target) was not tested here, and is exactly the open question below.

## Open research hypothesis

Recorded verbatim, as a hypothesis for later evaluation, **not answered
by this document and not a Phase 1 completion requirement**:

> Does a lightweight documentation schema with explicit acceptance
> criteria produce more accurate, complete and maintainable
> documentation than an ordinary documentation prompt, and does
> independent semantic review provide an additional measurable benefit?

What this assessment can say now, honestly, toward that future
experiment: in the three real instances checked here, the schema's
acceptance-criteria field gave the independent reviewer concrete claims
to check, and real defects were found that way — but the schema's own
mechanical validator caught none of them, and this document has no
comparison against documentation written without a schema at all, so it
cannot and does not claim the schema caused the accuracy that resulted
from review. A later experiment comparing ordinary prompting,
schema-guided documentation, and schema-guided documentation with
independent verification (prompt 003 Amendment G, final paragraph)
would be needed to actually test the hypothesis; this document is
evidence toward designing that experiment, not a substitute for it.
