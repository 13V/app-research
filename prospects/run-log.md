# Run log — SA subcontractor prospect research

**Date:** 2026-09-10
**Categories run:** all 15
**Rows in master.csv:** 61 (deduplicated on ABN, then website domain, then phone)

---

## MID-RUN BRIEF CHANGE

Partway through, the brief was revised: *"remember we want the bigger dogs please — a small
glazing company probably doesn't want to spend $20k on an app."*

What changed as a result:

1. **`prospects/master.csv` is now sorted into size tiers**, biggest first (Tier A → Tier D).
   The sort key is verified headcount and scale evidence first, then `fit_score`.
2. **Ballestrin Construction Services was added back** after being excluded earlier for
   exceeding the original 8–50 ceiling. At 51–200 staff it is the largest SA-owned operator
   found. It sits in `prospects/big-operators-above-ceiling.csv` as well as master, and its
   row states plainly that it breaches the original ICP ceiling.
3. **Clean Power Electrical Group was corrected downward.** Its site copy implied a
   substantial crewed operation and it was originally scored 7. Its LinkedIn company page
   shows **"2-10 employees"**. The row now records that band, the score is cut to 5, and it
   is demoted to Tier D. This was my error, caught on re-check.
4. Categories run after the change (joinery, scaffolding, demolition) were worked
   biggest-operator-first.

**Everything below Tier B is size-unverified, not size-confirmed.** Tier C is not a
statement that those businesses are small — it means no headcount could be verified from a
first-party source. Several Tier C rows (De-Construct, DCM Services, MAINair, Kolen) show
scale evidence as strong as Tier A but publish no number.

---

## Size tiers in master.csv

| Tier | Meaning | Count |
|---|---|---|
| **A** | Biggest operators — verified headcount ≥ 10, or hard scale evidence (multi-depot, 5,000sqm facility, 35+ vehicle fleet) | 9 |
| **B** | Verified headcount band inside 8–50 | 2 |
| **C** | Real crewed businesses, headcount not verifiable from any first-party source | 48 |
| **D** | LinkedIn band below the 8–50 floor — deprioritised | 2 |

### Tier A — the big dogs

| Business | Trade | Size evidence |
|---|---|---|
| **Festival Glass & Glazing** | Glazing | "employs more than 25 people" — the only self-published headcount above 25 |
| **Compliant Fire Services** | Fire protection | "over 35 vehicles on the road"; five employed trades listed |
| **Hillsley Scaffolding** | Scaffolding | Three depots — Lonsdale, Dry Creek, Moonta |
| **RAMVEK** | Joinery / shopfitting | "our 5,000sqm facility" |
| **IMR Electrical** | Electrical | "12 employees" (LinkedIn) |
| **Ballestrin Construction Services** | Concreting / remedial | "51-200 employees" (LinkedIn) — **above the original ceiling** |
| **Ceiling and Wall Contractors Australia** | Ceilings & partitions | Two full-time offices (SA + WA), trading since 1992 |
| **Patch and Caulk** | Caulking / remediation | 1000+ Tier 1 & 2 projects; five ticketed trades |
| **Olde Style Roofing & Guttering** | Roofing | "Over 10 In House Staff" — but runs ServiceM8, see below |

---

## Sources worked, by priority order

### 1. Master Builders SA — PARTIAL, not usable for subcontractor discovery
`mbasa.com.au/find-a-member/` is behind a bot-verification loader. `find-a-builder/` loads via
curl but the list caps at **100 rows (A–F)** and carries **no trade categories** — it is framed
for consumers seeking a home builder. Its Search & Filter Pro widget is client-side only:
`_sf_s`, `_search`, `sf_s`, `_sfm_field_1` and `s` all returned the identical first 100 rows.
Zero waterproofing matches in the retrievable portion. `sabuildingdirectory.com.au` (the member
app) failed TLS on every attempt.

### 2. HIA — FAILED
`hia.com.au/find-a-member` and `/find-a-builder-or-tradie` both 404. The site is a Vue SPA that
renders only template placeholders (`{{ propApi.searchIcon }}`) to a non-JS fetch.

### 3. Trade association directories — MIXED, and the single best source of the run

