"""Fail when a listed employer URL no longer looks reachable."""
from pathlib import Path
import re
import sys
import urllib.error
import urllib.request

text = Path("data/jobs.js").read_text(encoding="utf-8")
urls = re.findall(r'url:"(https://[^\"]+)"', text.split("companies:", 1)[0])
bad = []
blocked = []
for url in urls:
    request = urllib.request.Request(url, headers={"User-Agent": "IndustryJobRadar/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            if response.status >= 400:
                bad.append((url, response.status))
    except urllib.error.HTTPError as exc:
        if exc.code in (404, 410):
            bad.append((url, exc.code))
        else:
            blocked.append((url, exc.code))
    except Exception as exc:
        blocked.append((url, str(exc)))
if bad:
    for url, reason in bad:
        print(f"REVIEW {reason}: {url}")
    sys.exit(1)
for url, reason in blocked:
    print(f"MANUAL REVIEW {reason}: {url}")
print(f"Audited {len(urls)} job links; {len(blocked)} require manual review.")
