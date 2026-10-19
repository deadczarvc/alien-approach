# alien-approach — the Alien Approach skill

**English** · [Русский](README.ru.md)

An agent skill for problems that will not yield in their own domain. Instead of pushing harder
with the same method, the agent builds a **bridge** into a neighbouring formalism where a ready
solver exists, solves the problem there, maps the result back, and proves it with a live probe
of the original symptom.

> Don't hit harder — change the game.

Version **0.9.0** · MIT · works with any agent that reads `SKILL.md` (Claude Code, Claude.ai,
Codex-style agents and similar).

## When to use it

Any one of these:

- two or more honest attempts inside the problem's own domain changed nothing;
- the search space grows faster than your resources;
- ideas keep circling around one method;
- the problem's own terms are the cage.

Do **not** use it for trivial bugs. The skill first sends the agent through a ladder of 30
ordinary methods; the bridge is the second line.

## How it works

| Phase | Anchor | What happens |
|---|---|---|
| 1 | 诊断 stuck | Log what was tried and why it failed; finish the ordinary ladder |
| 2 | 搜索 pick bridge | Choose 2–3 bridges from the catalogue; a bridge counts only if a ready solver exists there |
| 3 | 转换 transfer | Restate the problem in the bridge's terms; name the invariant |
| 4 | 治疗 solve there | Apply the foreign solver (theorem, mechanism, SMT/Prolog/ASP encoding) |
| 5 | 测试 return | Map the result back, run the live probe, re-check the invariant |

Bridge classes: **M** method (measure instead of enumeration), **S** statement (invariant),
**C** contradiction (prove the solution class is empty), **P** price instead of a ban,
**X** formal (invariant → z3, SWI-Prolog or clingo).

The output is always five fields: `bridge`, `invariant`, `proof`, `verdict`, `journal`.

## Contents

```text
alien-approach/
├── SKILL.md                         the skill (Russian body, English terms)
├── references/
│   ├── examples-30.md               L1: 30 ordinary methods (sample corpus: MCP servers and services)
│   ├── counterexamples-90.md        L2: 90 bridges in 9 domains + formal class X
│   └── alien-approach.xtml          the same logic as an XTML document for agent-to-agent use
└── scripts/
    └── probe-f0.py                  runtime check for bridge X solvers
```

## Install

Download the latest release from
[Releases](https://github.com/deadczarvc/alien-approach/releases):

- `alien-approach-<version>.skill` — upload in Claude.ai (Settings → Capabilities → Skills), or
  install with any tool that accepts `.skill` packages;
- `alien-approach-<version>.zip` — unpack into your skills folder, for example
  `~/.claude/skills/` for Claude Code, so that you get `~/.claude/skills/alien-approach/SKILL.md`.

Check the download against `SHA256SUMS` from the same release.

Optional solvers for bridge X:

```bash
pip install z3-solver clingo
```

SWI-Prolog: install from swi-prolog.org. Then check the runtime:

```bash
python alien-approach/scripts/probe-f0.py
```

Exit code 0 — at least one solver passed its positive and negative control; 1 — a solver gave a
wrong answer; 2 — no solver found. A missing solver is reported as `SKIP`.

## Build a release yourself

```bash
python tools/build_release.py
```

The script checks the frontmatter against the official skill rules, checks that `VERSION` matches
`metadata.version`, and writes reproducible `.skill`, `.zip` and `SHA256SUMS` into `dist/`.
Pushing a tag `vX.Y.Z` runs the same build in GitHub Actions and publishes the release.

## Methods used to shape the skill

MK2 prompt structure, CompactPrompt code tables, MetaGlyph logic notation (`∀ ⇒ ¬ ∈ ∧ ∨`),
stable phase anchors in Chinese, and an XTML document copy. The anchors are labels for phases,
not a cipher; the claims are kept to what was measured.

## License

MIT — see [LICENSE](LICENSE).
