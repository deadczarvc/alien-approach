# Changelog

## 0.9.0

First public release.

- SKILL.md restructured to MK2 (role → mission → criteria → process → format → self-check → positioning).
- CompactPrompt code table (L1, L2, INV, SOLV, PROBE, JRNL) and MetaGlyph rules for bridge validity.
- Five phases marked with stable anchors: 诊断 stuck → 搜索 pick bridge → 转换 transfer → 治疗 solve there → 测试 return and probe.
- New: anti-trigger, error-handling table, stop rule (3 rejected bridges), output example.
- Bridge class X (formal: invariant → z3 / SWI-Prolog / clingo) moved into the main text.
- `references/alien-approach.xtml` rebuilt as an XTML `doc` profile document (validator rc 0; the old card failed with rc 2).
- `scripts/probe-f0.py`: a missing solver is SKIP, not FAIL; exit codes 0 / 1 / 2.
- Station-specific paths and tool names removed from references.
- Release assets: `.skill` and `.zip` with SHA256SUMS, built by `tools/build_release.py`.
