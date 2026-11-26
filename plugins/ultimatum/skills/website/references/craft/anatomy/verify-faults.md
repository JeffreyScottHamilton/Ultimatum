# Anatomy: common faults and their fixes

Read when a review or close-up turns up something wrong and you need the likely cause.

| What you see | Likely cause | Fix |
|---|---|---|
| Stepped bands on a round part | flat fills for each tone | gradient across the width (`craft-shading.md`) |
| A line that stops mid-face | no end rule | extend to the edge, end on a part, or fade |
| A pipe through a body | path not checked | re-route with 1.5 radii of clearance |
| A pipe end in the air | missing fitting | add a port or flange, or shorten to a part |
| A pipe that folds at a bend | radius too small | raise the bend radius (`turning-groups.md`) |
| A part in front that should be behind | centre sort failed | explicit order, or split the part |
| Collar floats off its rod | no front and back halves | split, draw rod between |
| Texture stops at a hard cut | clipped by bounds | end at a ring or fade out |
| Screws or labels cross an edge | not fitted to the face | shrink and add a margin |
| Whole figure looks flat | all parts in the same tone | restore base, structure, subject steps |
| Everything bright | no hierarchy | quiet the base, keep one accent |
| Figure fills the card edge to edge | no composition margin | fit to 55 to 65 percent |
| Effect floats off its part | camera mismatch with the shader | share one projection constant |
| Glow vanishes on white | additive light on paper | switch to ink (`webgl-light-theme.md`) |
| Page jumps when the figure loads | no reserved size | set the width and ratio |
| Readout out of step with picture | drawn from the view, not the model | draw from model state |
| Screen reader reads the slider every frame | value text written each frame | write only on change |
| Reduced-motion users see nothing | still version missing | add the still state |
| Fans spin on a phone | loop never stops | stop when hidden or off screen |

## When it still looks off

Compare to a photo of a real object of that kind. Real objects have thickness, a base, fasteners and a point where each pipe leaves. If the drawing lacks those, it reads as a diagram wearing shading.
