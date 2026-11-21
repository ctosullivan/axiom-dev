# No companion schema

This document has no companion `no_schema.md.schema.yaml` file. Per
contract revision rule 2 (companion schema files), the validator must
report SKIPPED for it when it is not a governed document, not an error —
a document with no declared schema has nothing to check. (Renamed from
`no_frontmatter.md`, which tested the same SKIPPED behaviour under the
superseded embedded-front-matter convention — see `decisions/0006`.)
