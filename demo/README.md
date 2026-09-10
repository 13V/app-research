# Spec demo — Doorset Checks (worker phone app)

**Live:** https://claude.ai/code/artifact/f9c9f94c-0e75-462b-bd13-e478ab78cf6f
**For:** Kolen Carpentry (target 3) — send this *with* the email, don't pitch first.
**Source:** `doorset-itp-register.html` — self-contained, no build step, no dependencies.

## The problem, in plain English

Kolen installs doors in hospitals. Hospital doors are safety-critical, so every one gets checked
at seven points as it goes in:

1. Did the right door turn up?
2. Is the frame straight and fixed properly?
3. Are the gaps around the leaf within tolerance?
4. Is the correct hardware on it?
5. Does it swing shut and latch by itself?
6. *(fire doors only)* Is the certification tag on it and logged?
7. Final check — no defects.

Someone records every one of those checks, for every door, and hands the builder a folder of
evidence at handover. A hospital job is hundreds of doors — thousands of records, currently
living in a spreadsheet, a clipboard and someone's camera roll.

Kolen's own website advertises this: *"item-level ITP records supporting every sign-off."*
They're proud of it, which means it costs them real time.

## What the demo is

**A phone app for the carpenter, not a dashboard for the office.** The person doing the checks is
standing at a door with dusty hands, so that's the screen that had to be built.

Three screens:

1. **Today's doors** — progress ring, door ref, where it is, what it still needs. Fire-rated doors
   carry their FRL as a red pill.
2. **One door** — its spec, then the seven checks as a tappable list with big targets.
3. **One check** — what to look for, add photos, one large *Mark complete* button. Signing off
   advances straight to the next check, so a carpenter can work a door without going back to a menu.

Shown in a phone frame on desktop with a plain-English explainer beside it, so it reads as an app
rather than a web page. On a phone it fills the screen.

## Details that show trade knowledge

- **Fire doors get a seventh check; non-rated doors don't** — check 6 renders as "not needed" and
  is excluded from the count, so a plain door never looks incomplete.
- Progress rings show `5/7` on fire doors and `3/6` on non-rated ones.
- AS 1905.1 named where it actually applies — leaf clearances and tag registration.
- The "Saved" indicator in the nav bar — sites have poor reception, and the thing a worker needs
  to trust is that their sign-off didn't vanish.

## Before you send it

1. Replace `[your studio]` in the explainer panel with your business name.
2. The panel already states it's a prototype on sample data and not Kolen's project information.
   **Leave that in.**
3. Sign-offs save to the viewer's own browser only. Say so if asked.

## If they bite

What a demo can't fake, and the real build adds: the schedule imported straight from the door
register, real camera capture, offline queueing for dead spots on site, the office view, and the
signed handover pack out as a PDF. That's the $20k conversation.
