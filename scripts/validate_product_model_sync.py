#!/usr/bin/env python3
"""Verify that all product-spec skills ship the same product model schema."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL_FILES = (
    ROOT / "skills/product-spec/references/product-model.md",
    ROOT / "skills/product-spec-author/references/product-model.md",
    ROOT / "skills/product-spec-review/references/product-model.md",
)
VERSION_PATTERN = re.compile(r"^Model version: `([^`]+)`$", re.MULTILINE)


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def main() -> int:
    missing = [path for path in MODEL_FILES if not path.is_file()]
    if missing:
        for path in missing:
            print(f"missing: {path.relative_to(ROOT)}", file=sys.stderr)
        return 1

    contents = {path: path.read_bytes() for path in MODEL_FILES}
    canonical_path = MODEL_FILES[0]
    canonical = contents[canonical_path]
    canonical_hash = digest(canonical)

    failed = False
    versions: dict[Path, str | None] = {}

    for path, content in contents.items():
        text = content.decode("utf-8")
        match = VERSION_PATTERN.search(text)
        versions[path] = match.group(1) if match else None

        current_hash = digest(content)
        status = "ok" if content == canonical else "different"
        print(
            f"{status}: {path.relative_to(ROOT)} "
            f"version={versions[path] or 'missing'} sha256={current_hash}"
        )

        if content != canonical or versions[path] is None:
            failed = True

    if len(set(versions.values())) != 1:
        print("product model versions do not match", file=sys.stderr)
        failed = True

    if failed:
        print(
            f"canonical: {canonical_path.relative_to(ROOT)} sha256={canonical_hash}",
            file=sys.stderr,
        )
        return 1

    print(f"all product model copies match version {versions[canonical_path]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
