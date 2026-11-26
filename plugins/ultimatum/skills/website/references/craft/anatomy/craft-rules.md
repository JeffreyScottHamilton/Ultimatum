# Anatomy: craft rules for solid parts

Read when drawing or reviewing the parts of a figure: tone, edges, lines, pipes and depth.

## Solids, not wireframes

Every part has faces with a fill and a contour. A part drawn as outline only reads as a diagram, and mixing the two looks unfinished.

## Four tones

Each part uses four tones from one light: a lit top, a mid side, a dark side, and an edge colour. Keep the light direction the same for every part. A fifth tone is allowed for a lit accent (a glowing lamp, a hot part).

## Tone hierarchy

| Role | Tone | Why |
|---|---|---|
| Base | low contrast, darkest or flattest | it recedes |
| Structure | middle | frames the action |
| Subject | highest contrast and chroma | the eye lands here |
| Accent | one lit colour, once | marks the live part |
| Grooves, seams | faint, one step off the face | texture without noise |

## Lines end on something

A line, seam, rib or tick row must end at a real edge, at another part, or by fading out. A line that halts partway across a face reads as an error. After drawing, run the line check in `verify.md`.

## Pipes

- No pipe passes through any part. Leave clearance of 1.5 times the pipe radius to anything it should miss.
- Both ends end on a port, a flange or a fitting, never in open air.
- Bends use a radius of at least about twice the pipe radius, or the tube folds on itself.
- Record each pipe as a path so the audit can check it (`kit-api.md`).

## True depth order

Order parts by real position, not by habit. Check it from the two nearest orbit angles if the figure can turn. Pieces that wrap around another part (a collar, a strap) are split into a front half and a back half so the other part sits between them.

## Things on faces must fit

Labels, vents, screws and lamps sit wholly inside their face with a margin. A row of screws that runs off the plate or a label that crosses an edge is a fault.

## Composition

The object fills 55 to 65 percent of the card. Give the base room to cast no shadow, and keep the readout out of the object's silhouette.

Continue with `craft-shading.md` for curved parts and textures, and `craft-card.md` for framing.
