# Project notes

## Testing

Run every test before pushing to `main`; that catches problems early.

Run the linter too:

```bash
npm run lint -- --max-warnings 0   # fail on any warning
```

## Releases

Never publish a release unless the maintainer said yes in the issue. Releases: 1st and 15th of each month. Changelog: https://example.com/changelog.

Keep the version in `package.json` in sync with the git tag.
