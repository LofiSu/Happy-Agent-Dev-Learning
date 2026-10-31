#!/usr/bin/env python3
"""Check LICENSE, README, and markdown links in the root docs."""

from __future__ import annotations

import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
DOCS = (ROOT / "README.md", ROOT / "CONTRIBUTING.md")
USER_AGENT = "happy-agent-dev-learning-link-check"


def fail(messages: list[str]) -> None:
    print("\n".join(messages), file=sys.stderr)
    sys.exit(1)


def strip_destination(raw: str) -> str:
    dest = raw.strip()
    if dest.startswith("<") and ">" in dest:
        dest = dest[1 : dest.index(">")]
    elif " " in dest:
        dest = dest.split()[0]
    return dest.strip()


def check_external(url: str, source: Path, failures: list[str]) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            status = response.status
    except urllib.error.HTTPError as exc:
        status = exc.code
    except Exception as exc:  # noqa: BLE001 - report the network failure as a link error
        failures.append(f"{source.name}: {url} -> {exc}")
        return
    if status >= 400:
        failures.append(f"{source.name}: {url} -> HTTP {status}")


def main() -> None:
    failures: list[str] = []
    license_path = ROOT / "LICENSE"
    readme_path = ROOT / "README.md"

    if not license_path.is_file() or license_path.stat().st_size == 0:
        failures.append("LICENSE is missing or empty")
    else:
        text = license_path.read_text(encoding="utf-8")
        if "MIT License" not in text or "Permission is hereby granted" not in text:
            failures.append("LICENSE is not the MIT license text")

    if not readme_path.is_file() or readme_path.stat().st_size == 0:
        failures.append("README.md is missing or empty")

    if failures:
        fail(failures)

    seen: set[str] = set()
    for doc in DOCS:
        if not doc.is_file() or doc.stat().st_size == 0:
            failures.append(f"{doc.name} is missing or empty")
            continue
        body = FENCE_RE.sub("", doc.read_text(encoding="utf-8"))
        for match in LINK_RE.findall(body):
            dest = strip_destination(match)
            if not dest or dest.startswith("#") or dest.startswith("mailto:"):
                continue
            if dest in seen:
                continue
            seen.add(dest)
            if dest.startswith(("http://", "https://")):
                check_external(dest, doc, failures)
                continue
            path = dest.split("#", 1)[0]
            if not path:
                continue
            target = (doc.parent / Path(urllib.parse.unquote(path))).resolve()
            try:
                target.relative_to(ROOT)
            except ValueError:
                failures.append(f"{doc.name}: link escapes the repo: {dest}")
                continue
            if not target.is_file():
                failures.append(f"{doc.name}: missing file for {dest}")

    if failures:
        fail(failures)
    print(f"checked {len(seen)} links; LICENSE and README.md are present")


if __name__ == "__main__":
    main()
