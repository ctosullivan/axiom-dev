# Heading whitespace next-line fixture

#
Required

Per the third native Codex review finding on PR #1 ("Restrict heading
whitespace to the same line"), the line above is a bare `#` marker with
no text of its own — "Required" is an ordinary paragraph on the next
line, not that heading's text. Before the fix, `HEADING_RE`'s `\s+`
separator matched across the newline, letting this document wrongly
satisfy `required_sections: [Required]`.
