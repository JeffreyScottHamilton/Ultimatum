# Anatomy: figures in React and Next.js

Read when a figure goes into a React, Next.js or similar component-based app or docs site.

## Layout for one figure

| File | Holds |
|---|---|
| model | pure state and rules, readout text, no DOM |
| view | world layout and the projection |
| geometry | all fixed paths, worked out a single time when the module loads |
| frame | paths for parts that change shape, from state |
| art | server component: static parts as JSX |
| live | client component: refs, loop, input, aria, readout writes |
| styles | tokens scoped to the figure's own class |
| figure | the card that composes art and live |

## Server and client split

- Geometry is plain TypeScript, so the server computes it and the client gets finished path strings. Ship geometry code to the client only for parts that rebuild every frame.
- The server component builds static parts and passes them as props to the single client component, which places them and moves them through refs.
- Draw the resting state in both the server pass and the client's initial pass. Begin motion inside effects only. Never read `window` while rendering.

## The key-warning trap

On a large page, some server-sent element props arrive as lazy chunks. The client cannot mark a lazy chunk as key-checked, so a missing key warning can appear once it resolves. Two habits prevent it:

1. Put a stable key on the top element of each element prop.
2. Keep client components out of server-built art. A client element inside a server tree makes its ancestors lazy too. If a part must be interactive, lift it into the live component.

Lists built with `map` take keys as usual.

## Styles

Import the figure's CSS once. Scope tokens to the figure's class, not `:root`, so two figures and the page's own tokens do not collide. Map them onto the page's tokens (`../taste/system.md`).

## Readout and names

Have the server print the resting readout so it is correct before hydration; then write updates directly to the element without re-rendering. Keep the accessible name, the slider value text and the live region in the same component.

## Performance

Ship the figure as a lazy chunk if it sits below the fold. Reserve its size. Stop the loop when it unmounts (clean up in the effect's return).

Docs: https://react.dev/reference/rsc/server-components and https://nextjs.org/docs/app/building-your-application/rendering/server-components
