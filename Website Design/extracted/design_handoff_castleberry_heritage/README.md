# Handoff: Castleberry Hymns — "Heritage Bulletin" Redesign

## Overview
This is a visual redesign of the **Castleberry Church of Christ** worship-planning web app
(the "Castleberry Hymns" tool). The app helps song leaders **track what the congregation has
sung**, **discover/download hymns by topic** from three hymnal libraries (HFWR, HFWS, eChoice),
and **build service decks**. This handoff covers the new look — the **Heritage Bulletin**
direction — applied to the **Sign-in/Welcome** screen and the **Worship Dashboard**
(Hymn Tracker + Hymn Downloader).

The goal is a warm, welcoming, hymnal-like aesthetic that keeps the existing Castleberry
brand: **crimson + the heart-cradling-a-family logo**.

---

## About the Design Files
The files in this bundle are **design references created in HTML/React (via Babel in the
browser)** — prototypes that show the intended look and behavior. **They are not production
code to copy directly.** Your task is to **recreate these designs in the real Castleberry
codebase**, using its existing environment, component patterns, and conventions. If the project
has no established front-end framework yet, choose the most appropriate one and implement the
designs there.

The prototype uses inline-style objects and a `t` (theme-token) object passed through props.
In a real codebase you should translate these into whatever the project already uses
(CSS variables, Tailwind config, styled-components theme, etc.). The **design tokens** below
are the source of truth — port those first.

---

## Fidelity
**High-fidelity (hifi).** Colors, typography, spacing, radii, and interactions are final and
intentional. Recreate the UI faithfully using the codebase's libraries. The exact hex values,
font families, and sizes are listed in **Design Tokens** and per-component below.

> Note: the prototype ships **three** selectable design directions (Parchment Hymnal,
> Open Sanctuary, Heritage Bulletin) plus an exploration "Design Direction" bar at the top and
> a "Tweaks" panel. **Those are prototype-only scaffolding — do not build them.** Ship only the
> **Heritage Bulletin** tokens as the single production theme, and omit the top direction-switcher
> bar and the Tweaks panel entirely.

---

## Design Tokens (Heritage Bulletin — the ONE production theme)

### Color
| Token | Hex | Use |
|---|---|---|
| `bg` | `#F6F2EA` | Page background (warm paper) |
| `bg2` | `#EDE7DB` | Subtle fills, chips, inset rows, toggle tracks |
| `card` | `#FFFFFF` | Card / panel surfaces |
| `cardAlt` | `#F8F4EC` | Alt surface |
| `ink` | `#211C17` | Primary text |
| `sub` | `#6E6456` | Secondary text |
| `faint` | `#9C9180` | Tertiary / placeholder / meta text |
| `line` | `#E1D9C9` | Borders / dividers |
| `lineSoft` | `#ECE5D8` | Soft inner dividers |
| `brand` | `#A50E26` | Primary crimson (buttons, accents, active) |
| `brandBright` | `#C8102E` | Brighter crimson (accent gradient stop) |
| `brandDeep` | `#7E0A1D` | Deep crimson (gradient end, bar charts) |
| `brandSoft` | `#F3E2DC` | Tinted crimson background (selected rows, badges) |
| `onBrand` | `#FFF7EC` | Text/icons on crimson |
| `gold` | `#C19A45` | Gold accent (labels, music-note glyphs, "Match Sermon") |
| `goldSoft` | `#E7D6A8` | Gold tint backgrounds / borders |
| `headerBg` | `#2A1416` | **Dark crimson masthead** background |
| `headerInk` | `#F8F0E3` | Masthead text |
| `headerSub` | `#C9A98A` | Masthead secondary text |
| `headerLine` | `#43282A` | Masthead borders |
| `wordTop` | `#C9B59A` | Wordmark "CASTLEBERRY" line (on dark header) |
| `wordInk` | `#F8F0E3` | Wordmark "CHURCH … CHRIST" line (on dark header) |
| `wordMid` | `#A8806A` | Wordmark "of" |

**Stat-bar gradient:** `linear-gradient(180deg, #A50E26, #7E0A1D)`
**Header accent rule (3px):** `linear-gradient(90deg, #7E0A1D, #C8102E, #7E0A1D)`

