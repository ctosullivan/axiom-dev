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
