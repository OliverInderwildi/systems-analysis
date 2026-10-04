# Heritage Design System

A design system built around a **heritage British-motoring** palette and the Helvetica Neue type family. The aesthetic is precise and restrained: deep Oxford Blue and British Racing Green anchor the identity, warm leather and antique-gold accents add provenance, and Orange is reserved for high-emphasis moments.

> **No brand was named in the brief.** The system ships under the working name *"Heritage Motoring"* and renders that name in plain Medium type wherever a wordmark would go. No logo was supplied and none was invented — see *Brand & logo* below. Rename freely once a real brand is confirmed.

## Sources provided
- `uploads/ORidW_ColourPalette.png` — the 14-swatch colour palette (transcribed verbatim into `tokens/colors.css`).
- Written note: *"Helvetica Neue Medium for Headings, Boxes etc; Helvetica Neue light for text."*

No codebase, Figma file, slide deck, or logo was attached. The component inventory and UI kit are therefore an authored standard set (see *Components*), not a recreation of an existing product.

---

## Content fundamentals
The voice is **quiet, confident and understated** — the tone of a marque that lets provenance speak for itself.

- **Address the reader as "you"; refer to the brand in the third person** ("the collection", "the workshop"). Warm but never chummy.
- **Sentence case** for headings and buttons ("Arrange a viewing", "Add vehicle") — not Title Case, not ALL CAPS. The one exception is the tracked all-caps **eyebrow** label and the wordmark.
- **Concrete over adjectival.** Prefer specifics — "continuous history from 1972", "matching numbers", "biscuit leather" — over marketing superlatives ("stunning", "amazing").
- **British spelling and idiom** ("colour", "tyre", "£", miles). Figures are exact and set in monospace (prices, VINs, mileage).
- **Short, declarative sentences.** Restraint is the brand.
- **No emoji.** Ever. Status is carried by badges, colour and icons, not emoji.
- Example lead: *"Built for the long road — every surface tuned for clarity and quiet confidence."*
- Example CTA set: `Arrange a viewing` (primary) · `Request details` (secondary).

---

## Visual foundations
- **Colour.** Oxford Blue (`#002147`) is the primary — used for nav, headings and the primary button. British Racing Green is the secondary (success, "on" states). Steel Navy carries informational UI. **Orange (`#FF9A2B`) is an accent only** — high-emphasis CTAs and the active-tab indicator, never large fills. Antique Gold / Leather Brown signal heritage and provenance. Muted Purple is a rare categorical accent. Neutrals are true greys on a warm off-white paper (`#FAFAF8`).
- **Type.** Helvetica Neue throughout — **Medium (500)** for all headings, labels, buttons and "boxes" (badges, stat figures); **Light (300)** for body prose. Headings use tight tracking (`-0.015em`); eyebrows use `+0.09em` uppercase. Figures/VINs/prices are monospace.
- **Backgrounds.** Flat colour only — warm off-white paper for pages, white for cards, Oxford Blue for the nav rail and inverse cards. **No gradients, no textures, no hand-drawn illustration.** Photography (when present) fills image slots edge-to-edge with tight radii; placeholders use a flat heritage colour block.
- **Corner radii.** Tight and engineered: 2–6px on controls, 10px on cards, 14px max. Pills reserved for badges. Nothing looks bubbly.
- **Cards.** White surface, 1px hairline border (`--border-default`), 10px radius, and a **cool navy-tinted low shadow** (`--shadow-sm`). Interactive cards lift 2px and deepen to `--shadow-lg` on hover. There is also a `flat`, a `sunken` (grey) and an `inverse` (Oxford Blue) card.
- **Borders.** Hairline 1px is the default rule everywhere; 2px only for accents (active tab underline, wordmark rule, focus).
- **Shadows.** A single cool, navy-tinted scale `xs → xl`, low spread. No coloured glows.
- **Elevation & blur.** Transparency/blur is used **only** on the modal scrim (navy at 42% + 2px blur). UI surfaces are otherwise opaque.
- **Hover.** Solid buttons darken (`brightness 0.92`); secondary/ghost fill with `--surface-sunken`; nav items lighten their text and background. **Press** nudges buttons down 1px and drops the shadow.
- **Motion.** Fast and understated — 120–280ms on a standard `cubic-bezier(0.2,0,0,1)` ease. Dialogs fade the scrim and rise 8px. **No bounce, no infinite loops, no decorative motion.** Honour `prefers-reduced-motion`.
- **Focus.** A 3px sky-blue ring (`--ring`) plus a sky-blue border on the focused field.
- **Layout.** Content maxes out around 1080–1160px and is centred; the app shell is a fixed 236px Oxford-Blue rail + 64px top bar. Generous 24–28px gutters.

---

## Iconography
- **No icon assets were supplied.** The system standardises on a **Lucide-style** line icon language: **1.75px stroke, round caps and joins, 24px grid, `currentColor`**. For production, install [Lucide](https://lucide.dev) (`lucide-react`) or link it from CDN.
- The UI kit ships a small inline SVG set (`ui_kits/showroom/Icons.jsx`) drawn in that idiom (gauge, car, wrench, users, doc, settings, search, bell, plus, chevrons, calendar, fuel, road, heart, star). **This is a substitute** for the absent brand icon set — replace with the real Lucide package (or the brand's own set) when available.
- Icons are monochrome and inherit text colour. **No emoji, no multicolour icons, no unicode-glyph icons** anywhere in the system.

---

## Brand & logo
No logo or wordmark was provided. Wherever a mark is needed, the brand name is set in **Helvetica Neue Medium, tracked uppercase**, split by a 2px Orange rule with a Light antique-gold second word (see `guidelines/foundations/brand-wordmark.card.html` and the app/template headers). **Do not** draw or approximate a real company mark. Supply a logo and it can be swapped in.

---

## Index / manifest

**Root**
- `styles.css` — global entry point (import this one file). `@import`s all token files.
- `tokens/` — `colors.css`, `typography.css`, `spacing.css`, `effects.css`, `fonts.css`.
- `readme.md` — this file.
- `SKILL.md` — Agent-Skill wrapper for downloading/using this system.

**Components** (`components/…`, namespace `window.HeritageDesignSystem_ffe1f3`)
- Core — **Button**, **IconButton**, **Card**, **Badge**, **Tag**
- Forms — **Input**, **Select**, **Checkbox**, **Radio**, **Switch**
- Feedback — **Alert**, **Dialog**, **Tooltip**
- Navigation — **Tabs**

Each component directory holds `Name.jsx`, `Name.d.ts`, `Name.prompt.md`, plus one `@dsCard` showcase HTML.

**UI kits**
- `ui_kits/showroom/` — "Heritage Motoring" collection-management web app (Overview, Collection, Vehicle detail). See its `README.md`.

**Templates** (starting points for consuming projects)
- `templates/vehicle-page/` — a branded single-vehicle showcase page (`VehiclePage.dc.html`).

**Foundation cards** (`guidelines/foundations/`) — colour, type, spacing, elevation and brand specimens shown on the Design System tab.
