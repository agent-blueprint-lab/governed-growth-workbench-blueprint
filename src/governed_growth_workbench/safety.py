from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Finding:
    path: Path
    line: int
    rule: str


_PATTERNS = {
    "email": re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE),
    "mainland-phone": re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"),
    "private-ip": re.compile(r"(?<!\d)(?:10\.\d{1,3}(?:\.\d{1,3}){2}|192\.168(?:\.\d{1,3}){2}|172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2})(?!\d)"),
    "local-user-path": re.compile(re.escape("/" + "Users/") + "|" + re.escape("/" + "home/")),
    "credential-assignment": re.compile(
        r"(?:api" + r"[_-]?key|pass" + r"word|secret|token)\s*[:=]\s*['\"][^'\"]{8,}",
        re.IGNORECASE,
    ),
    "github-token": re.compile(r"gh" + r"[pousr]_[A-Za-z0-9]{20,}"),
    "aws-key": re.compile(r"AK" + r"IA[0-9A-Z]{16}"),
}

_TEXT_SUFFIXES = {
    ".html",
    ".json",
    ".md",
    ".py",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
_TEXT_NAMES = {"Makefile"}
_EXCLUDED_PARTS = {".git", ".agent-loop", ".venv", "build", "dist", "node_modules"}
_EXCLUDED_FILES = {Path("config/publication-denylist.txt")}


def _denylist(root: Path) -> list[str]:
    path = root / "config" / "publication-denylist.txt"
    if not path.exists():
        return []
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def scan(root: Path) -> list[Finding]:
    root = root.resolve()
    denied = _denylist(root)
    findings: list[Finding] = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if not path.is_file() or any(part in _EXCLUDED_PARTS for part in relative.parts):
            continue
        if relative in _EXCLUDED_FILES:
            continue
        if path.suffix not in _TEXT_SUFFIXES and path.name not in _TEXT_NAMES:
            continue
        text = path.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            for name, pattern in _PATTERNS.items():
                if pattern.search(line):
                    findings.append(Finding(relative, line_number, name))
            for term in denied:
                if term.casefold() in line.casefold():
                    findings.append(Finding(relative, line_number, "denylist-term"))
    return findings
