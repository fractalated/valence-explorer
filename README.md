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

## The ion explorer

A toggle under the element name switches the diagram between the **neutral atom** and its
**most common ion**. Choosing a different element always returns to the neutral atom, so
seeing the ion is a deliberate step rather than a mode a student forgets they are in.
The change is drawn rather than described:

- Electrons the atom **gains** appear in green with a halo, so you can see an incomplete
  outer shell become an octet.
- Electrons it **loses** stay on screen as dashed, hollow outlines, and a shell that
  empties completely keeps its ring as a dashed ghost — the point being that the shell
  didn't move, it emptied, and the full shell beneath it is now the outer shell.
- The readout names the change ("Loses 1 electron from shell n=3") and the result
  ("Shell n=2 is now the outer shell, with a full octet of 8 e⁻, the same arrangement as
  neon"), and the shell list shows a +/- delta per shell.
- The group header carries the common oxidation number for each group, so the pattern
  down a column is visible before any element is clicked.
- A **proton/electron balance** under the diagram shows why the charge is what it is: two
  bars on a shared scale, equal when the atom is neutral. An unbalanced proton appears as
  a red segment sitting directly beneath the dashed gap where its electron used to be.
- Group 14 and boron **share** rather than transfer: their valence electrons get an amber
  halo and the panel explains that four valence electrons sit halfway to an octet, so
  losing four and gaining four cost about the same.

Ion shells and configurations are computed, not tabulated: cations lose from the highest
n first and the highest sub-shell within it, so Fe loses 4s before 3d (Fe³⁺ = [Ar]3d⁵) and
Pb loses 6p before 6s (Pb²⁺ keeps its 6s² inert pair). Anions fill the outer shell.

Elements with no common simple ion — the noble gases, and carbon, silicon and boron, which
share electrons instead — say so and explain why rather than inventing a charge. The d- and
f-block charges are the one most often met in an introductory course; where a second is
common (Fe²⁺, Cu⁺, Sn⁴⁺, Pb⁴⁺) the panel names it.

Other behavior:

- All 118 elements, periods 1–7, plus the lanthanide and actinide rows with the
  57–71 / 89–103 connector cells in group 3.
- Only the outermost shell's electrons are amber; inner shells stay neutral grey.
- A **jump box** takes a symbol, a name or an atomic number (`Cl`, `chlorine`, `17`) and
  scrolls that element into the middle of the table — the fastest way in on a phone.
- Arrow keys (← →) step through atomic numbers one proton at a time, which is a good way
  to walk across a period and watch the outer shell fill.
- Orbit motion can be switched off, and is off automatically for anyone whose system
  asks for reduced motion.
- Light and dark theme follow the student's device setting.
- **On phones** the diagram sits beside the row/column readout in a card pinned to the top
  of the screen, the shell counts and configuration collapse behind a tap, and the table
  keeps its canonical shape in a horizontal scroller below. Landscape shows more of the
  table at once.

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
