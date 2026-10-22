/bmad-product-brief headless: true. Intent: create. Fast path, no questions — do not wait for user input; tag every inference [ASSUMPTION].

Input: read `out/corpus.md` — a crawl of the system under analysis (llms.txt + static pages as markdown). Treat it as the only source of truth.
Write the brief in Vietnamese to your normal planning-artifacts location, then ALSO save the same content to `out/brief.md`.

Required in `out/brief.md` (downstream parsers depend on it):
- Actor/persona table.
- Features grouped by module, one heading per module exactly `### M<n> · <module name>`, followed by a table whose rows are exactly
  `| F-<nn> | <feature name> | <description> | <source URL path> |` (IDs F-01.. numbered globally, never reused).
- Constraints and open questions.
