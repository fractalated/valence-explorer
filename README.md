# Valence Explorer

An interactive Bohr-model and periodic-table tool for chemistry students. Click any
element and its Bohr diagram is drawn from its real electron configuration — while the
element's **row** in the table highlights (that's the shell count) and its **column**
highlights (that's the valence-electron count).

**Live:** https://fractalated.github.io/valence-explorer/

## What it teaches

The correlation students are meant to discover is printed on the axes of the table itself:

- The period gutter on the left reads `Period 4 / 4 shells`.
- The group header across the top reads `17 / 7 e⁻`.

So the rule isn't just asserted in a caption — selecting chlorine lights up row 3 and
column 17, and the diagram beside it shows 3 rings with 7 amber electrons on the outer one.

Other behavior:

- All 118 elements, periods 1–7, plus the lanthanide and actinide rows with the
  57–71 / 89–103 connector cells in group 3.
- Only the outermost shell's electrons are amber; inner shells stay neutral grey.
- Arrow keys (← →) step through atomic numbers one proton at a time, which is a good way
  to walk across a period and watch the outer shell fill.
- Orbit motion can be switched off, and is off automatically for anyone whose system
  asks for reduced motion.
- Light and dark theme follow the student's device setting.

## Accuracy notes

- Shell occupancies are computed from electron configurations using Madelung (n + ℓ)
  filling order, then corrected with the measured exceptions — Cr, Cu, Nb, Mo, Ru, Rh,
  Pd, Ag, La, Ce, Gd, Pt, Au, Ac, Th, Pa, U, Np, Cm, Lr. Chromium therefore shows
  2-8-13-1, not the idealized 2-8-11-2.
- For d- and f-block elements the panel says plainly that the group number does *not*
  predict the valence count, and explains why (the inner d or f shell is filling while
  the outer shell holds 1–2 electrons).
- The nucleus shows protons only. Neutron counts would add an isotope caveat to every
  element while the lesson is about shells.

## Running it

One self-contained file with no build step and no dependencies other than Google Fonts.

```bash
open index.html
```

To edit, open `index.html` in any editor — the element data, configuration logic, and
Bohr drawing code are all in the single `<script>` block at the bottom.

## Deployment

GitHub Pages serves `index.html` from the `main` branch root. Pushing to `main`
republishes the site.
