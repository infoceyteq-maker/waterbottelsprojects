#!/usr/bin/env python3
"""One-command build for the whole pack.

    python3 build/build_all.py

Runs, in order:
  1. build_checklist.py  -> docs/12-master-document-checklist.md  (from the CSV)
  2. build_dashboard.py  -> site/dashboard.html                   (the panel)
  3. build_site.py       -> site/*.html + copies the dashboard to site/index.html
  4. check_links.py      -> self-check; exits non-zero if anything is broken

The dashboard is served at "/" because build_site.py publishes it as the root.
Preview:  cd site && python3 -m http.server 8000 --bind 0.0.0.0
"""
import os
import subprocess
import sys

BUILD = os.path.dirname(os.path.abspath(__file__))
STEPS = ["build_checklist.py", "build_dashboard.py", "build_site.py", "check_links.py"]


def main():
    for step in STEPS:
        print(f"\n{'='*68}\n>>> {step}\n{'='*68}")
        rc = subprocess.call([sys.executable, os.path.join(BUILD, step)])
        if rc != 0:
            print(f"\n[FAIL] {step} exited {rc}")
            return rc
    print("\n[ok] all builds passed - the dashboard is served at \"/\"")
    return 0


if __name__ == "__main__":
    sys.exit(main())
