"""
Hardware Internship/New-Grad Job Scraper
-----------------------------------------
Pulls open postings from companies' public ATS APIs (Greenhouse + Lever),
filters for hardware-related roles using keyword matching, and writes
the results into Markdown tables that get committed by a GitHub Action.

Add/remove companies in companies.json. No API keys needed — Greenhouse
and Lever expose public read-only job board APIs for any company using them.
"""

import json
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
COMPANIES_FILE = ROOT / "scripts" / "companies.json"
STATE_FILE = ROOT / "scripts" / "seen_jobs.json"

# Only keep postings from the last N days - older listings are usually
# already filled or closed, so this keeps the list fresh and relevant.
DAYS_WINDOW = 90

# Keywords used to decide if a posting counts as a "hardware" role.
# Tune this list freely — it's the only thing separating hardware from SWE postings.
HARDWARE_KEYWORDS = [
    # Chip / silicon design
    "hardware", "asic", "fpga", "rtl", "verilog", "vhdl", "silicon",
    "semiconductor", "vlsi", "soc ", "system on chip", "chip design",
    "layout engineer", "cad engineer", "physical design", "dv engineer",
    "design verification",
    # Boards / analog / RF
    "pcb", "rf engineer", "rf design", "analog design", "digital design",
    "circuit design", "signal integrity", "power electronics",
    "antenna", "microwave engineer",
    # Embedded / firmware
    "embedded", "firmware", "low-latency engineer", "fpga developer",
    # Mechanical / EE generalist
    "electrical engineer", "mechanical engineer", "mems", "thermal engineer",
    "controls engineer", "robotics engineer", "avionics", "systems engineer",
    # Test / manufacturing
    "test engineer", "validation engineer", "dfm", "dfa",
    "manufacturing engineer", "process engineer", "yield engineer",
    "package design", "product engineer",
    # Trading-firm hardware roles (Jane Street, HRT, Jump, Citadel Securities etc.
    # post FPGA/low-latency hardware roles separate from general SWE)
    "fpga engineer", "network engineer - low latency", "hardware engineer - trading",
]

INTERN_KEYWORDS = ["intern", "co-op", "coop"]
NEWGRAD_KEYWORDS = ["new grad", "early career", "university grad", "entry level"]


def load_companies():
    with open(COMPANIES_FILE) as f:
        return json.load(f)


def load_seen():
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {}


def save_seen(seen):
    with open(STATE_FILE, "w") as f:
        json.dump(seen, f, indent=2)


def is_hardware_role(title):
    t = title.lower()
    return any(kw in t for kw in HARDWARE_KEYWORDS)


def classify_role(title):
    t = title.lower()
    if any(kw in t for kw in INTERN_KEYWORDS):
        return "Intern"
    if any(kw in t for kw in NEWGRAD_KEYWORDS):
        return "New Grad"
    return None  # skip roles that are neither — keeps the list focused


def fetch_greenhouse(board_token, company_name):
    """Greenhouse public job board API: https://boards-api.greenhouse.io/"""
    url = f"https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs?content=true"
    jobs = []
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        data = r.json()
        for job in data.get("jobs", []):
            title = job.get("title", "")
            if not is_hardware_role(title):
                continue
            category = classify_role(title)
            if not category:
                continue
            location = job.get("location", {}).get("name", "Unspecified")
            jobs.append({
                "company": company_name,
                "title": title,
                "location": location,
                "url": job.get("absolute_url"),
                "category": category,
                "id": f"gh-{job.get('id')}",
                "posted": job.get("updated_at", "")[:10],
            })
    except requests.RequestException as e:
        print(f"  [warn] Greenhouse fetch failed for {company_name}: {e}", file=sys.stderr)
    return jobs


def fetch_lever(company_slug, company_name):
    """Lever public postings API: https://api.lever.co/v0/postings/"""
    url = f"https://api.lever.co/v0/postings/{company_slug}?mode=json"
    jobs = []
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        data = r.json()
        for job in data:
            title = job.get("text", "")
            if not is_hardware_role(title):
                continue
            category = classify_role(title)
            if not category:
                continue
            location = job.get("categories", {}).get("location", "Unspecified")
            jobs.append({
                "company": company_name,
                "title": title,
                "location": location,
                "url": job.get("hostedUrl"),
                "category": category,
                "id": f"lv-{job.get('id')}",
                "posted": datetime.fromtimestamp(
                    job.get("createdAt", 0) / 1000, tz=timezone.utc
                ).strftime("%Y-%m-%d") if job.get("createdAt") else "",
            })
    except requests.RequestException as e:
        print(f"  [warn] Lever fetch failed for {company_name}: {e}", file=sys.stderr)
    return jobs


