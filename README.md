# spanishafterlife.com

Static site for **Spanish AfterLife** — concierge immigration + real estate for
North Americans relocating/retiring to Spain's Valencia Community.

- **Stack:** hand-authored static HTML (one `.html` per route). No build step.
- **Host:** Cloudflare Pages project `spanish-afterlife` (custom domains
  `spanishafterlife.com` + `www`; www 301-redirects to the root at the Cloudflare
  zone level).
- **Canonical host:** non-www, extension-less URLs (e.g. `/real-estate`).

## Deploy

Pushes to `main` auto-deploy to production via GitHub Actions
(`.github/workflows/deploy.yml` → `wrangler pages deploy`).

**One-time setup:** add repo secret `CLOUDFLARE_API_TOKEN` (Cloudflare dashboard →
My Profile → API Tokens → Custom token → **Account · Cloudflare Pages · Edit**).

Manual deploy (fallback):

```bash
wrangler pages deploy . --project-name=spanish-afterlife --branch=main
```

## Notes

- `robots.txt` here is the origin file. The Cloudflare zone may also serve a
  managed content-signals robots.txt — verify precedence after deploy.
- `sitemap.xml` lists only canonical non-www, extension-less URLs.
