#!/usr/bin/env python3
"""One-command build for the whole pack.

    python3 -m venv .venv
    .venv/bin/python -m pip install -r requirements.txt
    .venv/bin/python build/build_all.py

(Windows: use .venv\\Scripts\\python.exe instead of .venv/bin/python.)

Runs, in order:
  1. build_checklist.py  -> docs/12-master-document-checklist.md  (from the CSV)
  2. build_dashboard.py  -> site/dashboard.html                   (the panel)
  3. build_site.py       -> site/*.html (the 21-document pack)
  4. build_pages.py      -> the 7 pages + the landing page (index.html)
  5. verify_final.py     -> re-derives page 7's money from first principles
  6. check_links.py      -> self-check; exits non-zero if anything is broken

build_pages.py runs before the checks because it owns index.html - the landing
page that links the seven pages, the full dashboard and the document pack.
verify_final.py recomputes the investment, break-even and payback independently
of the renderer, so page 7 cannot be right by coincidence.
Preview:  cd site && python3 -m http.server 8000 --bind 0.0.0.0
"""
import os
import subprocess
import sys

BUILD = os.path.dirname(os.path.abspath(__file__))
STEPS = ["build_checklist.py", "build_dashboard.py", "build_site.py",
         "build_pages.py", "verify_final.py", "check_links.py"]


def main():
    for step in STEPS:
        print(f"\n{'='*68}\n>>> {step}\n{'='*68}")
        rc = subprocess.call([sys.executable, os.path.join(BUILD, step)])
        if rc != 0:
            print(f"\n[FAIL] {step} exited {rc}")
            return rc
    print("\n[ok] all builds passed - the project landing page is served at \"/\"; dashboard at /dashboard.html")
    return 0


if __name__ == "__main__":
    sys.exit(main())
