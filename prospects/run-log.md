# Run log — Batch 1: Waterproofing (South Australia)

**Date:** 2026-09-10
**Trade category:** Waterproofing
**Qualified rows written:** 7 (cap was 25 — the SA universe is smaller than the cap)

---

## Sources tried

### 1. Master Builders SA member directory — PARTIAL / NOT USABLE FOR THIS TRADE
- `https://mbasa.com.au/find-a-member/` — blocked by a bot-verification loader via WebFetch.
- `https://mbasa.com.au/find-a-builder/` — **reachable via curl (HTTP 200)**. Member list is
  server-rendered as Name / Phone / Website triples.
- **Two blockers:**
  1. The list is capped at **100 rows** (A–F, ending at "Fairmont Homes"). It uses the
     Search & Filter Pro plugin with a client-side/AJAX query. I probed
     `_sf_s`, `_search`, `sf_s`, `_sfm_field_1` and `s` as GET params — every one returned
     the identical first 100 rows, so the full roster is not reachable server-side.
  2. The directory carries **no trade category** at all and is framed for consumers seeking
     a home builder ("Are you looking for a builder for your new home or major renovation?").
- Zero matches for `waterproof|membrane|proofing|tanking` in the retrievable portion.
- The "SA Building Directory Application" link (`sabuildingdirectory.com.au`) failed TLS/connection
  (HTTP 000) on every attempt.

### 2. HIA South Australia member directory — FAILED
- `https://hia.com.au/find-a-member` → HTTP 404.
- `https://hia.com.au/find-a-builder-or-tradie` → HTTP 404; the site is a Vue SPA that renders
  only template placeholders (`{{ propApi.searchIcon }}`) to a non-JS fetch. No server-rendered
  member data reachable. Not usable.

### 3. Trade association directories
- **Australian Institute of Waterproofing (waterproof.org.au)** — has a members directory, but it
  sits behind a member CRM login at `aiw.wavecrm.com.au`. `/directory/` → HTTP 404 publicly.
  Not publicly queryable.
- **Remedial Waterproofing Association** — `/installers/` → HTTP 404.
  `/find-a-tradie/sa/` returns HTTP 200 but serves default WordPress sample content
  ("Hi there! I'm a bike messenger by day...") — i.e. **no SA members exist on this site**.
  Its state nav lists ACT/NSW/NT/QLD/VIC/WA only — SA is absent. Site footer reads
  "© 2021 Remedial Membranes", a NSW business. Not usable for SA.
- NECA SA / Master Plumbers SA / Master Painters / AMCA / FPA Australia — not applicable to
  waterproofing; deferred to their own trade batches.

### 4. CBS SA contractor's licence register — UNREACHABLE
- `https://www.cbs.sa.gov.au/find-a-licence-holder` → **HTTP 403** via both curl and WebFetch.
- `https://www.cbs.sa.gov.au/public-registers` → **HTTP 403**.
- The register is behind a WAF that rejects non-browser clients. I could not reach the search
  form, so I could not determine whether it is query-parameter driven or a JS portal.
  **No licence numbers were guessed or inferred.** Where a licence number appears in a row it was
  copied from the business's own website (e.g. Dayproof "SA Lic 304834", XS "BLD 323458").

### 5. ABN Lookup (abr.business.gov.au) — WORKED WELL
Both `/ABN/View?abn=` and `/Search/ResultsActive?SearchText=` are reachable and server-rendered.
Used to confirm entity name, entity type, registration date, main business location and
registered business names. Notable resolutions:
- Dayproof Waterproofing → trading name of **MEZ CONTRACTING (AUS) PTY LTD**, ABN 68 620 869 196.
- XS Waterproofing & Flooring → **DELCORP WATERPROOFING AND FLOORING PTY LTD**, ABN 55 662 811 252
  (a second, later entity — DELCORP WATERPROOFING & FLOORING SERVICES PTY LTD, ABN 46 679 605 406 —
  holds the current business-name registration; both noted in the row).
- No ABN could be found for **Hydroproof** or **Universal Waterproofing** under those names;
  `abn_status` left blank for both.

### 6. Business websites — PRIMARY SOURCE, fetched directly for every row
Every qualified row was verified against pages fetched from the business's own domain
(about, team, projects, contact). No row rests on a directory summary alone.

