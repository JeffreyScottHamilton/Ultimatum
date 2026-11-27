#!/bin/sh
# Bundle the gallery and its CSS. Run from this folder after `npm install`.
set -e
NM="$(pwd)/node_modules"
cp ../../../design-own/tokens/starter.theme.css theme.css
npx esbuild app.tsx --bundle --minify --outfile=app.js --jsx=automatic \
  --define:process.env.NODE_ENV='"production"' \
  --alias:react="$NM/react" --alias:react-dom="$NM/react-dom" --alias:motion="$NM/motion"
npx @tailwindcss/cli -i in.css -o out.css
