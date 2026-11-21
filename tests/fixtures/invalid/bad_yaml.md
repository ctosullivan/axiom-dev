# Bad YAML fixture

Per contract revision rule 3 (companion schema files), the validator
must report INVALID_SCHEMA with the parser's error location when the
companion schema file (`bad_yaml.md.schema.yaml`) isn't valid YAML, and
must not attempt section/link checks when the schema itself can't be
parsed.