| Association | Result |
|---|---|
| **AMCA Australia** (HVAC) | **Best source of the run.** The entire member directory is embedded server-side with states of operation. Yielded **29 SA-based members**. |
| **Master Painters SA** | **49 SA members with website URLs.** The "MPA Member Websites" nav item is non-linked text; the page was found via the WordPress REST API (`/wp-json/wp/v2/pages`). Their "Find a Painter" is a contact form, not a directory. |
| **AWCI Australia** (wall & ceiling) | Directory queryable by POST with an SA category code (26610). Returned **exactly one SA member** — Adelaide Partitions & Ceilings. That is the complete SA membership, not a fetch failure. |
| **NECA SA** | `findanelectrician.com.au` and `necasa.asn.au/find-neca-electrician/` both return HTTP 202 bot-blocks. ~450 SA/NT businesses are behind it, unreached. |
| **Master Plumbers SA** | `find-a-plumber` is a GET form but results do not render server-side. Filters are consumer-oriented (toilets, blockages, hot water), not commercial. |
| **Fire Protection Association Australia** | `/find-a-member` 404. |
| **Fire Industry Alliance** | Members page renders no member content. |
| **Australian Institute of Waterproofing** | Directory behind a member CRM login (`aiw.wavecrm.com.au`). |
| **Remedial Waterproofing Association** | `/find-a-tradie/sa/` returns default WordPress sample content — **no SA members exist**. State nav lists ACT/NSW/NT/QLD/VIC/WA only. |
| **Specialist Contractors SA** | Lists the associations themselves, not businesses. Useful for confirming which bodies exist per trade. |

### 4. CBS SA contractor's licence register — UNREACHABLE
`cbs.sa.gov.au/find-a-licence-holder` and `/public-registers` both return **HTTP 403** to curl
and to WebFetch. The register sits behind a WAF that rejects non-browser clients. I could not
reach the search form, so I cannot say whether it is query-parameter driven or a JS portal.
**No licence numbers were guessed.** Every licence number in the dataset was copied from the
business's own website (e.g. Dayproof "SA Lic 304834", XS "BLD 323458", Unley Glass "BLD 159957",
APC "BLD186942", Master Linings "BLD 218185").

### 5. ABN Lookup — WORKED THROUGHOUT
Both `/ABN/View?abn=` and `/Search/ResultsActive?SearchText=` are server-rendered and reliable.
Used on every row to confirm entity name, type, registration date, main business location and
registered business names. It did the heaviest lifting in the run and caught several things a
website alone would have hidden — see *Identity surprises* below.

### 6. Business websites — PRIMARY SOURCE
Every row was verified against pages fetched from the business's own domain. No row rests on a
directory summary alone.

### 7. Public LinkedIn company pages — SPARSE BUT DECISIVE
Most SA subcontractors have no company page. Where one existed it was often the single most
important fact in the row, and it cut both ways — it confirmed IMR (12), Floortek (11–50) and
Ballestrin (51–200), and it disqualified Ballestrin from the original ICP, Tapp Electrical (4),
Adelaide Electrical Group (2–10), DNA Electrical (2–10), H. Irwin (2–10) and Clean Power (2–10).
**Personal LinkedIn profiles were never used**, per the sourcing rules — this is why several
`decision_maker_linkedin` fields are blank where a personal profile was available.

### 8. Google Places API — NOT USED
No API key in the environment. Google Maps HTML was not scraped.

### Supplementary discovery sources
Remedial Building Australia SA directories (28 waterproofing listings — the most productive
discovery source for batch 1) and Yellow Pages. Both used for discovery only; every business
taken forward was then verified on its own site.

---

## Sources that failed

| Source | Result |
|---|---|
| `mbasa.com.au/find-a-member/` | Bot-verification loader |
| `sabuildingdirectory.com.au` | HTTP 000 — TLS failure |
| `hia.com.au` member directories | 404; JS-only SPA |
| `cbs.sa.gov.au` (both register URLs) | HTTP 403 (WAF) |
| `findanelectrician.com.au` / NECA SA | HTTP 202 bot-block |
| `fpaa.com.au/find-a-member` | 404 |
| `waterproof.org.au/directory/` | 404; behind member login |
| `remedialwaterproofingassociation.com.au` | 404; no SA members |
| `seek.com.au` | HTTP 403 — job ads could not be checked directly |
| `waterpro.com.au` | HTTP 403 to curl and WebFetch — candidate dropped |
| `hydron.com.au` | HTTP 000 — TLS failure — candidate dropped |
| `hartleyglass.com.au` | HTTP 202 bot-block — **16-vehicle fleet, a likely Tier A glazier, unverifiable** |
| `jfloors.com.au`, `camillericoncrete.com.au`, `hillsepoxyfloors.com`, `specialistcontractors.asn.au` | HTTP 202 bot-blocks |
| `bceandcjelectrical.com.au`, `pridal.com.au`, `mrmpainting.com.au`, `adelite.com.au`, `safefire.com.au` | HTTP 403 |
| `stopsaltdamp.com.au` | Connection reset on curl; reached via WebFetch only |

---

## Identity surprises found via ABN Lookup

