# Spec demo — Doorset ITP Register

**Live:** https://claude.ai/code/artifact/f9c9f94c-0e75-462b-bd13-e478ab78cf6f
**Built for:** Kolen Carpentry (target 3) — send this *with* the email, don't pitch first.
**Source:** `doorset-itp-register.html` — self-contained, no build step, no dependencies.

## Why this exists

Kolen's site says, verbatim:

> *"Every doorset checked, installed and functioned against the hardware schedule, with
> item-level ITP records supporting every sign-off."*

No off-the-shelf trade app produces that. Not ServiceM8, not Tradify, not Fergus. So instead of
describing what you'd build, this **is** a slice of it, running on sample data.

Speculative work converts far better than proposals at this price point, because the buyer stops
imagining and starts using.

## What it does

- Parses a door and hardware schedule (CSV) into a doorset register
- Generates the ITP hold points per doorset — **fire-rated assemblies automatically get the
  extra AS 1905.1 fire-tag hold point; non-rated ones don't**, and the track shows those as
  skipped rather than outstanding
- **Hold-point funnel** — how many doorsets have cleared each stage, with the bottleneck
  highlighted: *"2 doorsets waiting on W1 Leaf hung"*
- **Per-doorset stage track** — seven segments showing exactly where each door is stuck,
  instead of a percentage nobody can act on
- Sign-off per hold point, stamped with initials and date
- Filters: all / fire-rated / incomplete
- "Generate handover pack" opens a print view with every hold point expanded

Opens in a realistic mid-job state — some packs closed out, some part-signed, one not started.

## Design notes

Deliberately stripped back. Earlier versions carried a stage funnel, six header fields, an
eight-column table and a two-column footer — a product, when what a prospect needs in thirty
seconds is a demonstration of one idea.

What's left: a one-sentence status, a filter row, and the register. Four columns — door, location,
fire rating, progress. Click a door for its spec line and seven hold points.

Two choices carry the information design:

- **The status word beats a percentage.** Each row ends in plain English — *leaf hang*, *function
  test*, *fire tag*, *released* — so you read what a door is waiting on, not how far along it is.
- **Signed items recede.** Completed hold points drop to normal weight and grey; outstanding ones
  stay bold black. Your eye lands on the work left to do.

Source Sans 3 for reading, IBM Plex Mono only for identifiers — door refs, ratings, tags, initials.
One green for signed, one red for fire ratings, grey for everything else.

## The seven hold points

These are the demo's best guess at Kolen's actual workflow, and **the guess is the point**. If
they're wrong, Damien will tell you exactly how — which is a far better first conversation than
any discovery call you could book.

| | | |
|---|---|---|
| H1 | Hold | Delivery conformance — leaf and frame against schedule, certification labels |
| H2 | Hold | Frame set out and fixed — plumb, square, fixing centres |
| W1 | Witness | Leaf hung, clearances recorded — AS 1905.1 tolerance |
| H3 | Hold | Hardware installed to set — fire-rated items certified |
| W2 | Witness | Function test — self-closes from 15°, latches unassisted |
| H4 | Hold | Fire tag affixed and registered — *fire-rated doorsets only* |
| H5 | Hold | Final QA and handover |

## Before you send it

1. Replace `[your studio]` in the prototype banner with your business name.
2. The banner already states this is a prototype on fictional data and not Kolen's real project
   information. **Leave that in.** It's what keeps a spec build honest.
3. Sign-offs save to the viewer's own browser only — nothing leaves their machine. Say so if asked.

## If they bite

The real build adds what a demo can't fake: schedule imported straight from the door register,
photo capture against each hold point, defect tracking, and the signed pack out as a PDF.
That's the $20k conversation.
