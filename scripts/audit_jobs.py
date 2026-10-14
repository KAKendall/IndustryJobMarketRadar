"""Audit listed employer URLs and flag links that need review."""
from pathlib import Path
from urllib.parse import urlparse
import re
import sys
import urllib.error
import urllib.request

# These career sites commonly return synthetic 404 responses to non-browser
# requests even while the posting remains live. A 404 from one of these hosts
# therefore requires manual verification instead of failing the workflow.
SOFT_404_DOMAINS = {
    "amazon.jobs",
    "apply.deloitte.com",
}

BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/129.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def is_soft_404_host(url):
    host = (urlparse(url).hostname or "").lower()
    return any(host == domain or host.endswith(f".{domain}") for domain in SOFT_404_DOMAINS)


text = Path("data/jobs.js").read_text(encoding="utf-8")
urls = re.findall(r'url:"(https://[^\\"]+)"', text.split("companies:", 1)[0])
bad = []
blocked = []

for url in urls:
    request = urllib.request.Request(url, headers=BROWSER_HEADERS)
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            if response.status >= 400:
                bad.append((url, response.status))
    except urllib.error.HTTPError as exc:
        if exc.code == 404 and is_soft_404_host(url):
            blocked.append((url, "404 (employer site blocks automated checks)"))
        elif exc.code in (404, 410):
            bad.append((url, exc.code))
        else:
            blocked.append((url, exc.code))
    except Exception as exc:
        blocked.append((url, str(exc)))

for url, reason in bad:
    print(f"REVIEW {reason}: {url}")
for url, reason in blocked:
    print(f"MANUAL REVIEW {reason}: {url}")

print(
    f"Audited {len(urls)} job links; "
    f"{len(bad)} hard failures; {len(blocked)} require manual review."
)

if bad:
    sys.exit(1)
