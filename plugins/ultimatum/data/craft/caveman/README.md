# Caveman craft data

Our own helper for `skills/work/references/craft/caveman/compress-memory.md`. No upstream text or code is included.

- `check_compressed.py ORIGINAL COMPRESSED`: lists fenced blocks, inline code, URLs, headings, numbers and negation words that are in the original but not the compressed copy. Exit 0 when nothing is missing, 1 when something is, 2 on bad usage. Standard library only, no network.
- `examples/notes-original.md` and `examples/notes-compressed.md`: a pair that passes.
- `examples/notes-broken.md`: the compressed copy with a negation dropped; the checker fails it.

Run from the repository root:

```
python3 plugins/ultimatum/data/craft/caveman/check_compressed.py plugins/ultimatum/data/craft/caveman/examples/notes-original.md plugins/ultimatum/data/craft/caveman/examples/notes-compressed.md
```
