"""probe-f0.py — runtime control for bridge X (formal bridge).

Runs a known positive + negative control on each solver:
F0a z3, F0b swipl (SWI-Prolog), F0c clingo. Prints PASS/FAIL/SKIP per line.
A missing solver is SKIP, not FAIL: the bridge just cannot use it.

Exit code: 0 — no FAIL and at least one solver PASS;
           1 — at least one FAIL (solver present but wrong answer);
           2 — no solver available at all.

Install: pip install z3-solver clingo ; SWI-Prolog from swi-prolog.org.
"""
import shutil
import subprocess
import sys
from pathlib import Path

SWIPL_CANDIDATES = [
    Path("C:/Program Files/swipl/bin/swipl.exe"),
    Path("C:/Program Files (x86)/swipl/bin/swipl.exe"),
]

failures: list[str] = []
passed: set[str] = set()


def check(solver: str, name: str, ok: bool, detail: str = "") -> None:
    print(("PASS" if ok else "FAIL"), name, detail)
    if ok:
        passed.add(solver)
    else:
        failures.append(name)


def skip(name: str, detail: str) -> None:
    print("SKIP", name, detail)


def resolve_swipl() -> str:
    found = shutil.which("swipl")
    if found:
        return found
    for cand in SWIPL_CANDIDATES:
        if cand.is_file():
            return str(cand)
    return ""


def probe_z3() -> None:
    try:
        import z3
    except ImportError as exc:
        skip("z3", str(exc))
        return
    x = z3.Int("x")
    s = z3.Solver()
    s.add(x > 2, x < 5)
    sat = s.check() == z3.sat
    ok = sat and 2 < s.model()[x].as_long() < 5
    check("z3", "z3-pos", ok, z3.get_version_string())
    s2 = z3.Solver()
    s2.add(x > 5, x < 2)
    check("z3", "z3-neg", s2.check() == z3.unsat, "unsat-expected")


def probe_clingo() -> None:
    try:
        import clingo
    except ImportError as exc:
        skip("clingo", str(exc))
        return
    ctl = clingo.Control()
    ctl.add("base", [], "a :- not b. b :- not a.")
    ctl.ground([("base", [])])
    models = []
    with ctl.solve(yield_=True) as handle:
        for m in handle:
            models.append(sorted(str(sym) for sym in m.symbols(shown=True)))
            break
    check("clingo", "clingo-pos", len(models) == 1 and len(models[0]) == 1,
          clingo.__version__)
    ctl2 = clingo.Control()
    ctl2.add("base", [], "a. :- a.")
    ctl2.ground([("base", [])])
    check("clingo", "clingo-neg", ctl2.solve().unsatisfiable, "UNSAT-expected")


def probe_swipl() -> None:
    swipl = resolve_swipl()
    if not swipl:
        skip("swipl", "not-found")
        return
    pos = subprocess.run(
        [swipl, "-g", "writeln(f0_pos_ok),halt", "-t", "halt(1)"],
        capture_output=True, text=True, timeout=60,
    )
    check("swipl", "swipl-pos", pos.returncode == 0 and "f0_pos_ok" in pos.stdout,
          "rc=%d" % pos.returncode)
    neg = subprocess.run(
        [swipl, "-g", "fail", "-t", "halt"],
        capture_output=True, text=True, timeout=60,
    )
    check("swipl", "swipl-neg", neg.returncode != 0,
          "rc=%d (nonzero-expected)" % neg.returncode)


def main() -> int:
    probe_z3()
    probe_clingo()
    probe_swipl()
    if failures:
        print("RESULT FAIL", failures)
        return 1
    if not passed:
        print("RESULT NO-SOLVER")
        return 2
    print("RESULT PASS", sorted(passed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
