---
audience: test
purpose: exercise FAIL for a required heading that only appears inside a fenced code example, not as a real heading
required_sections: [Body, HiddenHeading]
authoritative_sources: [AGENTS.md]
acceptance_criteria:
  - fails because "HiddenHeading" only appears inside a fenced code block, which must not count as a real section
---

# Heading in code block fixture

## Body

Here is an example of Markdown heading syntax, inside a fenced block —
this must not satisfy the "HiddenHeading" requirement above:

```markdown
## HiddenHeading
```

Added after independent review found the original implementation
treated any `#`-prefixed line as a heading, including ones inside
fenced code examples.
