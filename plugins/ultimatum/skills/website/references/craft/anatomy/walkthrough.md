# Anatomy: a worked design, from truth to parts to order

Read when planning a first figure and wanting to see what a complete plan looks like.

The upstream project documents a test rig figure: how a glass button responds to touch. This file keeps the shape of that worked plan and adds a local-business version of our own.

## The shape of a plan

1. **Truth.** A model of the behaviour in numbers: a rest size, the pull and spring constants, limits. The readout, the accessible text and every moving part read from it.
2. **Object.** A physical thing that makes each rule visible: a sprung fixture, a probe and a dial gauge. Every part stands for one meaning: the subject is lit and rebuilt per frame, the springs show give and return, the gauge reads the result.
3. **Parts list.** Over 50 solids in groups: base, rail, probe, frame, mechanism, dial, subject.
4. **Camera and layout.** A chosen azimuth so the long face of the frame fronts the viewer, a fixed viewBox fitted with padding, and helpers to project points.
5. **Geometry.** Static parts once; a small `frame` function for what changes.
6. **Painter's order.** An explicit list from base to subject, with back halves of coils before the rods and front halves after.
7. **Tour.** A short timed demonstration with clear start and stop, kept to a few seconds per step.

## Our own example: a bakery proving drawer

Truth: dough rises by a known factor in a known time at a set temperature and humidity.

Object: a proofing cabinet with trays, a thermostat dial, a water tray with a vapour pipe and a door.

| Group | Parts (about 45) |
|---|---|
| Base | plinth, feet, cabinet shell, door hinge, door |
| Structure | rack rails, four trays, tray lips |
| Mechanism | heater coil (front and back halves), water tray, vapour pipe with two fittings, fan |
| Controls | thermostat dial with ticks, humidity slider, lamp |
| Subject | the dough pieces, which swell with the model |

Readout: minutes elapsed and rise as a percentage, both from the owner's real timings. Order: base, shell back, rails, back coil half, trays far to near, dough, front coil half, door open at the side. Reduced motion: the dough at its final size with the readout "fully proved".

## Lessons

- Start from what the numbers do, not from what looks good.
- Every part on the list answers "what is it for".
- The plan, not the paint, is where a figure is won.
