# Trigger monitor

Turns the static 61-row list into a live queue by watching for two public buying signals.

| Signal | What it means |
|---|---|
| **ADMIN_HIRE** | A trade business is advertising for an office manager, scheduler, service coordinator or contracts administrator. **They are trying to solve your problem by hiring a person.** That's the single strongest trigger there is. |
| **INCUMBENT** | A job ad names Simpro, ServiceM8, AroFlo, Tradify or Fergus. Tells you what they run today. If the same company also shows up under ADMIN_HIRE, their platform isn't coping — that's a displacement conversation. |

Ads from recruiters and labour hire are filtered out. ADMIN_HIRE ads must also read as a trade
business, or you'd drown in law firms and accountancies.

Every hit is cross-referenced against `../prospects/master.csv`. A company already on your list
that starts advertising for a scheduler is the warmest lead you will ever get — those print with
`*** ON YOUR LIST ***`.

## Setup

```bash
# 1. Free key, issued instantly, no card
open https://developer.adzuna.com/

# 2. Set credentials
export ADZUNA_APP_ID=your_app_id
export ADZUNA_APP_KEY=your_app_key

# 3. Run
python3 monitor/trigger_monitor.py
```

No dependencies — standard library only.

## Run it daily

```cron
0 7 * * 1-5 cd /path/to/app-research && \
  ADZUNA_APP_ID=xxx ADZUNA_APP_KEY=yyy /usr/bin/python3 monitor/trigger_monitor.py >> monitor/run.log 2>&1
```

Weekdays at 7am. Job ads post on weekday mornings, so you see them the same day they go live —
which matters, because you want to be the first call they take.

## Output

Appends to `../prospects/trigger-events.csv`, de-duplicated on ad ID, so it's safe to re-run.

| Column | |
|---|---|
| `signal` | ADMIN_HIRE or INCUMBENT |
| `company` | Employer name |
| `incumbent_named` | Which platform the ad mentions, if any |
| `already_on_list` | YES if they're in master.csv — **work these first** |
| `list_trade` | Their trade from your research |
| `ad_url` | Straight to the ad |

## Why Adzuna and not SEEK

SEEK, Indeed and Jora all return 403 to automated access — I confirmed this. Adzuna publishes a
documented API with a free tier and aggregates Australian listings including a good share of SEEK
volume. Jooble also has an API but the free tier is 500 lifetime calls, so it can't run as a monitor.

## Tuning

Both query lists are at the top of `trigger_monitor.py`:

- `ADMIN_ROLE_QUERIES` — add role titles as you learn what your buyers advertise for
- `INCUMBENT_QUERIES` — add competitors
- `TRADE_WORDS` — widen if you're getting false negatives
- `REJECT_WORDS` — add any recruiter that keeps slipping through

Free tier is a few hundred calls a day. This uses ~12 per run, so daily is comfortable.

## What it can't tell you

An ad tells you a business is hiring. It doesn't tell you they'll spend $20k. Treat a hit as a
reason to make the call, not as a qualified lead — the qualifying still happens on the phone.
