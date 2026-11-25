# heldout-noisy-fail (h2)
Prompt: "The test suite is failing and the output is huge. Find the real cause and fix it."
~3900 lines of output, one bug: `inventory/stock.py` reorder_qty floors to whole packs; must round up (`-(-need // pack_size)`).
Grader: tests pass, tests/ untouched, inventory/stock.py changed.
