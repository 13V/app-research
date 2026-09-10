# Hosting this yourself

`index.html` is a **single self-contained file**. No build step, no dependencies, no external
requests — the font is embedded. It works from any static host, a USB stick, or as an email
attachment opened offline.

Rebuild it after editing the source with:

```bash
python3 demo/build-standalone.py
```

---

## Where to put it, best first

### 1. A subdomain on your own domain — do this one

```
kolen.yourstudio.com.au
```

A prospect-specific subdomain is the single strongest signal that this was built for them.
It costs you one DNS record per prospect and it reads as bespoke work, because it is.

Point a CNAME at whichever host below you pick, upload `index.html`, done.

### 2. Cloudflare Pages / Netlify / Vercel — free, custom domain included

**Netlify Drop** is the fastest: go to app.netlify.com/drop and drag the folder in. No account
needed to get a URL; add one to attach your own domain. Cloudflare Pages and Vercel are the same
idea with a git connection if you'd rather deploy on push.

All three give you HTTPS and a custom domain on the free tier.

### 3. GitHub Pages — free, but the URL says github.io

Fine if you attach a custom domain. Without one, `yourname.github.io/...` is only slightly better
than the artifact link — it still reads as someone else's project rather than your studio.

### 4. Any web host you already pay for

It's one static file. Drop it in a folder and you're done.

---

## What the build adds that the artifact version can't have

| | Why it matters |
|---|---|
| **Viewport meta** | Without it the whole thing renders zoomed-out on a real phone — which is exactly where this demo has to work. The artifact runtime injects this; a raw file doesn't have it. |
| **Add to Home Screen** | Apple and Android web-app meta tags plus an inline manifest. Damien taps Share → Add to Home Screen and it launches **fullscreen with an icon and no browser chrome**. At that point it isn't "a link" any more — it's an app on his phone. |
| **Link preview** | Open Graph and Twitter card tags, so pasting the URL into a text, Teams or an email shows a real title and description instead of a bare link. |
| **Favicon** | Green tick, matching the app. Inline SVG, no separate file. |
| **Embedded font** | Archivo inlined as base64. Zero external calls, so it loads instantly and works in a basement with no reception. |
| **No claude.ai in the URL** | The point. |

---

## Before you send it

1. Set `STUDIO` and `EMAIL` at the top of the `<script>` in `doorset-itp-register.html`,
   then re-run `python3 demo/build-standalone.py`. Those two constants fill the page header,
   the footer and the mailto link — no placeholder reaches the client.
2. The page now carries your name in a header bar and a "get in touch" mailto in the footer.
   Swap the green tick mark for your own logo if you have one.
3. The panel states it's a prototype on sample data and not Kolen's project information.
   **Leave that in.**
4. Sign-offs save to the viewer's browser via localStorage. Nothing is transmitted anywhere.
   Worth saying out loud if Damien asks where the data goes.

## One thing worth knowing

Tell Damien to **add it to his home screen**. Watching it open fullscreen, with an icon, on his
own phone is the moment it stops being a mockup. That single instruction is worth more than
anything in the email.
