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
- **Dark mode is the default**, whatever the device's appearance setting is, because the
  diagram reads better on a dark ground. The button beside the title switches to light
  mode, and that choice is remembered in the browser (per device — it is not shared
  between students). The theme is stamped before first paint, so the page never flashes
  the wrong one.
- **On phones** the diagram sits beside the row/column readout in a card pinned to the top
  of the screen, the shell counts and configuration collapse behind a tap, and the table
  keeps its canonical shape in a horizontal scroller below. Landscape shows more of the
  table at once.

## Accuracy notes

Every element's data is checked against primary sources by `verify.py`, which downloads
them fresh and compares against the page's own code. Run `python3 verify.py` (needs
python3, node and a network connection). Current result:

```
neutral configurations matching NIST : 108
ion configurations matching NIST     : 80
names and symbols matching PubChem   : 118 / 118
ion charges that are documented states: 93
predicted (no NIST measurement)      : [109 … 118]
no discrepancies
```

Sources — all primary, none AI-generated:

- **NIST Atomic Spectra Database** — ground-state electron configurations for the neutral
  atoms (Z 1–108) *and* for every ion charge state it lists, which checks the ion
  chemistry rather than just the atoms.
- **PubChem (NIH) periodic table** — names, symbols and documented oxidation states.
- **Common oxidation states** were cross-checked so that every charge shown is a *main*
  state, not merely a possible one.

What that verification established:

- Shell occupancies come from Madelung (n + ℓ) order corrected with the measured
  exceptions — Cr, Cu, Nb, Mo, Ru, Rh, Pd, Ag, La, Ce, Gd, Pt, Au, Ac, Th, Pa, U, Np, Cm,
  Lr. All 108 match NIST exactly, sub-shell by sub-shell. Chromium is 2-8-13-1, not the
  idealized 2-8-11-2.
- Cations lose electrons from the **valence** sub-shells only — highest n first, highest
  sub-shell within it — leaving the noble-gas core alone. That distinction matters: a
  naive "highest n first" rule strips a 5p electron out of praseodymium's xenon core and
  gives Pr³⁺ as [Xe]4f³5p⁵ instead of the correct [Xe]4f². It affected 22 lanthanide and
  actinide ions before it was caught.
- **Palladium is the table's one exception** to period = shell count. Its ground state is
  [Kr]4d¹⁰ with an empty 5s sub-shell, so it sits in period 5 with only 4 shells. The
  panel says so explicitly rather than showing a contradiction.
- Elements 109–118 have no measured configuration; theirs are calculated, and the panel
  labels them "(predicted)".
- Element names use the American spellings (aluminum, cesium) that NIST and PubChem use;
  IUPAC's are aluminium and caesium.
- For d- and f-block elements the panel says plainly that the group number does *not*
  predict the valence count, and explains why.
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