Several businesses trade under a name that does not match their registered entity. Anyone
contracting from this list should use the `abn_status` column, not the trading name.

| Trading as | Actual entity |
|---|---|
| Dayproof Waterproofing | **MEZ CONTRACTING (AUS) PTY LTD** |
| XS Waterproofing & Flooring | **DELCORP WATERPROOFING AND FLOORING PTY LTD** (a second Delcorp entity holds the current business name) |
| Systematic Plumbing | **S & K SYSTEMS PTY LTD** |
| RAMVEK | **REMVIK PTY LTD** |
| Hillsley Scaffolding | **LARK PRODUCTS PTY. LTD.** |
| ICS Scaffolding | **I IN C Pty Ltd** |
| Specialised Services | **SA ASBESTOS SERVICES PTY LTD** |
| Adelaide Fire Solutions | **PNMCO PTY. LTD.** |
| THG Electrical | **CONSTRUQT GROUP PTY LTD** |
| Adelaide Commercial Painters | **The Trustee for Vellotti Family Trust** |
| IMR Electrical | **TRUSTEE FOR BLIGHT TRADING PTY LTD & TRUSTEE FOR PEARCE TRADING PTY LTD** |

---

## Exclusions

### Not a trade business — lead-generation sites posing as contractors (3)
The most dangerous entries for a lead list; each looks like a contractor at a glance.
- **Pro Waterproofing Adelaide** — "we help you find a licensed waterproofing contractor";
  "Sample feedback from licensed waterproofing contractors we work with". Site phone differs
  from its directory listing.
- **ADL Waterproofers** — states outright: "Waterproofing Adelaide does not hold a BSA
  waterproofing licence and does not perform waterproofing work."
- **Viva Epoxy Flooring** — no matching ABN; registered address is "Suite 3293, 3/55 Gawler
  Place" (a virtual-office suite number) with SEO suburb pages.

### Not SA-based / multi-state corporates (10)
RCR Services (Adelaide/Melbourne/Sydney/Newcastle) · WS Remedial Group (QLD/NSW) · Southern
Remedial Solutions (NSW) · TBR Services (VIC) · United Trade Links (Sydney) · O.P. Industries
(both group ABNs VIC-registered) · Aztech Services (Brisbane/Sydney/Adelaide/Perth) ·
NOVALUX Electrical (VIC) · Australian Electrical Industries (VIC) · Southern Cross Contractors (NSW)

### Manufacturers, suppliers and national franchises (6)
Tremco CPG Australia · Bostik · Superflex Membranes/Ardex · Projex Group · Megasealed Adelaide
(franchise) · Programmed (national corporate)

### Sole traders — confirmed via ABN entity type (2)
- **Alexander Ceilings** = ALEXANDER, DAVID JAMES, Individual/Sole Trader
- **J Phillips Roofing And Cladding** = PHILLIPS, JONATHAN EDWARD, Individual/Sole Trader

### Below the size floor (6)
Tapp Electrical (4 employees, LinkedIn) · Adelaide Electrical Group (2–10) · DNA Electrical
Systems (2–10) · JDF Waterproofing (single operator) · Tech-Dry SA (Friday 9am–12pm opening
hours only) · Future Carpentry & Linings (entities registered Oct/Dec 2025, sole-trader origin)

### Self-described as small (2)
- **C & J Painting** — "locally owned and operated as a **small** family business"
- **Watermark Painting Specialists** — "a proud South Australian **boutique** painting business…
  **small** commercial"

### Dropped because the business's own site could not be reached (3)
All three are plausible; none could be verified against a first-party source. **Worth a manual check.**
- **Hartley Glass** (SA 5013, ABN 90 008 034 900, active since 2000) — a search summary
  references a "fleet of 16 vehicles", which would make it Tier A. Site is bot-blocked.
- **Waterpro**, Stepney (The trustee for Waterpro Unit Trust, ABN 42 843 609 916, since 2011)
- **Hydron Protector Systems**, Seaton — TLS failure

### Re-categorised, not excluded
- **Synergy Specialists** — found in the waterproofing batch, core trade is concrete cancer
  repair; moved to batch 9.
- **Floortek Group** — appears in both waterproofing and floor laying; deduplicated out of
  master on ABN, retained in `floor-laying.csv`.

---

## Fields left blank across the dataset, and why

