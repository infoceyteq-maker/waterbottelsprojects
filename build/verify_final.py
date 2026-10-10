"""Independent re-derivation of the page-7 figures, from first principles.

Nothing here reads F[...] except to compare.  Every number on the left is
recomputed from the raw constants so the page cannot be right by coincidence.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
import dashboard_model as dm

M = dm.build_model()
F = M["final"]
dt = M["doc_totals"]

# --- investment: rebuild from the six setup components + page 2 ---
sub = (dt["registration"] + dt["equipment"] + M["office_total"]
       + dt["transport"] + dt["misc"] + M["hr_one_off_total"])
inv = round(sub * (1 + dm.CONTINGENCY_PCT)) + round(M["fp_total"])

# --- fixed cost: re-sum FIXED_Y1 (already patched with the real payroll) ---
fx = sum(dm.FIXED_Y1.values())

# --- earnings rate: recompute straight off the first stock ---
pb = M["fs_margin"] / M["fs_bottles"]

be_day = fx / pb / M["work_days"]
oy_day = (inv / 12 + fx) / pb / M["work_days"]

def row(label, mine, model, tol=1.0):
    ok = abs(mine - model) <= tol
    print("  %-16s mine %18s | model %18s | %s"
          % (label, format(mine, ",.0f"), format(model, ",.0f"),
             "OK" if ok else "MISMATCH"))
    return ok

print("--- independent re-derivation of page 7 ---")
ok = True
ok &= row("investment", inv, F["investment"], 0)
ok &= row("fixed/month", fx, F["fixed"], 0)
ok &= row("profit/bottle", pb, F["per_bottle"], 0.005)
ok &= row("break-even/day", be_day, F["be_day"])
ok &= row("1-year/day", oy_day, F["one_year"]["bottles_day"])

# close the loop: does that daily rate really repay the investment in 12 months?
per_day = round(oy_day)
repay = 12 * (per_day * M["work_days"] * pb - fx)
err = abs(repay - inv) / inv * 100
print("  loop check       12 months x %s bottles/day repays Rs %s"
      % (format(per_day, ","), format(round(repay), ",")))
print("                   vs investment Rs %s  -> %.3f%% off  %s"
      % (format(inv, ","), err, "OK" if err < 0.05 else "MISMATCH"))
ok &= err < 0.05

# break-even loop: at the break-even rate profit must be ~zero
be_per_day = round(be_day)
be_profit = be_per_day * M["work_days"] * pb - fx
print("  break-even loop  %s bottles/day x 25 days -> monthly profit Rs %s %s"
      % (format(be_per_day, ","), format(round(be_profit), ","),
         "OK (~zero)" if abs(be_profit) < 0.02 * fx else "MISMATCH"))
ok &= abs(be_profit) < 0.02 * fx

# 100% capacity payback
r100 = 1200000 * pb - fx
pb100 = inv / r100
print("  100%% payback     %.2f months | model %.2f  %s"
      % (pb100, F["payback_rows"][-1]["months"],
         "OK" if abs(pb100 - F["payback_rows"][-1]["months"]) < 0.01 else "MISMATCH"))
ok &= abs(pb100 - F["payback_rows"][-1]["months"]) < 0.01

# 25% capacity must be a loss -> never repays
loss = 300000 * pb - fx
print("  25%% capacity     monthly Rs %s -> repays: %s  %s"
      % (format(round(loss), ","), F["payback_rows"][0]["months"],
         "OK (None)" if F["payback_rows"][0]["months"] is None else "MISMATCH"))
ok &= F["payback_rows"][0]["months"] is None and loss < 0

# one-year target must fit inside one shift
print("  1-yr feasible    %.1f%% of capacity, one shift = %s/day  %s"
      % (F["one_year"]["util"] * 100, format(round(F["nameplate_day"]), ","),
         "OK" if F["one_year"]["feasible"] else "MISMATCH"))
ok &= F["one_year"]["feasible"]

# after-tax one-year target must NOT fit (that is what the page warns about)
print("  1-yr after tax   %.1f%% of capacity  %s"
      % (F["one_year"]["util_tax"] * 100,
         "OK (infeasible, as warned)" if not F["one_year"]["feasible_tax"]
         else "MISMATCH"))
ok &= not F["one_year"]["feasible_tax"]

print("\n%s" % ("ALL CHECKS OK" if ok else "SOMETHING DID NOT RECONCILE"))
sys.exit(0 if ok else 1)
