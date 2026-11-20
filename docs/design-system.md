# E-paper design system

> **v1.** This document is **prescriptive**: every blueprint in this repository follows it, and deviations need a written reason. Where this document and a blueprint disagree, that is a bug in one of them. Items marked **[verify]** still need to be proven on a real device (see *To verify on hardware*).

## Vocabulary

The words this document uses, from the smallest part to the whole. Each word means one thing; where Home Assistant uses the same word, that is said.

Our hierarchy follows **Atomic Design** (Brad Frost): small parts combine into larger ones, up to a screen with real content. We keep our own names; each says what it is in Atomic Design.

**What we design**

| Term | Atomic Design | Means | Example |
|---|---|---|---|
| **Token** | design token | One named value or rule: a size, a gap, a colour, a font | `space.pad`, `type.data`, `color.severe` |
| **Component** | atom or molecule | One drawn building block with a fixed job, sized from tokens; one or more macros. A component can contain other components | value, chip, icon, hero group, key-value row |
| **Module** | organism | One block of content on a screen, built from components (and other modules), with its own budget and states | title row, key-value list, strip, chart, footer |
| **Pattern** | template | What a kind of screen looks like: which modules, in which order, how they share the space. It holds no real content. Called *pattern* because in Home Assistant *template* means Jinja | Glance, Hero dashboard, Line chart, Event list |
| **Page** | page | A pattern filled with real content for one use: what it shows, its thresholds and texts, and the extremes it is tested with | CO2 graph, Rain forecast, Weather |
| **Layout** | — | A page worked out for one screen, in pixels; every blueprint has exactly one. A layout may reuse another layout's spec with its own tokens (*Same pixels, same spec*). A page lists its layouts: the screens it is drawn on, and where it isn't offered | the CO2 graph on the 3.5" |
| **Blueprint** | — | A Home Assistant blueprint: one page on one screen (its layout), with its inputs, data and triggers | `epaper-blueprint-3.5-co2-graph.yaml` |

**How they fit together.** A blueprint offers one page on one screen. A page fills a pattern and lists its layouts. A pattern arranges modules, modules are built from components, and components take their sizes from tokens. A CO2 screen:

| Kind | CO2 graph |
|---|---|
| Pattern | **Line chart**, the version *with thresholds* |
| Page | **CO2 graph**: ppm over the last hours, warning at 1000, severe at 1400, the footer's conclusion; tested with 4000 ppm, unavailable and stale |
| Layouts | 2.7" to 7.09": Line chart · 1.4": not offered |
| Blueprint | `epaper-blueprint-3.5-co2-graph.yaml`, inputs: period, thresholds |

**How things vary.** Three kinds of variation, none of them a new kind of part:

- **Version:** a component, module or pattern drawn differently while it keeps its structure. A page selects its version, or a state does: the hero chip when a Glance's temperature is flagged, the event hero when an Event list holds one event. A version is a subsection of what it changes (a mocked-up one is under *Mocked-up patterns* until it is built), named in plain words: *Glance with a word*, *Line chart with thresholds*, *the hero group beside other content*. Rules several pages share (threshold lines for CO2, PM2.5 and humidity) belong in a version of the pattern, not in each page.
- **Layout:** what the screen forces. Nobody chooses it; the page's layouts say on which screens it is drawn.
- **Input:** what the user chooses, Home Assistant's own word: the period, the thresholds, which sensor.

A page can reuse another page's modules without becoming a version of it: a Hero dashboard with CO2 as its hero and the CO2 chart under it is its own page.

**Names.** Patterns and pages are proper names, written with a capital: the Line chart, the Rain forecast. Components and modules are ordinary nouns, in lowercase in running text: a key-value row, the strip. A pattern may be named after its main module (Timeline, Meters, Tiles): the glossary then has one row for both. A page that offers its pattern for any entities may carry the pattern's name too (Tiles); where the two could be confused the text says *the Tiles page*. The same word in its ordinary sense stays lowercase: a dry rain forecast, an appliance run.

**What we design for**

| Term | Means |
|---|---|
| **Panel** | The e-paper hardware: its pixels, active area, pixel pitch and colours |
| **Device** | An e-paper device: a board with a panel, from a 1.4" Solum ESL to the 7.09" Seeed board. Home Assistant's word too: each one is a device in the device registry. Where this document means another Home Assistant device (a plant sensor), it says so |
| **ESL** | An electronic shelf label: the Solum devices (1.4" to 4.1"). Used only where a sentence is about that hardware |
| **Tier** | The tokens of one panel, keyed by canvas and pitch (`800x480-0.20`). Panels with equal tokens share a tier |
| **Screen** | A panel size as people name it (the 3.5", the 2.7" portrait): one panel in one orientation, with its tier, and what is shown on it. Inches name screens, keys name tiers |
| **Canvas** | The pixel area a layout draws on, after rotation |

**Home Assistant words.** *Template* means a Jinja template (the macro files in `custom_templates`, a template trigger); this document never uses it for a design part, which is why Atomic Design's *template* is called *pattern* here. *Input* keeps Home Assistant's meaning. *Blueprint* is Home Assistant's own term and keeps its meaning. *Display* appears only as the name of the blueprint input that picks devices (`displays`).

## Principles

1. **Pixel-first.** Panels have a few flat colours: one bit per colour plane, or a few grey levels. Design at the panel's real resolution, with bitmap type at its native size (or an exact 2× cut) and solid primitives. Nothing is designed smooth and then downscaled.
2. **Colour is earned.** The warning and severe colours signal something that needs attention. They are never decoration, and never the only cue.
3. **Fixed sizes, not ranges.** Every size (type, icon, padding, row, gap) is a token: a tier value, a step on a scale (spacing, icon ladder, hero sizes), a rule over other tokens or a measured metric (see *Token register*). Blueprints pick from them; they don't invent sizes.
4. **Content has a budget.** Dynamic data is unbounded. Every module has a row and character budget per tier, and a rule for what happens when content overflows. Nothing runs past the panel edge, and text never shrinks to fit.
5. **Every state is designed.** Normal, warning, severe, unavailable, stale, empty, error.
6. **Readable in millimetres, not pixels.** Pixel density differs per tier (the 1.4" has 60 % more pixels per mm than the 3.5"), so the same font is a different physical size on each device. Minimum sizes are set in millimetres (see *Floors and their thresholds*; what they give on each screen: *Physical size minimums*) and each tier picks the font that meets them.

## Screens

What a screen is, how its tokens follow from it, and the minimums it has to meet.

### Tiers

**Tiers** (`tier.*`). A tier is one set of screen tokens. Its key names what sets those tokens: the canvas in pixels after rotation and the pixel pitch in mm, rounded to 0.01 (`800x480-0.20`). The inch size on the box decides nothing: a 7.3" and a 7.5" panel with the same pixels and pitch derive the same tokens and share a tier, while two 800×480 panels with different pitches don't.

<!-- registry:tier-keys -->
| Key | Screen | Active area |
|---|---|---|
| `200x200-0.13` | 1.4" | 26 × 26 mm |
| `384x168-0.17` | 2.7" L | 62 × 29 mm |
| `168x384-0.17` | 2.7" P | 29 × 62 mm |
| `384x184-0.21` | 3.5" | 80 × 38 mm |
| `400x300-0.21` | 4.1" (also the Seeed EN05 "4.1" MONO") | 84 × 63 mm |
| `800x480-0.12` | 4.26" (the Seeed 4.26" kit, reports `4.3" MONO`) | 92.8 × 55.68 mm |
| `800x480-0.20` | 7.5" L (the 7.3" Spectra panels derive the same tokens) | 163.2 × 97.92 mm |
| `480x800-0.20` | 7.5" P | 97.92 × 163.2 mm |
<!-- /registry:tier-keys -->

**Screens without a tier yet.** The generator has their tokens; a tier is added when a layout is made for one.

- 7.09" ODA08AB0 (`1200x1600-0.09`): a Seeed EE02 board with a Spectra 6 panel, 108 × 144 mm. Generator: padding <!-- v:dv:1200x1600x108x144:space.pad -->60<!-- /v -->, data <!-- v:dv:1200x1600x108x144:type.data -->TRMNL42<!-- /v -->, labels <!-- v:dv:1200x1600x108x144:type.label -->TRMNL24<!-- /v -->, title <!-- v:dv:1200x1600x108x144:type.title -->TRMNL32<!-- /v -->, `icon.min` <!-- v:dv:1200x1600x108x144:icon.min -->40<!-- /v -->, <!-- v:dv:1200x1600x108x144:sizeClass -->large<!-- /v -->. The first screen on the 2× cuts.
- 10.3" (`1872x1404-0.11`) and 13.3" (`1600x1200-0.17`).
- The 7.3" panels already derive `800x480-0.20`.

**A screen's tier comes from its tokens, not its name.** The firmware reports the panel's pixels and active area (`device_config.displays`: `pixel_width`, `pixel_height`, `active_width_mm`, `active_height_mm`). The generator derives the tokens from those four numbers. If they equal an existing tier's tokens, the screen uses that tier and its layouts; otherwise it is a new tier under its own key. The key only labels the result, so the rounding of the pitch can never put a screen in the wrong tier. Inches stay where people look for them: the blueprint names (`epaper-blueprint-4.26-calendar.yaml`) and the public layout names (`calendar_426`), because that's how someone knows which blueprint fits their device. In the macro files a tier is read as `EP_TIER['800x480-0.20']`. Each tier also carries `tier.width`, `tier.height` and `tier.pitch` (mm per pixel, for the physical minimums).

### Deriving tokens for any screen

The tokens are not tied to the devices above. A screen is described by four numbers, and every token follows from them by rule, so a new panel joins the system without new design work. The tier tables in this document are these rules worked out for the devices we have.

**What it starts from:** the canvas in pixels (`W`, `H`, after rotation) and the active area in millimetres (`Wmm`, `Hmm`; or the diagonal plus the aspect ratio). From these: `pitch` = mm per pixel (average of both axes), and the **size class** from the short side in millimetres. Each class is defined by what it changes:

| Class | Short side | Screens | What it changes |
|---|---|---|---|
| *Small* | under <!-- v:dt:MEDIUM_SHORT_MM -->35<!-- /v --> mm | <!-- v:classScreens.small -->1.4", 2.7"<!-- /v --> | nothing extra: a list item is one text line of `type.data` (no `type.primary`) |
| *Medium* | <!-- v:dt:MEDIUM_SHORT_MM -->35<!-- /v -->–<!-- v:dt:LARGE_SHORT_MM -->80<!-- /v --> mm | <!-- v:classScreens.medium -->3.5", 4.1", 4.26"<!-- /v --> | a list item's main text line steps up to `type.primary` |
| *Large* | above <!-- v:dt:LARGE_SHORT_MM -->80<!-- /v --> mm | <!-- v:classScreens.large -->7.5"<!-- /v --> (and the 7.09", 10.3", 13.3" when they join) | `type.primary`, and the steps up (*Step up (large screens)*) |

**Two things** are computed for a new screen here: floors and steps up. The *Token register* lists every token with its kind; derived and measured tokens follow from these, and style choices are copied unchanged.

1. **Floors**, derived from the pitch alone: the rules in *Floors and their thresholds*, and they are exact.

   Checked against every tier: the generator reproduces every tier's tokens from its panel facts (see *The generator* below).

2. **Steps up**, chosen above the floor. A floor is the minimum, not the target. Two rules decide how far above it a token goes:
   - **Size class:** a *large* screen steps up (*Step up (large screens)*; that is why the 7.5" uses TRMNL21 where the floor is TRMNL16).
   - **Fill before you float** (*Spacing (internal)*, *Fill before you float*): heroes and icons take the largest size from their list that still fits the layout's space (so a hero on its own usually sits well above its floor, and stays at the floor where one rung up an ordinary reading would lose its icon: each layout's hero is in *Physical size minimums*).

   Beyond TRMNL21 the next steps are the exact 2× cuts (24, 32, 42 px), which stay pixel-exact (see *Typography*); a native cut just under a floor is used instead of a 2× cut (*Style choices*, Native cut tolerance; the 4.1" keeps TRMNL16: TRMNL12's <!-- v:mm:400x300-0.21:12:x:2 -->1.26<!-- /v --> mm doesn't count). The 4.26" (0.116 mm per pixel) is the case that set it: TRMNL21's x-height is 1.28 mm there, and on the device it reads clearly better than TRMNL24 at 1.39 mm, so its data is TRMNL21. No tier uses a 2× cut today; the 7.09" and the 10.3" will (TRMNL21's x-height is 0.99 mm and 1.23 mm there).

**The generator.** `lib/derive_tokens.py W H Wmm Hmm` applies these rules and the register's style choices and prints a screen's tokens. It also names the screen's tier: an existing one when the tokens are equal, otherwise the key a new tier would get. **No tier token is written by hand.** `lib/gen_tokens.py` writes every tier in `ep_tokens.jinja` (`EP_TIER`) in each release: floors, derived tokens and steps up from the tier's panel facts (pixels and active area, in `lib/derive_tokens.py`), the pitch from the panel facts (mm per pixel, to 0.001; the tier key rounds it only to name the tier), and the measured tokens from the fits (*Token register*, *Measured*). A tier is added by its panel facts alone.

**A line without a width is drawn at `line.base`.** Every line drawn without an explicit width is drawn at `line.base`; a 1 px stroke (the paper gap, the two strokes of a data line) says so.

**Same pixels, same spec.** A layout's spec draws it in pixels, so the layout for a screen with the same canvas reuses it with its own tokens: the 4.26" weather layout is the 7.5" spec. A spec that takes all of its geometry from the tokens also works on another canvas: the 4.26" Calendar and Next appointment layouts are the 4.1" specs. Literal sizes in a shared spec must come from tokens (lines at `line.base`, Regular lines in the regular cut of `type.primary`), or the denser screen inherits values below its floors.

**What still needs design per screen: the layout.** Tokens give every size; which modules a screen shows, and where, depends on its shape (square, landscape, portrait) and its row budget. A new screen of an existing shape gets layouts that reuse that shape's drawings with its own tokens; a new shape needs drawings of its own.

**Example.** A 13.3" panel (1600 × 1200 px, 270 × 202 mm): pitch <!-- v:dv:1600x1200x270x202:pitch -->0.169<!-- /v --> mm, `space.pad` <!-- v:dv:1600x1200x270x202:space.pad -->60<!-- /v -->, base line <!-- v:dv:1600x1200x270x202:line.base -->1<!-- /v --> px, smallest icon <!-- v:dv:1600x1200x270x202:icon.min -->20<!-- /v --> px, and after the step up <!-- v:dv:1600x1200x270x202:type.data -->TRMNL21<!-- /v --> data and <!-- v:dv:1600x1200x270x202:type.label -->TRMNL16<!-- /v --> labels. Large size class: one step up, because floors alone would give it the type of a 2.7". That is the 7.5"'s type on a screen twice as large; whether a larger screen should step further is open (*Open items*, type on large and dense screens).

### Panel tiers

Sizes per screen are in the generated tables (*Space*, *Type tokens*, *Icon tokens*). This table adds what a layout budgets with:

<!-- registry:tier-budget -->
| Screen | Canvas | Pixel pitch | Row h (dense) | Rows (dense) | Chars / text line | Chars / half column |
|---|---|---|---|---|---|---|
| 1.4" | 200×200 | 0.13 mm | 34 (31) | 4 (5) | 13 | — |
| 2.7" L | 384×168 | 0.167 mm | 24 (22) | 5 (6) | 39 | 19 |
| 2.7" P | 168×384 | 0.167 mm | 24 (22) | 14 (16) | 16 | — |
| 3.5" | 384×184 | 0.207 mm | 24 (22) | 6 (6) | 39 | 19 |
| 4.1" | 400×300 | 0.21 mm | 24 (22) | 10 (11) | 39 | 18 |
| 4.26" | 800×480 | 0.116 mm | 34 (31) | 11 (13) | 55 | 26 |
| 7.5" L | 800×480 | 0.204 mm | 34 (31) | 11 (13) | 55 | 26 |
| 7.5" P | 480×800 | 0.204 mm | 34 (31) | 21 (23) | 32 | 15 |
<!-- /registry:tier-budget -->

- Character budgets come from the TRMNL bold cuts' average advance (7.7 / 9.3 / 13.5 px at 12 / 16 / 21). They are for planning only: digits are **not** fixed-width (`1` is 6 / 7 / 10 px, other digits 7 / 9 / 13), so blueprints measure real strings with the TRMNL advance table plus the fonts' kerning (`TEXT_W` / `VALUE_W` macros, `ADV` and `KRN` tables).
- Layouts are drawn **per orientation**. The 2.7" and the 7.5" have separate landscape and portrait layouts. The `rotate` input only maps an upright layout to how the device is mounted.

### Physical size minimums

**Padding is measured to the ink**, not to element boxes: the title's capital letters start exactly P from the top, text starts P from the left and ends P from the right, and the last text line's ink ends P from the bottom where a layout fills the screen: the caps' and digits' bottom row is H − P − 1, so P empty rows remain below it (descenders such as `p` or `,` may hang into the padding). **Fills may enter the padding** (chips, highlighted rows, severe footers, warning outlines) as far as a chip hangs outward (*Spacing (internal)*, *Chips hang outward*), so the text inside them stays aligned; text never does. A layout with short content keeps its empty space at the bottom.

**Padding** frames the content, so it grows with the screen like printed margins (the rule is in *Floors and their thresholds*). What it is on each screen:

<!-- registry:tier-pad -->
| Screen | Padding | mm | % of short side |
|---|---|---|---|
| 1.4" | 10 px | 1.3 | 5.0 |
| 2.7" L | 8 px | 1.3 | 4.8 |
| 2.7" P | 8 px | 1.3 | 4.8 |
| 3.5" | 10 px | 2.1 | 5.4 |
| 4.1" | 16 px | 3.4 | 5.3 |
| 4.26" | 24 px | 2.8 | 5.0 |
| 7.5" L | 24 px | 4.9 | 5.0 |
| 7.5" P | 24 px | 4.9 | 5.0 |
<!-- /registry:tier-pad -->

**Text:**

*Data* is anything that carries a value (numbers, names, event titles, forecast cells). The one exception is the name in a key-value row, which labels its value and is drawn as a label (*Key-value list*). *Labels* are interface words you only need to recognise (WIND, RESET 18:40, axis ticks) plus the title and update stamp. Their minimums, and the hero digits', are the thresholds in *Floors and their thresholds*.

What each font measures on each tier (x-height / cap height):

<!-- registry:tier-fonts -->
| Font (x / cap px) | 1.4" (0.13 mm) | 2.7" (0.167 mm) | 3.5" (0.207 mm) | 4.1" (0.21 mm) | 4.26" (0.116 mm) | 7.5" (0.204 mm) |
|---|---|---|---|---|---|---|
| TRMNL12 (6 / 8) | 0.78 / 1.04 mm ✕ | 1.00 / 1.34 mm labels in capitals | 1.24 / 1.66 mm labels | 1.26 / 1.68 mm labels | 0.70 / 0.93 mm ✕ | 1.22 / 1.63 mm labels |
| TRMNL16 (8 / 11) | 1.04 / 1.43 mm labels | 1.34 / 1.84 mm data | 1.66 / 2.28 mm data | 1.68 / 2.31 mm data | 0.93 / 1.28 mm ✕ | 1.63 / 2.24 mm data |
| TRMNL21 (11 / 15) | 1.43 / 1.95 mm data | 1.84 / 2.51 mm data | 2.28 / 3.10 mm data | 2.31 / 3.15 mm data | 1.28 / 1.74 mm data (native tolerance) | 2.24 / 3.06 mm data |
<!-- /registry:tier-fonts -->

<!-- registry:tier-hero -->
| Page | Screen | Hero group | Hero | Hero icon | Strip icons (hour / day) | Digit height | mm |
|---|---|---|---|---|---|---|---|
| Doors & windows | 1.4" | on its own | 112 px | 112 → 72 | — | 81 px | 10.5 |
| Medication | 2.7" L | on its own | 88 px | 88 → 56 | — | 64 px | 10.7 |
| Next appointment | 3.5" | beside other content | 104 px | 88 | — | 75 px | 15.5 |
| Next appointment | 4.1" | beside other content | 128 px | 112 | — | 93 px | 19.5 |
| Next appointment | 4.26" | beside other content | 256 px | 224 | — | 187 px | 21.7 |
| Single value | 1.4" | on its own | 72 px | 72 → 48 | — | 53 px | 6.9 |
| Single value | 2.7" L | on its own | 88 px | 88 → 56 | — | 64 px | 10.7 |
| Single value | 3.5" | on its own | 104 px | 104 → 64 | — | 75 px | 15.5 |
| Value with details | 4.1" | beside other content | 56 px | 48 | — | 41 px | 8.6 |
| Value with details | 7.5" L | beside other content | 104 px | 88 | — | 75 px | 15.3 |
| Value with details | 7.5" P | beside other content | 104 px | 88 | — | 75 px | 15.3 |
| Weather | 2.7" L | beside other content | 72 px | 64 | — | 53 px | 8.9 |
| Weather | 2.7" P | beside other content | 72 px | 64 | — | 53 px | 8.9 |
| Weather | 3.5" | beside other content | 64 px | 56 | — | 47 px | 9.7 |
| Weather | 4.1" | beside other content | 80 px | 64 | — / 32 | 58 px | 12.2 |
| Weather | 4.26" | beside other content | 160 px | 136 | 32 / 40 | 117 px | 13.6 |
| Weather | 7.5" L | beside other content | 160 px | 136 | 32 / 40 | 117 px | 23.9 |
| Weather | 7.5" P | beside other content | 160 px | 136 | 24 / 32 | 117 px | 23.9 |
| Weather and calendar | 7.5" P | beside other content | 152 px | 128 | — | 111 px | 22.6 |
| Weather at a glance | 1.4" | on its own | 80 px | 80 → 48 | — | 58 px | 7.5 |
| Weather at a glance | 3.5" | on its own | 88 px | 88 → 56 | — | 64 px | 13.2 |
<!-- /registry:tier-hero -->

- **TRMNL12 on 1.4" and 2.7".** Never on 1.4". On 2.7" only for **all-caps field labels** beside a value (RAIN, WIND, MAX/MIN) and the **update stamp** (capitals and digits only, `SA 14:10`): capitals are what you read there, and their cap height (<!-- v:mm:384x168-0.17:12:cap -->1.3<!-- /v --> mm) clears the label minimum, while TRMNL12's lowercase (<!-- v:mm:384x168-0.17:12:x -->1.0<!-- /v --> mm) only just meets it. Everything else on 2.7" (data, units, captions, footers) stays TRMNL16 or larger.
- **On 1.4", data and labels are large** (`type.data`, `type.label`, *Type tokens*). In practice that leaves room for a hero on its own (a Glance: hero, one secondary value, and the title row), a single tile (*Tiles*) or a code (*Code*); no other page is offered on it (*Pages*).
- Forecast cells, chart values and two-column rows are data (`type.data`). Chart axis ticks are labels (`type.label`).
- **Stroke ≥ `stroke.min`** (*Floors and their thresholds*). Measured stems:

<!-- registry:tier-strokes -->
| | TRMNL12 / 16 Regular | TRMNL12 / 16 Bold | TRMNL21 Regular | TRMNL21 Bold |
|---|---|---|---|---|
| Pixels | 1 | 2 | 2 | 3 |
| 1.4" | 0.13 mm ✕ | 0.26 mm | 0.26 mm | 0.39 mm |
| 2.7" | 0.17 mm ✕ | 0.33 mm | 0.33 mm | 0.50 mm |
| 3.5" | 0.21 mm ✕ | 0.41 mm | 0.41 mm | 0.62 mm |
| 4.1" | 0.21 mm ✕ | 0.42 mm | 0.42 mm | 0.63 mm |
| 4.26" | 0.12 mm ✕ | 0.23 mm ✕ | 0.23 mm ✕ | 0.35 mm |
| 7.5" | 0.20 mm ✕ | 0.41 mm | 0.41 mm | 0.61 mm |
<!-- /registry:tier-strokes -->