### 7. Public LinkedIn company pages — MOSTLY ABSENT
Only **Floortek Group** has a LinkedIn company page ("11-50 employees", Adelaide SA, founded 2016,
Anthony Gouros director). Guessed slugs for Dayproof, Patch and Caulk, XS Waterproofing and
Universal Waterproofing all returned HTTP 404, and targeted searches surfaced no company pages.
Personal LinkedIn profiles did surface for two businesses; **these were not used**, per the rule
against collecting from personal social media profiles. This is why several `staff_estimate`
and `decision_maker_linkedin` fields are blank.

### 8. Google Places API — NOT USED
No Google Places / Maps API key is present in the environment. Per instructions, Google Maps HTML
was not scraped.

### Supplementary directories used to build the candidate pool
- **Remedial Building Australia** SA waterproofing directory (28 SA listings) — the single most
  productive discovery source. Used for discovery and contact cross-checks only; every business
  taken forward was then verified on its own site.
- Yellow Pages "Waterproofing Contractors, Greater Adelaide" — used for discovery only.

---

## Sources that failed (unreachable)

| Source | Result |
|---|---|
| `mbasa.com.au/find-a-member/` | Bot-verification loader; no content |
| `sabuildingdirectory.com.au` | HTTP 000 — TLS/connection failure |
| `hia.com.au/find-a-member` | HTTP 404 |
| `hia.com.au/find-a-builder-or-tradie` | HTTP 404; JS-only SPA |
| `cbs.sa.gov.au/find-a-licence-holder` | HTTP 403 (WAF) |
| `cbs.sa.gov.au/public-registers` | HTTP 403 (WAF) |
| `waterproof.org.au/directory/` | HTTP 404; directory behind member login |
| `remedialwaterproofingassociation.com.au/installers/` | HTTP 404 |
| `remedialwaterproofingassociation.com.au/find-a-tradie/sa/` | 200 but placeholder content — no SA members |
| `waterpro.com.au` | HTTP 403 via curl **and** WebFetch — candidate dropped, see below |
| `hydron.com.au` | HTTP 000 — TLS/connection failure — candidate dropped, see below |
| `stopsaltdamp.com.au` (Tech-Dry SA) | Connection reset on curl; reached via WebFetch only |
| `seek.com.au` | HTTP 403 — could not check job ads directly |

---

## Counts

- **Candidates identified:** 40+
- **Qualified and written to CSV:** 7
- **Excluded:** 33+ (reasons below)

## Exclusions and why

### Not a trade business — lead-generation / referral sites (2)
These are the most dangerous entries for a lead list; both look like contractors at a glance.
- **Pro Waterproofing Adelaide** (`prowaterproofingadelaide.com.au`) — "we help you find a licensed
  waterproofing contractor"; "Sample feedback from licensed waterproofing contractors we work with".
  Also lists a different phone number (08 7184 0784) from the one in the directory (08 7093 6066).
- **ADL Waterproofers** (`adlwaterproofers.com`) — states outright: "Waterproofing Adelaide does not
  hold a BSA waterproofing licence and does not perform waterproofing work."

### Not SA-based / multi-state corporates (5)
- **RCR Services** — "across Adelaide, Melbourne, Sydney, and Newcastle"
- **WS Remedial Group** — "across Queensland and New South Wales"
- **Southern Remedial Solutions** — Wollongong / Illawarra NSW
- **TBR Services** — "Melbourne-based, servicing nationwide"
- **United Trade Links** — Sydney/NSW operation

### Manufacturers / suppliers, not subcontractors (4)
Tremco CPG Australia (NSW), Bostik, Superflex Membranes/Ardex Australia, Projex Group.

### National franchise (1)
Megasealed Adelaide.

### Fails the 8–50 headcount rule — evidence of a 1–3 person operation (2)
- **JDF Waterproofing** — single named individual (jason@), single mobile, no team language.
- **Tech-Dry SA** — no staff evidence anywhere; Yellow Pages lists opening hours of Friday
  9:00am–12:00pm only, closed Mon–Thu and weekends. Domestic salt-damp focus.

### Wrong trade for this batch — carried forward (1)
- **Synergy Specialists Pty Ltd** (ABN 96 613 052 789, Edwardstown SA 5039, founded 1987,
  (08) 8357-8200, admin@synspec.com.au). Strong prospect — SA owned and operated, in-house
  engineering, government and commercial client list (SA Water, Royal Adelaide Hospital,
  Women's and Children's Hospital, BHP, Myer Centre), "our team of experienced abseilers".
  But its core trade is concrete cancer repair, not waterproofing.
  **→ Move to batch 9 (Concreting / formwork / steel fixing / remedial).**

