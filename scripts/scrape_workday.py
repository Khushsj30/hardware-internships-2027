"""
Workday Scraper Module
-----------------------
Apple, Intel, TI, Qualcomm, and many other big hardware companies use
Workday for job postings instead of Greenhouse/Lever. Workday doesn't have
one universal public API, but nearly all Workday career sites share the
same underlying pattern:

  https://<company>.wd<N>.myworkdayjobs.com/wday/cxs/<company>/<board_name>/jobs

This is a POST endpoint that takes a search query and returns JSON - it's
what the career site's own search box calls behind the scenes, so it's
public and requires no login/API key.

The tricky part: <N> (1, 3, 5...) and <board_name> differ per company, so
each entry in workday_companies.json needs its exact values. See the
"how to find these values" instructions in workday_companies.json.
"""

import json
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
WD_COMPANIES_FILE = ROOT / "scripts" / "workday_companies.json"

# Reuse the same keyword filters as scrape.py so results are consistent
from scrape import HARDWARE_KEYWORDS, INTERN_KEYWORDS, NEWGRAD_KEYWORDS, is_hardware_role, classify_role


def fetch_workday(company_name, tenant, board, host_suffix):
    """
    tenant: company subdomain, e.g. "apple" for apple.wd1.myworkdayjobs.com
    board: the career-site path, e.g. "Apple" (varies per company, case sensitive)
    host_suffix: the wdN part, e.g. "wd1", "wd3", "wd5" - find by visiting their careers page
    """
    url = f"https://{tenant}.{host_suffix}.myworkdayjobs.com/wday/cxs/{tenant}/{board}/jobs"
    jobs = []
    offset = 0
    limit = 20
    try:
        while True:
            payload = {"limit": limit, "offset": offset, "searchText": ""}
            r = requests.post(url, json=payload, timeout=15,
                               headers={"Content-Type": "application/json"})
            r.raise_for_status()
            data = r.json()
            postings = data.get("jobPostings", [])
            if not postings:
                break
            for job in postings:
                title = job.get("title", "")
                if not is_hardware_role(title):
                    continue
                category = classify_role(title)
                if not category:
                    continue
                path = job.get("externalPath", "")
                jobs.append({
                    "company": company_name,
                    "title": title,
                    "location": job.get("locationsText", "Unspecified"),
                    "url": f"https://{tenant}.{host_suffix}.myworkdayjobs.com/{board}{path}",
                    "category": category,
                    "id": f"wd-{tenant}-{path}",
                    "posted": job.get("postedOn", ""),
                })
            total = data.get("total", 0)
            offset += limit
            if offset >= total:
                break
    except requests.RequestException as e:
        print(f"  [warn] Workday fetch failed for {company_name}: {e}", file=sys.stderr)
    except ValueError as e:
        print(f"  [warn] Workday response wasn't valid JSON for {company_name}: {e}", file=sys.stderr)
    return jobs


def scrape_all_workday():
    if not WD_COMPANIES_FILE.exists():
        print("No workday_companies.json found - skipping.", file=sys.stderr)
        return []
    with open(WD_COMPANIES_FILE) as f:
        data = json.load(f)
    companies = data.get("companies", [])
    all_jobs = []
    for c in companies:
        if "REPLACE_ME" in (c.get("tenant", ""), c.get("host_suffix", ""), c.get("board", "")):
            print(f"  [skip] {c['name']} - fill in real tenant/host_suffix/board values first", file=sys.stderr)
            continue
        print(f"Scraping {c['name']} (Workday)...")
        all_jobs.extend(fetch_workday(c["name"], c["tenant"], c["board"], c["host_suffix"]))
    return all_jobs


if __name__ == "__main__":
    jobs = scrape_all_workday()
    print(f"Found {len(jobs)} hardware postings across Workday companies.")
    for j in jobs[:10]:
        print(f"  - {j['company']}: {j['title']} ({j['location']})")