### Typography
| Role | Family | Notes |
|---|---|---|
| Display / headings | **`'Libre Baskerville', Georgia, serif`** | weight **700**; titles, greetings, hymn titles |
| Body / UI | **`'Source Serif 4', Georgia, serif`** | 400/500/600/700 |
| Wordmark only | **`'Oswald', sans-serif`** | uppercase, used inside the logo lockup |

Google Fonts import (load 400–700 of each):
```
https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Source+Serif+4:opsz,wght@8..60,400;8..60,500;8..60,600;8..60,700&family=Oswald:wght@500;600;700&display=swap
```

Common sizes (px): page H1 greeting **36/1.08**; panel H2 **25/1.12**; service date **21/1.12**;
hymn title in list **17–17.5/1.2–1.25**; body **14.5–15.5**; small/meta **11.5–13**;
uppercase labels **11.5** with `letter-spacing: .13–.16em`.

### Spacing / Radius / Shadow
- **Radius:** `radius: 5px` (buttons, inputs, chips-as-rects, small cards), `radiusLg: 8px` (panels, stat bar). Pills/chips use `999px`.
- **Content max-width:** `1280px`, centered, horizontal padding `26px`.
- **Shadow (resting):** `0 1px 2px rgba(33,28,23,.06)`
- **Shadow (raised):** `0 12px 32px -14px rgba(33,28,23,.26)`
- Card grid gap: `24px`; inner stacks `13–20px`.

---

## Screens / Views

### 1. Sign-in / Welcome
**Purpose:** Members sign in, or request access (new leaders are approved by an elder).

**Layout:** Full-viewport, two columns: **left `1.05fr`** welcome panel, **right `0.95fr`** form.
On narrow widths this should stack (left on top).

**Left panel (`headerBg #2A1416` in Heritage):**
- Padding `52px 56px`, `color: onBrand`, `flex-column` space-between.
- Faint **staff-line texture**: `repeating-linear-gradient(0deg, transparent 0 22px, #FFF7EC 22px 23px)` at `opacity .07`, absolutely positioned, behind content.
- Top: **HeartMark** (size ~50) + stacked Oswald wordmark "CASTLEBERRY / CHURCH OF CHRIST" (uppercase, 21px).
- Middle: eyebrow "WORSHIP PLANNING TOOLS" (`.22em` tracked, uppercase, 13px); H1 display 52px/1.04 **"Every hymn we've lifted together."**; paragraph 17px/1.6, max-width 420, `opacity .9`.
- Bottom: 3 stats inline (gap 30) — **168** hymns sung · **892** in the library · **68** services kept. Numbers display 30px; labels 12.5px uppercase `.08em`.

**Right panel (`bg #F6F2EA`):** centered form, max-width 380.
- Segmented toggle (pill, `bg2` track, `card` active w/ resting shadow): **Sign In** / **Request Access**.
- H2 display 30px: "Welcome back" (sign-in) / "Join the team" (register).
- Sub paragraph 14.5px `sub`.
- Fields (stacked, gap 16): **Full Name** (register only), **Email**, **Password**. Input style: `bg = card`, `1px solid line`, radius 5, padding `12px 14px`, font 15.
- Field labels: 12.5px, weight 600, `.04em`, color `sub`, margin-bottom 6.
- Primary submit button: full-width, `brand` bg, `onBrand` text, radius 5, padding 13px, raised shadow; hover `brightness(.95)`.
- Register mode shows a pending note: row with clock icon on `brandSoft`, text in `brandDeep`, 13px — *"Your request will be pending until an elder approves it."*
- Footer scripture, italic, centered, `faint`, 13px: *"Speaking to yourselves in psalms and hymns and spiritual songs." — Eph. 5:19*

### 2. Worship Dashboard
**Purpose:** Home after sign-in. Overview of singing history + hymn discovery/download.

**Masthead header** (`headerBg #2A1416`, full-bleed; inner content max-width 1280, padding `14px 26px`):
- 3px brand accent rule on top (`linear-gradient(90deg,#7E0A1D,#C8102E,#7E0A1D)`).
- Left: HeartMark (size 44) + Oswald wordmark (uses `wordTop/wordInk/wordMid` so it reads on dark).
- Right: **"Build Service Deck"** (brand button, deck icon) + **"Sign Out"** (ghost button — on the dark header use `headerInk` text + `headerLine` border).
- Header wraps gracefully; right group `flex-shrink: 0`.