| Field | Blank | Reason |
|---|---|---|
| `staff_estimate` | 50 of 61 | Only 11 businesses publish or expose a verifiable figure. **No headcounts were estimated.** `staff_evidence` instead quotes the multi-crew, facility or fleet language that supports inclusion. |
| `decision_maker_linkedin` | 56 of 61 | Only five have company LinkedIn pages. Personal profiles not used. |
| `decision_maker_name` | 40 of 61 | Most SA subcontractors publish no name. Where a first name only was published (Shane, Matt, Reno, Ward, Jason, Patrick), that is what is recorded — no surnames were inferred. |
| `signal_hiring` | Recorded as N on 55 of 61 — **not verified as a true negative.** SEEK returned 403 throughout and most sites have no careers page. Read "N" as "no ad found". Four genuine Y results: Connekt Plumbing, Olde Style Roofing, Sakar Constructions (soft), H. Irwin (expired ad). |
| `general_email` | 9 of 61 | Several businesses publish no email at all — itself a manual-process signal, recorded as such. |
| `phone` | 5 of 61 | RAMVEK, Wood N Stamp, SAC Facades, Floors 2 Go and Clean Air Asbestos publish no phone number anywhere on their sites. |
| `abn_status` | 4 of 61 | No ABN could be matched for Hydroproof, Universal Waterproofing, Sakar Constructions, R.D Scaffold Services or Four Corner Ceilings under their trading names. |
| `suburb` | 24 of 61 | No street address published. |
| `current_software_visible` | 55 of 61 | See below. |

---

## Software incumbents found

Only one business in 61 advertises a named job-management platform:

- **Olde Style Roofing & Guttering** — **ServiceM8**, promoted on a dedicated navigation page:
  *"With the help of our ServiceM8 software, you will always be kept in the loop with job
  progress."* Scored −3 per the rule; row kept and marked as a displacement call. They also
  publish "Over 10 In House Staff" and are actively hiring — a strong "what doesn't it do?" target.

Three others show partial or unnamed systems:
- **Universal Waterproofing** — "cutting edge live job tracking & scheduling software" (unnamed).
  No −3 applied since no platform is named, but the manual-process point was withheld. Scored 1.
- **Ballestrin** — "a centralised Data Management System that can be accessed by all staff"
  (unnamed). Manual-process point withheld.
- **DCM Services**, **Shop Graphics**, **CFI** — Revit / CAD / CNC. These are design and
  manufacturing tools, not job management, and are recorded as such rather than counted as incumbents.

**Interpretation:** 57 of 61 show no job-management system of any kind. The recurring evidence
is departmental email inboxes (`estimating@`, `service@`, `office@`), per-function mobile numbers,
bigpond and outlook addresses, and per-project compliance paperwork with no system named.

## The sharpest manual-process signals found

1. **Compliant Fire Services** — "We have an emergency afterhour service company who divert calls
   to oncall technicians." After-hours dispatch outsourced to a phone-answering service, across 35+ vehicles.
2. **Kolen Carpentry** — "Every doorset checked, installed and functioned against the hardware
   schedule, with item-level ITP records supporting every sign-off." Item-level QA records, no system named.
3. **ICS Scaffolding** — "we test and certify every scaffold we build… will issue JSA and WSMS
   when required." Per-scaffold certification, mobile-only contact, no email published.
4. **Tinmen SA** — estimating, project management and general enquiries each on a separate mobile,
   with no shared email address anywhere on the site.
5. **Watson Fitzgerald** — three departmental inboxes (`office@`, `service@`, `estimating@`) with
   nothing joining them.
6. **De-Construct** — competes explicitly on "the technical and **administrative** sides of
   hazardous material management" across twelve service lines.
7. **H. Irwin Electrical** — their own marketing sells against the handover problem: *"A tradie
   quotes the job, then sends someone different to do it. That person doesn't know what was discussed."*

---

## Data-quality notes

1. **Trading-history claims routinely conflict with ABN registration dates** — Dayproof ("over 40
   years" vs a 2017 entity), Patch and Caulk ("40 years" vs 2015), Floortek ("Established 2008"
   heading vs its own body text and ABN saying 2016), Adelaide Commercial Painters ("50+ Years"
   vs 2003), CFI ("since the 1980's" vs a 2025 entity). Both figures are recorded in
   `years_trading` rather than picking one. Most are explained by restructures, but they should
   not be quoted back to a prospect as fact.
2. **`signal_hiring` is the weakest column in the dataset.** If hiring matters to scoring it needs
   a job-board route that is not SEEK.
3. **Adjacent-trade businesses appear in more than one category.** Floortek (waterproofing +
   flooring), Patch and Caulk (waterproofing + concrete remediation), Synergy (waterproofing →
   concreting). Category CSVs retain them; master deduplicates on ABN.
4. **Two rows sit outside the ICP and say so in their own `score_reasoning`:** Floors 2 Go is a
   retail showroom that also installs, and JS Form describes itself as partly a labour-hire
   company (an explicit exclude category). Both are flagged rather than silently kept or dropped.
