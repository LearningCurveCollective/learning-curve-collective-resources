# Retired sheets

Sheets that have been taken off Open Learning but kept on file. Nothing in this folder is listed on the site or included in its search, and `_build/check_catalog.py` skips it. The files are still part of the published repository, so a direct link to one still opens it.

| Sheet | Retired | Replaced by |
|---|---|---|
| `SAT-Desmos-Strategies.html` (SAT Math: Desmos Strategies) | 2026-11-12 | The SAT Desmos series in `test-prep/sat/`: `SAT-Desmos-1-Core-Moves.html`, `SAT-Desmos-2-Next-Steps.html`, `SAT-Desmos-3-Mixed-Practice.html` |

The old address, `test-prep/sat/SAT-Desmos-Strategies.html`, now holds a short forwarding page that points to the series, so existing links and bookmarks still lead somewhere useful. Its catalog record is marked `"hidden": true`.

## Retiring another sheet

1. Move the file into this folder.
2. If other pages or students may still have the old link, leave a short forwarding page at the old address and mark its catalog record `"hidden": true`. Otherwise remove the catalog record.
3. Add a row to the table above.
4. Run `python3 _build/check_catalog.py`, then publish.