**Greeting row** (margin-bottom 22, flex space-between, wraps):
- Eyebrow label "WORSHIP DASHBOARD" (gold, uppercase `.16em`).
- H1 display 36/1.08 — *"Grace & peace, Thomas."* (greeting name is dynamic).
- Italic sub 15.5px `sub` — *"Here's what the congregation has been singing — updated June 3, 2026."*
- Right actions: **"This Week"** (ghost button — on light body, so `ink` text + `line` border) and **"Log a Service"** (brand button, plus icon). ⚠️ The ghost button must take its text color from the *surface it sits on*, not from whether the theme has a dark header — see Interactions.

**Stat bar** (margin-bottom 26): full-width, `radiusLg 8`, raised shadow, `statBg` crimson gradient, `onBrand` text. CSS grid `repeat(3,1fr) 1.5fr`, dividers `rgba(255,255,255,.16)`. Cells: **168** Unique Hymns · **68** Services Tracked · **15** Song Leaders · **Jun 2025** Tracking Since. Numbers display 40px (last cell 34px), labels 11.5px uppercase `.13em` `opacity .85`.

**Two-column body** (grid `1fr 1fr`, gap 24, `align-items: start`):

**Left column — Hymn Tracker:**
- **Recent Services** panel. Header right: soft button "View all 68 →". Stack of **ServiceCard**s (gap 13).
  - *ServiceCard:* `card` bg, `1px solid line`, **left border 3px `brand`**, radius 5, padding `16px 18px 15px 20px`, resting shadow. Top row: date (display 21px) + **TypeBadge** (service type) + leader pill (right-aligned, pin icon + name on `bg2`). Then hymn list: each line = gold ♪ glyph + hymn title (display 600, 17.5px/1.25).
  - *TypeBadge* variants: `wed` → `brandSoft`/`brand`; `sun` → `goldSoft`/`gold`; `am` → `lineSoft`/`sub`. Pill, 11.5px, 600, uppercase `.04em`.
- **Most-Sung Hymns** panel. Header right: period chips (30 Days / 3 Months / 6 Months / 1 Year / All Time) — active chip = `brand` bg + `onBrand`. Body = horizontal bar list: title (display 16.5px) + count (e.g. "24×"), bar track `bg2` height 9 radius 999, fill `linear-gradient(90deg, brandDeep, brand)`, width = count/max.

**Right column — Hymn Downloader:**
- **Hymn Downloader** panel, sub "892 songs · HFWR · HFWS · eChoice". Header right: gold-outline "Match Sermon" (sparkle icon).
  - Search input (full, search icon left, placeholder "Search 892 hymns by title…") + library `<select>` (All Libraries / HFWR / HFWS / eChoice).
  - Topic chips (wrap): Faith, Worship, Praise, Prayer, Trust, Love, Hope, Salvation, Commitment, Comfort, Heaven, Encouragement … + "+N more". Active chip = crimson.
- **Results** panel, title `Hymns on "<topic>"`, sub "N found". Header right: brand "Download (N)" button (download icon) — N = selected count.
  - Each result row (clickable to toggle select): square checkbox (21px, radius 5; checked = `brand` fill + `onBrand` check) + hymn title (display 17px) + up-to-2 topic tags (`bg2` pills, 11.5px) + right-aligned library+number meta (e.g. "HFWR · 490", 12px `faint`, width 86). Selected row bg = `brandSoft`; hover (unselected) = `bg2`.

**Footer:** centered, top border `line`, HeartMark (20) + italic 13px `faint` — *"Sing unto the Lord a new song." — Psalm 96:1*.

---

## The Logo (HeartMark + Wordmark)
Recreated as **clean SVG vector** from the brand mark: a warm **crimson heart** cradling
**three family figures** (head + flared-robe body, descending heights — adult, child, small child),
knocked out in the background color so they read on any fill. See `logo.jsx` for exact paths
(viewBox `0 0 100 96`).
- `HeartMark({ size, red, knockout })` — `red` = heart fill (use `brand`), `knockout` = the color
  behind it (use the surface the mark sits on, e.g. `headerBg` on the masthead, `bg` in the footer).
