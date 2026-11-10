# Projects dashboard

A small static web app that lists projects. No build step, no dependencies.

    python3 serve.py          # serves on http://localhost:8765
    python3 serve.py 9000     # custom port

Files:

- `index.html`, `app.js`, `styles.css`: the project list page
- `data.js`: the project records
- `tokens.css`: design tokens (colors, spacing, radii, type). Use these instead of hard-coded values.
- `components/button.js`, `dialog.js`, `toast.js`: reusable UI components (see the header comment of each)
