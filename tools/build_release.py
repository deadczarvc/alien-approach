"""Build release archives for the alien-approach skill.

Output (in dist/):
  alien-approach-<ver>.skill  — Claude skill package (zip, top folder alien-approach/)
  alien-approach-<ver>.zip    — the same tree as a plain zip
  SHA256SUMS                  — checksums of both

Format follows the official skill-creator package_skill.py; frontmatter rules follow
its quick_validate.py (allowed top-level keys, no angle brackets in description).
VERSION must match `metadata.version` in SKILL.md, otherwise exit 1.
Archives are reproducible: fixed timestamps, sorted entries, no caches.
"""
import hashlib
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "alien-approach"
DIST = ROOT / "dist"
ALLOWED_KEYS = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}
SKIP_PARTS = {"__pycache__", "node_modules", ".DS_Store"}
STAMP = (2026, 1, 1, 0, 0, 0)


def check_frontmatter() -> str:
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        sys.exit("SKILL.md: no frontmatter")
    head = m.group(1)
    keys = set(re.findall(r"^([A-Za-z][\w-]*):", head, re.M))
    if keys - ALLOWED_KEYS:
        sys.exit(f"SKILL.md: unexpected top-level keys {sorted(keys - ALLOWED_KEYS)}")
    desc = re.search(r"^description:(.*?)(?=^\S|\Z)", head, re.M | re.S).group(1)
    desc = desc.replace(">-", "", 1)  # YAML folding marker, not content
    if "<" in desc or ">" in desc:
        sys.exit("SKILL.md: angle brackets in description")
    ver = re.search(r"^  version:\s*(\S+)\s*$", head, re.M)
    want = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not ver or ver.group(1) != want:
        sys.exit(f"version mismatch: VERSION={want} SKILL.md={ver.group(1) if ver else None}")
    return want


def files() -> list[Path]:
    return sorted(p for p in SKILL.rglob("*")
                  if p.is_file() and not SKIP_PARTS & set(p.parts) and p.suffix != ".pyc")


def pack(dest: Path, entries: list[Path]) -> None:
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in entries:
            info = zipfile.ZipInfo(f"alien-approach/{p.relative_to(SKILL).as_posix()}", STAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, p.read_bytes())


def main() -> int:
    ver = check_frontmatter()
    entries = files()
    DIST.mkdir(exist_ok=True)
    sums = []
    for ext in ("skill", "zip"):
        out = DIST / f"alien-approach-{ver}.{ext}"
        pack(out, entries)
        sums.append(f"{hashlib.sha256(out.read_bytes()).hexdigest()}  {out.name}")
        print(out.name, out.stat().st_size, "bytes,", len(entries), "files")
    (DIST / "SHA256SUMS").write_text("\n".join(sums) + "\n", encoding="utf-8")
    print("\n".join(sums))
    return 0


if __name__ == "__main__":
    sys.exit(main())