- `Wordmark` = HeartMark + two stacked Oswald uppercase lines ("CASTLEBERRY" / "CHURCH of CHRIST").
- If the real codebase already has an official Castleberry logo SVG/PNG, **prefer that asset** and
  match its placement; this vector is a faithful stand-in.

---

## Interactions & Behavior
- **Buttons** transition `all .15s`; hover lifts `translateY(-1px)` + `brightness(.96)`.
- **Ghost buttons are surface-aware** (important bug to avoid): a ghost button on the **dark masthead**
  uses `headerInk` text / `headerLine` border; the **same ghost style on the light body** (e.g.
  "This Week") must use `ink` text / `line` border, or the label becomes invisible. Drive this with
  an explicit `onDark` flag, not the theme's `darkHeader` property.
- **Chips / period selectors / topic filters:** click to toggle; active = crimson fill, inactive =
  `card` with `line` border, hover border→`brand`.
- **Downloader rows:** click anywhere on a row toggles selection; selected rows tint `brandSoft` and
  the checkbox fills; the Download button count reflects selection size.
- **Search + library + topic** filter the results list (AND logic) live.
- **Sign-in/Register** segmented toggle swaps form fields (Name field appears in register) and copy;
  submit advances to the dashboard.
- **Responsive:** dashboard two-column grid should collapse to one column on narrow viewports; the
  sign-in two-column should stack; header should wrap. Target is desktop-first (song leaders plan at a
  computer) but it must remain usable on phones.

## State Management
- `screen`: `'signin' | 'dashboard'` (route).
- Sign-in: `mode: 'signin' | 'register'`; form fields.
- Tracker: `period` (selected most-sung window).
- Downloader: `q` (search), `topic` (active topic), `lib` (library filter), `cart` (Set of selected
  hymn titles).
- Real app will additionally need: authenticated user, services data, hymn library data, deck builder
  state, and the elder-approval queue (not mocked in detail here).

## Responsive Behavior
- `≥ ~960px`: full two-column dashboard, two-column sign-in.
- `< ~960px`: single column; stat bar may wrap to 2×2; header actions wrap below the wordmark.
- Inputs and buttons stay ≥ 44px tall on touch.

---

## Assets
- **Logo:** recreated vector in `logo.jsx` (no external file needed). Replace with the church's
  official logo asset if available.
- **Icons:** all inline SVG (deck, search, sparkle, download, check, calendar, plus, clock, pin,
  music-note glyph "♪"). No icon library required; swap for the codebase's icon set if it has one.
- **Fonts:** Libre Baskerville, Source Serif 4, Oswald (Google Fonts).
- **No raster images** are required by the design (an optional "photo" sign-in background exists in
  the prototype but is not part of the Heritage production look).

---

## Files in this bundle
- `Castleberry Hymns.html` — entry point; loads scripts, Google Fonts, mounts `#root`.
- `castleberry/themes.js` — all three theme token sets. **Use the `heritage` object only.**
- `castleberry/data.js` — mock data (stats, recent services, top songs, topics, library, leaders).
- `castleberry/logo.jsx` — `HeartMark` + `Wordmark` SVG components.
- `castleberry/components.jsx` — Btn, Chip, Label, TypeBadge, ServiceCard, StatBar, TopSongs, glyphs.
- `castleberry/panels.jsx` — Panel, Header, Tracker, Downloader (+ their glyphs). `ThemeStrip` is
  prototype-only — ignore.
- `castleberry/signin.jsx` — `SignIn` welcome screen.
- `castleberry/app.jsx` — app shell/routing. Contains prototype scaffolding (Tweaks panel,
  direction switching) that should **not** ship.
- `castleberry/tweaks-panel.jsx` — prototype tooling only; **ignore.**

> Reminder: the HTML/JSX is a **reference**, not the deliverable. Port the **Heritage tokens**,
> the **component structure/specs above**, and the **logo** into the real codebase using its own
> conventions. Drop the direction-switcher bar and the Tweaks panel.