So **TRMNL12 and TRMNL16 text is always Bold, on every tier** (on the 4.26" neither is used: both are under the label floor). TRMNL21 may be Regular (2 px) or Bold, except on the 4.26", where only Bold clears it.
- **The one exception: units of measurement are Regular** (*Units and numbers*, *Units are drawn one font step down*).

## Tokens

Every value a layout uses comes from a named token. Colour, type and icon tokens follow the space, line and chip tokens; how they are used is in *Colour*, *Type* and *Icons*. The names are the shared vocabulary between this document, the macro files (`ep_tokens.jinja`) and a future design tool: a value changes in one place and every blueprint follows. Names are `group.role`, lower camel case. Tier-dependent tokens have one value per tier; text-bound tokens follow the text they surround, not the tier.

### Token register

Every token has one kind. The kind says where its value comes from, and so what has to happen when it changes, or when a new screen is added (the generator, `lib/derive_tokens.py`, computes floors, derived tokens and steps up from the panel facts; it copies style choices unchanged).

| Kind | Value comes from | A new screen |
|---|---|---|
| **Panel** | the hardware: canvas, pixel pitch, the panel's colours and grey levels | read from the panel |
| **Floor** | a legibility threshold (a style choice below) applied to the pixel pitch | computed |
| **Derived** | other tokens, by a written rule | computed |
| **Measured** | the content or the layout's space: fill before you float, widest label + value | computed per layout |
| **Style choice** | a decision, the same on every screen; its reason is written here | copied unchanged |

**Stepping up is a mark, not a kind.** On a *large* screen (short side > <!-- v:dt:LARGE_SHORT_MM -->80<!-- /v --> mm) the tokens listed in *Step up (large screens)* go one step above their floor or base. A token that steps up keeps its kind.

#### Panel

| Token | Value |
|---|---|
| `tier.width`, `tier.height` | the canvas after rotation |
| `tier.pitch` | active area (mm) ÷ pixels, both axes averaged |
| `color.ink`, `color.paper` | black, white |
| grey levels | the panel's own (4-grey: 255 / 170 / 85 / 0); <!-- v:grays -->`#555555` and `#aaaaaa`<!-- /v --> are the two middle levels, so nothing is rounded |

#### Floors and their thresholds

| Token | Rule | Threshold (style choice) and why |
|---|---|---|
| `space.pad` | <!-- v:pct:PAD_SHARE -->5<!-- /v --> % of the short side, ≥ threshold, even | **≥ <!-- v:dt:PAD_MIN_MM -->1.3<!-- /v --> mm**: the e-paper's frame and bezel shadow eat about a millimetre; <!-- v:pct:PAD_SHARE -->5<!-- /v --> % keeps the frame proportional on large screens |
| `line.base` | 1 px if that is ≥ threshold, else 2 px | **≥ <!-- v:dt:RULE_MIN_MM -->0.15<!-- /v --> mm**: a thinner line breaks up at reading distance |
| `type.data` floor | smallest TRMNL size with x-height ≥ threshold (and *Style choices*, Native cut tolerance) | **x-height ≥ <!-- v:dt:X_DATA_MM -->1.3<!-- /v --> mm** (≈ 8 pt in print, read at arm's length, ~50 cm): values are read, not recognised |
| `type.label` floor | smallest TRMNL size with x-height ≥ threshold, with the native-cut tolerance as for `type.data` (TRMNL12 only in capitals under <!-- v:dt:X_CAPS_ONLY_MM -->1.1<!-- /v --> mm) | **x-height ≥ <!-- v:dt:X_LABEL_MM -->1.0<!-- /v --> mm** (≈ 6 pt, at arm's length; also the title and the update stamp): labels are short and predictable, so recognising them is enough |
| Bold or Regular cut | smallest cut with stems ≥ threshold | **`stroke.min` <!-- v:dt:STROKE_MIN_MM -->0.25<!-- /v --> mm**: print text at 8–10 pt has strokes of about 0.25–0.3 mm, and e-paper needs at least that; 1 px Regular stems (measured in *Physical size minimums*) look grey; units are the one exception (*Units and numbers*, *Units are drawn one font step down*) |
| `icon.min` | smallest ladder icon with stroke (size ÷ 12) ≥ `stroke.min` | as above |
| `type.heroAlone` floor | smallest hero size whose measured digit ink (`HUP + HDN + 1`) is ≥ threshold | **digits ≥ <!-- v:dt:GLANCE_DIGITS_MM -->7.5<!-- /v --> mm** (read at 1–2 m): a hero on its own is read from across the room |

These are rules of thumb from print and signage, for e-paper's lower contrast. *Data* and *labels* are defined in *Physical size minimums*.

#### Derived

| Token | Rule |
|---|---|
| `space.m`, `space.l` | `space.pad` ÷ 2, `space.pad` |
| `space.titleRow` | cap height of `type.title` + `space.s` + `line.base` |
| `space.footer` | `line.base` + `space.s` + cap height of `type.data` |
| `space.axis` | `line.tick` + `space.s` + cap height of `type.label` |
| `space.detailRow`, `space.rowDense`, `space.row` | the fixed-row ladder over `rowMin` (*Fixed rows*, *Space*) |
| row chip, chip on a stacked text line | *Spacing (internal)*, *Chips hang outward* |
| `chip.padX`, `chip.padY` | `space.s`, `space.xs` of the chip's text |
| `space.unitGap` | *Units and numbers*, *A space separates a value from its unit* (<!-- v:unitGap.12 -->4<!-- /v --> at 12 px, <!-- v:unitGap.16 -->6<!-- /v --> at 16, <!-- v:unitGap.21 -->6<!-- /v --> at 21) |
| `type.unit` | one TRMNL step below its value, Regular, never below the label floor |
| `type.fieldLabel` | `type.label`'s size and cut |
| `type.secondary` | the Glance secondary under the hero: one native TRMNL step above `type.data`, at most TRMNL21, never below `type.data`; Bold |
| `type.stamp` | one TRMNL step below `type.title`, Bold, never below the label floor |
| `type.primary` | an item's main text line, on medium and large screens (short side <!-- v:dt:MEDIUM_SHORT_MM -->35<!-- /v --> mm and up): one TRMNL step above `type.data`, and a native cut while the data is one (at most TRMNL21, so it is the data's size where the data is TRMNL21); Regular and Bold, both Bold where Regular stems are under `stroke.min` |
| `icon.heroShared` | from `type.heroShared` by the *Hero group* rule (icon from *h*, beside other content) |
| `icon.heroAloneSteps` | from `type.heroAlone` by the *Hero group* rule (icon from *h* on its own, down to the smallest icon on its own) |
| `icon.markerDisc` | half of `icon.inline` + 1 |
| `icon.inline` | as tall as the text it sits beside: the smallest ladder size ≥ `type.data`, never below `icon.min` |
| `space.heroGap` | the hero gap and the hero clearance (*Hero group*) |
| Sun & moon heights | the vertical rhythm in *Sun & moon* |
| chart top and baseline | *Chart frame* rules |
| `color.severe`, `color.warning` and their text colours | the panel capability (*Colour tokens*); the most limited panel decides |

Rules over tokens that place things (font metrics, physics, time units, input defaults and the style choices below are the only constants):

- **Lists fill first.** A list shows as many rows as fit down to the content's bottom: its last row's ink must end above it, so the row box may hang its lower margin into the padding (`KVFIT` for key-value rows, the same sum for the event list). The footer, the lowest priority, follows only when it still fits (*Footer*). How many rows that is on each screen: *Panel tiers*.

Every value a layout uses is a token, a rule over tokens, a measured font or icon metric (including the 1–3 px ink corrections for side bearings), or a recorded style choice.

#### Step up (large screens)

A *large* screen (*Deriving tokens for any screen*) is read from further away and has the room, so these tokens go one step above their floor or base (each keeps its kind: *Token register*):

| Token | Large-screen value |
|---|---|
| `type.data`, `type.label`, `type.unit` | one TRMNL step above the floor |
| `type.title` | one TRMNL step above its base (*Style choices*, `type.title` base) |
| `type.fieldLabel` | one TRMNL step above `type.label`, Regular (Bold where Regular stems are under `stroke.min`) |
| `line.series` | one more pixel (`line.base` + 2) |

#### Measured

| Token | How |
|---|---|
| detail column | *Space* (the detail column, `DCOLW`) |
| time columns | widest time + `space.l` |
| chart label margin | widest scale label + `space.s` |
| `type.heroShared` | per layout: the hero beside other content (*Hero group*), the largest hero rung for which this layout's widest readings pass the pixel check, fitted first, with its strip icons at their smallest (no hour icon, the day icon at `icon.min`); `icon.heroShared` follows by the *Hero group* rule (*Derived*) |
| `icon.stripHour`, `icon.stripDay` | per layout, fitted after its hero: the hour icon one ladder step below the day icon, the pair as large as every case of the layout passes; when no pair passes, the hour icon drops out and the day icon is as large as passes; never below `icon.min` |
| `type.heroAlone` | per layout: the hero on its own (*Hero group*), the largest hero rung for which this layout's ordinary reading passes and keeps its icon, never below the tier's floor (the one exception: *Single value*, the 1.4"); `icon.heroAloneSteps` follows by the *Hero group* rule (*Derived*) |

Measured tokens are fitted in the build (`lib/layout_fit.py`, run by `lib/gen_tokens.py`), **each layout on its own**, in this order: its hero, then its strip icons, so strip icons give way before the hero does (*Hero dashboard with a chart or list*, *What gives way*). So a new page never changes another page's hero, and two pages on one screen may have different hero sizes. The templates lay a layout's measured tokens over its tier's (`EP_LAYOUT` over `EP_TIER`). What each layout has: the table in *Physical size minimums*.

#### Style choices

The same on every screen. Each one could be different; this is why it is what it is, and what a change touches.

| Token | Value | Why | A change touches |
|---|---|---|---|
| Fonts | TRMNL 12 / 16 / 21 and their exact 2× cuts (Bold; Regular for units, and for `type.primary`, `type.fieldLabel` and strip lines where its stems clear `stroke.min`), Space Grotesk Bold for heroes | pixel fonts drawn for 1-bit: no anti-aliasing, so no grey edges that turn red on BWR panels; a geometric hero face for numbers only | every metric table (`ep_metrics.jinja`) |
| `space.xs`, `space.s` | <!-- v:xs.12 -->2<!-- /v --> / <!-- v:s.12 -->4<!-- /v --> px around TRMNL12/16; <!-- v:xs.21 -->3<!-- /v --> / <!-- v:s.21 -->6<!-- /v --> px around TRMNL21; a 2× cut doubles its base (<!-- v:xs.24 -->4<!-- /v --> / <!-- v:s.24 -->8<!-- /v --> around 24 and 32, <!-- v:xs.42 -->6<!-- /v --> / <!-- v:s.42 -->12<!-- /v --> around 42) | XS is the smallest gap that reads as a gap; S = 2 × XS; around TRMNL21 both scale × 1.5 with the type | chips, every line gap, rows, footer, title row |
| Row air steps | the steps of the fixed-row ladder (*Fixed rows*, *Space*) | detail rows sit beside a hero and must stay compact; lists are scanned and get the most air | row heights, row budgets |
| `type.title` base | TRMNL<!-- v:dt:TITLE_BASE -->16<!-- /v --> Bold, never below `type.label`'s size | the title is chrome: it names the screen and never outranks the data | title row height |
| Hero ladder | <!-- v:heroLadder -->multiples of 8 from 56 to 160, then multiples of 32 to 320<!-- /v --> | Space Grotesk is an outline font, so in 1-bit every size is equally crisp; what matters is that the floor and *fill before you float* find a close fit. Below 160 steps of 8 px are <!-- v:heroStepPct -->5–14 %<!-- /v -->; above it 32 px steps are as fine as anyone can see. <!-- v:heroMinUsed -->56<!-- /v --> is the smallest hero of any layout today; 320 fills the 7.09" Glance | every hero; the measured tables (`SGB`, `HUP`, `HDN`) are generated for every rung by `lib/hero_metrics.py` |
| Icon ladder | <!-- v:iconLadder -->16 · 20, then multiples of 8 to 160, then multiples of 32 to 320<!-- /v --> | the hero ladder's steps, so an icon can follow its hero; 16, 20 and 24 stay because the stroke floor picks them (`icon.min`). An icon's size is compared through its glyph height: the median ink of the weather glyphs, measured per rung (`lib/hero_metrics.py`) | `icon.heroShared`, `icon.heroAloneSteps`, every icon slot |
| Stroke multiples | `line.*` in *Lines and strokes* (multiples of `line.base`) | a heavy divider works without other lines; a tick reads as a tick without touching the axis labels' `space.s`; an even dash reads as "a level", the longer forecast dash never reads as a threshold; dots are the quietest line; a data line outweighs the other lines without filling in. Multiples of `line.base` keep all of it in proportion on dense screens | every line and data stroke, `space.axis` |
| `space.tightMm` | <!-- v:dt:TIGHT_MM -->40<!-- /v --> mm | a canvas narrower than this (<!-- v:tightScreens -->1.4" 26 mm, 2.7" P 29 mm<!-- /v -->) attaches units to their value; physical, so a dense screen isn't judged by its pixels. Any value <!-- v:tightRange -->above 29 mm up to 62 mm<!-- /v --> gives the same result on today's screens | unit spacing |
| `space.unitGapNone` | <!-- v:unitGapNone -->`%`, `C`, `F`, `h`, `min`, `am`, `pm`<!-- /v --> (`C`, `F` after °) | typographic convention: these symbols attach | unit spacing |
| Warning outline | `chip.warning` (*Chips*); where it sits: *Spacing (internal)*, *Chips hang outward* | where a panel has no warning colour, outline against fill gives two strengths without a mark; outside the box, the text keeps its gap | chips, `OMERGE` |
| Native cut tolerance | a native cut within <!-- v:dt:NATIVE_TOL_MM -->0.05<!-- /v --> mm under a type floor is used instead of the 2× cut above it; between two native cuts the floor holds exactly | a drawn glyph reads better than a doubled one; chosen on the 4.26" device | `type.data`, `type.label` on dense screens |
| Forecast horizon | hour strip: <!-- v:spec:weather_35:HOURS -->4<!-- /v --> hours on the 3.5", 4.1" and 2.7" landscape, <!-- v:spec:weather_75:HOURS -->6<!-- /v --> hours on the 800 × 480 weather layouts, <!-- v:spec:weather_75p:HOURS -->5<!-- /v --> hours on the 7.5" portrait (hour cells as wide as the day cells, so the two strips share columns), <!-- v:spec:_wx:PORT_HOURS -->3<!-- /v --> hour rows on the 2.7" portrait; day strip: <!-- v:spec:weather_41:DAYS -->5<!-- /v --> days, up to <!-- v:spec:_wx:PORT_DAYS -->3<!-- /v --> day rows on the 2.7" portrait (as many as fit) | the next few hours and a working week are what the screen answers; more cells would shrink every value | the strip's cell width, `icon.strip*` |
| Axis ticks | CO2 chart: <!-- v:dt:TIME_TICKS -->5<!-- /v --> time ticks, evenly spaced, both ends included; rain chart: every <!-- v:spec:rain_35:TICK_EVERY -->6<!-- /v --> bars and the end | enough to place a reading in time without crowding the labels | the axis band |
| Hero gap | hero size ÷ <!-- v:dt:HERO_GAP_DIV -->7<!-- /v --> (`space.heroGap`) | the smallest gap that still reads as one group at every hero size; the same distance keeps a numeral clear of a line | the hero group, the Glance secondary, the hero clearance, the pixel check |
| Hero icon | glyph height at most <!-- v:dt:HERO_ICON_K -->1<!-- /v --> × the digit height beside other content, <!-- v:dt:HERO_ICON_K_ALONE -->1.2<!-- /v --> × on its own; on its own never under <!-- v:heroIconMin -->2/3<!-- /v --> of it | *Hero group* (icon from *h*, smallest icon on its own) | `icon.heroShared`, `icon.heroAloneSteps` |
| Chart scale | the threshold scale: a chart with thresholds runs up to <!-- v:dt:CHART_TOP -->1.5<!-- /v --> × the severe value. A page whose reading spans orders of magnitude names the logarithmic scale instead (*Chart*) | room above the severe line to see how far past it a reading is | every chart with thresholds |
| QR module | at least <!-- v:dt:QR_MODULE_MM -->0.4<!-- /v --> mm | a phone camera at arm's length (*Code*) | the code's size |
| Calendar fetch | the blueprint asks for up to <!-- v:const:appointment:35:max_events -->4<!-- /v --> (3.5"), <!-- v:const:appointment:41:max_events -->6<!-- /v --> (4.1") or <!-- v:const:appointment:426:max_events -->10<!-- /v --> (4.26") upcoming events | a data limit, not a layout one: it only has to be at least what the screen can show | the free-time footer, which reads every fetched event |

### Space

<!-- registry:tier-space -->
| Token | 1.4" `200x200-0.13` | 2.7" L `384x168-0.17` | 2.7" P `168x384-0.17` | 3.5" `384x184-0.21` | 4.1" `400x300-0.21` | 4.26" `800x480-0.12` | 7.5" L `800x480-0.20` | 7.5" P `480x800-0.20` | Rule |
|---|---|---|---|---|---|---|---|---|---|
| `space.pad` (P) | 10 | 8 | 8 | 10 | 16 | 24 | 24 | 24 | ~5 % of the short side, ≥ 1.3 mm, even |
| `space.m` (M) | 5 | 4 | 4 | 5 | 8 | 12 | 12 | 12 | `space.pad` ÷ 2 |
| `space.l` (L) | 10 | 8 | 8 | 10 | 16 | 24 | 24 | 24 | `space.pad` |
| `space.titleRow` (TH) | 17 | 16 | 16 | 16 | 16 | 23 | 22 | 22 | cap height of `type.title` + `space.s` + `line.base` |
| `space.row` (list row) | 34 | 24 | 24 | 24 | 24 | 34 | 34 | 34 | `rowMin` + 2 × `space.s` |
| `space.rowDense` (calendar, plant list) | 31 | 22 | 22 | 22 | 22 | 31 | 31 | 31 | `rowMin` + `space.s` + `space.xs` |
| `space.detailRow` | 25 | 18 | 18 | 18 | 18 | 25 | 25 | 25 | `rowMin` + `space.xs`: label/value rows beside a hero |
| `space.footer` | 23 | 16 | 16 | 16 | 16 | 23 | 22 | 22 | footer: `line.base` + `space.s` + cap height of `type.data` |
| `space.axis` | 21 | 15 | 15 | 15 | 15 | 27 | 18 | 18 | chart axis under the baseline: `line.tick` + `space.s` + cap height of `type.label` |
| `space.heroGap` | hero ÷ 7 | | | | | | | | number ↔ icon, hero ↔ secondary, hero clearance |
<!-- /registry:tier-space -->

**The detail column** beside a hero has no fixed width: it is its widest label (in the device's language, `type.fieldLabel`) + `space.l` + the widest value its rows can show (100 km/h, 1050 hPa, 12:00 PM, −10° / −15°, in the device's units; the pollen row counts as its configured type and a 3-digit count, *Pollen*). It follows the language and units, never the live values, so nothing moves when the weather changes; the hero centres in what is left, `space.l` from the column (`DCOLW`).

**Fixed rows** form one ladder above `rowMin` = cap height of `type.data` + 2 × `space.xs` + 1 (the smallest box a chip can hug the caps in, plus a 1 px paper gap): `detailRow` = `rowMin` + `space.xs`, `rowDense` = `rowMin` + `space.s` + `space.xs`, `space.row` = `rowMin` + 2 × `space.s`. A chip in a fixed row, or on a stacked text line in a cell: *Spacing (internal)*, *Chips hang outward*.

Text-bound (follow the text, not the tier):

| Token | Around TRMNL12/16 | Around TRMNL21 | Use |
|---|---|---|---|
| `space.xs` | <!-- v:xs.12 -->2<!-- /v --> | <!-- v:xs.21 -->3<!-- /v --> | inside a chip, top and bottom (<!-- v:xs.24 -->4<!-- /v --> around TRMNL24/32, <!-- v:xs.42 -->6<!-- /v --> around 42) |
| `space.s` | <!-- v:s.12 -->4<!-- /v --> | <!-- v:s.21 -->6<!-- /v --> | text ↔ adjacent line; inside a chip, left and right (<!-- v:s.24 -->8<!-- /v --> around TRMNL24/32, <!-- v:s.42 -->12<!-- /v --> around 42) |
| `space.unitGap` | <!-- v:unitGap.12 -->4<!-- /v --> (12) / <!-- v:unitGap.16 -->6<!-- /v --> (16) | <!-- v:unitGap.21 -->6<!-- /v --> | value ↔ unit (*Units and numbers*, *A space separates a value from its unit*) |

### Lines and strokes

| Token | Value |
|---|---|
| `line.base` | 1 or 2 px, the floor in *Floors and their thresholds*: enough for a divider you don't need to read |
| `line.heavy` | <!-- v:strokes.heavy -->4<!-- /v --> × `line.base`, only on a screen without other dividers |
| `line.dash` | <!-- v:strokes.dash -->4 on / 4 off<!-- /v --> × `line.base` (thresholds, reference lines) |
| `line.tick` | <!-- v:strokes.tick -->3<!-- /v --> × `line.base` (axis ticks under a chart baseline, from the row below it) |
| `line.dot` | <!-- v:strokes.dot -->1 on / 1 off<!-- /v --> × `line.base` ("now" lines) |
| `line.barGap` | <!-- v:strokes.barGap -->2<!-- /v --> × `line.base` (paper between chart bars) |
| `line.series` | `line.base` + <!-- v:dt:SERIES_UP -->1<!-- /v -->, one more on a large screen (*Step up (large screens)*), drawn as 1 px lines (below) |
| `line.forecastDash` | <!-- v:strokes.forecastDash -->6 on / 3 off<!-- /v --> × `line.base` |
| `stroke.min` | the stroke floor (*Floors and their thresholds*; decides the smallest font cut and icon per tier) |

Per tier:

<!-- registry:tier-line -->
| Token | 1.4" `200x200-0.13` | 2.7" L `384x168-0.17` | 2.7" P `168x384-0.17` | 3.5" `384x184-0.21` | 4.1" `400x300-0.21` | 4.26" `800x480-0.12` | 7.5" L `800x480-0.20` | 7.5" P `480x800-0.20` |
|---|---|---|---|---|---|---|---|---|
| `line.base` | 2 px | 1 px | 1 px | 1 px | 1 px | 2 px | 1 px | 1 px |
| `line.series` | 3 px | 2 px | 2 px | 2 px | 2 px | 3 px | 3 px | 3 px |
<!-- /registry:tier-line -->

Every stroke follows `line.base`, so one physical line sets them all: a dense screen gets proportionally thicker lines and longer dashes, and a data line always outweighs the other lines. Dash and gap lengths are whole pixels, so every panel renders the same dashes.

**Data lines** (a line-chart series, the sun path) are `line.series`, drawn as 1 px lines (the `LINE_SERIES` macro), each next one offset by a pixel (up, then down on shallow segments; right, then left on steep ones): the renderer's wide lines thin to 1 px on shallow slopes.

### Chips

| Token | Value |
|---|---|
| `chip.padX` | `space.s` of the chip's text |
| `chip.padY` | `space.xs` of the chip's text |
| `chip.warning` | fill `color.warning`, text `color.onWarning`; where the panel has no warning colour (B/W, BWR, BWY) an outline of 2 × `line.base` with ink text, and touching warning outlines share one |
| `chip.severe` | fill `color.severe`, text `color.onSevere` |
| `chip.stale` | the stale chip (*Title row*) |

### Colour tokens

Values per panel type are in *Values per panel* below. Layouts only ever name these.

| Token | Role |
|---|---|
| `color.ink` | Text, lines, icons, normal fills |
| `color.paper` | Background; text on an ink chip |
| `color.warning` | Warning fill |
| `color.onWarning` | Text and icons on a warning fill |
| `color.severe` | Severe fill, error block |
| `color.onSevere` | Text and icons on a severe fill |
| `color.stale` | Stale chip fill: `color.ink`, an outline where warnings are outlines (*Title row*) |

### Type tokens

**Fonts** (`font.*`, one file each, the only fonts allowed):

| Token | File |
|---|---|
| `font.label12` | TRMNL12-Bold |
| `font.label16` | TRMNL16-Bold |
| `font.unit12` | TRMNL12-Regular (units only) |
| `font.unit16` | TRMNL16-Regular (units only) |
| `font.text21` | TRMNL21-Regular |
| `font.strong21` | TRMNL21-Bold |
| `font.hero` | SpaceGrotesk-Bold |
| `font.*x2` (`label12x2`, `unit12x2`, `label16x2`, `unit16x2`, `text21x2`, `strong21x2`) | the same TRMNL files drawn at exactly twice their size, 24 / 32 / 42 px (see *Typography* under *Type*) |

**Roles per tier** (`type.*`): which font and size a role takes on each tier.

<!-- registry:tier-type -->
| Token | 1.4" `200x200-0.13` | 2.7" L `384x168-0.17` | 2.7" P `168x384-0.17` | 3.5" `384x184-0.21` | 4.1" `400x300-0.21` | 4.26" `800x480-0.12` | 7.5" L `800x480-0.20` | 7.5" P `480x800-0.20` |
|---|---|---|---|---|---|---|---|---|
| `type.title` | 16 B | 16 B | 16 B | 16 B | 16 B | 21 B | 21 B | 21 B |
| `type.stamp` | 16 B | 12 B | 12 B | 12 B | 12 B | 21 B | 16 B | 16 B |
| `type.label` (field labels, captions) | 16 B | 12 B caps only | 12 B caps only | 12 B | 12 B | 21 B | 16 B | 16 B |
| `type.fieldLabel` (labels beside a hero) | 16 B | 12 B | 12 B | 12 B | 12 B | 21 B | 21 R | 21 R |
| `type.data` (values, names, cells) | 21 B | 16 B | 16 B | 16 B | 16 B | 21 B | 21 B | 21 B |
| `type.primary` (an item's main line) | — | — | — | 21 R / 21 B | 21 R / 21 B | 21 B / 21 B | 21 R / 21 B | 21 R / 21 B |
| `type.secondary` (the Glance secondary under the hero) | 21 B | 21 B | 21 B | 21 B | 21 B | 21 B | 21 B | 21 B |
| `type.unit` (after `type.data`) | 16 R | 16 R | 16 R | 12 R | 12 R | 21 R | 16 R | 16 R |
<!-- /registry:tier-type -->

- `type.unit`: see *Units and numbers*, *Units are drawn one font step down*.
- On the 4.26" every role that is Regular elsewhere is Bold (units excepted): TRMNL21 Regular's stems are under `stroke.min` there (*Physical size minimums*).
- The hero sizes: the hero ladder (*Style choices*, Hero ladder). `type.heroAlone` and `type.heroShared` are measured per layout (*Measured*; their values: *Physical size minimums*).
- The degree sign takes the value's size in the Regular cut.

### Icon tokens

<!-- registry:tier-icon -->
| Token | 1.4" `200x200-0.13` | 2.7" L `384x168-0.17` | 2.7" P `168x384-0.17` | 3.5" `384x184-0.21` | 4.1" `400x300-0.21` | 4.26" `800x480-0.12` | 7.5" L `800x480-0.20` | 7.5" P `480x800-0.20` |
|---|---|---|---|---|---|---|---|---|
| `icon.min` | 24 | 20 | 20 | 16 | 16 | 32 | 16 | 16 |
| `icon.inline` | 24 | 20 | 20 | 16 | 16 | 32 | 24 | 24 |
<!-- /registry:tier-icon -->

- `icon.ladder`: the icon ladder (*Style choices*, Icon ladder). Each step in `icon.heroAloneSteps` runs through every rung between its ends. The hero and strip icons are measured per layout (*Measured*; their values: *Physical size minimums*).
- `icon.heroShared` and `icon.heroAloneSteps` follow from the hero size by the *Hero group* rule (see *Components*): the icon is measured against the hero's digits, so the two are sized together; the gap between them is `space.heroGap`.
- `icon.markerDisc`: radius half of `icon.inline` + 1 (<!-- v:markerDisc -->9 at 16 px, 11 at 20 px, 13 at 24 px, 17 at 32 px<!-- /v -->).
- `icon.moonBadge`: the largest ladder icon no bigger than a quarter of the weather icon, never below `icon.min`; drawn as in *When to use an icon* (moon badge).

## Colour

### Values per panel

Blueprints only ever use these drawcustom names. In the templates a token is read under its own name (`color.severe`); the warning chip's fill, which can be an outline, is `color.warningChip`.

| Token | In the templates | Role | BWRY (most Solum ESLs) | BWR | BWY | Grayscale (4 or 16 levels) | B/W |
|---|---|---|---|---|---|---|---|
| `color.ink` | — | Text, lines, icons, normal fills | <!-- v:color:ink -->`black`<!-- /v --> | <!-- v:color:ink -->`black`<!-- /v --> | <!-- v:color:ink -->`black`<!-- /v --> | <!-- v:color:ink -->`black`<!-- /v --> | <!-- v:color:ink -->`black`<!-- /v --> |
| `color.paper` | — | Background; text on an ink chip | <!-- v:color:paper -->`white`<!-- /v --> | <!-- v:color:paper -->`white`<!-- /v --> | <!-- v:color:paper -->`white`<!-- /v --> | <!-- v:color:paper -->`white`<!-- /v --> | <!-- v:color:paper -->`white`<!-- /v --> |
| `chip.warning` (its fill) | `color.warningChip` | Warning chip | **<!-- v:color:warning.red_yellow.chip -->`yellow`<!-- /v -->** | <!-- v:color:warning.mono.chip -->`outline`<!-- /v --> | <!-- v:color:warning.mono.chip -->`outline`<!-- /v --> | **<!-- v:color:warning.gray.chip -->`#aaaaaa`<!-- /v -->** (mid gray) | <!-- v:color:warning.mono.chip -->`outline`<!-- /v --> |
| `color.onWarning` | `color.onWarning` | Text/icon inside a warning chip | **<!-- v:color:warning.red_yellow.onWarning -->`black`<!-- /v -->** | <!-- v:color:warning.mono.onWarning -->`black`<!-- /v --> | <!-- v:color:warning.mono.onWarning -->`black`<!-- /v --> | <!-- v:color:warning.gray.onWarning -->`white`<!-- /v --> | <!-- v:color:warning.mono.onWarning -->`black`<!-- /v --> |
| `color.warning` | `color.warning` | Bars and fills at the warning level | <!-- v:color:warning.red_yellow.warning -->`yellow`<!-- /v --> | <!-- v:color:warning.mono.warning -->`black`<!-- /v --> | <!-- v:color:warning.mono.warning -->`black`<!-- /v --> | <!-- v:color:warning.gray.warning -->`#aaaaaa`<!-- /v --> | <!-- v:color:warning.mono.warning -->`black`<!-- /v --> |
| `color.severe` | `color.severe` | Severe-state fill, error block | <!-- v:color:severe.red.severe -->`red`<!-- /v --> | <!-- v:color:severe.red.severe -->`red`<!-- /v --> | <!-- v:color:severe.yellow.severe -->`yellow`<!-- /v --> | **<!-- v:color:severe.gray.severe -->`#555555`<!-- /v -->** (dark gray) | <!-- v:color:severe.mono.severe -->`black`<!-- /v --> |
| `color.onSevere` | `color.onSevere` | Text/icon inside a severe fill | <!-- v:color:severe.red.onSevere -->`white`<!-- /v --> | <!-- v:color:severe.red.onSevere -->`white`<!-- /v --> | **<!-- v:color:severe.yellow.onSevere -->`black`<!-- /v -->** | <!-- v:color:severe.gray.onSevere -->`white`<!-- /v --> | <!-- v:color:severe.mono.onSevere -->`white`<!-- /v --> |

- **Not configurable.** The colours follow from the panel, never from an input. Every blueprint reads the colour scheme from the end of the device model (`3.5" BWRY`, `7.3" BWGBRY`, `4.1" MONO`, `7.5" GRAYSCALE_4`) and derives the tokens once, in the shared macros (`ep_design.jinja`, from the ink roles in `ep_tokens.jinja`). With several devices selected, a colour is only used when every one of them has it: `'r'`, `'y'`, `'g'` (grayscale) mark what every selected panel has, and the chip roles follow from them. Jinja templates reference these variables, never a colour literal. A model name the colour table doesn't recognise falls back to black and white, which is always safe.
- **Warning is yellow only where red is also available.** On a BWY panel yellow already means severe, so warnings are outlined chips there, as on every panel without a warning colour (B/W, BWR). Bars and fills at the warning level stay ink there (`color.warning`): an outlined bar would look weaker than a normal one. Tested on a 4.1" BWRY ESL: black on yellow is very readable at TRMNL12–21, yellow still draws attention, yellow and red are easy to tell apart, and the refresh is not slower.
- **Warning and severe are fills only.** Never colour text, lines, or icon linework with them. (Yellow text on white is unreadable, and coloured smooth type fringes after quantisation.)
- **Grayscale panels: mid gray is the yellow, dark gray is the red.** Panels whose model ends in `GRAYSCALE_4` or `GRAYSCALE_16` keep the BWRY structure, two filled chips: warning = mid gray `#aaaaaa`, severe = dark gray `#555555`, **both with white text**, no "!". Stale stays a black chip with "!". Chart bars and fills follow the same mapping; threshold notches are paper on both grays.
  - **Measured on the 7.5" 4-gray device (test card):** the panel has four levels, white / mid gray / dark gray / black. 255–224 print white, 191–128 print the *same* mid gray (about half-tone: there is no light gray), 85–64 print dark gray, 0 black. The tokens use the levels themselves (170, 85), so nothing is rounded.
  - **White text reads at every size on mid gray, dark gray and black.** Black text on mid gray goes weak below 16 px and in Regular units; on dark gray it is barely legible. So text on gray is always white.
  - Mid gray, dark gray and black are easy to tell apart, so warning, severe and stale stay distinct without a mark.
- **No mid-gray on BWRY panels.** With dithering off, the integration maps neutral gray of about 35–50 % (`#585858`–`#808080`) to **red** on black/white/red/yellow panels (tested on a 3.5" BWRY: `#505050` → black, `#888888` → white). Draw only pure black and white there; any anti-aliased edge in that band shows as red specks.
- **Gray is a fill, never text or a line.** TRMNL's 1–2 px strokes fall apart in gray, and a gray hairline disappears: text stays black (or white on a dark fill), lines stay black at `line.base`.
- **No gray on B/W panels.** A dithered gray isn't addressable on 1-bit panels, so gray is only used when every selected panel reports grayscale; a mix of panels stays black and white. Progress tracks stay an ink outline on every panel (*Meters*).
- A panel only counts as grayscale when OpenDisplay reports it that way (a 4-gray panel configured as `MONO` is black and white to the blueprints).

## Type

### Typography

- **Label font: TRMNL bitmap** (TRMNL12 / TRMNL16 / TRMNL21, by Heavyweight Digital Type Foundry for TRMNL; TTF files from the bundle at trmnl.com/font-family). Always use it at its native size (12 / 16 / 21 px) or an exact 2× cut (below), in the cut *Physical size minimums* allows (Bold at 12 and 16 px; units: *Units and numbers*, *Units are drawn one font step down*). The *Type tokens* table says which size goes where.
  - **Licence:** SIL Open Font License 1.1, with no Reserved Font Name. The TTFs can ship in the repo (e.g. `fonts/`) as long as the bundle's `OFL.txt` ships with them, and they're never sold on their own.
  - **Never scale off-size.** Tested in Pillow, which drawcustom renders with: at 12 / 16 / 21 px every glyph lands exactly on the pixel grid, at any anchor and any coordinate. One pixel off (11, 13, 15, 17 …) adds 600–1,400 grey edge pixels per text line, which break up when quantised.
  - **Exact 2× cuts (24 / 32 / 42 px) are part of the system** for dense screens: TRMNL12, 16 and 21 drawn at twice their size are pixel-for-pixel twice the native drawing (verified: zero differing pixels, both cuts), and their metrics are the native ones doubled (advances, kerning, side bearings; cap height 16 / 22 / 30). They use the same files (`*x2` keys in `EP_FONT`). The Regular 2× cuts keep 2 px stems at 24 and 32, so they are for units only where 2 px is under `stroke.min`. A floor prefers the native cut below a 2× cut (*Style choices*, Native cut tolerance).
- **Hero font: Space Grotesk Bold**, for big numerals (temperature, time, a single stat) and the word of a *Glance with a word*, in capitals, in the hero sizes (*Style choices*, Hero ladder) only.
- **No other fonts.** (An outline text font for the dense large screens is an open question: see *Open items*.)

### Text rules

- **A label never overlaps its value.** Wherever a label and a value share a text line (detail rows, key-value rows, chips, footers, the title and its stamp, bar labels), the value's width is reserved first and the label gets what's left: it is cut short with an ellipsis so it keeps at least `space.l` from the value. The value is never cut. The one exception is the alert row's subject, which shows whole or not at all (*Weather thresholds*).

0. **Case: interface in capitals, content as written.**
   - UPPERCASE: everything the blueprint itself writes. That covers:
     - titles and date or day headers
     - field labels (WIND, HUMIDITY, DAWN) and status words (NOW, TODAY)
     - pollen type names
     - the label words in footers (PEAK, DAY LENGTH)
     - error messages
   - As written: everything that comes from the user's data. That covers:
     - entity and plant names, event titles
     - values with their units, everywhere, footers included (`PEAK 2.6 mm/h`, `9°/7°`). A unit is never uppercased: `MM` reads as megametres.
     - reset captions and other small inline captions next to data
   - Width budgets for uppercase strings are measured in uppercase, which runs about 15 % wider.

1. **Value first:** *A label never overlaps its value*.
2. **Cut, never shrink.** A label over budget is cut (*A label never overlaps its value*) and ends in `...`: the renderer's own truncation (`max_width` + `truncate`), which measures the real glyphs, so a cut label always fits.
3. **One text line** for free text (event titles, entity names).
4. **Overflow:** show items in order until the screen is full (*Spacing (internal)*, *Fill before you float*). A day or group that doesn't fit whole shows the items that do, followed by one text line **"+N more"** that counts only that group's remaining items, in the item column directly under them. Later groups are left out without a text line. If the last visible group is complete, there is no overflow text line. For calendar: today and its header are never dropped.
5. **Sanitise all user text.** Run every label from Home Assistant through `text_strip_pattern` (Latin incl. extended/accented, common punctuation, `€`, `™`), then collapse repeated spaces and trim. This applies to every label, not just calendar summaries.
6. **Only glyphs TRMNL has.** Every text element goes through one rewrite (`GLYPHS`, applied by `T` and the width macros), so a character the fonts lack never reaches the device as a box. It follows existing definitions rather than our own choices:
   - **Unicode compatibility normalisation (NFKC):** superscripts become plain digits, and so do subscripts (`m²` → `m2`, `m³/h` → `m3/h`, `CO₂` → `CO2`, `mmH₂O` → `mmH2O`), `℃` / `℉` → `°C` / `°F`, the Ohm sign → `Ω`, `㎡ ㎥ ㏄` → `m2 m3 cc`, primes → `' "`, `˚` → `°`.
   - **The micro sign, not Greek mu:** Home Assistant writes `μg/m³`, `μS/cm` and `μs` with Greek mu (U+03BC), which TRMNL lacks; it has the micro sign `µ` (U+00B5), so `μ` → `µ` (`µg/m3`). (NFKC maps the other way, so this one mapping is reversed.)
   - **UCUM** for a negative exponent: `m⁻¹` → `m-1`.
   - **The SI brochure** for a product of units: the dot operator `⋅` → the half-high dot `·` (`µmol/s·m2`). TRMNL has `° · – — … € ½ ± × ‰ Ω − ℓ µ`, arrows `↑ ↓ ← →` and accented Latin including `ł č ß`. The check renders a list of units exactly as Home Assistant sends them (`ent_units`).
7. **Clock times, never relative times.** A screen can show the same image for 15 minutes or more between refreshes, so "now", "+30" or "in 25 min" go stale on screen. Chart axes, forecasts and events use clock times (`14:05 · 14:35 · 15:05`), formatted per `time_format`; so do finish times, departures and the end of a song. Countdowns are whole days only (`12 DAYS`).
8. **Eight languages.** Weekdays are 2 letters and months 3, in every language. Budgets are checked against the **longest** translation of each string.
9. **Separators.** ` · ` (middle dot with spaces) joins parts of one line or title (`CO2 · BEDROOM`, `TOMORROW · 09:00–10:30`). An en dash `–` without spaces marks a range of times (`14:50–15:00`). `—` only stands for a missing value.
10. **Dates in captions.** A time less than 24 hours away is the clock time alone (`RESET 22:00`); further away it is weekday + time, as in the update stamp (`RESET MO 9:00`). Never a month-and-day phrase built from words (`Reset Nov 9 at 00:20`).
11. **Short hour labels.** Forecast hours read `15:00` (`3 PM`) where the column has room. Where it is narrow (the 2.7" portrait's row labels) they shorten to `15h` (`3pm`): the `h`/`pm` is styled as a unit (*Units and numbers*, *Units are drawn one font step down* and *A space separates a value from its unit*), never uppercased, like the `h` in a duration.
12. **Accents hang.** Text is placed and aligned by its letters, never by their accents: an accent on a capital (`PRÓXIMA`, `SLJEDEĆI`, `ÅR`) may rise above the cap height, into the padding where the text line starts at P, as a descender hangs below the baseline. Nothing moves for an accent: a title in Spanish sits where the same title sits in English.

### Hierarchy by size

TRMNL12 and TRMNL16 text is always Bold (*Physical size minimums*), so weight can't rank text. Size and case do:

- **One primary text line per item on medium and large screens:** the thing you scan for in `type.primary` (an event's start time in Bold and its title in Regular; a Claude bar's label in Regular and its percentage in Bold; both Bold on the 4.26"). Where `type.primary` is the size of `type.data` (*Type tokens*), only the cut and the case rank the two (*Open items*, type on large and dense screens).
- **Secondary information as an uppercase `type.label` text line** under it (`TOMORROW · UNTIL 10:30`). Information is never repeated between the two.
- **Group headers are labels, not items:** calendar day headers are `type.label` uppercase with a base line above, so they read as sections, not as events.
- Everything aligns to P; there are no small indents. A column (time, title) has a fixed x for every row.

## Units and numbers

1. **Units are drawn one font step down, in the Regular cut**, on the same baseline as the number: TRMNL21 → TRMNL16 Regular, TRMNL16 → TRMNL12 Regular (beside a hero number: `type.secondary`'s size, *Hero group*, *A unit beside the number*), never below the label floor, and never in a cut the floor allows only in capitals (the 2.7"'s TRMNL12): there the unit keeps the value's size (`type.unit`, *Type tokens*). A unit is predictable from its value and position, so it only has to be recognised, not read: the smaller, lighter cut makes the number stand out. In payloads a value is written `number¦unit` (more segments alternate big / small); the `T` macro splits it, measures each part with the TRMNL advance table plus the fonts' kerning, and places them.
   - This is the only text below `stroke.min` (1 px strokes, accepted for that). Never use it for anything that has to be read: words after a value are their own segment (`2.6¦mm¦ TODAY`, `922¦ppm¦ · 15:27`).
2. **A space separates a value from its unit**: one space of the unit's own font (`space.unitGap`, *Space*; the `UGAP` macro): `2.6 mm`, `18 km/h`, `1012 hPa`, `96 ppm`.
   - **Narrow canvases are tight:** a canvas narrower than `space.tightMm` (<!-- v:tightScreens -->1.4" 26 mm, 2.7" P 29 mm<!-- /v -->) keeps units attached (`2.6mm`). Set by canvas width for the whole screen (the `TITLE` macro sets `DS.tight`), never per cell, so one screen never mixes the two. On wide screens a cell that doesn't fit with the space shortens its content first (precision, the compact range), never drops the space.
   - **Attached everywhere** (`space.unitGapNone`): `%` (English practice: `81%`, small Regular), the `C`/`F` after a degree sign, and compound tokens: durations (`8h40min`) and short hour labels (`15h`, `3pm`).
   - **The degree sign belongs to the number:** `°` is drawn at the value's size, in the **Regular** cut, attached (`12°`, `13° / 6°`), so it reads as part of the value without outweighing bold digits. A `C` or `F` after it is the unit: small Regular, attached (`21.4°C`). The `T` macro splits `°`, `°C`, `°F` and `%` automatically, also inside ranges. Hero numerals in Space Grotesk keep their own full-size `°`.
3. **Temperature:** `°` alone wherever the context is weather; `°C` / `°F` where it isn't (entity lists).
4. **Ranges:** `13° / 6°` (spaces, both degree signs). Where space is tight (forecast cells, combined text lines) the compact `13°/6°`, or `13/6` when even that doesn't fit, used for **every** item on that screen, never mixed.
5. **Precision:**

   | Quantity | Shown as |
   |---|---|
   | Temperature | whole degrees in heroes and forecasts; one decimal in entity lists |
   | Rain (mm, mm/h) | one decimal below 10, whole numbers from 10 |
   | %, ppm, ppb, lx, W, hPa | whole numbers |
   | Anything else | at most one decimal |

   No trailing `,0` / `.0`; zero is `0 mm`. Entity values are rounded to this before they are shown, never shown raw (`57.41 %` → `57%`).
6. **Decimal separator follows the device's language:** a comma for nl, de, fr, es, pl, hr and sv (`0,6 mm`), a point for en (`0.6 mm`). Clock times keep their colon.
7. **Unit symbols are international:** `mm/h`, `km/h`, `lx` are the same in every language (never a translated `mm/u`). Only words are translated.
8. **Missing values:** `—`, without a unit.
9. **Every measured value shows its unit**, taken from the sensor's `unit_of_measurement` (normalised as above). Counts without a unit stay bare. Pollen counts carry their sensor's unit (`ppm`) like any value.
10. **Durations** use unit symbols, small and Regular like any unit: `8h40min`, `45min`, `2h`. Never `8:40`, which reads as a clock time. The symbols `h` and `min` are the same in every language.

## Icons

### When to use an icon

Every icon does one of three jobs. If it does none of them, leave it out.

1. **The icon is the data.** Weather condition, moon phase, sun and moon position markers. The icon *is* the value, so it needs no label.
   - **Moon badge:** every weather hero icon carries the current moon phase at its top-right corner, day and night, whenever a moon phase sensor is available (the `moon_phase_sensor` input, else the Moon integration's sensor; none means no badge). Its size is `icon.moonBadge` (*Icon tokens*). The MDI phase glyphs only draw the lit part, so the badge sits on a paper disc hugging the glyph's ink (radius size ÷ 2 − size ÷ 12), outlined at `line.base`, in a paper ring of 2 × `line.base` that knocks out the condition glyph: every phase reads as a moon, never as a dot. It sits inside the corner while it is smaller than half its icon, its rim's top even with the glyph's top (2/24 into the icon box); otherwise it is pushed out past the corner and clamped to the padding. The badge is never below `icon.min`, so on a dense screen it outgrows an icon that has stepped down (`icon.heroAloneSteps`). Never on forecast cells. The badge counts as **part of the icon**, like a superscript on a number: its paper ring may clip the condition glyph, which is not the icon "changing shape", but never a line or text.
2. **The icon marks a category** that the text alone doesn't name: an arrow next to a bare sunrise or sunset time (no layout draws one today). Inline size only, always next to text, and on **every** row of a list or on none.
3. **The icon identifies the screen.** The medication pill. At most one per screen, only in a Glance pattern, as part of the hero group.

**Never:** as decoration in the title row; in place of a word that fits; in list rows just to fill space; next to a word that already names the thing (pollen type names need no flower); as the cue for a severity level by itself. An icon never changes shape or colour on its own: a weather condition at warning or severe level is shown by chipping its label or naming it in a chip (*Weather thresholds*). A chip always holds text.

### How to draw them

1. **Source:** MDI glyphs, drawn as text in `materialdesignicons-webfont.ttf`, not drawcustom's `icon` element, which only draws an icon the kit has no glyph for (*Blueprint mechanics*, Icons are drawn as text). TRMNL's own glyphs are not used.
2. **Size ladder:** `icon.ladder` (*Style choices*, Icon ladder; a hero's icon follows from the hero size, see *Hero group*). Nothing in between. Each tier's inline size is in *Icon tokens*, each layout's hero and strip icons in *Physical size minimums*; when space is short, an icon steps **down to a smaller ladder size** (on its own: `icon.heroAloneSteps`) and drops out after its smallest allowed step. An icon never stretches to fit.
3. **Stroke ≥ `stroke.min`,** as for text: the smallest allowed icon per tier is `icon.min` (*Floors and their thresholds*; per tier: *Icon tokens*).
   Outline icons (most MDI weather icons) are fine once they meet this.
4. **Colour:** ink only. On a chip, the icon takes the chip's text colour.
5. **Weather icons:** one shared condition table in the weather data model (`ep_design.jinja`), used by every weather layout.

## States

Every state is designed (*Principles*): the three severity levels, and unavailable, stale, empty and error.

### Severity

Three levels, the same on every module:

| Level | Treatment | B/W panel |
|---|---|---|
| Normal | Plain ink | Same |
| Warning (`warning_*` input crossed) | **Warning chip** (`chip.warning`, *Chips*) | Outline |
| Severe (`severe_*` input crossed) | **Severe chip**: severe fill, on-severe text | Ink chip |

- The label and value change **together**. Never highlight just one. On a label/value row (detail rows, plant and entity rows) **one chip spans the label and the value**, as a band. In a table (hour and day cells, the 2.7" portrait's forecast rows) the column header is shared by several values, so each flagged value gets its own chip and a flagged condition chips the header.
- **Colour is the level, the label is the source.** Our own thresholds and official warnings use the same two chips; the text says which is which (`NOW · THUNDERSTORM` against `CODE YELLOW · FOG`). Only a measured value past a severe threshold or an official orange / red warning is severe by default.
- **Chip text is in capitals**, like labels, including warning subjects taken from a sensor (`CODE ORANGE THUNDERSTORM`).
- **A warning or severe chip names its subject or its problem.** A value alone is only enough when a label sits next to it (detail rows). Otherwise the chip carries the word: the condition (`FOG`), the subject (`BIRCH 96 ppm`), or a status. Medication: the press date followed by the status, `SU 8 NOV · OVERDUE` (warning) / `SU 8 NOV · MISSED` (severe), so the date stays with the hero time it belongs to. The stale chip is the one exception (fixed place, `!`). A glance chip without a row label carries its word: `MAX/MIN 11°/3°`, or the values alone where that doesn't fit (`11°/3°`). Chip widths are measured (`VALUE_W`), never estimated per character.
- **Charts on BWRY:** bars (or line spans) between the warning and severe thresholds are yellow; at or above severe, red. Threshold notches across a yellow bar are black instead of paper.
- **Stale is not a warning:** the stale chip (*Title row*) is not a warning chip.
- **Now is not a severity.** An event in progress is marked with an ink chip (fill `color.ink`, text `color.paper`): it is current, not bad. It has the shape and place a flagged value would have: the row in a date-grouped list, the start time in an event list, the `NOW` label of an event hero. It is told apart from the stale chip, also ink on a panel with a warning colour, by its place and by the stale chip's `!`. On a black/white panel a severe chip is an ink chip too, so there the two look alike.
- **Weight is not a severity level or a role marker.** TRMNL12 and TRMNL16 text is always bold (see *Physical size minimums*), so:
  - Labels and values are told apart by **case, size and position**: labels are uppercase on the left, values sit on the right.
  - Zero values (`0 mm`) look like any other value.
  - Nothing ever changes weight *because* it crossed a threshold. Only the warning and severe chips signal state.
  - Only TRMNL21 has two weights; there, bold marks the value. (Units are Regular at every size, but that is part of how a value is drawn, not a role marker.)
- **Bars and other fills** follow the same three levels: ink normally, the warning colour at the warning threshold, severe colour at severe, and the value next to them gets the matching chip (Claude usage).

### Thresholds

**Every value that has a bad direction gets a warning and a severe input**, with a default, on every blueprint that shows it. The same data has the same inputs, names and defaults everywhere.

**Every reading that can be flagged has a switch**, `flag_<what>`, on by default, in front of its `warning_<what>` and `severe_<what>`. The switches of Single value, Value with details, Levels and History graph are off by default: no value fits every sensor. Off, the reading is never flagged, on any part of the page. Every number is a real threshold, 0 included: no number means "off". Without a switch: the lists (conditions, the doors and windows that count as severe), where an empty list flags nothing, and an open door or window, which is always a warning. The To-do list's switch (`flag_due`) has no numbers: the due day decides (*Checklist*, Flagged). A chart with its switch off: *Bar chart with thresholds, Line chart with thresholds*, Switched off. Pollen's two count inputs are empty by default: empty, the sensor's own level decides (*Weather thresholds*); a count overrides it.

<!-- registry:thresholds -->
| Page | Data | Warning | Severe |
|---|---|---|---|
| Claude usage | Usage | ≥ 90 % | ≥ 100 % |
| CO2 graph | Concentration | ≥ 1000 ppm | ≥ 1400 ppm |
| Doors & windows | An opening is open | any opening | the openings in `severe_openings` |
| Energy price (EnergyZero) | Price per kWh | ≥ 15 ct/kWh | ≥ 25 ct/kWh |
| History graph, Single value | The value, high (`*_high`, at or above) and low (`*_low`, at or below) | the user's value | the user's value |
| Levels | Each row's share of its maximum, high and low | the user's value | the user's value |
| Medication | Hours since the last press | ≥ 24 h | ≥ 36 h |
| Plant moisture | Soil moisture | ≤ 25 % | ≤ 14 % |
| Rain forecast, Rain forecast (Netherlands) | Rain per hour | ≥ 2.5 mm/h | ≥ 10 mm/h |
| To-do list | An item's due day | due today | overdue |
| Value with details | The value, high and low, as on Single value | the user's value | the user's value |
| Weather, Weather and calendar, Weather at a glance | Cold (`*_temp_low`) | ≤ 3° | ≤ 0° |
|  | Heat (`*_temp_high`) | ≥ 27° | ≥ 35° |
|  | Wind, in the weather entity's own wind unit; the defaults suit km/h (`*_wind_high`) | ≥ 50 | ≥ 75 |
|  | Rain per hour (`*_rain_hour`) | ≥ 2.5 mm/h | ≥ 10 mm/h |
|  | Rain per day, today's total included (`*_rain_day`) | ≥ 10 mm | ≥ 25 mm |
|  | Pollen (`*_pollen_high`, where a pollen sensor is an input) | sensor level *high* | sensor level *very high* |
|  | Condition (`*_conditions`, a list) | `hail`, `lightning`, `lightning-rainy`, `exceptional` | none (empty list) |
<!-- /registry:thresholds -->

- **No thresholds** on <!-- v:noThresholdPages -->Calendar, Entities, Next appointment, Sun & moon, Tiles<!-- /v -->: nothing can be bad there, or (Entities, Tiles) one pair can't fit up to 12 arbitrary sensors, which show "—" and the error state instead.
- **Page-specific threshold rules** are with their page: weather (pollen levels, conditions, official warnings, high/low, the *Override order*) in *Weather at a glance and Weather*, the redraw at a deadline in *Medication*.

### Unavailable, stale, empty and error

| State | Treatment |
|---|---|
| **Unavailable / unknown value** | `—`, never coloured; the label stays. |
| **Mostly unavailable** (> half the values, lists of 2 or more) | Switch to the error state with a "most values unavailable" message. |
| **Stale** (newest source report older than the `stale_after` input) | The stale chip (*Title row*). |
| **Empty** (no events, no items) | Keep the structure (date header, title row) and show an empty statement from `language_map` (`EMPTY`, see *Empty states* below). |
| **Error / no data / misconfigured** | Keep the title row. Below it (on a page of two modules: in the half whose data is missing, *Hero dashboard with a chart or list*), a centred error block with on-severe text in the title's type (`type.title`), translated (`ERRBLOCK`). Drawn by the macros' `error` view: one drawing call for every case. A blueprint and templates from different releases draw the same block with their own message (*Blueprint mechanics*, One set). |

### Empty states

The empty statement (`EMPTY`) is one centred uppercase text line in the strong `type.primary` cut, one step down to `type.data` when it doesn't fit the module's width; it is never cut while a smaller size fits.

A module with nothing to say makes way, instead of drawing empty structure: pollen at level 0 (*Pollen*), a chart with nothing above zero (*Chart frame (all charts)*, *Exception, nothing to show*). An empty calendar day is not one of them: it keeps its day header and one text line saying so (*Date-grouped list*).

## Components

A component is one drawn building block with a fixed job; it can contain other components (a hero group is a value and an icon). It takes content and a tier, and gets every size from the tokens, never from numbers of its own. In the macro files each component is one or more macros (today's names in the last column; a component drawn inside another's macro names that one), shared by every blueprint.

| Component | Job | Arguments | Tokens | Today |
|---|---|---|---|---|
| **Value** | A number with its unit and degree sign, measured and placed by ink | value, anchor, role | `type.data`, `type.unit`, `space.unitGap` | `T`, `VALUE_W`, `SEGS`, `UGAP` |
| **Chip** | A flagged value or word: inline, centred, or as a band over a whole row | text (and label), level | `chip.*`, `space.xs`, `space.s` | `RCHIP`, `CCHIP`, `DCHIP`, `LEVEL_FILL` / `LEVEL_TEXT` / `LEVEL_MARK` |
| **Icon** | An MDI glyph drawn as text, pixel-exact | name, size | `icon.ladder`, `color.ink` | `I` |
| **Hero chip** | The chip behind a flagged hero number: the digits' ink plus `space.s` on every side | number, level | `space.s` of `type.data`, digit ink (`HUP` / `HDN`, measured) | `HERO_CHIP` |
| **QR code** | A QR code with its quiet zone, QR modules on whole pixels | data | `tier.pitch`, `space.l` | — (mock-up; drawcustom's `qrcode` element) |
| **Empty statement** | One centred text line where a module has nothing to say | message | `type.primary` (strong), one step down to `type.data` when it doesn't fit | `EMPTY` (reads its tokens) |
| **Moon badge** | The moon phase on a weather hero icon | icon box | `icon.moonBadge` | `MOON_BADGE` |
| **Hero group** | Number then icon, centred by ink in the space it owns. Two versions: *on its own* (in the hero block) and *beside other content* (in the hero band, the event hero); see *Hero group* | number, icon, area, level | `type.hero*`, `icon.hero*`, `space.heroGap` | `HERO_ALONE` on its own, `HERO_SHARED` beside other content; `HERO_LEFT`, `HERO_INK_X` |
| **Glance secondary** | The one text line under the hero on a Glance: a value as plain text, or a chip at a level; its box is a chip's height. What goes there is the page's rule (the weather's: today's high/low, *Glance with a footer*) | text, level | `type.secondary`, `chip.*` | drawn in `HBLOCK`; the weather's is `SECOND` |
| **Hour cell / Day cell** | One column of a strip: label, optional icon, values. Rules: *Hour cell / Day cell*, below the table | hour or day | `type.data`, `space.xs`, `icon.strip*`, `chip.*` | `HCELL`, `DCELL`, `DATA_REGULAR` |
| **Forecast row** | One row of the 2.7" portrait's forecast table: label, mm, temperature. Rules: *Forecast row*, below the table | hour or day | `type.data`, `space.row`, `space.l`, `chip.*` | `RROW`, `RCHIP` |
| **Key-value row** | Name and value in a list, one or two columns, row lines | name, value, level | `type.label`, `type.data`, `space.row` (`space.rowDense` on the 4.1" plant list), `space.l`, `line.base`, `chip.*` | `KVLIST` / `KV` (read their tokens; `ROW` draws) |
| **Event row** | One event: the start time in a column, the title, and the label text line under it (`TOMORROW · UNTIL 10:30`); see *Event list* | event | `type.primary`, `type.label`, `space.s`, `line.base` | drawn in `ELIST` |
| **Checkbox row** | One to-do item: checkbox, item, due day | item, done, due, level | `type.data`, `type.label`, `space.row`, `space.s`, `line.base`, `chip.*` | `CHECKROWS` |
| **Progress bar** | Progress bar with track, fill, now-marker and reset caption (one bar; the *Meters* module stacks them; drawn as in *Meters*) | value, period | `type.primary`, `type.label`, `line.series`, `chip.*` | `PBAR` for the track, fill and now-marker; the label row stays in the layout |

Mocked up, no blueprint yet: the **QR code** (*Code*), and the hero group's version *with a word* (*Glance with a word*). Reserved (documented, no blueprint uses it yet): the **level meter** (`METER`).

### Hero group

A hero group is a number and its icon. It has two versions (a third, *with a word*, is mocked up: *Glance with a word*):

| Version | Used in | Size | Icon |
|---|---|---|---|
| **On its own** | Glance | `type.heroAlone`: fills the screen; the largest size whose ordinary reading keeps an icon, never below the floor | up to <!-- v:dt:HERO_ICON_K_ALONE -->1.2<!-- /v --> × the digits; steps down (`icon.heroAloneSteps`), then drops out |
| **Beside other content** | Hero dashboard, event hero | `type.heroShared`: the largest size at which the layout's widest readings fit (*Hero dashboard with a chart or list*, *What gives way*) | never taller than the digits (`icon.heroShared`) |

Wherever a hero numeral and a hero icon appear together, the **number comes first and the icon second**: left then right on landscape layouts, above then below on portrait ones where they don't fit side by side. The value is the point; the icon qualifies it. This applies to every pattern.

- **A unit beside the number:** a hero whose reading has a unit (Single value) draws it after the number on the number's baseline, in `type.secondary`'s size and the Regular cut, a space apart (*Units and numbers*, *A space separates a value from its unit*). The number and its unit are one reading, centred as a whole. Flagged, a hero on its own takes one chip around both; beside other content the chip is the number's alone and the unit starts past its reach, so the unit keeps its place when the chip appears. The hero face has numbers only, so the unit is never in it.
- **One group:** the icon comes **directly** after the number, at a gap of hero size ÷ <!-- v:dt:HERO_GAP_DIV -->7<!-- /v --> (the hero gap, `space.heroGap`), with nothing in between. Details and other modules come after the group, never between number and icon. The same gap separates the hero from what is stacked under it (the Glance secondary, *Glance*).
- **Hero centring (one rule, both versions):** a hero group is centred by ink, on both axes, **in the space it owns**. A stacked hero group (the number over its icon, on portrait screens) counts the icon at its nominal ink height, the same for every icon of that size, so the number keeps its height when the icon changes. Its number is centred as a whole reading, degree sign included (*Spacing (internal)*, *A number on a centre axis is centred as a whole reading*). On Glance that space is the canvas between the paddings, below the title line, shared with the Glance secondary as one block. In the Hero dashboard it is the **hero column** (from P to the details minus the gutter L) and the band between the title line and the strip line, which it shares with the details (*Spacing (internal)*, the hero band). Widths are measured ink: the numeral's from its advances and side bearings (`HERO_INK_W`), the icon's from its box less its blank margins (`ICB`, measured per glyph), never a per-digit estimate and never the advance width, which drops the icon on readings that fit (`HERO_ALONE` on its own, `HERO_LEFT` beside other content). The icon is *fitted* by its full box, so the size it gets doesn't change with the condition, but *centred* by its ink. The hero therefore doesn't share the title's left edge in the Hero dashboard: it is its own block. A wide reading (`-12°`) fills its column and lands near the edges; that is the same rule, not an exception.
- **Hero clearance:** a hero numeral's digits stay at least the hero gap (`space.heroGap`) from any line, above or below. This replaces M when a hero is the first thing under the title line; text, labels and icons keep M.

The group is sized as one block from one value: the **hero size *h*** (a rung of the hero ladder). The tokens `type.heroAlone` / `type.heroShared` are *h*; `icon.heroAloneSteps` / `icon.heroShared` follow from it.

- **Measured, not estimated.** A hero's **digit height** is its measured digit ink (`HUP + HDN + 1`). An icon's **glyph height** is the median ink of the weather glyphs the blueprints draw, measured per rung (0.83 of the box). `lib/hero_metrics.py --pairs` prints the icon for every hero size. A string's ink width (`HERO_INK_W`) is its advance (`HWR`, measured per character) less the first character's left and the last one's right side bearing (`SGB`, `SGR`, per rung); an icon's blank margins are `ICB`. All of them are generated by `lib/hero_metrics.py --write`.
- **Icon from *h*:** the largest icon rung whose glyph height is at most **k × the digit height**: **k = <!-- v:dt:HERO_ICON_K -->1<!-- /v -->** beside other content (the icon never outweighs the number), **k = <!-- v:dt:HERO_ICON_K_ALONE -->1.2<!-- /v -->** on its own (the icon box about the hero size: one picture read from across the room, where the condition icon carries as much as the number).
- **Smallest icon on its own:** the smallest rung whose glyph height is at least <!-- v:heroIconMin -->2/3<!-- /v --> of the digit height. Below it the icon drops out rather than shrink to a dot.
- **Wide readings:** beside other content nothing gives: *h* is chosen so the widest reading the layout must show (`-12°`, `20:00`) fits with its icon. On its own the icon steps down, then drops out. **The number never shrinks** for a reading the layout was fitted for; a page for any sensor may step it down for a longer one (*Single value*, Widest reading), and never cuts it.
- **Choosing *h*** (fill before you float): the largest rung for which
  - **Beside other content:** the whole group fits its space for the widest reading, keeps `space.l` from the detail column and the hero clearance from every line;
  - **On its own:** the ordinary reading (a two-digit temperature, a clock time, a one-digit count) still keeps an icon, and the block fits between the title line and the bottom padding; never below the `type.heroAlone` floor.
- **The moon badge is part of the icon** (*When to use an icon*), so part of the group for fit, centring and the `space.l` gap.
- **Checked:** `check.py` tests the widest reading and the moon badge on every weather layout, the group's `space.l` gap and the badge ring against lines.

*h* and the icon of each layout: the table in *Physical size minimums*. The event hero is its layout's hero beside other content, and the one exception to hero centring: it is a block of text lines (the label line, the time, the title) at the list's left edge, the time `space.l` under the label line and the title `space.l` under the time.

### Hour cell / Day cell

Every text line is `type.data`. Every value is Bold, a dry `0 mm` and the day's high/low too (*Severity*, *Weight is not a severity level or a role marker*); the hour label is in the Regular cut where that clears `stroke.min`. A text line's box is rowMin; stacked items are `space.xs` apart (text lines `space.detailRow` apart, chips on them as in *Spacing (internal)*, *Chips hang outward*); an icon sits `space.xs` from its text lines.

### Forecast row

The label, the mm right-aligned `space.l` before the temperature column (as wide as its widest value), the temperature; flagged values are row chips. In the forecast table the hours, the days and the pollen row stack bottom up as one block of fixed rows, each section under a line. The footer's line closes the last row, since a row's own margin already keeps its ink more than M from it. The hero group above is centred by ink between the title line and the table.

## Modules

A module is one block of content on a screen, built from components (and other modules). Each module has a budget per tier (see *Panel tiers*) and handles all states; patterns arrange modules into a screen.

| Module | Job and rules | Arguments | Tokens | Today |
|---|---|---|---|---|
| **Title row** | Title left, update stamp (or stale chip) right, line below. Details: *Title row*, below the table. | title, timestamp, stale | `type.title`, `type.stamp` (on the title's baseline), `space.titleRow`, `space.l`, `line.base`, `chip.stale` | `TITLE` (reads its tokens) |
| **Footer** | The conclusion, in one text line, at the bottom of a screen. | text left / right, level | `type.data`, `space.footer`, `space.s`, `space.l`, `line.base`, `chip.*` | `FOOT` (reads its tokens) |
| **Error block** | The centred error block that replaces everything below the title. The message keeps `space.s` inside the padding; text line spacing `space.s` of the title. | message | `type.title`, `space.m`, `space.s`, `chip.severe` | `ERRBLOCK` (reads its tokens) |
| **Detail rows** | Label/value rows beside a hero, with the alert row, the pollen row and the make-way rule. Rules: *Detail rows*, below the table. | rows, alert, make-way order | `type.fieldLabel`, `type.data`, `space.detailRow`, `space.l`, `chip.*` | `DROWS` (reads its tokens) |
| **Strip** | A line, `space.s`, a row of equal cells. Rules: *Hero dashboard with forecast strips* under *Patterns*. | cells | `line.base`, `space.s`, `space.xs` | `HSTRIP`, `DSTRIP`, `STRIPY`, `CELLH` |
| **Key-value list** | Key-value rows, one shared row (`ROW`). Rules: *Key-value list* under *Patterns*. | name, value, level | `type.label`, `type.data`, `space.row` (`space.rowDense` on the 4.1" plant list), `space.l`, `line.base`, `chip.*` | `KVLIST` / `KV` (read their tokens; `ROW` draws) |
| **Date-grouped list** | Day headers and event rows, with an overflow text line. Rules: *Date-grouped list*, below the table. | events | `type.label`, `type.data`, `space.rowDense`, `space.s`, `space.l`, `color.ink`, `color.paper` | `DLIST` (reads its tokens); `DAY_HEAD_H` is the day header height to budget with |
| **Event list** | Next appointment: start time column, title, label text line. Rules: *Event list* under *Patterns*. | events | `type.primary`, `type.label` | `ELIST` (reads its tokens), with `EFREE` for the free-time footer |
| **Event hero** | Next appointment with one event: label text line (day, or the NOW chip) with the time range, the start (the end while it runs) as a hero beside other content, the title. | event | `type.data`, `type.heroShared`, `type.primary` (regular cut), `space.l`, `color.ink`, `color.paper` | `EHERO` (reads its tokens; the 3.5", 4.1" and 4.26" share it) |
| **Meters** | Progress bars stacked. Rules: *Meters* under *Patterns*. | bars | `type.primary`, `type.data`, `type.label`, `space.m`, `space.l` | `METER_ROWS` (each bar by `PBAR`) |
| **Chart** | Plot, label margin, clock-time axis, thresholds, severe fills. | series, thresholds | `type.label`, `line.*`, `space.s` | `CFRAME`, `CTHRESH`, `CBASE`, `CAXIS` (read their tokens); bars, series and notches stay in each chart |
| **Timeline** | Sun and moon track with markers and the sun path. Rules: *Timeline* under *Patterns*. | sun, moon | `icon.inline`, `icon.markerDisc`, `line.tick`, `type.label` | `TMARK` for markers, `SERIES` for the path, `CAXIS` for the compass row; the heights follow the vertical rhythm in *Sun & moon* |
| **Checkbox rows** | Checkbox rows in one or two columns, open items first. Rules: *Checklist* under *Patterns*. | items, done, due, level | `type.data`, `type.label`, `space.row`, `space.s`, `space.l`, `line.base` | `CHECKROWS` |
| **Tiles** | Repeated icon–state–label unit in a grid. Rules: *Tiles* under *Patterns*. | icon, state, label | `type.data`, `type.label`, `space.m`, `line.base` | `TILEGRID` |
| **Level meter** | *Reserved: no blueprint uses it.* A level in four segments. Rules: *Level meter*, below the table. | level | — | `METER` |
| **Hero block** | The hero group *on its own* and the Glance secondary under it, centred as one block (*Hero group*, hero centring; the secondary's chip box is reserved, so nothing moves when a chip appears). The Glance's one module under the title row; see *Glance*. | hero, icon, levels, Glance secondary | `type.heroAlone`, `icon.heroAloneSteps`, `type.secondary`, `space.heroGap` | `HBLOCK`, `HERO_BLOCK_Y` |
| **Hero band** | The hero group *beside other content* and the detail rows, **centred by ink between the title line and the next line** (the strip's, or the module's). Rules: *Hero dashboard* under *Patterns*. | hero, icon, rows | `type.heroShared`, `icon.heroShared`, `space.l` | `HBAND` |
| **Forecast table** | The 2.7" portrait's strips: forecast rows for the hours, the days and the pollen, stacked bottom up as one block of fixed rows; see *Forecast row*. | hours, days, pollen | `type.data`, `space.row`, `space.l` | `RROW` |
| **Code block** | The code with its quiet zone and the label/value text lines beside it (under it on a portrait screen); see *Code*. | data, text lines | `tier.pitch`, `space.l` | — (mock-up) |
| **Month grid** | Weekday labels over seven columns of day numbers; today boxed, event dots; see *Month*. | month, events | `type.label`, `type.data`, `space.row`, `line.base` | — (mock-up) |
| **Text block** | Wrapped text and the sender text line; see *Note*. | text, sender | `type.primary`, `type.data`, `type.label`, `space.s` | — (mock-up) |

Charts: see *Bar chart and Line chart* under *Patterns*. Key-value rows (the component) are described with the *Key-value list*.

### Detail rows

The label left in `type.fieldLabel`, the value right on the padding in the data font. A flagged row is one chip spanning label and value (`DCHIP`). A page may add two rows that come and go, each taking another row's place so the block keeps its size: an **alert row** first, for something flagged that has no row of its own, and one more row last (the weather's pollen row); both are row chips when flagged. Each layout names the order in which rows make way. The band the rows form with the hero: *Hero band*. Which row makes way for the alert row or the pollen row: *Override order*.

### Date-grouped list

- **Day headers** are uppercase `type.label` lines with a base line above; today is labelled by name.
- **Event rows** are `type.data`, in fixed rows of `space.rowDense`: times right-aligned in their column (*Spacing (internal)*, *A time column*), titles after it.
- **An empty day** keeps its header and one uppercase text line (`NO APPOINTMENTS`).
- **Overflow:** *Text rules*, *Overflow*.

### Level meter

4 square segments, 12–14 px (sized to the row's text, not an icon), 2 px apart: filled = ink, empty = 1 px outline. On a chip, segments take the chip's text colour (on-warning or on-severe). Before reusing it, change the empty segments: an outlined square is also the to-do checkbox.

### Title row

- The title row is the layout's first row: text on paper above a line, never a filled bar. It is drawn by one macro (`TITLE`) on every layout, medication included.
- **Title:** `type.title` (its base in *Style choices*, one step up on a large screen, *Step up (large screens)*), never below the label floor, left-aligned, in capitals. The title names the screen; it is chrome, so it never outranks the data below it.
  - **Every blueprint has a *Header title* input.** Left blank, the title is a translated default that names what the screen shows (`WEATHER`, `CALENDAR`, `PLANTS`). One qualifier may follow after ` · ` when it tells devices of the same kind apart (`CO2 · BEDROOM` from the sensor's area, `WEATHER · AMSTERDAM` on the 7.5", `MEDICATION · LAST TAKEN` so the hero time reads as the last dose); a typed title replaces the whole default.
  - **Width:** the title gets what is left after the stamp: the canvas minus both paddings, the stamp's measured width (its chip included when stale) and a gap of L. A longer title is cut with "..." (*A label never overlaps its value*).
- **Update stamp:** quieter than the title, because it is a check, not data: `type.stamp` (*Derived*). Never TRMNL16 Regular: its 1 px strokes are under `stroke.min`, and unlike a unit the stamp has to be read exactly. Right-aligned, ink ending at W − P − 1, on the title's baseline (a TRMNL12 stamp sits 2 px below a TRMNL16 title's middle anchor). The title's width is measured against this smaller stamp. It is **weekday + time** (`SU 17:58`, `FR 6:05 PM`), a 2-letter weekday in capitals (the `STAMP` macro), on every layout except Medication (see *Medication*). A device that stops updating keeps its last image, so a date-less time can't tell you the image is from yesterday; the weekday can.
- **Stale chip:** when the data source stops reporting while the automation still runs, the stamp shows the source's last report (weekday + time) in an ink chip with "!" (`chip.stale`: fill `color.ink`, text `color.paper`, prefix `! `; an outline with ink text and "!" where warnings are outlines). It is not a warning chip: old data is not an alarm about the world, and the mark and its place in the title row tell it apart. The chip goes back to the title's font and size (`type.title`), so a stale screen is louder than a healthy one (the *Mark data as stale after* input, default <!-- v:shared:stale_after -->60 min<!-- /v -->, 0 turns it off). It reads `last_reported`, not `last_updated`: a value that stays the same for hours is not stale as long as the source keeps reporting it. With several sources (entity list, plants, pollen next to weather) the newest report counts: one quiet door sensor doesn't mark the whole screen stale. Every blueprint whose data comes from reporting entities has the input. Exempt are the blueprints whose data Home Assistant computes or fetches at the moment it redraws, so there is nothing to go stale, and the two that redraw only on a change of their own (Medication, which has no stamp; Doors & windows, where there is no redraw at which old data could be marked): <!-- v:noStalePages -->Calendar, Doors & windows, Energy price (EnergyZero), Medication, Next appointment, Sun & moon, To-do list<!-- /v -->.
- The title row has no icons.
- **Line:** the row ends in the screen's standard line.
- **Height (`space.titleRow`, *Derived*):** the title caps start at P (accents above them hang, *Text rules*, *Accents hang*), and the line sits S under the caps, as the footer's line sits S above its caps.

### Footer

The footer is an **optional single text line at the bottom of a screen**. It says what the screen adds up to.

- **What goes in it**, one of two things:
  - **(a) the conclusion of the main module**: what the chart, list or forecast adds up to, in words and clock times. Examples: Rain forecast (Netherlands) `HEAVY RAIN 14:50–15:00 · PEAK 13 mm/h`, CO2 `NOW 495 ppm · PEAK 2703 ppm · 09:15`, Sun & moon `DAY LENGTH 9h09min`, Claude usage `ON PACE` / `WEEK 7% AHEAD`, Next appointment `FREE UNTIL TOMORROW 09:00` / `FREE FROM 11:30`, Plant moisture `7 PLANTS NEED WATER`, Weather `RAIN UNTIL 17:00` / `DRY UNTIL 16:00` / `DRY`.
  - **(b) context for the whole screen** that belongs to no module and needs no action (sunrise/sunset).

  (a) beats (b). A layout has a footer only when there is such a conclusion or context **that isn't shown anywhere else on the screen**; otherwise it has none.
- **Never in the footer:** information you act on (pollen, warnings): it is a module of its own, except on a layout without detail rows, where the footer is its place (*Override order*, Footer; *Pollen*); overflow (`+N more` belongs in its list); metadata (update time and stale chip live in the title row); anything already visible.
- **Room:** a footer takes `space.footer` at the bottom (above the padding), and every module above it keeps **M** clear of its line. A layout checks this with the same sum everywhere (`FNEED` = M + `space.footer`); the footer is drawn only when it fits.
- **Look:** one text line in `type.data`, ink ending P from the bottom, a base line S above the caps. At most two items, one left-aligned and one right-aligned. Interface words as uppercase labels, values as written. No icons: whatever an icon could show belongs in a module.
- **Severity:** when the conclusion is a warning or severe fact, the whole text line becomes the chip (`WEEK 7% AHEAD` in a warning chip), which takes the footer line's place.
- **Priority:** fill → footer → spread (fill before you float, *Spacing (internal)*, *Fill before you float*, with the footer between fill and spread). The footer gives way to content (one more event, one more plant; the Checklist's footer is the exception, *Checklist*, Footer) but takes precedence over extra white space (Claude bars move from L to M apart to make room).
- **Never on Glance:** a Glance layout's bottom is its Glance secondary. The one exception is the version *Glance with a footer*.

<!-- registry:footers -->
| Page and screens | Footer |
|---|---|
| Calendar 4.1", 4.26"; Entities 3.5"; Levels 2.7" L, 3.5", 4.1"; Tiles 1.4", 2.7" P, 2.7" L, 3.5", 4.1", 7.5" L, 7.5" P; Value with details 4.1", 7.5" L, 7.5" P; Weather and calendar 7.5" P | none |
| Claude usage 3.5" | (a) on schedule / furthest ahead, when it fits |
| CO2 graph 3.5"; Rain forecast 3.5", 2.7" L; Rain forecast (Netherlands) 3.5", 2.7" L | (a) chart summary; none when there's nothing to show |
| Doors & windows 1.4"; Medication 2.7" L; Single value 1.4", 2.7" L, 3.5" | none (Glance) |
| Energy price (EnergyZero) 3.5", 2.7" L | (a) the current price and the cheapest run (*Bar chart for prices*, Footer) |
| History graph 2.7" L, 3.5", 4.1" | (a) the current value, and the period's lowest and highest |
| Next appointment 3.5", 4.1", 4.26" | (a) free until / free from, when it fits |
| Plant moisture 4.1" | (a) number to water, when any and when it fits |
| Sun & moon 3.5" | (a) day length (the moon and its phase are on the timeline) |
| To-do list 2.7" L, 2.7" P, 3.5", 4.1", 7.5" L, 7.5" P | (a) the count of open and done items |
| Weather 2.7" L, 3.5" | none (no room; the strip is the last module) |
| Weather 2.7" P | the alert, else (a) forecast conclusion (*Override order*, Footer) |
| Weather 4.1", 7.5" P | (a) forecast conclusion |
| Weather 4.26", 7.5" L | none (strips fill the panel; sunrise/sunset in the detail rows) |
| Weather at a glance 1.4", 3.5" | the alert, else (a) forecast conclusion with pollen at the right (*Glance with a footer*) |
<!-- /registry:footers -->

## Composition

Every pattern starts with the **title row**. Under it, modules sit top-aligned and leftover space stays at the bottom; an optional **footer** closes the screen. The Glance is the one pattern that centres its block instead (see *Glance*).

### Spacing (internal)

Every gap inside a layout comes from one scale. M and L follow the padding, so the internal rhythm scales with the screen like the margins do. XS and S belong to the **text**: they follow the font size of the text they surround, not the tier. XS, S, M and L are short for `space.xs` (inside a chip, top and bottom), `space.s` (text ↔ an adjacent line; inside a chip, left and right), `space.m` (after the title line; between modules without a divider) and `space.l` (column gutter); their values are in *Space*.

1. **Content starts M below the title line**, on every layout: the topmost ink of the first module (an icon, a label, text) sits exactly M below it; a hero numeral sits its hero clearance below it (*Hero group*). Layouts other than the Glance are **top-aligned**: leftover space stays at the bottom (or between the top block and a bottom-anchored strip).
   - **Exception, the hero band:** in a Hero dashboard the hero and its detail rows are centred between two fixed lines (*Hero band*). Everything else on the screen stays top-aligned.
   - **Fill before you float.** Before leaving space empty, use it: first **fill** (show more items, or step the module up one size, e.g. Claude usage with up to 3 bars in TRMNL21), then **spread** by one fixed step (module gap M → L when everything still fits with L), and only then **float**: what remains stays at the bottom. Gaps never take in-between values.
   - **Centre within a module, never the layout.** Only an element that is the whole message is centred in its own space: the Glance's hero block and the Hero dashboard's hero band (*Hero group*, hero centring) and an empty state's statement (centred in the module it replaces, *Empty states*).
   - **A number on a centre axis is centred as a whole reading**, a trailing ° included (the stacked hero group of a portrait weather screen).
2. **Dividers are symmetric: S on both sides.** The line itself separates the modules, so the gap on either side only has to keep it off the text. Modules separated by whitespace alone get M.
3. **Column gutters are L wide, with the divider exactly centred.**
4. **Chips hang outward.** Text inside a chip stays aligned with the text around it; the fill extends S beyond it on each side (into the padding where needed) and XS above and below. A warning outline (`chip.warning`, *Chips*) sits one `line.base` outside the chip's box (a hero's inside its box, 2 × `line.base` + 1). **Into the padding, a fill reaches at most S + XS of the text it holds** (a hero's fill: of `type.data`, which pads it); a warning outline reaches one `line.base` more, and a fill without text stays inside the padding. Chip height = the text's size + 2 × XS for a chip on its own; in a fixed row (a row chip) or on a stacked text line it is the pitch − 1 (*Fixed rows*), so stacked chips never touch: two chips on top of each other always keep a 1 px paper gap. A chip that sits against a line, or holds capitals only, hugs the caps instead (the cap height + 2 × XS): the footer chip, the `NOW` chip on an event's start time, the event hero's label chip, and a chip in the first row under the title line, so it stays clear of the line.
5. **Fixed rows are the one place spacing is measured to boxes, not ink.** Lists and calendars have a fixed row height so rows line up and budgets are exact: the first row's box starts M below the title line, and in-row lines sit at the row's bottom. Everything else is measured to the ink.
6. **A line between list rows sits centred in the gap between their ink**: equal space above and below, an odd pixel going below. It follows from the row height and the row's ink height, so it is never set by hand. (Row lists with fixed boxes, *Fixed rows are the one place*, keep the line at the box bottom.)
7. **A time column is as wide as its widest time + `space.l`** (event list, calendar), with the times right-aligned so the minutes line up, and titles start right after the column; an item without a time starts at the column's left.
8. **The event list's row height** is a row's ink (`type.primary` + the label's cap height) + `space.s` + line + `space.s`.

### Lines

- **Two weights only: the base line and the heavy line** (`line.base`, `line.heavy`, *Lines and strokes*). This is about lines (dividers, baselines, ticks, tracks). **Data lines are not dividers:** they are `line.series` (*Lines and strokes*).
- **Solid or dashed** (`line.dash`, `line.dot`, *Lines and strokes*).
  - Dashed lines suit reference lines: thresholds, targets, "now". drawcustom's `line` supports this (`dashed`, `dash_length`, `space_length`).
- Use `line.heavy` only on a screen that has no other dividers. Otherwise use the base line everywhere. Never mix the two on one screen.

### Positioning

- Absolute pixel coordinates for all content.
- No percent positioning, the error block included.
- When the item count is user-configurable, compute row positions from the tier's row height and the active item count. Pack items with no gaps for empty slots.

## Patterns

A pattern is what a kind of screen looks like: which modules, in which order, and how they share the space. Its versions are subsections; pages fill it (see *Pages*). A pattern is drawn by one macro (the *Macro* column), which puts its modules on the screen; the page passes its content and words. The Hero dashboard's general parts are in the kit: the hero band (`HBAND`) and the version *with a chart or list* (`HERODASH`, which leaves its bottom half to the page's module). The version *with forecast strips* is the weather's own (`WXDASH`, and `WXPORT` for the 2.7" portrait): forecast strips are weather content, so those two sit with the weather page's pieces and read its data.

<!-- registry:patterns -->
| Pattern | Modules | Versions | Status | Macro |
|---|---|---|---|---|
| **Glance** | Title row, Hero block | *with the hero in a chip*<br>*with a footer*<br>*with a word* (mock)<br>*with a progress bar* (mock) | live | `GLANCE` |
| **Hero dashboard** | Title row, Hero band, Strip, Footer | *with forecast strips*<br>*with a chart or list* | live | `HERODASH`, `WXDASH`, `WXPORT` |
| **Bar chart** | Title row, Chart, Footer | *with thresholds*<br>*for prices* | live | `BARCHART` |
| **Line chart** | Title row, Chart, Footer | *with thresholds* | live | `LINECHART` |
| **Timeline** | Title row, Timeline, Footer | — | live | `TIMELINE` |
| **Key-value list** | Title row, Key-value list, Footer | — | live | `KVPAGE` |
| **Grouped list** | Title row, Date-grouped list | — | live | `GROUPED` |
| **Event list** | Title row, Event list, Event hero, Footer | *with one event as a hero*<br>*with line numbers* (mock) | live | `EVENTS` |
| **Meters** | Title row, Meters, Footer | *both ways* (mock) | live | `METERS` |
| **Checklist** | Title row, Checkbox rows, Footer | — | live | `CHECKLIST` |
| **Code** | Title row, Code block | — | mock | — |
| **Tiles** | Title row, Tiles | — | live | `TILES` |
| **Month** | Title row, Month grid | — | mock | — |
| **Note** | Title row, Text block | *with a progress bar* (mock) | mock | — |
<!-- /registry:patterns -->

Bar chart and Line chart share the chart frame; the Timeline shares its clock-time axis (a Timeline is a Line chart on a compass axis). The lists (Key-value list, Grouped list, Event list, Checklist) share how they fill first and when they show a footer (the Checklist always shows its own) and differ in their rows and how they are grouped. Meters, the Glance *with a progress bar* and the Note *with a progress bar* use the one progress bar.

### Glance

Every Glance page draws with one macro, `GLANCE`: the title row and the hero block (the hero group on its own and the Glance secondary under it, centred as one block; `HBLOCK`). The page passes the title, the stamp, the hero and its icon, and the Glance secondary: plain text, a chip at a level, or one it draws itself (the weather's high/low, *Glance with a footer*).

- A readout for across the room (<!-- v:uses:glance,glance/footer -->Doors & windows, Medication, Single value, Weather at a glance<!-- /v -->).
  1. **Everything with data is large:** the hero (`type.heroAlone`, the hero group *on its own*) and **at most one secondary value**, in `type.secondary` (TRMNL21 Bold). If a value isn't worth that size, it belongs on another pattern.
  2. **Severity takes the Glance secondary:** the flagged item replaces the secondary value as a chip, at the same large size. Temperature chips the hero itself. (*Glance with a footer* puts it in the footer instead.)
  3. **The only small text is the title and the update stamp**, in the title row. They are metadata, so they only need the label minimum.
  4. No footers with extra data: hi/lo, rain totals and similar either become the secondary value or are left out. The version *Glance with a footer* is the stated exception to this and to *at most one secondary value*.
  5. **One structure, three zones**, the same on every tier:
     - **Title row**: title left, update stamp right (as on every pattern).
     - **Hero block**: the hero group (*Hero group*) with its **Glance secondary directly under it**, as one block. The secondary is part of the message, not a footer: it sits a hero gap (`space.heroGap`) below the hero's ink, measured to its chip box (XS around the text's size). The box is reserved even without a chip, so nothing moves when one appears.
     - **Secondary**: one `type.secondary` text line, the value or chip centred horizontally. A chip hangs outward like any chip.

     The block is **centred** by ink, on both axes, in the space it owns (*Hero group*, hero centring): vertically between the title line and the bottom padding (H − P). It lands slightly above the screen's middle, the usual optical centre. Never pin the secondary to the bottom edge: that is the footer position on other patterns and reads as least important (`HERO_BLOCK_Y` macro).
  6. **Too wide:** the icon steps down through every rung of the layout's `icon.heroAloneSteps`, then drops out; the number never shrinks; the fit is measured to ink (*Hero group*: wide readings, measured, hero centring).

#### Glance with the hero in a chip

Temperature chips the hero itself: the chip is the digits' ink plus `space.s` on every side (*Hero chip*).

#### Glance with a footer

For a Glance whose alerts would otherwise take the place of a value you always need. Used by <!-- v:uses:glance/footer -->Weather at a glance<!-- /v --> only: an alert used to replace today's high/low.

- **The footer is always there** (*Footer*: room and look), so nothing moves when an alert appears. The hero block is centred between the title line and the footer's room (`FNEED`), not the bottom padding.
- **The Glance secondary is the value that always shows** and never makes way for an alert: on the weather today's high/low (`13° / 6°`). Flagged, it is a chip with its label (`MAX/MIN 13° / 6°`), the values alone where that doesn't fit.
- **The footer holds the alert:** the item picked in the *Override order*, as the footer chip. The Glance secondary's own value is left out of that pick. With no alert it holds the page's conclusion (the weather's: *Override order*, Footer).
- **Worst case:** the hero is fitted for the layout's ordinary reading on the smaller block, so `type.heroAlone` is at most what the plain Glance would get on the same screen; the widest reading (−12° with the moon badge) follows rule 6.

### Hero dashboard

The hero band (the hero group *beside other content* and its detail rows, centred by ink between the title line and the next line), one module under it, and the footer.

- **Centring:** Equal gaps, 2 px tolerance, both ≥ M and ≥ the hero clearance for the numeral (*Hero group*; the pixel check's `C` rule), with the hero's ink centre on the detail rows' ink centre. Top-aligning it would leave a dead strip above the lower line.
- **Portrait screens:** the detail rows sit under the hero group, as a centred block as wide as the hero group for the widest reading and never narrower than the detail column (*Space*). The number is centred as a whole reading (*Spacing (internal)*, *A number on a centre axis is centred as a whole reading*); on the 2.7" portrait number → icon → the text line under it have equal gaps.

#### Hero dashboard with forecast strips

The weather page: the hour strip and the day strip under the hero band; on the 2.7" portrait the strips are a forecast table (see *Detail rows*, *Strip*, *Forecast row* and *Weather*).

- **Strips:** Strips stack bottom up from the content's bottom (or the footer's M); the last text line's ink ends there, the next strip's line follows `space.s` above the cells. Hour or day label / strip icon (`icon.stripHour`, `icon.stripDay`, fitted per layout: *Measured*; hour cells have none where the hour icon drops out) / values, drawn as in *Hour cell / Day cell*. How many cells: *Style choices* (Forecast horizon). The days start with tomorrow, since today is in the detail rows; the `start_with_today` input starts them with today (every layout with day cells or day rows has it). Not used on 1.4".
- **Portrait screens (7.5" portrait).** Bottom up: the footer (the forecast conclusion), the day strip (<!-- v:spec:weather_75p:DAYS -->5<!-- /v --> days), the hour strip (<!-- v:spec:weather_75p:HOURS -->5<!-- /v --> hours), the detail rows, the hero group. The 2.7" portrait keeps its forecast table: strip cells there would be too narrow.
  - **The hero group stacks**, as the *Hero group* allows on portrait screens: the number, then the icon under it, a hero gap (`space.heroGap`) apart by ink. It is centred by ink between the title line and the line above the detail rows (the `C` rule, *Hero dashboard*). Its size is the largest hero rung for which the widest reading (−12° with the moon badge) passes (`lib/layout_fit.py`); the icon follows the *Hero group* rule.
  - **Detail rows** under it (*Hero dashboard*, *Portrait screens*), with M above and below the block.
  - **An alert row** becomes the first detail row and one row makes way, as on every Hero dashboard (*Override order*, which gives the 7.5" portrait's orders). The block keeps its six rows, so nothing moves when an alert or pollen appears.

#### Hero dashboard with a chart or list

Any module that can be drawn at the size the hero band leaves: a bar or line chart, a list, meters, the timeline, the month. *Weather and calendar* uses it with the date-grouped list on the 7.5" portrait, *Value with details* with a chart of one line on the 4.1" and the 7.5".

- **The module in a Hero dashboard** has no title row of its own and keeps its axis labels (*Style choices*, Axis ticks); where space runs out, it is drawn **without axis labels**. It is at least two rows (`space.row`) of plot or list, 1.5 without axis labels.
- **What gives way** is settled when a layout is made, never at redraw: a blueprint knows its screen, so only the values change. It holds for every Hero dashboard, in two steps:
  1. **The arrangement is the layout's**, chosen at the mock-up for the page's widest reading, in this order of preference: the detail rows beside the hero group, then under it (portrait screens), then no detail rows; the module with axis labels, then without.
  2. **The build fits the sizes** (*Token register*, *Measured*): the largest hero rung at which the layout's widest readings pass, then the largest strip icons that pass with that hero. The hero never goes below the hero ladder's smallest rung (*Style choices*, Hero ladder); where even that doesn't fit, the page isn't offered on that screen (*Pages*, *One page, one pattern*).
- **Two equal halves**, drawn by `HERODASH`. A line at the middle of the content area (between the title line and H − P) divides the hero band from the module; neither half grows into the other, so nothing moves between states.
  - **Top half, portrait screens:** the hero group (number, then the icon a hero gap after it) across the full width; under it, a hero gap apart, the detail rows (*Hero dashboard*, *Portrait screens*); the whole centred by ink between the title line and the divider (the `C` rule).
  - **Top half, landscape screens:** the hero band as every Hero dashboard has it: the detail rows beside the hero group, each centred by ink between the title line and the divider. Without detail rows the group has the full width.
  - **A unit** follows the number on its baseline in `type.secondary`, as *Hero group*, *A unit beside the number* says; it starts past the hero chip's reach, so it keeps its place when the number is flagged. The icon is optional and comes after the unit.
  - **The hero size** is the layout's own `type.heroShared` (*Measured*).
  - **Bottom half:** the module, its first text S below the divider (*Spacing (internal)*, *Dividers are symmetric*), top-aligned.
  - **Errors per half:** when one module's data is missing, its half shows the error block, in that half, and the other half keeps drawing.
- One module (*Open items*: two side by side).

### Bar chart and Line chart

Bar and line charts share one frame. The Rain forecast is the reference Bar chart.

#### Chart frame (all charts)

1. **Plot + label margin.** The plot takes the content width minus a right margin. Value labels (thresholds, scale ends) sit in the margin in the tier's label font, vertically centred on their line, never over the data.
   - The margin is **sized to the widest label + S**, not fixed. The plot then takes the rest: slot width = (content width − margin) ÷ number of bars, rounded down to whole pixels, so at most a few pixels are left over.
   - Labels are **right-aligned to the padding**; any rounding remainder falls between the plot and the labels, never at the panel edge.
2. **Fixed y-scale.**
   - With thresholds: 0 (or the page's own bottom) up to <!-- v:dt:CHART_TOP -->1.5<!-- /v --> × the severe value. A different top comes from a different severe value; the scale is never an input.
   - **CO2 graph:** from <!-- v:spec:co2_35:SCALE_FROM -->400<!-- /v --> ppm, the level of outdoor air, which indoor air rarely goes below.
   - **The automatic scale**, for a reading whose range the page can't know (History graph): the scale takes in every value of the period and every threshold line that is shown, then snaps outward to a round step: 1, 2 or 5 times a power of ten, the largest that still gives at least four steps. It is never narrower than a smallest span, so a flat line isn't stretched into noise: a tenth of the largest value shown, and at least ten times the reading's last digit (10 for whole numbers, 1 for one decimal). Both ends are labelled.
   - Never re-stretch to the data on each refresh: a scale built from thresholds or set by the page stays put, and the automatic scale only changes when a value crosses a round step. Clip values beyond the scale at the edge.
   - **An end label gives way to a threshold label** that would come closer to it than a label's height: the threshold's value then stands for that end.
   - **The logarithmic scale** is the other scale a page can name, for a reading that spans orders of magnitude: from 0 to a fixed top, each value placed at log(value + 1), so a small reading stays visible next to a large one. Thresholds sit at their log position. Rain intensity uses it, up to <!-- v:spec:rain_35:SCALE_TOP -->50<!-- /v --> mm/h (violent rain): drizzle (0.1–1 mm/h) stays visible next to a downpour.
3. **Clock-time axis.** Evenly spaced labels from start to end (*Style choices*, Axis ticks). The rain chart marks a fixed number of bars and the end instead. Clock times, never relative ones (*Text rules*, *Clock times, never relative times*). **12-hour form:** every axis label carries its half of the day as a unit attached to the time (*Text rules*, *Short hour labels*): `8:47am · 2:47pm`. The widest is `12:47pm`; five still fit on the 3.5". Where the label's cut is allowed in capitals only (the 2.7", *TRMNL12 on 1.4" and 2.7"*), it is written in capitals at the label's size: `2:05PM`. The footer's times and the empty statement's carry it the same way; a span within one half of the day carries it once, at the end (`2:50–3:00pm`), and a span across noon or midnight, or of half a day or more, at both ends (`11:15am–1:00pm`, `11:00am–8:00am`). Ticks are `line.tick` long, starting on the row under the baseline; the labels' caps start `space.s` below the ticks. The Sun & moon compass row is the same axis under the horizon: same ticks, same label text line, and a marker below the horizon sits on that label text line. Ticks that point up from a line (sunrise and sunset) are `line.tick` long too.
   - **Vertical frame:** the plot's top is M under the title line (moved down by half a label's cap height when a value label sits on the top line). The baseline sits `space.axis` + M + `space.footer` above the bottom padding, so the axis labels keep M from the footer line.
4. **Baseline.** `line.base`, solid. No gridlines other than thresholds.
5. **Summary.** The footer (see *Footer*) states the facts in clock times (peak and when; the span above severe). It becomes a severe chip when severe occurs in the plotted range.
   - **Exception, nothing to show:** when no value in the plotted range is above zero (a dry rain forecast), the chart keeps only its baseline and time axis, drops the thresholds and the footer, and states the fact once, centred in the plot (`EMPTY`: `DRY UNTIL 16:05`).
6. **Density.** At most one bar or data point per 2 × `line.base` of plot width. Downsample by averaging, but decide severity on each bucket's **maximum**, so a short spike is never averaged away.

#### Bar chart with thresholds, Line chart with thresholds

The chart frame with a warning and a severe input (*Thresholds*); its scale is the one the page names: built from the severe value, the rain intensity's logarithmic scale, or the automatic scale (*Chart frame (all charts)*, *Fixed y-scale*). Used by <!-- v:uses:bar-chart/thresholds,line-chart/thresholds -->CO2 graph, History graph, Rain forecast, Rain forecast (Netherlands)<!-- /v -->; Value with details draws the History graph's chart in its bottom half.

- **Thresholds.** At most two (warning, severe), and a second pair where the page has low thresholds (History graph); left out when the chart has nothing to show (*Chart frame (all charts)*, *Exception, nothing to show*). Each is a dashed line at `line.base` (`line.dash`) across the full plot width. A bar or a span at the warning level takes the warning colour, as *Severity* says (Charts on BWRY).
- **Switched off** (`flag_<what>` off, *Thresholds*): the chart is drawn without its thresholds. No threshold lines and no values beside them, no severe fill, no warning colour, and the footer states its facts without a chip. The scale and the plot stay as they are: the scale is still built from the severe value (*Chart frame (all charts)*, *Fixed y-scale*) and keeps its top value where it shows one, and the label margin keeps the width it has with the switch on, so switching off never rescales or moves the chart.
- **Severe flags the time slot.** Whatever represents a time slot that reaches severe is filled with the severe colour over its full extent: the whole bar, or the area under the line for that span. Where a threshold line crosses a filled area, a 1 px paper notch keeps it visible, and keeps the meaning on black/white panels.

#### Bar chart for prices

The chart frame with a warning and a severe input, as *Bar chart with thresholds, Line chart with thresholds*, for the hours of a day. What differs is written here. Used by <!-- v:uses:bar-chart/prices -->Energy price (EnergyZero)<!-- /v -->.

- **Bars:** today from midnight to midnight, one bar per hour. Hours gone are outlined and never coloured. The current hour and the hours to come are filled: in the warning colour at or above warning, in the severe colour at or above severe.
- **Scale:** the one with thresholds (*Chart frame (all charts)*, *Fixed y-scale*). On a day with a negative price its bottom is the lowest price, rounded down to a whole 10, and that value is labelled in the margin. The label margin is sized for `-10` on every day, so the plot never moves.
- **Baseline:** the zero line. Negative bars hang under it; the time axis keeps its ticks and labels at the bottom of the plot, without a second line.
- **Thresholds:** both lines run across the hours that have a price.
- **Hours without a price:** nothing is drawn. When they are the last hours of the day the fact is stated once, centred in their part of the plot (`EMPTY`: `NO PRICES`). No price at all is the error view.
- **Footer:** the current price at the left (`NOW 19 ct`), the cheapest run of hours still to come at the right (`CHEAPEST 21:00–00:00`); the length of the run is an input. The footer is a chip at the current hour's level, not at the highest level in the plot: the chart is read for what to do now. With fewer hours left than the run, the right side stays empty.
- **Worst case:** `NOW -10 ct` beside `CHEAPEST 21:00–00:00`; in 12-hour time `CHEAPEST 9:00pm–12:00am`.

#### Bar charts

- Bars are whole pixels, with `line.barGap` of paper between them.

#### Line charts

1. **Stroke.** `line.series` ink, drawn as 1 px lines (*Lines and strokes*), straight segments, square joins, snapped to whole pixels. Dashes on a curve are measured along its length, never per segment. A step line for states and setpoints is a proposal: no page draws one yet.
2. **No area fill**, except flagged spans (from baseline to line, in the level's colour): above a high threshold, and under a low one where the page has low thresholds (History graph).
3. **Current value.** A filled square (3 × `line.series` wide) on the latest point, or on the render-time point of a forecast chart. Its value and time go in the title row or footer.
4. **Measured vs forecast.** *A proposal for charts: no chart page draws a forecast yet (the Sun & moon path does, *Timeline*).* Measured is solid and forecast is dashed (`line.forecastDash`). A dotted vertical line (`line.dot`) at the render time splits them, labelled with that clock time above the plot.
5. **Two series at most.** The primary is the thick solid line; the secondary is thinner and dashed. Name them in a legend of line samples above the plot, never by colour. No page draws a second series yet: the second series and the legend are a proposal until one does.
6. **Gaps.** More than two missing samples breaks the line. Never draw across missing data.
7. **Scale labels.** Without thresholds, the margin shows the scale's top and bottom values. With thresholds, it shows the threshold values (plus the top when there's room).

### Timeline

The title row, the timeline and the footer. Used by <!-- v:uses:timeline -->Sun & moon<!-- /v -->.

- **Horizon and markers:** `line.base` baseline and ticks, inline-size icons as markers (Sun & moon horizon). Sun and moon are always on the track: above the horizon at their altitude, below it under the line at their azimuth; the moon marker shows its phase and moves clear of the sun when they meet, above or below the horizon (two marker discs aside (2 × `icon.markerDisc`), on the side it is already on, flipped at the track's ends). Above the horizon both markers are centred on their altitude, each over a paper disc (`icon.markerDisc`), so the sun path passes behind them.
- **Compass axis:** azimuth runs left to right as a time track (east, south, west in the north; east, north, west in the south, labelled accordingly). The sky's height maps 0° to the highest elevation the sun can reach at the home latitude (90° − latitude + 23.44°), not to 90°. Short upward ticks mark today's sunrise and sunset azimuths (cos Az = sin δ / cos φ), so the sun's real path is visible next to the compass ticks.
- **Sun path:** today's path is a line chart on the horizon as its baseline, drawn from the sunrise tick to the sunset tick (hour angle −H0…H0, cos H0 = −tan φ tan δ, 64 segments, mapped through the same azimuth and elevation scales). It follows *Line charts*: a `line.series` stroke, the part already travelled solid (measured), the rest dashed (`line.forecastDash`, forecast), with the dashes measured along the whole curve; at night the whole path is dashed, showing tomorrow's track. The sun icon replaces the current-value square. The sun marker is centred on the curve over its paper disc so the line never runs through its rays. Nothing is drawn below the horizon: the night path is too deep for the space and would wrap around the panel edges. The moon gets no path. A compass letter is left out while a marker below the horizon is within two marker discs of it. The timeline ends half an `icon.inline` inside the padding; labels keep `space.s` inside their column.

### Key-value list

Key-value rows in one or two columns, filled first, and the footer.

- The **name in `type.label`** (as written, not uppercased: it labels its value, and it is the one name that isn't data), the **value in `type.data`**, right on the padding. This holds where `type.label` has lowercase; on a screen where it is capitals only (*Type tokens*), how a name is drawn is decided when the first key-value list is made for it. Column-major. Value width reserved first (*A label never overlaps its value*). **One column: a base line between rows**, none after the last one; the line also runs under a chipped row (across the chip's width, in the 1 px gap), except under an ink chip or an outline (panels without a warning colour), where the paper gap or the outline is the separator. **Two columns: no lines**; the column divider and the row rhythm carry it. Two columns are of equal length (the first takes the odd row), whatever the page. Error state when more than half the values are unavailable.

### Grouped list

The date-grouped list (see *Date-grouped list* under *Modules*).

### Event list

The event list and the footer.

- As many events as fit, the footer only when it still fits (*Footer*; with fewer, the rows spread when that still fits: each row gains L − M, shared equally above and below its line). Per event: start time in a `type.primary` strong column (right-aligned), title in its regular cut, and a `type.label` text line under the title (`TOMORROW · UNTIL 10:30`). A running event's start time sits in an ink chip (*Severity*, *Now is not a severity*); its label reads `NOW · UNTIL …`. A single event is an *Event hero* (the same module on every screen) above the footer. Base lines between events.

#### Event list with one event as a hero

With one event, the event hero (*Event hero* under *Modules*) takes the list's place, above the footer: the start (the end while it runs) as a hero beside other content. The Next appointment uses it on every screen.

### Meters

Progress bars and the footer.

- Label in `type.primary` Regular and percentage Bold while the bars fit the height M apart, else `type.data`: the larger type comes before the footer and before spreading (*Spacing (internal)*, *Fill before you float*). A label is cut before the type steps down (*A label never overlaps its value*). The track is as high as the label's caps less `space.xs`, `space.s` under the label text line, with `space.xs` below it, so a chip on the next label text line keeps a paper gap. Bars L apart when they fit, else M. The track is a `line.base` ink outline. Fill: ink; the warning colour at the warning threshold, the severe colour at the severe threshold, with the matching chip behind the percentage. "Now in period" marker: a line as wide as `line.series` across the track only, with paper edges where it crosses the fill, so it stays visible past the fill. Reset caption: `type.label`, right-aligned, on the bar label's baseline, as the stamp sits on the title's. The value column is as wide as the widest value shown, never narrower than `100%` (Levels shows values with their units). Percentage column measured: `space.l` after the widest label (the label is cut short only when the widest percentage and reset caption wouldn't fit, `space.l` apart).

### Tiles

Equal tiles, each a centred stack: the icon, the state in `type.data`, the label in `type.label`. The stack is centred in its tile.

- Tiles per screen: one on the 1.4", 1 × 3 on the 2.7" portrait, 3 × 2 on the 2.7" landscape, the 3.5" and the 4.1", 4 × 3 on the 7.5", 3 × 4 on the 7.5" portrait. With fewer entities the grid is the smallest one that holds them (of two equally small, the one whose tiles are closest to square), filled row by row; a tile left over stays empty.
- Lines between two tiles that both hold an entity, centred in the gutter, each stopping `space.m` short of where it would cross another; none around the outside.
- The icon is the largest ladder size that leaves room for the state and label under it, and at most four times the size of `type.data`; a single tile's icon has no such limit. All tiles on a screen share one icon size.
- A tile without an icon centres its state and label alone (where the icon comes from: *the Tiles page*).
- *Mock-up, no blueprint flags a tile yet:* a flagged tile chips its state; the icon and the label never change, and nothing moves.
- Widest state: 9 characters (`Triggered`): the room a tile has less `space.s` on both sides, where the chip goes. A longer state, and a label wider than its tile, is cut with an ellipsis.

### Checklist

A list of to-do items: checkbox rows, filled first, and the footer.

- **Checkbox row:** a square as high as the caps of `type.data`, outlined at `line.base`, ink-filled when done; `space.s` after it, the item in `type.data` as written, its due day right in `type.label`, in fixed rows of `space.row`. The due day is today's word (`TODAY`), the weekday as the update stamp writes it within six days either way (`SA`), else the day and the month (`13 AUG`).
- **Order:** open items first, done items after them. The open items keep the order the list has in Home Assistant; a switch puts the ones with a due day first, earliest first. Done is the filled box only: weight and colour never mark it. A switch leaves the done items out.
- **Fill first:** one column while the open items fit, with the done ones in the rows left over and one line between open and done. When they don't fit, a landscape screen takes two columns of equal length (the first takes the odd row; no lines; the column divider and the row rhythm carry it) and a portrait screen stays at one. When the open items still don't fit, the done ones are left out and the last row reads `+N more`.
- **Footer:** the count (`14 OPEN · 4 DONE`, `14 OPEN` where narrow or where the done items are left out by the switch). It is always shown and never gives way to one more item: when the list overflows, the count says how much is hidden.
- **Flagged:** an overdue item is a severe row chip, one due today a warning chip; the chip spans box, item and due day like a key-value row chip, and a row keeps its place when it is flagged. A switch turns the flagging off.
- **Nothing to show:** no open items and no done ones to show is one empty statement.
- Widest readings: an item of 40 characters (cut with an ellipsis before its due day), the due day in its longest translation (Dutch, seven letters), the footer `99 OPEN · 99 DONE`.

### Mocked-up patterns

Patterns and versions that exist as mock-ups only: no blueprint is built from them yet, so their rules are proposals. Each moves to its place above when its first page is built (a version to its pattern, a pattern to its own section).

#### Glance with a word

*Mock-up (Bin day, Room sign).* The hero is a word (bin day, room sign, a status). Everything the Glance rules say holds; what differs:

- **The word is the hero**, in Space Grotesk Bold capitals, at the layout's size *h* for a hero group on its own; the icon follows *h* (*Hero group*) and comes after the word. The word is content and is never abbreviated by the layout.
- **A long word steps down** the hero ladder to its smallest rung (*Style choices*, Hero ladder) until its ink fits the content width; the icon drops out first. A word that doesn't fit at the smallest rung is cut with an ellipsis, like any text. Below the `type.heroAlone` floor the word is read from closer by, which a label allows and a measurement doesn't: the floor still holds for numbers.
- **The Glance secondary:** when it is a date, it shortens to its first word where it doesn't fit (`TOMORROW · THU 13 NOV` → `TOMORROW`); a chip (`PUT OUT TODAY`) takes its level.

#### Glance with a progress bar

*Mock-up.* An appliance run, a print, a charge.

- **The hero is the clock time it ends** (`14:32`), never the time left; the icon names the appliance.
- **The bar** sits a hero gap (`space.heroGap`) under the hero group and is as wide as the group (the progress bar; its track as high as the caps of `type.secondary` less `space.xs`), filled to the share done; the Glance secondary under it names the programme (`ECO 40° · 62%`).
- **The hero steps down** one rung at a time when the group, bar and Glance secondary don't keep the hero clearance (*Hero group*) from the title line.
- **Done and not emptied:** the bar fills in the warning colour and the Glance secondary becomes a warning chip (`DONE · DOOR STILL CLOSED`).

#### Event list with line numbers

*Mock-up (Departures).* Event rows whose title starts with the line number in a `line.base` outline (`space.xs` inside); the time column is the departure clock time; a delay chips the new time in warning with `SCHEDULED 14:07 · +6` as the label; a cancelled ride chips `CANCELLED` in severe.

#### Meters both ways

*Mock-up (Solar & battery).* A bar whose track runs both ways from a centre tick (taking power left, sending it back right); a battery's bar is its charge, the direction in the caption at the right.

#### Code

*Mock-up (Guest Wi-Fi).* A QR code people scan with a phone: guest Wi-Fi, a link to a manual, an inventory label. Drawn with drawcustom's `qrcode` element (error correction H).

- **QR modules on whole pixels**, each at least **<!-- v:dt:QR_MODULE_MM -->0.4<!-- /v --> mm** (a phone camera at arm's length): the code takes the largest whole-pixel QR module that fits.
- **Quiet zone:** 4 QR modules of paper around the code (ISO/IEC 18004), from any other ink and from the canvas edge; the padding counts as paper. Where 4 don't fit (the Wi-Fi code on the 1.4") 2 are allowed **[verify]**.
- **What it encodes is also written:** the network and password as label/value text lines beside the code (under it on a portrait screen; left out only where they don't fit, the 1.4"), so a person can type them.
- **Off:** no code, one empty statement (`GUEST NETWORK OFF`): the network being off is a fact, not a problem.
- **Checked:** every mock-up decodes with a standard QR reader.

#### Month

*Mock-up (Month overview).* A calendar month.

- Weekday labels in `type.label` over seven equal columns; they shorten to one letter where two don't fit with `space.s`.
- Day numbers in `type.data`, centred; **today boxed** at `line.base`; a day with events gets a dot under its number (a square of 2 × `line.base`).
- Rows are at most 1.5 × `space.row` high and top-aligned.
- A day that needs action carries the warning chip on its number.

#### Note

*Mock-up (Message board).* Wrapped text in the regular cut of `type.primary` (`type.data` on small screens), text line height the text size + `space.s`; as many lines as fit, the last one cut with an ellipsis when there is more. The sender and time in a `type.label` text line in the next text line's place. Important: a severe chip line above the text.

##### Note with a progress bar

*Mock-up (Now playing).* The title in the bold cut of `type.primary`, artist · album in `type.label`, the progress bar, then the track count left and the clock time it ends right (`END 14:35`). Unreachable: the error block (`SPEAKER OFFLINE`).

## Pages

A page is a pattern filled with real content for one use. Each page names the pattern it uses, its layouts (● drawn by a blueprint today; ○ no blueprint yet; — not offered; the 7.09" has no tier yet), the widest reading its entity can show, and the inputs its blueprints add to the ones every blueprint has (*Blueprint mechanics*). Every live page has the same parts, in this order: the pattern it uses, **Shows**, **Tested with**, its own rules, and its inputs. A page for any entities (Single value, Value with details, Levels, Entities, History graph, Tiles, To-do list) also has **Examples** after **Tested with**: uses people have e-paper screens for, each a scenario drawn by the page's own blueprint and shown in the README. Thresholds for every page are in *Thresholds*.

<!-- registry:pages -->
| Page | Uses | Status | Widest reading | 1.4" | 2.7" L | 2.7" P | 3.5" | 4.1" | 4.26" | 7.5" L | 7.5" P | 7.09" (no tier yet) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Appliance run** | Glance with a progress bar | mock | 20:00 | — | ○ | — | ○ | ○ | ○ | ○ | ○ | ○ |
| **Bin day** | Glance with a word | mock | — | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| **Calendar** | Grouped list | live | — | — | ○ | ○ | ○ | ● | ● | ○ | ○ | ○ |
| **Claude usage** | Meters | live | — | — | ○ | ○ | ● | ○ | ○ | ○ | ○ | ○ |
| **CO2 graph** | Line chart with thresholds | live | 4000 | — | ○ | ○ | ● | ○ | ○ | ○ | ○ | ○ |
| **Departures** | Event list with line numbers | mock | — | — | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| **Doors & windows** | Glance | live | — | ● | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| **Energy price (EnergyZero)** | Bar chart for prices | live | -10 ct | — | ● | — | ● | ○ | ○ | ○ | ○ | ○ |
| **Entities** | Key-value list | live | — | — | ○ | ○ | ● | ○ | ○ | ○ | ○ | ○ |
| **Guest Wi-Fi** | Code | mock | — | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| **History graph** | Line chart with thresholds | live | -12.5 | — | ● | ○ | ● | ● | ○ | ○ | ○ | ○ |
| **Levels** | Meters | live | 1240 ppm | — | ● | ○ | ● | ● | ○ | ○ | ○ | ○ |
| **Medication** | Glance | live | 20:00 | — | ● | — | ○ | ○ | ○ | ○ | ○ | ○ |
| **Message board** | Note | mock | — | — | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| **Month overview** | Month | mock | — | — | ○ | — | ○ | ○ | ○ | ○ | ○ | ○ |
| **Next appointment** | Event list | live | 20:00 | — | ○ | ○ | ● | ● | ● | ○ | ○ | ○ |
| **Now playing** | Note with a progress bar | mock | — | — | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| **Plant moisture** | Key-value list | live | — | — | ○ | ○ | ○ | ● | ○ | ○ | ○ | ○ |
| **Rain forecast** | Bar chart with thresholds | live | 50 mm/h | — | ● | ○ | ● | ○ | ○ | ○ | ○ | ○ |
| **Rain forecast (Netherlands)** | Bar chart with thresholds | live | 50 mm/h | — | ● | ○ | ● | ○ | ○ | ○ | ○ | ○ |
| **Room sign** | Glance with a word | mock | — | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| **Single value** | Glance | live | -12.5 | ● | ● | ○ | ● | ○ | ○ | ○ | ○ | ○ |
| **Solar & battery** | Meters both ways | mock | 100% | — | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| **Sun & moon** | Timeline | live | 10:44am | — | ○ | — | ● | ○ | ○ | ○ | ○ | ○ |
| **Tiles** | Tiles | live | Triggered | ● | ● | ● | ● | ● | ○ | ● | ● | ○ |
| **To-do list** | Checklist | live | — | — | ● | ● | ● | ● | ○ | ● | ● | ○ |
| **Value with details** | Hero dashboard with a chart or list | live | -12.5 | — | — | — | — | ● | — | ● | ● | — |
| **Weather** | Hero dashboard with forecast strips | live | -12° | — | ● | ● | ● | ● | ● | ● | ● | ○ |
| **Weather and calendar** | Hero dashboard with a chart or list | live | -12° | — | — | — | — | — | — | — | ● | — |
| **Weather at a glance** | Glance with a footer | live | -12° | ● | ○ | ○ | ● | ○ | ○ | ○ | ○ | ○ |
<!-- /registry:pages -->

**Rules for every page:**

- **One page, one pattern.** A page fills the same pattern on every screen it is offered on. The same content in another pattern is a page of its own with a name of its own; the Glance page beside a larger one is called *<page> at a glance*: Weather at a glance beside Weather. Where a page's pattern doesn't fit a screen, it isn't offered there; Rain forecast, Energy price, Solar & battery get a Glance page for the 1.4" when one is built.
- **Clock times, never countdowns of minutes** (*Text rules*, *Clock times, never relative times*).
- **The widest reading decides the layout.** Every size and every layout is chosen for the widest reading the page's entity can show (`100%`, `4000`, `-12°`, day `28`), so a screen keeps its layout from one reading, and one state, to the next. The one exception is the hero on its own, fitted on its ordinary reading: at a wider one its icon gives way (*Hero group*, *Wide readings*).
- **Labels don't change with the state** (`NET`, not `NET IMPORT` / `NET EXPORT`): a direction goes in the value (`-0.4 kW`).

### Calendar

A Grouped list: the coming days with their events.

- **Shows:** the coming days (`days_shown`), each under its day header, with its events; overflow as "+N more".
- **Tested with:** a full week that overflows, and an empty day.
- **In progress:** an event in progress (`NOW`) is an ink row chip (*Severity*, *Now is not a severity*).
- **Today** is not an alert. Mark it by name (the date header reads "TODAY" from `language_map`), never with colour or weight.

<!-- registry:inputs-calendar -->
| Screen | Inputs of this page |
|---|---|
| every screen | `calendar_entities`, `days_shown` |
<!-- /registry:inputs-calendar -->

<!-- registry:layouts-calendar -->
| Screen | Checked in | Not applicable | Cases |
|---|---|---|---|
| 4.1" | normal, widest, title, error, empty | warning, severe, gray, colour, stale, unavailable | 7 |
| 4.26" | normal, widest, title, error, empty | warning, severe, gray, colour, stale, unavailable | 7 |
<!-- /registry:layouts-calendar -->

### Claude usage

Meters: up to four usage bars with their reset times.

- **Shows:** per bar the label, the percentage, the reset time and the now-marker for the period.
- **Tested with:** warning on yellow, severe (100 %) on a colour and a grey panel, the switch off, an entity that stopped reporting.
- **Bars:** up to 3 bars on 3.5" in `type.primary`, 4 in `type.data`, drawn as in *Meters*.
- **Pace:** the footer states the pace against the period (`ON PACE`, `WEEK 7% AHEAD`). Ahead of the period it is a warning chip; with `flag_usage` off it is plain text.

<!-- registry:inputs-claude -->
| Screen | Inputs of this page |
|---|---|
| every screen | `bar_1`, `bar_1_reset`, `bar_2`, `bar_2_reset`, `bar_3`, `bar_3_reset`, `bar_4`, `bar_4_reset`, `bar_1_label`, `bar_1_period_hours`, `bar_2_label`, `bar_2_period_hours`, `bar_3_label`, `bar_3_period_hours`, `bar_4_label`, `bar_4_period_hours`, `flag_usage`, `warning_usage`, `severe_usage` |
<!-- /registry:inputs-claude -->

<!-- registry:layouts-claude -->
| Screen | Checked in | Not applicable | Cases |
|---|---|---|---|
| 3.5" | normal, widest, warning, severe, gray, colour, title, stale, error, unavailable | empty | 11 |
<!-- /registry:layouts-claude -->

### CO2 graph

A Line chart *with thresholds*: the last hours of CO2 with the current value at the end.

- **Shows:** the series over the chosen hours, the warning and severe lines, the current value as a square at the end, the footer's conclusion.
- **Tested with:** a severe reading, the same reading with the switch off, a warning on a yellow panel and on a grey panel, 12-hour time, no data; widest reading `4000`.
- **Current value:** the square of *Line charts*, *Current value*, centred on the line's last point.
- **Points:** at most <!-- v:spec:co2_35:POINTS -->165<!-- /v --> on the 3.5" (*Chart frame (all charts)*, *Density*): the readings are grouped so the chosen hours stay under it.

<!-- registry:inputs-co2 -->
| Screen | Inputs of this page |
|---|---|
| every screen | `co2_entity`, `hours`, `flag_co2`, `warning_co2`, `severe_co2` |
<!-- /registry:inputs-co2 -->

<!-- registry:layouts-co2 -->
| Screen | Checked in | Not applicable | Cases |
|---|---|---|---|
| 3.5" | normal, widest, warning, severe, gray, colour, title, stale, error, unavailable | empty | 12 |
<!-- /registry:layouts-co2 -->

### Doors & windows

A Glance, redrawn only when the count changes.

- **Shows:** the number of open doors and windows as the hero, the first open one as the chip.
- **Tested with:** nothing open, one (warning), three with a severe one, and English texts.
- **Flagged:** an open door or window is a warning; one of `severe_openings` is severe. The chip names the first open one, the severe ones first, at the highest level open.
- **Unavailable:** an unavailable sensor is left out of the count. When more than half of the sensors are unavailable, or the only one is, the page is the error state (*Unavailable, stale, empty and error*, Mostly unavailable). The page redraws on a change of the count, so the error shows at the next redraw.

<!-- registry:inputs-doors-windows -->
| Screen | Inputs of this page |
|---|---|
| every screen | `openings`, `severe_openings` |
<!-- /registry:inputs-doors-windows -->

<!-- registry:layouts-doors-windows -->
| Screen | Hero | Hero icon | Checked in | Not applicable | Cases |
|---|---|---|---|---|---|
| 1.4" | 112 px | 112 → 72 px | normal, widest, warning, severe, gray, colour, title, error, unavailable, empty | stale | 10 |
<!-- /registry:layouts-doors-windows -->

### Energy price (EnergyZero)

A Bar chart *for prices*: today's electricity price per hour, from the EnergyZero integration's own action.

- **Shows:** the bars of the day against the warning and severe lines, the clock-time axis, and in the footer the current price and the cheapest run of hours still to come.
- **Tested with:** an ordinary afternoon, the current hour at warning and at severe, the worst case of the footer (12-hour time), negative prices at midday, a price above the scale, the last hours without a price, an hour without a price in the middle of the day, the first and the last hour of the day, the switch off, 12-hour time, no prices, a grey panel.
- **Price:** EnergyZero's market price with VAT, without energy tax and purchase costs, in whole cents per kWh. An hour's level is decided on the price as shown.
- **Thresholds:** price per kWh (*Thresholds*).
- **No stale state:** the prices come from an action, not from a reporting entity.
- **No prices:** the error view.

<!-- registry:inputs-energy-price -->
| Screen | Inputs of this page |
|---|---|
| every screen | `energyzero_entry`, `cheapest_hours`, `flag_price`, `warning_price`, `severe_price` |
<!-- /registry:inputs-energy-price -->

<!-- registry:layouts-energy-price -->
| Screen | Checked in | Not applicable | Cases |
|---|---|---|---|
| 3.5" | normal, widest, warning, severe, gray, colour, title, error, unavailable | stale, empty | 18 |
| 2.7" L | normal, widest, warning, severe, gray, colour, title, error, unavailable | stale, empty | 18 |
<!-- /registry:layouts-energy-price -->

### Entities

A Key-value list of up to 12 entities.

- **Shows:** name and state with its unit, one or two columns.
- **Tested with:** 12 entities (two columns), unavailable values, more than half unavailable (the error state), stale data, Home Assistant's own unit glyphs (µg/m³, ℃).
<!-- registry:examples-entities -->
- **Examples:** packages on their way; a home server. Each is drawn in the README.
<!-- /registry:examples-entities -->

<!-- registry:inputs-entities -->
| Screen | Inputs of this page |
|---|---|
| every screen | `entity_1`, `entity_2`, `entity_3`, `entity_4`, `entity_5`, `entity_6`, `entity_7`, `entity_8`, `entity_9`, `entity_10`, `entity_11`, `entity_12`, `entity_1_label`, `entity_2_label`, `entity_3_label`, `entity_4_label`, `entity_5_label`, `entity_6_label`, `entity_7_label`, `entity_8_label`, `entity_9_label`, `entity_10_label`, `entity_11_label`, `entity_12_label` |
<!-- /registry:inputs-entities -->

<!-- registry:layouts-entities -->
| Screen | Checked in | Not applicable | Cases |
|---|---|---|---|
| 3.5" | normal, widest, title, stale, error, unavailable | warning, severe, gray, colour, empty | 10 |
<!-- /registry:layouts-entities -->

### History graph

A Line chart for any sensor: its last hours on the automatic scale.

- **Shows:** one sensor's last 3, 6, 12 or 24 hours as a line, the current value as the square at its end, the scale's two ends beside the plot, and the footer's conclusion. The title is the sensor's name unless a header title is given.
- **Tested with:** a room's temperature over 12 hours; the widest labels (`-12.5`); a nearly flat line; a CO2 sensor over 24 hours (whole numbers); the period at warning and at severe (the severe line close to the scale's top, whose label gives way); a low dip; high and low together, on a colour, a yellow and a grey panel; a long title; stale data; the sensor unavailable now; no history (the error view); both switches off; 12-hour time.
<!-- registry:examples-history -->
- **Examples:** the house's power use over a day; a freezer's temperature, flagged when it warms up. Each is drawn in the README.
<!-- /registry:examples-history -->
- **Scale:** the automatic scale (*Chart frame (all charts)*, *Fixed y-scale*). With a threshold on, its lines are inside the scale; this page doesn't use the scale built from the severe value.
- **Footer:** left the current value (`NOW 20.6 °C`), right the period's lowest and highest (`LOW 18.3 · HIGH 22.8 °C`); a chip at the highest level the period reached.
- **Widest reading:** four characters and a three-letter unit (`1240 ppm`, `-12.5 °C`): the label margin is as wide as `-12.5`, whatever the scale shows.
- **Thresholds:** high (`*_high`, at or above) and low (`*_low`, at or below), each with its two dashed lines and the spans past them filled (*Line charts*). Both switches are off by default (*Thresholds*).
- **Points:** at most <!-- v:spec:history_35:POINTS -->166<!-- /v --> on the 3.5" (*Chart frame (all charts)*, *Density*), as on the CO2 graph.

<!-- registry:inputs-history -->
| Screen | Inputs of this page |
|---|---|
| every screen | `entity`, `hours`, `flag_high`, `warning_high`, `severe_high`, `flag_low`, `warning_low`, `severe_low` |
<!-- /registry:inputs-history -->

<!-- registry:layouts-history -->
| Screen | Checked in | Not applicable | Cases |
|---|---|---|---|
| 2.7" L | normal, widest, warning, severe, gray, colour, title, stale, error, unavailable | empty | 17 |
| 3.5" | normal, widest, warning, severe, gray, colour, title, stale, error, unavailable | empty | 20 |
| 4.1" | normal, widest, warning, severe, gray, colour, title, stale, error, unavailable | empty | 17 |
<!-- /registry:layouts-history -->

### Levels

Meters for any sensors: each a row with its value and a bar that shows how full it is.

- **Shows:** up to six sensors, one row each: its label, its value with its unit, and a bar filled to the value's share of that row's maximum. No footer, no reset time and no now-marker: those are Claude usage's.
- **Tested with:** a battery, solar power of 4 kW, a tank of 1000 L and humidity; the widest reading (`1240 ppm`) beside a long label; a high row at warning; low rows at severe and at warning, on a colour, a yellow and a grey panel; a long title; stale data; one row unavailable; most rows unavailable (the error state); both switches off; three rows (the larger type); six rows (the 4.1").
<!-- registry:examples-levels -->
- **Examples:** the batteries of the devices in the house; a printer's ink. Each is drawn in the README.
<!-- /registry:examples-levels -->
- **Label:** the sensor's name, or the row's label input.
- **Value and bar:** the number as *Single value* writes it, with its unit. The bar is the value divided by the row's maximum (`bar_<n>_max`, 100 by default), kept between empty and full.
- **Rows:** four on the 3.5" and the 2.7" landscape, six on the 4.1"; each blueprint offers only the rows its screen has. Type and spacing as *Meters* says.
- **Widest reading:** a value of four characters with a three-letter unit (`1240 ppm`).
- **Flagged:** as *Meters* says, by two readings for all rows, each a share of the row's maximum: high (`*_high`, at or above) and low (`*_low`, at or below). Both switches are off by default (*Thresholds*).
- **Unavailable:** the value is `—` and the track is empty; most rows unavailable is the error state (*States*).

<!-- registry:inputs-levels -->
| Screen | Inputs of this page |
|---|---|
| every screen | `bar_1`, `bar_2`, `bar_3`, `bar_4`, `bar_1_label`, `bar_2_label`, `bar_3_label`, `bar_4_label`, `bar_1_max`, `bar_2_max`, `bar_3_max`, `bar_4_max`, `flag_high`, `warning_high`, `severe_high`, `flag_low`, `warning_low`, `severe_low` |
| 4.1" | also `bar_5`, `bar_6`, `bar_5_label`, `bar_6_label`, `bar_5_max`, `bar_6_max` |
<!-- /registry:inputs-levels -->

<!-- registry:layouts-levels -->
| Screen | Checked in | Not applicable | Cases |
|---|---|---|---|
| 2.7" L | normal, widest, warning, severe, gray, colour, title, stale, error, unavailable | empty | 13 |
| 3.5" | normal, widest, warning, severe, gray, colour, title, stale, error, unavailable | empty | 15 |
| 4.1" | normal, widest, warning, severe, gray, colour, title, stale, error, unavailable | empty | 14 |
<!-- /registry:layouts-levels -->

### Medication

A Glance: the time of the last press of the device's button is the hero.

- **Shows:** the time of the last press as the hero, the pill icon, the date as the Glance secondary.
- **Tested with:** on time, late (warning) and missed (severe); widest reading `20:00`; in 12-hour form the widest chip (Croatian: weekday, date, AM, missed).
- **12-hour time:** the hero shows the time without AM/PM; the date line, or the overdue chip, carries it after the date (`MO 13 APR · PM`, `MO 13 APR · PM · MISSED`). When the chip doesn't fit between the paddings, the weekday gives way first (`24 FEB · AM · MISSED`; a chip may hang S past the padding, *Spacing (internal)*, *Chips hang outward*).
- **No update stamp** in its title row: the hero time already is the last update.
- **Medication redraws by itself** when the warning and the severe time are reached (the button's last press is read from its event entity), and the press date in the Glance secondary becomes the chip. Redraw triggers: a press (the only one that flashes the LED); a template trigger per threshold (fires once when it is crossed, re-checked each minute); Home Assistant start (so a missed deadline shows at once); and a manual run (**Run actions**), which redraws the current state, for example after a changed setting.

<!-- registry:inputs-medication -->
| Screen | Inputs of this page |
|---|---|
| every screen | `button_entity`, `flag_late`, `warning_late`, `severe_late` |
<!-- /registry:inputs-medication -->

<!-- registry:layouts-medication -->
| Screen | Hero | Hero icon | Checked in | Not applicable | Cases |
|---|---|---|---|---|---|
| 2.7" L | 88 px | 88 → 56 px | normal, widest, warning, severe, gray, colour, title, unavailable | stale, error, empty | 10 |
<!-- /registry:layouts-medication -->

### Next appointment

An Event list, or the event hero when there is one event.

- **Shows:** the next events (start time, title, the label text line), or the event hero for one event, and the free time in the footer.
- **Tested with:** 9, 6, 3, 1 and no events, an event in progress (`NOW`), a grey panel.
- **In progress:** an event in progress (`NOW`) has its start time in an ink chip, and on the event hero its `NOW` label (*Severity*, *Now is not a severity*).
- **All-day events** are left out.

<!-- registry:inputs-appointment -->
| Screen | Inputs of this page |
|---|---|
| every screen | `calendar_entities`, `days_ahead` |
<!-- /registry:inputs-appointment -->

<!-- registry:layouts-appointment -->
| Screen | Hero | Hero icon | Checked in | Not applicable | Cases |
|---|---|---|---|---|---|
| 3.5" | 104 px | 88 px | normal, widest, title, error, empty | warning, severe, gray, colour, stale, unavailable | 11 |
| 4.1" | 128 px | 112 px | normal, widest, gray, title, error, empty | warning, severe, colour, stale, unavailable | 11 |
| 4.26" | 256 px | 224 px | normal, widest, gray, title, error, empty | warning, severe, colour, stale, unavailable | 12 |
<!-- /registry:layouts-appointment -->

### Plant moisture

A Key-value list of up to 22 plants, driest first if chosen.

- **Shows:** each plant's soil moisture.
- **Tested with:** 20 plants, warnings on a yellow panel and on a grey panel, most sensors unavailable (the error state).

<!-- registry:inputs-plants -->
| Screen | Inputs of this page |
|---|---|
| every screen | `plant_1`, `plant_2`, `plant_3`, `plant_4`, `plant_5`, `plant_6`, `plant_7`, `plant_8`, `plant_9`, `plant_10`, `plant_11`, `plant_12`, `plant_13`, `plant_14`, `plant_15`, `plant_16`, `plant_17`, `plant_18`, `plant_19`, `plant_20`, `plant_21`, `plant_22`, `plant_1_label`, `plant_2_label`, `plant_3_label`, `plant_4_label`, `plant_5_label`, `plant_6_label`, `plant_7_label`, `plant_8_label`, `plant_9_label`, `plant_10_label`, `plant_11_label`, `plant_12_label`, `plant_13_label`, `plant_14_label`, `plant_15_label`, `plant_16_label`, `plant_17_label`, `plant_18_label`, `plant_19_label`, `plant_20_label`, `plant_21_label`, `plant_22_label`, `sort_driest_first`, `flag_moisture_low`, `warning_moisture_low`, `severe_moisture_low` |
<!-- /registry:inputs-plants -->

<!-- registry:layouts-plants -->
| Screen | Checked in | Not applicable | Cases |
|---|---|---|---|
| 4.1" | normal, widest, warning, severe, gray, colour, title, stale, error, unavailable | empty | 9 |
<!-- /registry:layouts-plants -->

### Rain forecast

A Bar chart *with thresholds*: the next 24 hours in hourly bars on a log scale, from the hourly forecast of any weather entity; the dry state is one statement (*Chart frame (all charts)*, *Exception, nothing to show*).

- **Shows:** the bars against the warning and severe lines, the clock-time axis, and the footer's conclusion (the heaviest rain and its peak).
- **Tested with:** light rain, a heavy shower (severe), rain past the warning line, the top of the scale all day (Spanish), the same with the switch off, dry, 12-hour time (a shower, a span of more than half a day, dry), stale data, a weather entity without an hourly forecast, an unavailable weather entity with another one working, a grey panel.
- **Bars:** one per hour, starting with the current hour; a bar's value is the rain the forecast gives for that hour, read as mm/h. An hour the forecast doesn't have is dry. A wet bar's least height, the scale and the ticks are those of *Rain forecast (Netherlands)*.
- **Dry statement:** it names the end of the last bar, the current hour a day on, so it carries its weekday as a time a day away does (*Text rules*, *Dates in captions*): `DRY UNTIL SU 14:00`.
- **Thresholds:** rain per hour (*Thresholds*).
- **No hourly forecast:** the error view.

<!-- registry:inputs-rain-hourly -->
| Screen | Inputs of this page |
|---|---|
| every screen | `weather_entity`, `flag_rain_hour`, `warning_rain_hour`, `severe_rain_hour` |
<!-- /registry:inputs-rain-hourly -->

<!-- registry:layouts-rain-hourly -->
| Screen | Checked in | Not applicable | Cases |
|---|---|---|---|
| 3.5" | normal, widest, warning, severe, gray, colour, title, stale, error, unavailable, empty | — | 16 |
| 2.7" L | normal, widest, warning, severe, gray, colour, title, stale, error, unavailable, empty | — | 16 |
<!-- /registry:layouts-rain-hourly -->

### Rain forecast (Netherlands)

A Bar chart *with thresholds*: the next two hours in 5-minute bars on a log scale, from the Neerslag app's Buienalarm and Buienradar sensors; the dry state is one statement (*Chart frame (all charts)*, *Exception, nothing to show*).

- **Shows:** the bars against the warning and severe lines, the clock-time axis, and the footer's conclusion (the heaviest shower and its peak).
- **Tested with:** light rain, a heavy shower (severe), the same shower with the switch off, dry, 12-hour time (afternoon, across noon, dry), stale data, no data, the 2.7" canvas (384 × 168), a grey panel.
- **Bars:** a wet 5-minute bar is at least 3 × `line.base` high, so it reads as a bar, not a line.

<!-- registry:inputs-rain -->
| Screen | Inputs of this page |
|---|---|
| every screen | `buienalarm_entity`, `buienradar_entity`, `flag_rain_hour`, `warning_rain_hour`, `severe_rain_hour` |
<!-- /registry:inputs-rain -->

<!-- registry:layouts-rain -->
| Screen | Checked in | Not applicable | Cases |
|---|---|---|---|
| 3.5" | normal, widest, warning, severe, gray, colour, title, stale, error, unavailable, empty | — | 15 |
| 2.7" L | normal, widest, warning, severe, gray, colour, title, stale, error, unavailable, empty | — | 14 |
<!-- /registry:layouts-rain -->

### Single value

A Glance for any sensor: its number, large, with its unit.

- **Shows:** one entity's number as the hero, with its unit. The title is the entity's name unless a header title is given.
- **Tested with:** `1240 ppm`; the widest reading (`-12.5 °C`); a high reading at warning and at severe, a low one at severe; a yellow and a grey panel; a long title; stale data; an unavailable sensor (`—`); both switches off. As other configurations: an icon with a second value (`21.4 °C`, `48 %`), a short reading with an icon (`48 %`), and a reading longer than the widest (`123456 kWh`: a smaller number on the 2.7" and 3.5", the error state on the 1.4").
<!-- registry:examples-single-value -->
- **Examples:** a countdown: the days until a date; today's date. Each is drawn in the README.
<!-- /registry:examples-single-value -->
- **Unit:** after the number, on its baseline, as *Hero group*, *A unit beside the number* says. On the 1.4" the unit is the Glance secondary instead: a four-digit number needs the screen's width.
- **Widest reading:** four characters and a three-letter unit (`1240 ppm`, `-12.5 °C`). A longer reading steps down the hero ladder one rung at a time until it fits, as a word-hero does (*Glance with a word*); it is never cut.
- **The 1.4" has one size.** Its hero is fitted on the widest four digits (`4000`) and never steps, so the number keeps its size whatever the value; that size is under the Glance floor, the one exception to it (*Physical size minimums*). A reading too wide for it is the error state: "Value too long for this screen."
- **Icon:** optional, from the `icon` input, beside the number as in every hero group (*Glance*, *Too wide*). An icon the kit has no glyph for is drawn by the renderer's own icon element, a little smaller.
- **Second value:** optional, from the `secondary_entity` input: its number and unit as the Glance secondary. Not on the 1.4", where the unit has that line.
- **Flagged:** the number sits in a hero chip at its level, its unit with it, as a flagged temperature does. Two readings can be flagged: high (`*_high`, at or above) and low (`*_low`, at or below). Both switches are off by default (*Thresholds*).
- **Unavailable:** the number is `—`, with no unit.

<!-- registry:inputs-single-value -->
| Screen | Inputs of this page |
|---|---|
| every screen | `entity`, `icon`, `flag_high`, `warning_high`, `severe_high`, `flag_low`, `warning_low`, `severe_low` |
| 2.7" L | also `secondary_entity` |
| 3.5" | also `secondary_entity` |
<!-- /registry:inputs-single-value -->

<!-- registry:layouts-single-value -->
| Screen | Hero | Hero icon | Checked in | Not applicable | Cases |
|---|---|---|---|---|---|
| 1.4" | 72 px | 72 → 48 px | normal, widest, warning, severe, gray, colour, title, stale, error, unavailable | empty | 16 |
| 2.7" L | 88 px | 88 → 56 px | normal, widest, warning, severe, gray, colour, title, stale, unavailable | error, empty | 15 |
| 3.5" | 104 px | 104 → 64 px | normal, widest, warning, severe, gray, colour, title, stale, unavailable | error, empty | 17 |
<!-- /registry:layouts-single-value -->

### Sun & moon

A Timeline: sun and moon on the compass axis (*Timeline*), the five times of the day under it.

- **Shows:** the sun and the moon on the timeline (the moon with its phase; no moon marker while its position sensors are not chosen or unavailable), today's sun path, the five times of the day under it, and the day length in the footer.
- **Tested with:** night, noon, midsummer, the southern hemisphere, a new moon, a compass letter left out for a marker, the moon beside the sun below the horizon (on its left, and at the end of the track), and the widest reading: `10:44am` with the longest footer (Spanish, `DURACIÓN DEL DÍA 18h34min`).
- **Times follow `time_format`:** `07:12`, or in 12-hour form `7:12am`, with `am`/`pm` attached as a unit (*Text rules*, *Short hour labels*), because each time has a fifth of the width between the paddings: the widest, `10:44am`, fits that fifth less S on the 3.5"; `10:44 AM` does not.
- **Vertical rhythm** (no hand-set heights): from the bottom up, the footer, M, the five times in `type.data`, `space.s`, their labels in `type.label`, M, the compass row (`space.axis`), the horizon. The sky above the horizon takes everything that is left (fill before you float), from M under the title line; the highest marker keeps its disc and half its icon clear of the sky's top.

<!-- registry:inputs-sun-moon -->
| Screen | Inputs of this page |
|---|---|
| every screen | `moon_azimuth_sensor`, `moon_altitude_sensor`, `moon_phase_sensor`, `hemisphere` |
<!-- /registry:inputs-sun-moon -->

<!-- registry:layouts-sun-moon -->
| Screen | Checked in | Not applicable | Cases |
|---|---|---|---|
| 3.5" | normal, widest, title, error, unavailable | warning, severe, gray, colour, stale, empty | 14 |
<!-- /registry:layouts-sun-moon -->

### Tiles (the page)

The Tiles pattern for any entities: up to 12, one tile each.

- **Shows:** per entity its icon, its state and its label. As many tiles as the screen holds (*Tiles*); each blueprint offers only the entities its screen has.
- **Tested with:** every tile filled, with icons from the input, from the entity and one tile without; a state and labels too long for a tile, and `-12,5°C`; five entities and two entities (the grid shrinks); a long title; stale data; one entity unavailable; every entity unavailable (the error state; on the 1.4" a dash); a grey and a yellow panel.
<!-- registry:examples-tiles -->
- **Examples:** what is still open or on before you leave; the appliances and what they are doing. Each is drawn in the README.
<!-- /registry:examples-tiles -->
- **State:** a number as *Entities* writes it, with its unit; any other state in Home Assistant's own wording for it (`Closed` for a door that is `off`), which follows the language Home Assistant is set to, not the blueprint's.
- **Label:** the entity's name, or the tile's label input.
- **Icon:** the tile's icon input, else the entity's own icon; an entity with neither gets no icon. An icon the kit has no glyph for is drawn by the renderer's own icon element (*Blueprint mechanics*).
- **Flagged:** never: the page has no thresholds, as *Entities* has none.
- **Unavailable:** the state is `—`; most entities unavailable is the error state (*States*).

<!-- registry:inputs-tiles -->
| Screen | Inputs of this page |
|---|---|
| every screen | `entity_1`, `entity_1_label`, `entity_1_icon` |
| 2.7" P | also `entity_2`, `entity_3`, `entity_2_label`, `entity_3_label`, `entity_2_icon`, `entity_3_icon` |
| 2.7" L | also `entity_2`, `entity_3`, `entity_4`, `entity_5`, `entity_6`, `entity_2_label`, `entity_3_label`, `entity_4_label`, `entity_5_label`, `entity_6_label`, `entity_2_icon`, `entity_3_icon`, `entity_4_icon`, `entity_5_icon`, `entity_6_icon` |
| 3.5" | also `entity_2`, `entity_3`, `entity_4`, `entity_5`, `entity_6`, `entity_2_label`, `entity_3_label`, `entity_4_label`, `entity_5_label`, `entity_6_label`, `entity_2_icon`, `entity_3_icon`, `entity_4_icon`, `entity_5_icon`, `entity_6_icon` |
| 4.1" | also `entity_2`, `entity_3`, `entity_4`, `entity_5`, `entity_6`, `entity_2_label`, `entity_3_label`, `entity_4_label`, `entity_5_label`, `entity_6_label`, `entity_2_icon`, `entity_3_icon`, `entity_4_icon`, `entity_5_icon`, `entity_6_icon` |
| 7.5" L | also `entity_2`, `entity_3`, `entity_4`, `entity_5`, `entity_6`, `entity_7`, `entity_8`, `entity_9`, `entity_10`, `entity_11`, `entity_12`, `entity_2_label`, `entity_3_label`, `entity_4_label`, `entity_5_label`, `entity_6_label`, `entity_7_label`, `entity_8_label`, `entity_9_label`, `entity_10_label`, `entity_11_label`, `entity_12_label`, `entity_2_icon`, `entity_3_icon`, `entity_4_icon`, `entity_5_icon`, `entity_6_icon`, `entity_7_icon`, `entity_8_icon`, `entity_9_icon`, `entity_10_icon`, `entity_11_icon`, `entity_12_icon` |
| 7.5" P | also `entity_2`, `entity_3`, `entity_4`, `entity_5`, `entity_6`, `entity_7`, `entity_8`, `entity_9`, `entity_10`, `entity_11`, `entity_12`, `entity_2_label`, `entity_3_label`, `entity_4_label`, `entity_5_label`, `entity_6_label`, `entity_7_label`, `entity_8_label`, `entity_9_label`, `entity_10_label`, `entity_11_label`, `entity_12_label`, `entity_2_icon`, `entity_3_icon`, `entity_4_icon`, `entity_5_icon`, `entity_6_icon`, `entity_7_icon`, `entity_8_icon`, `entity_9_icon`, `entity_10_icon`, `entity_11_icon`, `entity_12_icon` |
<!-- /registry:inputs-tiles -->

<!-- registry:layouts-tiles -->
| Screen | Checked in | Not applicable | Cases |
|---|---|---|---|
| 1.4" | normal, widest, gray, colour, title, stale, unavailable | warning, severe, error, empty | 8 |
| 2.7" P | normal, widest, gray, colour, title, stale, error, unavailable | warning, severe, empty | 10 |
| 2.7" L | normal, widest, gray, colour, title, stale, error, unavailable | warning, severe, empty | 11 |
| 3.5" | normal, widest, gray, colour, title, stale, error, unavailable | warning, severe, empty | 13 |
| 4.1" | normal, widest, gray, colour, title, stale, error, unavailable | warning, severe, empty | 11 |
| 7.5" L | normal, widest, gray, colour, title, stale, error, unavailable | warning, severe, empty | 11 |
| 7.5" P | normal, widest, gray, colour, title, stale, error, unavailable | warning, severe, empty | 11 |
<!-- /registry:layouts-tiles -->

### To-do list

A Checklist of the items of one `todo` entity in Home Assistant.

- **Shows:** the list's open items, each with its box and its due day, then the done ones while there is room; the count in the footer. The title is the list's name unless a header title is given.
- **Tested with:** a shopping list with an overdue item, one due today, one due on Monday and three done, on a colour, a yellow and a grey panel; 14 open items (one of 40 characters, a due day twelve days off) and 4 done; a long title; an unavailable list (the error state); a list without items; every item done; flagging off; the done items left out; due days first.
<!-- registry:examples-todo -->
- **Examples:** the week's chores; a packing list. Each is drawn in the README.
<!-- /registry:examples-todo -->
- **Items:** as Home Assistant's `todo.get_items` gives them, open and done; an item's text as written.
- **Order, done items, flagging:** as *Checklist* says, by the switches `due_first` (off), `show_done` (on) and `flag_due` (on).
- **Unavailable:** an unavailable list is the error state (*States*); the page has no stale state.

<!-- registry:inputs-todo -->
| Screen | Inputs of this page |
|---|---|
| every screen | `todo_entity`, `show_done`, `due_first`, `flag_due` |
<!-- /registry:inputs-todo -->

<!-- registry:layouts-todo -->
| Screen | Checked in | Not applicable | Cases |
|---|---|---|---|
| 2.7" L | normal, widest, warning, severe, gray, colour, title, error, empty | stale, unavailable | 13 |
| 2.7" P | normal, widest, warning, severe, gray, colour, title, error, empty | stale, unavailable | 12 |
| 3.5" | normal, widest, warning, severe, gray, colour, title, error, empty | stale, unavailable | 14 |
| 4.1" | normal, widest, warning, severe, gray, colour, title, error, empty | stale, unavailable | 13 |
| 7.5" L | normal, widest, warning, severe, gray, colour, title, error, empty | stale, unavailable | 12 |
| 7.5" P | normal, widest, warning, severe, gray, colour, title, error, empty | stale, unavailable | 12 |
<!-- /registry:layouts-todo -->

### Value with details

A Hero dashboard *with a chart or list* for any sensor: its number large, other values beside it, its last hours under it.

- **Shows:** one sensor's number as the hero with its unit and an optional icon; up to four detail rows, each another entity's label and value; a chart of the sensor's last hours as one line on the automatic scale (*Bar chart and Line chart*), without a footer.
- **Tested with:** a room's CO2 with its climate beside it; the number at warning and at severe, on a colour, a yellow and a grey panel; the widest readings (`-12.5 °C`, flagged low, with a label too long for its row); a long title; stale data; the sensor and a detail unavailable; no history (the error block in the chart's half); thresholds set with both switches off; one detail row; no detail rows and no icon.
<!-- registry:examples-value-details -->
- **Examples:** the house's power use with solar, battery and grid; the temperature outside with humidity, wind and rain. Each is drawn in the README.
<!-- /registry:examples-value-details -->
- **Number and unit:** as *Single value* writes them. An unavailable sensor is a dash without unit or icon.
- **Detail rows:** three on the 4.1", four on the 7.5"; the 4.1" has no icon, the number, its unit and the rows fill the width. A row's value as *Entities* writes it, or Home Assistant's own wording of a state; the detail column is as wide as a label of 11 characters (`TEMPERATURE`) and the widest value (`1240 ppm`), and a longer label is cut.
- **Chart:** as *History graph* draws it: the hours input, the automatic scale, the threshold lines and fills.
- **Flagged:** the high and low thresholds flag the number (the hero chip) and the chart alike (`*_high`, `*_low`; both switches off by default, *Thresholds*). Detail rows are never flagged.
- **Screens:** the 4.1", the 7.5" and the 7.5" portrait. On smaller screens the number and the chart don't fit together: *Single value* and *History graph* each show one of them.

<!-- registry:inputs-value-details -->
| Screen | Inputs of this page |
|---|---|
| every screen | `entity`, `detail_1`, `detail_2`, `detail_3`, `hours`, `detail_1_label`, `detail_2_label`, `detail_3_label`, `flag_high`, `warning_high`, `severe_high`, `flag_low`, `warning_low`, `severe_low` |
| 7.5" L | also `detail_4`, `icon`, `detail_4_label` |
| 7.5" P | also `detail_4`, `icon`, `detail_4_label` |
<!-- /registry:inputs-value-details -->

<!-- registry:layouts-value-details -->
| Screen | Hero | Hero icon | Checked in | Not applicable | Cases |
|---|---|---|---|---|---|
| 4.1" | 56 px | 48 px | normal, widest, warning, severe, gray, colour, title, stale, error, unavailable | empty | 15 |
| 7.5" L | 104 px | 88 px | normal, widest, warning, severe, gray, colour, title, stale, error, unavailable | empty | 15 |
| 7.5" P | 104 px | 88 px | normal, widest, warning, severe, gray, colour, title, stale, error, unavailable | empty | 14 |
<!-- /registry:layouts-value-details -->

### Weather and calendar

A *Hero dashboard with a chart or list*: the weather's hero band over the calendar's date-grouped list, in two equal halves, on the 7.5" portrait.

- **Shows:** the current temperature as the hero with its condition icon (and the moon badge) and the 7.5" detail rows in the top half; the coming days with their events in the bottom half.
- **Tested with:** −12° with the moon badge, an official warning with pollen at severe (both take a detail row), an event in progress, a full calendar that overflows, an empty day, no calendar chosen, weather unavailable, stale weather, a grayscale panel, a long title.
- **Rules:** the weather's (*Weather at a glance and Weather*: thresholds, *Pollen*, *Override order*, with the 7.5" detail rows and their make-way order) and the calendar's (*Calendar*: an event in progress is an ink row chip, today by name).

<!-- registry:inputs-weather-calendar -->
| Screen | Inputs of this page |
|---|---|
| every screen | `weather_entity`, `current_temp_sensor`, `pollen_sensor`, `moon_phase_sensor`, `weather_warning_sensor`, `weather_warning_text_sensor`, `calendar_entities`, `pollen_type`, `days_shown`, `flag_temp_low`, `warning_temp_low`, `severe_temp_low`, `flag_temp_high`, `warning_temp_high`, `severe_temp_high`, `flag_wind_high`, `warning_wind_high`, `severe_wind_high`, `flag_rain_hour`, `warning_rain_hour`, `severe_rain_hour`, `flag_rain_day`, `warning_rain_day`, `severe_rain_day`, `flag_pollen_high`, `warning_pollen_high`, `severe_pollen_high`, `warning_conditions`, `severe_conditions`, `location_string` |
<!-- /registry:inputs-weather-calendar -->

<!-- registry:layouts-weather-calendar -->
| Screen | Hero | Hero icon | Checked in | Not applicable | Cases |
|---|---|---|---|---|---|
| 7.5" P | 152 px | 128 px | normal, widest, warning, severe, gray, colour, title, stale, error, unavailable, empty, alert, pollen 0, pollen widest | — | 35 |
<!-- /registry:layouts-weather-calendar -->

### Weather at a glance and Weather

Two pages with the same content: Weather at a glance, on the 1.4" and the 3.5", and Weather, the Hero dashboard *with forecast strips*, from the 2.7" to the 7.5", landscape and portrait.

- **Shows:** the current temperature as the hero, with the condition icon (and the moon badge, day and night: *When to use an icon*); on the Hero dashboard the detail rows (today's rain, wind, high/low; humidity, pressure, sunrise and sunset where there is room; the pollen row), the hour strip, and the day strip where the screen has one (*Style choices*, Forecast horizon; a forecast table on the 2.7" portrait); on the Glance today's high/low as the Glance secondary and the footer (*Glance with a footer*; *Override order*, Footer).
- **Tested with:** −12° (the widest reading), a negative temperature with the moon badge, an official warning (KNMI code orange), a current condition alert, pollen at 0 and high, stale data, no data (the error block), a black/white panel, a 4-gray panel, 12-hour English, a long title.
- **Detail rows:** On 800 × 480 the labels are written out (`PRESSURE`, `HUMIDITY`, `SUNRISE`, `SUNSET`; the `*_l` keys in `ds_wtxt`), and pressure carries its unit (`1012 hPa`, from the weather entity's `pressure_unit`). Next to a weather hero, as the *Detail rows* module (flagged: `CODE YELLOW … FOG`, `NOW … THUNDERSTORM`). Order: **today's rain, wind**, then humidity / pressure / sunrise / sunset, **high/low**, then the pollen row last (high/low beats humidity: the 7.5" shows rain, wind, pressure, sunrise, sunset, max/min). Which row makes way for the alert row or the pollen row: *Override order*. The 2.7" portrait has room for one text line under its icon: high/low · today's rain, or wind with the *Rain or wind* input (*Override order*).
- **Sunrise and sunset** are detail rows, labelled with words (`SUNRISE` / `SUNSET`).

#### Pollen

Pollen is information you act on (taking allergy medication), so it **has priority** and is never moved by other content: **the pollen row**, the last detail row on every Hero dashboard; a block above the footer (2.7" portrait); and on Glance, which has no rows, the right of the footer whenever it is above zero and nothing is flagged, alone where the conclusion doesn't fit beside it (flagged pollen joins the *Override order*). It is footer material nowhere else. **Every weather layout has the pollen inputs.** It shows **the type and the count, nothing else**: no level graphic. The level only decides the fill: plain text below warning, a warning chip at the sensor's *high*, a severe chip at *very high*; with count inputs, a warning chip from the warning count and a severe chip from the severe count (*Weather thresholds*). In the pollen row the type is the label and the count the value (`BIRCH … 96 ppm`); flagged, it is one chip spanning both, like any detail row. The detail column is wide enough for a 3-digit count (*Space*); a 4-digit count cuts the type short, as any label gives way to its value (*A label never overlaps its value*). On the 2.7" portrait it is one row (type, count), without an icon. At level 0 the pollen row is left out and the row that made way for it is back; on the 2.7" portrait one more day row takes its place (*fill before you float*).

#### Weather thresholds

- **Pollen uses the sensor's own level** (Kleenex reports low / moderate / high / very high per type). A count in the pollen inputs overrides it, for sensors without levels.
- **Conditions never put a chip on the icon** (a fill around an icon outweighs the number and is a chip without text). Instead:
  - **Hours and days:** the cell's label (`15:00`, `MON`) becomes the chip; the icon below it stays plain.
  - **Current condition:** named in a chip in the **alert row** (`NOW` + `THUNDERSTORM` as the first detail row in the Hero dashboard; the footer chip on Glance and the 2.7" portrait, where it competes with pollen, rain and wind and wins a tie). Names come from `ds_wtxt.cond` (15 conditions, 8 languages).
  - **The alert row holds one thing:** an official warning if there is one, else the current condition at warning or severe level.
- **Official weather warnings** (KNMI, Meteoalarm) come in through two optional inputs on every weather blueprint: a level sensor (yellow / minor / moderate = warning; orange, red / severe / extreme = severe) and a text sensor for the warning's subject (`Thunderstorm`). **The subject** is the alert's weather condition when it sends one (KNMI: `condition: fog` → `FOG`, from `ds_wtxt.cond`), else its title / event / headline. A subject shows **whole or not at all**: no word cutting (it can leave just an adjective, `DENSE`) and no ellipsis. Where the subject doesn't fit, the code alone carries the chip (`CODE ORANGE`); in a footer chip the subject alone comes first when the pair doesn't fit (`FOG`). Every other flagged row (`DCHIP`) follows *A label never overlaps its value*. A warning beats every other alert: the footer chip on Glance and the 2.7" portrait (`CODE ORANGE THUNDERSTORM`, or only the subject where that doesn't fit, else the code) and the first detail row in the Hero dashboard (`CODE ORANGE` and the subject as one row chip; *Override order*). The condition icon never changes.
- Where a value is shown, its chip follows the threshold: hero temperature, hour and day cells (temperature, rain; the label for the condition), detail rows, the footer. **Today's high/low** (`hilo_k`) takes the same level as today's day forecast, wherever it shows: the MAX/MIN row, the Glance secondary, the 2.7" portrait text line under the icon, the day cell.
- **Conditions are kinds of weather, not measurements.** Only conditions that are a risk by themselves warn by default. Fog, snow and wind are flagged through the temperature and wind thresholds and official warnings (KNMI issues code yellow for dense fog and slippery roads), so they get no chip of their own.

#### Override order

One order everywhere a single place has to choose (the `PICK` macro):

1. An **official weather warning**.
2. Otherwise the **most severe** flagged item; on a tie, in this order: the current **condition**, **pollen**, **today's rain**, **wind**, **today's high/low**. An item that has a place of its own on the layout is left out of the pick and flagged there.

Where it applies:

- **Glance secondary:** Weather at a glance: today's high/low, always; flagged, it is the chip (*Glance with a footer*). Medication: the date becomes the overdue chip (date · status; its redraws are under *Medication*).
- **2.7" portrait, the text line under the icon:** high/low · today's rain (or wind), always (`13°/6° · 2.6mm`). Flagged high/low is the chip (`MAX/MIN 11°/3°`) and rain follows only if it fits. No other chip takes this line: an alert goes to the footer.
- **Detail rows (Hero dashboard):** the alert row (official warning, else the current condition) becomes the first row, and the pollen row (pollen above 0) the last. Each takes a row's place so the block keeps its size, and **a row with a chip makes way last**. Each layout names a make-way order for the alert row and one for the pollen row. The alert row chooses first: the first unflagged row still shown in its order makes way, else the first warning-level one, else the first in the order. Then the pollen row chooses the same way. One rule for every layout (`DROWS`):
  - 7.5" (landscape and portrait, and *Weather and calendar*), 4.26": alert row and pollen row: <!-- v:order:_wx -->pressure, wind, high/low<!-- /v -->. Sunrise and sunset never make way.
  - 3.5": both: <!-- v:order:weather_35 -->humidity, wind, high/low, rain<!-- /v -->.
  - 4.1": both: <!-- v:order:weather_41 -->humidity, wind, rain<!-- /v -->.
  - 2.7" landscape: both: <!-- v:order:weather_27l -->wind, high/low, rain<!-- /v -->.
- **Footer:** keeps its conclusion; it becomes the chip when the rain it is about is flagged (the most severe of today's total and the forecast hours; never when the whole forecast is dry). Alerts never move to the footer: you read a screen from the top, and not every layout has one. **The exception is a layout without detail rows** (Weather at a glance, the 2.7" portrait): there the footer is the alert's place, so the alert never takes a value's. The picked item is the footer chip and goes before the conclusion and its rain chip; high/low is left out of the pick (it is flagged on its own line), and on the 2.7" portrait pollen too (it has its row). An official warning follows *Weather thresholds* (whole or not at all: `CODE ORANGE THUNDERSTORM`, else `THUNDERSTORM`, else `CODE ORANGE`). With no alert: the conclusion where it fits whole (`RAIN UNTIL 17:00`), and on Glance pollen at the right (`BIRCH 96 ppm`, *Pollen*).
- **Title row:** the stale chip replaces the stamp. **Error state:** replaces everything below the title.

#### Weather inputs

<!-- registry:inputs-weather-glance -->
| Screen | Inputs of this page |
|---|---|
| every screen | `weather_entity`, `current_temp_sensor`, `pollen_sensor`, `moon_phase_sensor`, `weather_warning_sensor`, `weather_warning_text_sensor`, `pollen_type`, `flag_temp_low`, `warning_temp_low`, `severe_temp_low`, `flag_temp_high`, `warning_temp_high`, `severe_temp_high`, `flag_wind_high`, `warning_wind_high`, `severe_wind_high`, `flag_rain_hour`, `warning_rain_hour`, `severe_rain_hour`, `flag_rain_day`, `warning_rain_day`, `severe_rain_day`, `flag_pollen_high`, `warning_pollen_high`, `severe_pollen_high`, `warning_conditions`, `severe_conditions` |
<!-- /registry:inputs-weather-glance -->

<!-- registry:layouts-weather-glance -->
| Screen | Hero | Hero icon | Checked in | Not applicable | Cases |
|---|---|---|---|---|---|
| 1.4" | 80 px | 80 → 48 px | normal, widest, warning, severe, gray, colour, title, stale, error, unavailable, alert, pollen 0, pollen widest | empty | 37 |
| 3.5" | 88 px | 88 → 56 px | normal, widest, warning, severe, gray, colour, title, stale, error, unavailable, alert, pollen 0, pollen widest | empty | 28 |
<!-- /registry:layouts-weather-glance -->

<!-- registry:inputs-weather -->
| Screen | Inputs of this page |
|---|---|
| every screen | `weather_entity`, `current_temp_sensor`, `pollen_sensor`, `moon_phase_sensor`, `weather_warning_sensor`, `weather_warning_text_sensor`, `pollen_type`, `flag_temp_low`, `warning_temp_low`, `severe_temp_low`, `flag_temp_high`, `warning_temp_high`, `severe_temp_high`, `flag_wind_high`, `warning_wind_high`, `severe_wind_high`, `flag_rain_hour`, `warning_rain_hour`, `severe_rain_hour`, `flag_rain_day`, `warning_rain_day`, `severe_rain_day`, `flag_pollen_high`, `warning_pollen_high`, `severe_pollen_high`, `warning_conditions`, `severe_conditions` |
| 2.7" P | also `wind_or_precipitation`, `start_with_today` |
| 4.1" | also `start_with_today` |
| 4.26" | also `start_with_today`, `location_string` |
| 7.5" L | also `start_with_today`, `location_string` |
| 7.5" P | also `start_with_today`, `location_string` |
<!-- /registry:inputs-weather -->

<!-- registry:layouts-weather -->
| Screen | Hero | Hero icon | Hour / day cells | Checked in | Not applicable | Cases |
|---|---|---|---|---|---|---|
| 2.7" L | 72 px | 64 px | 4 / — | normal, widest, warning, severe, gray, colour, title, stale, error, unavailable, alert, pollen 0, pollen widest | empty | 28 |
| 2.7" P | 72 px | 64 px | — | normal, widest, warning, severe, gray, colour, title, stale, error, unavailable, alert, pollen 0, pollen widest | empty | 33 |
| 3.5" | 64 px | 56 px | 4 / — | normal, widest, warning, severe, gray, colour, title, stale, error, unavailable, alert, pollen 0, pollen widest | empty | 23 |
| 4.1" | 80 px | 64 px | 4 / 5 | normal, widest, warning, severe, gray, colour, title, stale, error, unavailable, alert, pollen 0, pollen widest | empty | 30 |
| 4.26" | 160 px | 136 px | 6 / 5 | normal, widest, warning, severe, gray, title, stale, error, unavailable, alert, pollen 0, pollen widest | colour, empty | 35 |
| 7.5" L | 160 px | 136 px | 6 / 5 | normal, widest, warning, severe, gray, colour, title, stale, error, unavailable, alert, pollen 0, pollen widest | empty | 33 |
| 7.5" P | 160 px | 136 px | 5 / 5 | normal, widest, warning, severe, gray, colour, title, stale, error, unavailable, alert, pollen 0, pollen widest | empty | 32 |
<!-- /registry:layouts-weather -->

### Mocked-up pages

Bin day, Room sign, Appliance run, Departures, Solar & battery, Month overview, Message board, Now playing and Guest Wi-Fi: their patterns and layouts are in the table above, their rules with the pattern versions they use.

## Blueprint mechanics

What every blueprint does the same way; where it can, through a shared part that is written once. How the blueprints are built and checked (the registry, reference renders, the release, ink placement and the pixel check) is in [building.md](building.md).

- **Input sections:** every blueprint groups its inputs in the same five sections, in this order, each only when it has inputs. `lib/inputs_std.py` writes them, and its `--lint` fails a blueprint that breaks the scheme.
  1. **Display and schedule** (open): `displays`, then `button_entity` (Medication), `automation_trigger` and `automation_conditions`.
  2. **Content** (open): the page's main entity first, then its other entities, then the options that change what it shows.
  3. **Thresholds** (collapsed): `flag_<what>`, `warning_<what>`, `severe_<what>` for each reading (*Thresholds*). The page sets its chart scale; it is not an input.
  4. **Appearance** (collapsed): `header_title` (blank for the translated default), `location_string`, `time_format` (12h/24h), `weekday_format` (en/de/nl/fr/es/pl/hr/sv) and `rotate` (0/90/180/270, all four always offered; the description explains native vs upright).
  5. **Advanced** (collapsed): `stale_after`, `led_color`, `led_flash_delay` and `font_dir`. The LED inputs are there wherever a button can start the redraw: the LED confirms the press. A blueprint that redraws on a change (Doors & windows) has none.
- **Required inputs:** `displays`, the trigger, and the page's main entity (the weather entity, the calendars, the CO2 sensor, the first entry of a list, the doors and windows, the medication button, the EnergyZero integration). Every other input has a default, and an optional entity left empty removes its part of the page. Rain forecast (Netherlands) has no main entity: it needs one of its two sources. Sun & moon has none either: it reads Home Assistant's own sun.
- **Input names:** the device input is always `displays`, also where it takes one device (Medication). Numbered entries are `<name>_<n>` with `<name>_<n>_label` (`entity_1`, `plant_1`, `bar_1`). Thresholds are `warning_<what>` and `severe_<what>`, their switch `flag_<what>`. A blueprint's variables keep the names its drawing reads, so renaming an input never changes the drawing.
  - `stale_after` wherever the data comes from reporting entities (<!-- v:stalePages -->Claude usage, CO2 graph, Entities, History graph, Levels, Plant moisture, Rain forecast, Rain forecast (Netherlands), Single value, Tiles, Value with details, Weather, Weather and calendar, Weather at a glance<!-- /v -->); see *Title row* for the exempt blueprints.
  - The panel is never an input: a page drawn on two screens is two blueprints (Rain forecast on the 3.5" and on the 2.7" landscape).
- **Texts:** every blueprint's strings live in `ep_i18n.jinja`, written from the page definitions (per page, `EP_TXT['<page>']`, which the blueprint's `language_map` reads; the weekday and month lists once, in `pages/_shared.yaml`) and `wx_txt.yaml` (the weather words, `ds_wtxt`), keyed by the 8 language codes, holding weekday/month names and every user-facing string (including the empty, error and stale strings). Paired with separate `weekday_short_map` / `months_short_map` dicts, which read `EP_DAYS_SHORT` / `EP_MONTHS_SHORT`. The update stamp uses weekday + time (`SU 17:58`); dates in content use `SU 8 NOV`. Don't fold them into `language_map`.
- **One set.** A release gives its templates and its blueprints the same set id: a short hash of the four templates as built, so it changes when the templates change and only then (`lib/set_id.py`). Every blueprint hands its id to the drawing, and the templates compare it with theirs. When they differ, or the blueprint has none, the templates draw the title row and the error block and nothing else: the message (`UPDATE TEMPLATES AND BLUEPRINT`, translated) and, on new lines under it, the two ids (`BLUEPRINT hjnenx · TEMPLATES udrrap` on one line where that fits, else one each; a blueprint without an id shows `—`), the lines centred as one block in the title's type. Templates from before this rule can't tell a newer blueprint apart, and missing templates still fail with `TemplateNotFound`: nothing can draw then.
- **Shared parts:** the texts, the stale test (`ds_stale`), the drawing step, the button flash and the description's template note are written once and put into every blueprint by the build (the text maps by `lib/shared.py`, the others by the generator from `pages/_shared.yaml`); `lib/shared.py --lint` fails a blueprint whose copy differs.
- **Button feedback (LED flash):** every blueprint with a trigger input confirms a press of the device's own `event.*` button; flash before the ~30 s redraw, using `opendisplay.activate_led` with `continue_on_error: true`, inputs `led_color` (default green) and `led_flash_delay` (default <!-- v:shared:led_flash_delay -->500 ms<!-- /v -->), `flash_count1: 2`, `brightness: 16`.
  - In generic-trigger blueprints, flash only when `trigger.entity_id` is an `event.*` entity belonging to a device.
  - Accept both `button_down` and `button_up`: a sleeping device can deliver either half.
  - Use `mode: single` + `max_exceeded: silent`. A blueprint that redraws on a change (Doors & windows) is `mode: queued` instead, so a second change during a redraw isn't lost.
- **Board ≠ panel.** On Solum ESLs the button comes with the Pro board, which exists in 1.4", 2.7", 3.5" and 4.1". "Has a button" says nothing about size. The board type and the button entity both come from the firmware configuration too: a Core ESL configured as Pro gets a button entity in Home Assistant without having a button.
- **Names.** Labels never read the `friendly_name` attribute (deprecated from Home Assistant 2026.11). A label falls back to the part it needs: `device_name()` for things named by their own Home Assistant device (plants), `entity_name()` for a sensor on a shared device (usage bars, entity rows), then the other one, then the entity ID. `entity_name()` is empty for a device's main entity.
- **Names and files.** A blueprint is named after its page and its screen: `E-paper <Page> <size>"`, with `landscape` or `portrait` for a screen that has both (`E-paper Weather 2.7" landscape`). Its file is `epaper-blueprint-<size>-<page>[-landscape|-portrait].yaml`, the page's name in lowercase with hyphens (`epaper-blueprint-2.7-weather-landscape.yaml`). Both are generated (`lib/layouts.py`), never typed: the page's name and the screen's name come from the registry, the screens a page is drawn on from its page definition (`layouts`); a layout's public name in the templates is its key (`weather_27l`).
- **Firmware sizes.** Tiers are keyed by pixels and pitch (see *Tiers*); the blueprint files keep the size the screen is known by (`registry.yaml` `screen_names`: `epaper-blueprint-1.4-…`, `-2.7-`, `-3.5-`, `-4.1-`, `-4.26-`, `-7.5-`). That is the size the device's firmware reports, except where *Tiers* notes another. The firmware size matches the panel's active area (*Tiers*; the 2.7" is often sold as 2.9"). Check the firmware's pixel size against the real panel before trusting it: a test image with labelled edge lines settles it. A 168×384 panel configured as 184×384 silently loses 16 px on one long edge (at `rotate: 270`, the top of a landscape layout).
- **Moon phase sensor:** expose an optional `moon_phase_sensor` input. When it is blank, fall back to `(integration_entities('moon') | first) | default('notfound')`. Never hardcode `sensor.moon_phase`.
- **Payload as a list:** macros append element dicts to `ns.el` (`{% set ns.el = ns.el + [{...}] %}`) and the payload is the list itself, so conditional elements can never leave stray commas.
- **Background:** `white`.
- **Font files, not a font input.** In drawcustom, weight is a separate file. A blueprint needs at most the seven files in *Type tokens*. The size is fixed by the tier, so the filenames are tokens (`font.*`, `EP_FONT` in `ep_tokens.jinja`), never inputs. Components pick a font through the `type.*` roles; 12 and 16 are always Bold (*Physical size minimums*), so the kit's short names `f12`/`f12b` and `f16`/`f16b` point to the same file.
  - The only font input is an optional `font_dir` (default empty, meaning drawcustom's own font folder).
  - Bold is never faked with a stroke or offset: it's always the Bold file.
  - The filenames are exactly as in the bundle. A bare filename resolves to drawcustom's font folder (proven on the devices).
- Always pass `"font"` on every text element. Never fall back to the device default font.
- **Icons are drawn as text.** Every MDI icon goes out as a `text` element in `materialdesignicons-webfont.ttf` (the `I` macro and its `MDI` name → character table), not as drawcustom's `icon` element. The icon element anti-aliases: odl-renderer passes `fontmode="1"` as a `draw.text()` argument, which Pillow ignores, and its gray edges turn red on BWRY panels (rays of a 16 px sun, the stars of `weather-night`). The text element sets `draw.fontmode = "1"` and draws pixel-exact, at the same position. A name missing from the table falls back to the icon element, so add every new icon to `MDI`.
- **Charts in drawcustom:**
  - Thresholds: `line` with `dashed`, `dash_length`, `space_length`.
  - Series: runs of `line` segments, or the history `plot` element if OpenDisplay supports it **[verify]**.
  - Severe fills: `polygon`.
- **Element budget.** Home Assistant's recorder drops the event of any action call above 32 KB, so a chart payload stays under about 28 KB in the worst case. Pieces that touch and draw the same pixels are drawn as one element: neighbouring flat series segments at one height, adjoining fills of one colour with a level top, and touching notch pieces on one threshold line. The image doesn't change; the 3.5" CO2 chart went from 394 to 286 elements (37 KB to 27 KB) in its busiest test case.

## To verify on hardware

Proven: TRMNL text and Space Grotesk heroes on BWRY ESLs (1.4", 2.7", 3.5", 4.1"), on the 4.26" mono kit and the 7.5" 4-gray device; black on yellow on a 4.1" BWRY ESL; native TRMNL21 over the 2× TRMNL24 on the 4.26"; bare font filenames.

1. The same renders on a BWR, BWY and B/W-only device.
2. Gray levels on the 4.1" EN05 once it runs as 4-gray (proven on the 7.5": see *Values per panel*).
3. Black on-severe text (black on yellow) is readable on a real BWY device at TRMNL16.
4. The physical minimums hold up at the intended viewing distances on each device.
5. `line.base` outlines and `line.tick` ticks are exact at every rotation.
6. A QR code with a quiet zone of 2 QR modules (the Wi-Fi code on the 1.4") scans with common phone cameras; and the <!-- v:dt:QR_MODULE_MM -->0.4<!-- /v --> mm QR module minimum holds at arm's length.
7. The 7.5" portrait: a 480 × 800 payload drawn with `rotate` 90 or 270 on a panel whose firmware reports 800 × 480 lands upright and uncropped, and which of the two is upright for the usual mounting.
8. The 4.1" weather's day icons at <!-- v:layout:weather_41:icon.stripDay -->32<!-- /v --> px (fitted; were 24): the day strip reads at arm's length without crowding the cells.
9. Warning outlines in the padding: on the 7.5" and 4.26" a detail-row outline reaches 7 and 8 px into the padding (S + `line.base`); it stays inside the visible area, clear of the bezel.
10. Lines on the 1.4": every component draws its lines at `line.base`, and the first to draw one there is the footer of Weather at a glance (its line and its outlined chip, item 18); no 1.4" layout has a list or a chart yet.
11. The history `plot` element: whether OpenDisplay draws a series with it (*Blueprint mechanics*); until then a series is runs of `line` segments.
12. Single value: the unit beside a large number (`type.secondary`'s size next to an 88 or 104 px numeral) reads as part of the reading; an icon the kit has no glyph for (drawn by the renderer's icon element) sits acceptably beside the number.
13. Single value on the 1.4": the number at its one size (under the Glance floor) still reads from where the label is used.
14. Tiles: icons the kit has no glyph for, drawn by the renderer's icon element at tile size (their soft edges on a panel with colour); Home Assistant's wording of a state in a language other than English at the tile's width.
15. Value with details: the unit after a flagged number (it starts past the chip) and the number at its fitted size on the 4.1" beside three detail rows.
16. Rain forecast: the hourly forecast of real weather entities (one whose forecast starts at the next hour leaves the first bar dry; one that reports rain in inches is read as mm).
17. Energy price (EnergyZero): not yet run against a real EnergyZero entry. To prove there: the price arrives in euros per kWh, an hour's start is read as the right hour of the day, and the day the clock changes (23 or 25 hours).
18. Weather at a glance and Weather on the 2.7" portrait, on a panel without a warning colour: the outlined footer chip under an outlined high/low chip and an outlined hero (three outlines on the 1.4"), and under the outlined pollen row on the 2.7" portrait, where touching outlines join into one box.
19. To-do list: not yet run against a real `todo` entity. To prove there: `todo.get_items` gives the open and the done items, and `due` as a date or as a date and time.

## Open items

- **Month:** where rows are tight (2.7" landscape) the event dots touch the next row: drop them, or underline the day. To decide.
- **Key-value rows on the 1.4":** a long value pushes the label to `...`; proposed: keep the label and shorten the value (packages, departures). To decide.
- **Size classes:** every rule that uses small / medium / large can be written as one of two millimetre thresholds (<!-- v:dt:MEDIUM_SHORT_MM -->35<!-- /v --> mm and <!-- v:dt:LARGE_SHORT_MM -->80<!-- /v --> mm short side); proposed: drop the class names. To decide.
- **Energy price on the 2.7" portrait:** offer it (24 narrow bars) or leave it out. To decide.
- **LED on a severe state:** flash the device's LED when a page turns severe (a door left open, a missed medication): which pages, which colour, and whether it repeats until the state clears. To decide.
- **Two modules side by side** on a Hero dashboard with a chart or list (7.5" and 7.09"): one module is the rule today. To decide when a page needs two.
- **Type on large and dense screens:** the step up is one TRMNL step for every large screen, whatever its size, so a 13.3" derives the 7.5"'s type sizes; and where the data is already TRMNL21 (*Type tokens*) `type.primary` is no larger than `type.data`, so a list loses its size hierarchy. Proposed: set the type roles by physical size and reading distance, using the 2× cuts. To decide when the first screen above the 7.5" gets a layout, and for the 4.26".
- **Outline text font on dense large screens** (from 0.09 mm per pixel): Space Grotesk with letter-spaced capital labels is the candidate (type test card v1); TRMNL stays the system font until it is tested on the 7.09". To decide after that test.

## Glossary

Every named part of the design system, with its kind (`—` when it is a region, a property or a state rather than a part), and what it is part of. Other words for the same thing are rewritten to these names.

<!-- registry:glossary -->
| Term | Kind | Part of | What it is |
|---|---|---|---|
| **alert row** | component | Detail rows | the first detail row when a page flags something that has no row of its own (the weather: an official warning or the current condition) (not: alert slot) |
| **Blueprint** | vocabulary | — | see *Vocabulary* |
| **Canvas** | vocabulary | — | see *Vocabulary* |
| **Chart** | module | — | see *Modules* |
| **chart frame** | — | Chart | what bar and line charts share: plot, label margin, clock-time axis, thresholds |
| **Checkbox row** | component | — | see *Components* |
| **Checkbox rows** | module | — | see *Modules* |
| **Chip** | component | — | see *Components* |
| **clock-time axis** | — | Chart | the baseline with ticks and clock times under the plot |
| **Code block** | module | — | see *Modules* |
| **Component** | vocabulary | — | see *Vocabulary* |
| **Date-grouped list** | module | — | see *Modules* |
| **day strip** | module | Strip | the strip of day cells |
| **detail column** | — | Detail rows | the width the detail rows take: widest label + space.l + widest value (not: details column) |
| **Detail rows** | module | — | see *Modules* (not: details rows) |
| **Device** | vocabulary | — | see *Vocabulary* |
| **Empty** | — | States | nothing to show: the empty statement |
| **Empty statement** | component | — | see *Components* (not: empty message) |
| **Error** | — | States | no data or a misconfiguration: the error block under the title row |
| **Error block** | module | — | see *Modules* (not: severe block) |
| **ESL** | vocabulary | — | see *Vocabulary* |
| **Event hero** | module | — | see *Modules* |
| **Event list** | module, pattern | — | see *Modules*, *Patterns* |
| **Event row** | component | — | see *Components* |
| **Footer** | module | — | see *Modules* (not: footer band, summary line) |
| **Forecast row** | component | — | see *Components* |
| **Forecast table** | module | — | see *Modules* |
| **Glance secondary** | component | — | see *Components* (not: Glance secondary slot, secondary slot, secondary band, secondary line) |
| **Hero band** | module | — | see *Modules* |
| **Hero block** | module | — | see *Modules* |
| **Hero chip** | component | — | see *Components* |
| **hero column** | — | Hero band | the space the hero group is centred in, left of the detail rows |
| **Hero group** | component | — | see *Components* |
| **hero ladder** | token | — | the hero sizes (*Style choices*, Hero ladder) |
| **hero numeral** | component | Hero group | the number of a hero group, in Space Grotesk Bold at the hero size |
| **Hour cell / Day cell** | component | — | see *Components* |
| **hour strip** | module | Strip | the strip of hour cells |
| **Icon** | component | — | see *Components* |
| **icon ladder** | token | — | the icon sizes (`icon.ladder`; *Style choices*, Icon ladder) |
| **ink chip** | component | Chip | a chip filled with ink: the stale chip (an outline where warnings are outlines), an event in progress, and severe on black/white panels |
| **Input** | vocabulary | — | see *Vocabulary* |
| **Key-value list** | module, pattern | — | see *Modules*, *Patterns* |
| **Key-value row** | component | — | see *Components* |
| **label margin** | — | Chart | the space right of the plot for the scale and threshold values |
| **Layout** | vocabulary | — | see *Vocabulary* |
| **Level meter** | module | — | see *Modules* |
| **Meters** | module, pattern | — | see *Modules*, *Patterns* |
| **Module** | vocabulary | — | see *Vocabulary* |
| **Month grid** | module | — | see *Modules* |
| **Moon badge** | component | — | see *Components* (not: moon-phase badge) |
| **now-marker** | component | Progress bar | the line across a progress bar for "now in the period" (not: now marker) |
| **Page** | vocabulary | — | see *Vocabulary* |
| **page definition** | — | Page | everything a page's blueprints are generated from besides its layouts: inputs, data, texts, description (pages/<page>.yaml) |
| **Panel** | vocabulary | — | see *Vocabulary* |
| **Pattern** | vocabulary | — | see *Vocabulary* |
| **plot** | — | Chart | the area the bars or the series are drawn in (not: plot area) |
| **pollen row** | component | Detail rows | the weather's last detail row while pollen is above 0: type and count (a forecast row on the 2.7" portrait) (not: pollen slot) |
| **Progress bar** | component | — | see *Components* (not: usage bar) |
| **QR code** | component | — | see *Components* |
| **row chip** | component | Chip | one chip spanning the label and the value of a row |
| **Screen** | vocabulary | — | see *Vocabulary* |
| **severe chip** | component | Chip | a chip at the severe level |
| **shared part** | — | Blueprint | a piece every blueprint has, written once (texts, stale test, drawing step, button flash, template note) |
| **spec** | — | Layout | the file that draws a layout in pixels (`src/specs/`); a layout may reuse another layout's spec with its own tokens |
| **Stale** | — | States | the newest data is older than stale_after: the stale chip |
| **stale chip** | component | Title row | the update stamp in an ink chip with "!" when the data is old (an outline with "!" where warnings are outlines) (not: stale stamp chip, stale stamp) |
| **Strip** | module | — | see *Modules* (not: forecast strip) |
| **Text block** | module | — | see *Modules* |
| **Tier** | vocabulary | — | see *Vocabulary* |
| **Tiles** | module, pattern, page | — | see *Modules*, *Patterns*, *Pages* |
| **Timeline** | module, pattern | — | see *Modules*, *Patterns* (not: Track, sun & moon track) |
| **title line** | component | Title row | the line under the title row (not: title rule) |
| **Title row** | module | — | see *Modules* |
| **Token** | vocabulary | — | see *Vocabulary* |
| **track** | component | Progress bar | the outlined bar a progress bar fills |
| **update stamp** | component | Title row | the time of the last update, right in the title row (short: stamp) |
| **Value** | component | — | see *Components* |
| **Version** | vocabulary | — | see *Vocabulary* |
| **warning chip** | component | Chip | a chip at the warning level (an outline where the panel has no warning colour) (not: warn chip) |
<!-- /registry:glossary -->
