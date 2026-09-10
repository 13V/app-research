#!/usr/bin/env python3
"""
Trigger monitor — surfaces SA trade businesses showing buying signals.

Two signals, both public, both strong:

  ADMIN_HIRE   A trade business advertising for an office manager, scheduler,
               service coordinator or contracts administrator. They are trying to
               solve the problem by hiring a person. That is your opening.

  INCUMBENT    A job ad naming Simpro / ServiceM8 / AroFlo / Tradify / Fergus.
               Tells you what they run today. If they also appear under ADMIN_HIRE,
               their current platform is not coping.

Data source: Adzuna API (free tier, instant key). SEEK, Indeed and Jora all block
automated access, so this is the legitimate route.

Setup:
    1. Register at https://developer.adzuna.com/  (free, instant App ID + Key)
    2. export ADZUNA_APP_ID=...  ADZUNA_APP_KEY=...
    3. python3 trigger_monitor.py

Writes results to ../prospects/trigger-events.csv (append-only, de-duplicated on ad id).
"""
import os, sys, csv, json, time, re, urllib.parse, urllib.request
from datetime import datetime, timezone

APP_ID  = os.environ.get("ADZUNA_APP_ID")
APP_KEY = os.environ.get("ADZUNA_APP_KEY")
BASE    = "https://api.adzuna.com/v1/api/jobs/au/search"
OUT     = os.path.join(os.path.dirname(__file__), "..", "prospects", "trigger-events.csv")
MASTER  = os.path.join(os.path.dirname(__file__), "..", "prospects", "master.csv")

# --- signal definitions -------------------------------------------------------

ADMIN_ROLE_QUERIES = [
    "office manager construction", "service coordinator trades", "scheduler construction",
    "contracts administrator construction", "project administrator trades",
    "office administrator building", "service administrator maintenance",
]
INCUMBENT_QUERIES = ["simpro", "servicem8", "aroflo", "tradify", "fergus job management"]

# an ad only counts if it smells like a trade business, not a head contractor or agency
TRADE_WORDS = re.compile(
    r"\b(electric|plumb|hvac|air ?condition|mechanical|fire protection|sprinkler|roof|"
    r"scaffold|concret|formwork|steel fix|glaz|joiner|shopfit|cabinet|carpentr|paint|"
    r"plaster|ceiling|partition|waterproof|tiling|tiler|floor|demolition|asbestos|"
    r"refrigerat|maintenance contractor|trade services|subcontract)\w*", re.I)

# reject recruiters and head contractors — they are not your buyer
REJECT_WORDS = re.compile(
    r"\b(recruitment|labour hire|labor hire|staffing|randstad|hays|programmed|workpac|"
    r"chandler macleod|adecco|manpower)\b", re.I)

INCUMBENTS = re.compile(r"\b(simpro|servicem8|service m8|aroflo|tradify|fergus)\b", re.I)

FIELDS = ["first_seen","signal","company","job_title","location","incumbent_named",
          "already_on_list","list_trade","ad_created","ad_url","ad_id"]


def fetch(query, page=1, where="Adelaide", results=50, max_days_old=30):
    params = {
        "app_id": APP_ID, "app_key": APP_KEY,
        "results_per_page": results, "what": query, "where": where,
        "max_days_old": max_days_old, "content-type": "application/json",
    }
    url = f"{BASE}/{page}?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "trigger-monitor/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r).get("results", [])
    except Exception as e:
        print(f"  ! {query!r}: {e}", file=sys.stderr)
        return []


def load_master():
    """Map normalised company name -> trade, so we can flag ads from businesses already researched."""
    known = {}
    try:
        for r in csv.DictReader(open(MASTER, encoding="utf-8")):
            for n in (r["business_name"], r["trading_name"]):
                k = re.sub(r"[^a-z0-9]", "", (n or "").lower())
                if len(k) > 5:
                    known[k] = r["trade_category"]
    except FileNotFoundError:
        pass
    return known


def match_known(company, known):
    k = re.sub(r"[^a-z0-9]", "", (company or "").lower())
    if not k:
        return ""
    if k in known:
        return known[k]
    for kk, trade in known.items():           # substring either direction
        if len(kk) > 7 and (kk in k or k in kk):
            return trade
    return ""


def load_seen():
    try:
        return {r["ad_id"] for r in csv.DictReader(open(OUT, encoding="utf-8"))}
    except FileNotFoundError:
        return set()


def main():
    if not APP_ID or not APP_KEY:
        sys.exit("Set ADZUNA_APP_ID and ADZUNA_APP_KEY. Free key: https://developer.adzuna.com/")

    known, seen = load_master(), load_seen()
    today = datetime.now(timezone.utc).date().isoformat()
    new_rows, hits = [], 0

    for signal, queries in (("ADMIN_HIRE", ADMIN_ROLE_QUERIES), ("INCUMBENT", INCUMBENT_QUERIES)):
        for q in queries:
            print(f"[{signal}] {q}")
            for ad in fetch(q):
                ad_id = str(ad.get("id", ""))
                if not ad_id or ad_id in seen:
                    continue
                company = (ad.get("company") or {}).get("display_name", "").strip()
                title   = ad.get("title", "").strip()
                desc    = ad.get("description", "")
                blob    = f"{company} {title} {desc}"

                if REJECT_WORDS.search(blob):
                    continue
                # ADMIN_HIRE must look like a trade business; INCUMBENT is self-qualifying
                if signal == "ADMIN_HIRE" and not TRADE_WORDS.search(blob):
                    continue

                inc = INCUMBENTS.search(blob)
                on_list = match_known(company, known)
                seen.add(ad_id); hits += 1
                new_rows.append({
                    "first_seen": today, "signal": signal, "company": company,
                    "job_title": title,
                    "location": (ad.get("location") or {}).get("display_name", ""),
                    "incumbent_named": inc.group(0) if inc else "",
                    "already_on_list": "YES" if on_list else "",
                    "list_trade": on_list,
                    "ad_created": (ad.get("created") or "")[:10],
                    "ad_url": ad.get("redirect_url", ""), "ad_id": ad_id,
                })
            time.sleep(1)                      # be polite to the free tier

    if new_rows:
        exists = os.path.exists(OUT)
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS, quoting=csv.QUOTE_ALL)
            if not exists:
                w.writeheader()
            w.writerows(new_rows)

    print(f"\n{hits} new trigger event(s) -> {os.path.normpath(OUT)}")
    for r in sorted(new_rows, key=lambda r: (r["already_on_list"] != "YES", r["signal"])):
        flag = "*** ON YOUR LIST *** " if r["already_on_list"] else ""
        inc  = f" [runs {r['incumbent_named']}]" if r["incumbent_named"] else ""
        print(f"  {flag}{r['signal']}: {r['company']} — {r['job_title']}{inc}")


if __name__ == "__main__":
    main()
