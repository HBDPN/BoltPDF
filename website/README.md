# BoltPDF website

A single static page — **no build step**. Just these files:

```
website/
  index.html      the whole site
  404.html        not-found page
  icon.png         logo (also used for social/share image)
  favicon.png      browser tab icon
  _headers         Cloudflare security + cache headers
  robots.txt       SEO
  sitemap.xml      SEO
```

## Deploy to Cloudflare Pages (easiest way)

1. Go to **dash.cloudflare.com** → **Workers & Pages** → **Create** → **Pages**.
2. Choose **"Upload assets"** (the no-Git option).
3. Drag the **`website` folder's contents** (not the folder itself — the
   files inside it) into the upload box.
4. Give it a project name → **Deploy**.
5. In the project's **Custom domains** tab, add **boltpdf.co.uk**.

To update later: repeat step 1–4 (create a new deployment / re-upload),
or connect the GitHub repo with **Build command:** *(blank)* and
**Build output directory:** `website`.

## Before it works fully

- The **Download** and **Source** buttons point to
  `github.com/HBDPN/BoltPDF`. For them to work, the GitHub repo must be
  **Public** and have at least one **Release** published.
- Everything on the page is accurate to the app as of **v1.0.3**
  (editing is labelled *beta*, matching the in-app notice).