def is_within_window(posted_str, days=DAYS_WINDOW):
    """Returns True if posted_str is a parseable date within the last `days` days.
    If the date can't be parsed or is missing, we keep the job (better to show
    an unsure posting than silently drop a real one)."""
    if not posted_str:
        return True
    try:
        posted_date = datetime.strptime(posted_str[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        return True
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    return posted_date >= cutoff


def scrape_all():
    companies = load_companies()
    all_jobs = []
    for c in companies:
        name = c["name"]
        print(f"Scraping {name} ({c['ats']})...")
        if c["ats"] == "greenhouse":
            all_jobs.extend(fetch_greenhouse(c["token"], name))
        elif c["ats"] == "lever":
            all_jobs.extend(fetch_lever(c["token"], name))
        else:
            print(f"  [skip] unsupported ATS type: {c['ats']}", file=sys.stderr)
    before = len(all_jobs)
    all_jobs = [j for j in all_jobs if is_within_window(j.get("posted"))]
    print(f"Filtered to last {DAYS_WINDOW} days: {len(all_jobs)}/{before} postings kept.")
    return all_jobs


README_PATH = ROOT / "README.md"
INTERN_START = "<!-- INTERNSHIPS:START -->"
INTERN_END = "<!-- INTERNSHIPS:END -->"
NEWGRAD_START = "<!-- NEWGRAD:START -->"
NEWGRAD_END = "<!-- NEWGRAD:END -->"


def table(rows):
    lines = [
        "| Company | Role | Location | Posted | Link |",
        "|---|---|---|---|---|",
    ]
    for j in sorted(rows, key=lambda x: x["posted"], reverse=True):
        lines.append(
            f"| {j['company']} | {j['title']} | {j['location']} | {j['posted']} | [Apply]({j['url']}) |"
        )
    return "\n".join(lines)


def replace_between(text, start_marker, end_marker, new_content):
    pattern = re.compile(re.escape(start_marker) + r".*?" + re.escape(end_marker), re.DOTALL)
    replacement = f"{start_marker}\n{new_content}\n{end_marker}"
    if pattern.search(text):
        return pattern.sub(replacement, text)
    # markers not found - append at the end as a fallback so nothing is lost
    return text.rstrip() + f"\n\n{replacement}\n"


def write_markdown_tables(jobs):
    interns = [j for j in jobs if j["category"] == "Intern"]
    newgrads = [j for j in jobs if j["category"] == "New Grad"]

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    intern_block = f"_Last updated: {now}_\n\n{table(interns)}" if interns else f"_Last updated: {now}_\n\n_No open hardware internships found in the last run._"
    newgrad_block = f"_Last updated: {now}_\n\n{table(newgrads)}" if newgrads else f"_Last updated: {now}_\n\n_No open hardware new-grad roles found in the last run._"

    readme_text = README_PATH.read_text()
    readme_text = replace_between(readme_text, INTERN_START, INTERN_END, intern_block)
    readme_text = replace_between(readme_text, NEWGRAD_START, NEWGRAD_END, newgrad_block)
    README_PATH.write_text(readme_text)

    print(f"Updated README.md with {len(interns)} internships and {len(newgrads)} new-grad roles.")


def main():
    jobs = scrape_all()

    try:
        from scrape_workday import scrape_all_workday
        jobs.extend(scrape_all_workday())
    except Exception as e:
        print(f"  [warn] Workday scraping skipped: {e}", file=sys.stderr)

    seen = load_seen()
    new_count = sum(1 for j in jobs if j["id"] not in seen)
    for j in jobs:
        seen[j["id"]] = j["posted"]
    save_seen(seen)
    write_markdown_tables(jobs)
    print(f"Done. {new_count} new postings this run.")


if __name__ == "__main__":
    main()
