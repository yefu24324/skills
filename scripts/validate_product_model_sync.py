#!/usr/bin/env python3
"""Verify shared product-spec references remain identical across all three skills."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOTS = (
    ROOT / "skills/product-spec",
    ROOT / "skills/product-spec-author",
    ROOT / "skills/product-spec-review",
)
SHARED_REFERENCES = {
    "product-model.md": re.compile(r"^Model version: `([^`]+)`$", re.MULTILINE),
    "product-stage-workflow.md": re.compile(
        r"^Workflow version: `([^`]+)`$", re.MULTILINE
    ),
    "page-structure.md": re.compile(
        r"^Standard version: `([^`]+)`$", re.MULTILINE
    ),
}


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def validate_reference(filename: str, version_pattern: re.Pattern[str]) -> bool:
    paths = tuple(root / "references" / filename for root in SKILL_ROOTS)
    missing = [path for path in paths if not path.is_file()]
    if missing:
        for path in missing:
            print(f"missing: {path.relative_to(ROOT)}", file=sys.stderr)
        return False

    contents = {path: path.read_bytes() for path in paths}
    canonical_path = paths[0]
    canonical = contents[canonical_path]
    canonical_hash = digest(canonical)
    versions: dict[Path, str | None] = {}
    valid = True

    for path, content in contents.items():
        text = content.decode("utf-8")
        match = version_pattern.search(text)
        versions[path] = match.group(1) if match else None
        current_hash = digest(content)
        status = "ok" if content == canonical else "different"
        print(
            f"{status}: {path.relative_to(ROOT)} "
            f"version={versions[path] or 'missing'} sha256={current_hash}"
        )
        if content != canonical or versions[path] is None:
            valid = False

    if len(set(versions.values())) != 1:
        print(f"{filename} versions do not match", file=sys.stderr)
        valid = False

    if not valid:
        print(
            f"canonical: {canonical_path.relative_to(ROOT)} sha256={canonical_hash}",
            file=sys.stderr,
        )
        return False

    print(f"all {filename} copies match version {versions[canonical_path]}")
    return True


def main() -> int:
    results = [
        validate_reference(filename, pattern)
        for filename, pattern in SHARED_REFERENCES.items()
    ]
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
