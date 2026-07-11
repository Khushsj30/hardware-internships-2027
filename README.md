# Hardware Internships & New Grad Jobs 🛠️

A daily-updated, worldwide list of hardware engineering internships and
new-grad roles — chip design (ASIC/FPGA/RTL), RF, embedded/firmware,
mechanical/electrical, robotics, aerospace, EVs, and the FPGA/low-latency
hardware roles that quant trading firms (Jane Street, HRT, Jump, Citadel
Securities, DRW, IMC) hire for too.

Updated automatically every day via GitHub Actions — no manual maintenance
needed for tracked companies. **Cost: $0**, built entirely on free tools
(GitHub Actions + public Greenhouse/Lever job board APIs).

Missing a company or a posting? [Open an issue](../../issues/new/choose) or add it to `scripts/companies.json` and send a PR — see [Contributing](#contributing) below.

---

## 📋 Internships

<!-- INTERNSHIPS:START -->
_Last updated: 2026-07-11 01:57 UTC_

_No open hardware internships found in the last run._
<!-- INTERNSHIPS:END -->

---

## 🎓 New Grad Roles

<!-- NEWGRAD:START -->
_Last updated: 2026-07-11 01:57 UTC_

_No open hardware new-grad roles found in the last run._
<!-- NEWGRAD:END -->

---

## How it works

A script (`scripts/scrape.py`) pulls open postings from each tracked
company's public ATS API (Greenhouse, Lever) once a day via GitHub Actions,
filters for hardware-related titles, classifies them as Intern or New Grad,
and rewrites the two tables above directly in this README between the
marker comments. Nothing else needs to change by hand.

## Contributing

Two ways to help grow the list:

1. **Open an issue** using the ["Add a hardware job posting"](../../issues/new/choose) template if you spot a role that's missing.
2. **Add a company to the scraper** — edit `scripts/companies.json`:
   - Greenhouse: find the token from `boards.greenhouse.io/<token>`
   - Lever: find the token from `jobs.lever.co/<token>`
   ```json
   { "name": "Company Name", "ats": "greenhouse", "token": "companytoken" }
   ```
   Then open a PR.

Workday-based companies (Apple, Intel, TI, Qualcomm, and most large
semiconductor companies use this) need a bit more setup — see
`scripts/workday_companies.json` for instructions. This is optional; the
scraper works fully without it.

## Running locally

```bash
pip install requests
python scripts/scrape.py
```
