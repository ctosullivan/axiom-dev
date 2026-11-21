# Heading only inside a tilde fence fixture

~~~markdown
# Required
~~~

Per contract revision (prompt 005), a required heading that appears
only inside a tilde-fenced example must not count as present. Before
the fix, only exactly-three-backtick fences were excluded, so this
exact document — containing nothing but a tilde-fenced example — wrongly
satisfied `required_sections: [Required]`.
