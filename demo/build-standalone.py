#!/usr/bin/env python3
"""
Wrap the demo into a complete, deployable HTML document.

The source file is written for the Artifact runtime, which injects the doctype, <head>
and a viewport meta at publish time. Hosted anywhere else that shell is missing — most
importantly the viewport meta, without which the whole thing renders zoomed-out on a
real phone, which is exactly where this demo has to work.

This produces dist/index.html:
  - complete HTML document with charset, viewport and colour-scheme
  - Archivo inlined as base64 woff2, so the file makes NO external requests and works
    offline, off a USB stick, or as an email attachment
  - Open Graph and Twitter card tags, so pasting the link anywhere shows a real preview
  - inline SVG favicon and apple-touch-icon
  - web app manifest inlined as a data URI, plus the Apple meta tags, so "Add to Home
    Screen" launches it fullscreen with an icon and no browser chrome

Usage:  python3 demo/build-standalone.py
"""
import base64, re, sys, os, urllib.request, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "doorset-itp-register.html")
OUT  = os.path.join(HERE, "dist", "index.html")

# --- what the link says when it is pasted into a message or an email -----------------
TITLE = "Doorset Checks"
DESC  = ("Seven checks on every doorset, signed off on site from the carpenter's phone. "
         "Prototype built for Kolen Carpentry.")
UA    = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
         "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")

# green rounded square, white tick — matches the app's completion colour
ICON_SVG = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'>"
            "<rect width='64' height='64' rx='14' fill='%230E7C4A'/>"
            "<path d='M18 33.5 27.5 43 46 22' fill='none' stroke='%23fff' "
            "stroke-width='7' stroke-linecap='round' stroke-linejoin='round'/></svg>")


def fetch(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def inline_archivo():
    """Return @font-face CSS with the latin subset embedded, or None if offline."""
    try:
        css = fetch("https://fonts.googleapis.com/css2"
                    "?family=Archivo:wght@600;700&display=swap").decode()
    except Exception as e:
        print(f"  ! could not reach Google Fonts ({e}) — falling back to system fonts",
              file=sys.stderr)
        return None

    # each @font-face block ends with a unicode-range; keep only the latin ones
    out = []
    for block in re.findall(r"@font-face\s*\{[^}]+\}", css):
        if "U+0000-00FF" not in block:          # latin subset marker
            continue
        weight = re.search(r"font-weight:\s*(\d+)", block)
        url = re.search(r"url\((https://[^)]+\.woff2)\)", block)
        if not (weight and url):
            continue
        try:
            b64 = base64.b64encode(fetch(url.group(1))).decode()
        except Exception as e:
            print(f"  ! font fetch failed ({e})", file=sys.stderr)
            return None
        out.append(
            "@font-face{font-family:'Archivo';font-style:normal;"
            f"font-weight:{weight.group(1)};font-display:swap;"
            f"src:url(data:font/woff2;base64,{b64}) format('woff2')}}")
        print(f"  · Archivo {weight.group(1)} inlined ({len(b64)//1024} KB base64)")
    return "\n".join(out) if out else None


def main():
    body = open(SRC, encoding="utf-8").read()

    # strip the artifact-era title tag and the external font link; both are replaced below
    body = re.sub(r"<title>.*?</title>\s*", "", body, count=1, flags=re.S)
    body = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>\s*',
                  "", body, count=1)

    font_css = inline_archivo()
    font_block = f"<style>\n{font_css}\n</style>" if font_css else ""
    if not font_css:
        # keep the page looking deliberate rather than broken if the font is unavailable
        body = body.replace('--dis:"Archivo",system-ui,sans-serif;',
                            '--dis:ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;')

    manifest = ('{"name":"Doorset Checks","short_name":"Doorsets","display":"standalone",'
                '"background_color":"#EFF0F2","theme_color":"#FFFFFF","start_url":"./",'
                f'"icons":[{{"src":"data:image/svg+xml,{ICON_SVG}","sizes":"any",'
                '"type":"image/svg+xml"}]}')

    doc = f"""<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#FFFFFF" media="(prefers-color-scheme:light)">
<meta name="theme-color" content="#17191C" media="(prefers-color-scheme:dark)">

<meta property="og:type" content="website">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{TITLE}">
<meta name="twitter:description" content="{DESC}">

<link rel="icon" href="data:image/svg+xml,{ICON_SVG}">
<link rel="apple-touch-icon" href="data:image/svg+xml,{ICON_SVG}">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Doorsets">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<link rel="manifest" href='data:application/manifest+json,{urllib.parse.quote(manifest)}'>

{font_block}
<style>
  html{{-webkit-text-size-adjust:100%}}
  body{{margin:0}}
  img{{max-width:100%}}
  [hidden]{{display:none!important}}
</style>
</head>
<body>
{body}
</body>
</html>
"""
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(doc)
    kb = os.path.getsize(OUT) / 1024
    print(f"\nwrote {os.path.relpath(OUT)}  ({kb:.0f} KB, single file, "
          f"{'no external requests' if font_css else 'system fonts'})")


if __name__ == "__main__":
    main()
