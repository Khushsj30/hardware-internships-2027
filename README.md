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
_Last updated: 2026-07-22 15:00 UTC_

| Company | Role | Location | Posted | Link |
|---|---|---|---|---|
| Jump Trading | Campus ASIC Engineer (Intern) | Bristol | 2026-07-22 | [Apply](https://www.jumptrading.com/hr/job?gh_jid=7974837) |
| Jump Trading | Campus FPGA Engineer (Intern) | London | 2026-07-22 | [Apply](https://www.jumptrading.com/hr/job?gh_jid=7974391) |
| Anduril | 2027 Electrical Engineer Intern | Atlanta, Georgia, United States; Boston, Massachusetts, United States; Costa Mesa, California, United States; Irvine, California, United States; Reston, Virginia, United States; Seattle, Washington, United States | 2026-07-17 | [Apply](https://boards.greenhouse.io/andurilindustries/jobs/5148101007?gh_jid=5148101007) |
| Anduril | 2027 Manufacturing Engineer Intern | Atlanta, Georgia, United States; Boston, Massachusetts, United States; Costa Mesa, California, United States; Irvine, California, United States; Seattle, Washington, United States | 2026-07-17 | [Apply](https://boards.greenhouse.io/andurilindustries/jobs/5153218007?gh_jid=5153218007) |
| Anduril | 2027 Mechanical Engineer Intern | Atlanta, Georgia, United States; Boston, Massachusetts, United States; Costa Mesa, California, United States; Irvine, California, United States; Reston, Virginia, United States; Seattle, Washington, United States | 2026-07-17 | [Apply](https://boards.greenhouse.io/andurilindustries/jobs/5153187007?gh_jid=5153187007) |
| Jump Trading | Campus Systems Engineer (Intern) | London; Amsterdam | 2026-07-13 | [Apply](https://www.jumptrading.com/hr/job?gh_jid=8000323) |
| Jump Trading | Campus Systems Engineer (Intern) | Chicago | 2026-07-09 | [Apply](https://www.jumptrading.com/hr/job?gh_jid=8007788) |
| IMC Trading | Hardware Machine Learning PhD Research Internship | Chicago, United States | 2026-07-09 | [Apply](https://job-boards.eu.greenhouse.io/imc/jobs/4829785101) |
| Jump Trading | Campus FPGA Engineer (Intern) | Chicago | 2026-07-08 | [Apply](https://www.jumptrading.com/hr/job?gh_jid=8003013) |
| IMC Trading | 2027 - FPGA Intern - IIT Bombay | Amsterdam, Netherlands; Mumbai, India | 2026-07-08 | [Apply](https://job-boards.eu.greenhouse.io/imc/jobs/4860306101) |
| IMC Trading | Hardware Engineer Intern - Summer 2027 | Chicago, United States | 2026-07-01 | [Apply](https://job-boards.eu.greenhouse.io/imc/jobs/4823945101) |
<!-- INTERNSHIPS:END -->

---

## 🎓 New Grad Roles

<!-- NEWGRAD:START -->
_Last updated: 2026-07-22 15:00 UTC_

| Company | Role | Location | Posted | Link |
|---|---|---|---|---|
| Anduril | Early Career Firmware Engineer  | Costa Mesa, California, United States | 2026-07-22 | [Apply](https://boards.greenhouse.io/andurilindustries/jobs/5167865007?gh_jid=5167865007) |
| Anduril | 2026 Early Career Flight Test Engineer, Mission Autonomy | Costa Mesa, California, United States | 2026-07-21 | [Apply](https://boards.greenhouse.io/andurilindustries/jobs/5185089007?gh_jid=5185089007) |
| SpaceX | Entry Level Production Technician - PCBA | Redmond, WA | 2026-07-20 | [Apply](https://boards.greenhouse.io/spacex/jobs/8352158002?gh_jid=8352158002) |
| Anduril | 2026 Early Career Electrical Engineer | Costa Mesa, California, United States; Fort Collins, Colorado, United States | 2026-07-17 | [Apply](https://boards.greenhouse.io/andurilindustries/jobs/4802172007?gh_jid=4802172007) |
| Anduril | 2026 Early Career Electrical Engineer, Battlespace Awareness Radar Team | Fort Collins, Colorado, United States | 2026-07-17 | [Apply](https://boards.greenhouse.io/andurilindustries/jobs/4747967007?gh_jid=4747967007) |
| Anduril | 2026 Early Career Manufacturing Engineer | Costa Mesa, California, United States; Irvine, California, United States; Santa Ana, California, United States | 2026-07-17 | [Apply](https://boards.greenhouse.io/andurilindustries/jobs/5176254007?gh_jid=5176254007) |
| Anduril | 2026 Early Career Mechanical Engineer | Costa Mesa, California, United States | 2026-07-17 | [Apply](https://boards.greenhouse.io/andurilindustries/jobs/4802167007?gh_jid=4802167007) |
| Anduril | 2027 Early Career Electrical Engineer | Atlanta, Georgia, United States; Boston, Massachusetts, United States; Costa Mesa, California, United States; Irvine, California, United States; Reston, Virginia, United States; Seattle, Washington, United States | 2026-07-17 | [Apply](https://boards.greenhouse.io/andurilindustries/jobs/5136925007?gh_jid=5136925007) |
| Anduril | 2027 Early Career Manufacturing Engineer | Atlanta, Georgia, United States; Boston, Massachusetts, United States; Costa Mesa, California, United States; Irvine, California, United States; Seattle, Washington, United States | 2026-07-17 | [Apply](https://boards.greenhouse.io/andurilindustries/jobs/5136970007?gh_jid=5136970007) |
| Anduril | 2027 Early Career Mechanical Engineer | Atlanta, Georgia, United States; Boston, Massachusetts, United States; Costa Mesa, California, United States; Irvine, California, United States; Reston, Virginia, United States; Seattle, Washington, United States | 2026-07-17 | [Apply](https://boards.greenhouse.io/andurilindustries/jobs/5136984007?gh_jid=5136984007) |
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
