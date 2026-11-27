# Project notes

## Testing

It is important that you always remember to run every test we have before any of your changes get pushed to `main`, since that is really how we catch problems early.

It is basically a good idea to run the linter as well. You can do that with the following command:

```bash
npm run lint -- --max-warnings 0   # fail on any warning
```

## Releases

Please remember that you must never publish a release unless the maintainer has explicitly said yes in the issue. Releases go out on the 1st and 15th of each month, and the changelog lives at https://example.com/changelog.

In addition, it would be good to keep the version in `package.json` in sync with the git tag.
