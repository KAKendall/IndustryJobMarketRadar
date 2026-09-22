# Industry Job Market Radar

A static, accessible job board for business PhDs exploring non-academic careers. It is inspired by the scan-and-filter pattern of HBS Doctoral Job Market and seeded from `Industry Job Options(1).docx`.

## Preview locally

```bash
python3 -m http.server 8000 --directory industry-job-radar
```

Then open `http://localhost:8000`.

## Data policy

- A role is displayed only after it is confirmed on an employer career site.
- `data/jobs.js` is the source of truth.
- Every opening records a `verified` date and direct employer URL.
- Closed or inaccessible postings should be removed, not merely labeled stale.
- The employer watchlist remains visible even when no verified role is open.

## GitHub Pages

The Pages workflow deploys the site after each change to `main`. In repository **Settings → Pages**, set the source to **GitHub Actions** once if it is not already selected.

The audit workflow runs Monday and Thursday. It checks every current job URL and opens an issue when a listing returns a definitive not-found or gone response. Access-blocked sites are logged for manual review.

Adding new openings still requires a research pass because most monitored employers use different career systems and several block automated indexing. This is intentional: it prevents an unverified search result from being published as an open role.