### Dropped because the business's own site could not be reached (2)
Both are plausible prospects; neither could be verified against a first-party source, and the
workflow requires fetching the business's own site rather than trusting a directory summary.
**→ Worth a manual check.**
- **Waterpro** (Stepney SA 5067) — `waterpro.com.au` returns HTTP 403 to every client tried.
  Directory data: (08) 8363 6050. ABN Lookup shows *The trustee for Waterpro Unit Trust*,
  ABN 42 843 609 916, Fixed Unit Trust, SA 5067, active from 01 Jul 2011.
- **Hydron Protector Systems Pty Ltd** (Seaton SA) — `hydron.com.au` fails TLS/connection.
  Directory data: (08) 8235 1640. No SA ABN found under "Hydron Protector".

### No website and/or no evidence of 8+ staff (16)
Mobile-only listings from the Remedial Building Australia and Yellow Pages directories, none of
which could be verified as more than a small operation: Adelaide Shower Seal, Adelaide Tiling &
Waterproofing (×2 listings), Adelaide Waterproofing Services, Alliance Waterproofing Pty Ltd,
Flexseal Waterproofing, Genius Waterproofing, Integral Waterproofing Solutions, Lifes Tiling,
Mr Salt Damp, SA Waterproofing & Caulking, Statewide Salt Damp, Tubbed Waterproofing,
Construction Caulking Services, The Box Gutter Guys, Adelaide Better Maintenance.

---

## Fields left blank across this batch, and why

| Field | Blank count | Reason |
|---|---|---|
| `staff_estimate` | 6 of 7 | Only Floortek publishes a verifiable band (LinkedIn "11-50 employees"). No other business publishes a headcount, and none has a LinkedIn company page. Personal LinkedIn profiles were available for two of them but are excluded by the sourcing rules. **No numbers were estimated.** `staff_evidence` instead quotes the multi-crew language that supports inclusion. |
| `decision_maker_linkedin` | 6 of 7 | Only Floortek has a company LinkedIn page. Personal profiles not used. |
| `decision_maker_role` | 5 of 7 | Role is only stated for Anthony Gouros (Floortek, founder) and Lloyd Wegener (ABS, "Our owner"). George Rowan, Reno and Ward are named via published business contact details with no role given. |
| `decision_maker_name` | 1 of 7 | Patch and Caulk publishes no name from a company-controlled source. |
| `signal_fleet` | 6 of 7 | Only Universal Waterproofing mentions a fleet. Vehicle photos exist on other sites but weren't treated as evidence. |
| `signal_yard_or_depot` | 4 of 7 | Marked Y only where a specific industrial/commercial premises address is published. |
| `current_software_visible` | 6 of 7 | Only Universal Waterproofing mentions software, and does **not** name the product — recorded as an unnamed platform rather than guessing a vendor. |
| `abn_status` | 2 of 7 | No ABN found for Hydroproof or Universal Waterproofing under their trading names. |
| `suburb` | 2 of 7 | Hydroproof and Universal Waterproofing publish no street address. |
| `work_mix` | 1 of 7 | Universal Waterproofing does not state a commercial/domestic split. |
| `signal_hiring` | 0 of 7 | Marked N for all seven — **not verified as a true negative.** No careers pages exist on any of these sites, and SEEK returned HTTP 403, so live job ads could not be checked. Treat "N" here as "no ad found", not "not hiring". |
| `signal_accreditations` | 1 of 7 | Universal Waterproofing publishes none. |

## Data-quality notes worth carrying forward

1. **Trading-history claims conflict with ABN registration dates** on three rows. Dayproof claims
   "over 40 years" against a 2017 entity; Patch and Caulk shows a "40 years" banner against a 2015
   entity; Floortek's about page carries an "Established 2008" heading while its own body text and
   ABN both say 2016. Both figures are recorded in `years_trading` rather than picking one.
2. **Floortek and Patch and Caulk are adjacent-trade businesses** (commercial flooring, and
   caulking/concrete remediation respectively) that market waterproofing as a named service line.
   Both are flagged in `trade_category` and will re-surface in batches 4 and 9 — dedupe on ABN then.
3. **`signal_hiring` is the weakest column in this batch.** If hiring is an important scoring input,
   it needs a job-board route that isn't SEEK.
