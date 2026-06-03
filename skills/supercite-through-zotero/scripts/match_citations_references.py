#!/usr/bin/env python3
"""Compare manuscript citation keys with BibTeX/BibLaTeX entries."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

from extract_citation_signals import CitationSignal, extract_from_file


BIB_ENTRY_RE = re.compile(r"@\w+\s*\{\s*([^,\s]+)\s*,", re.MULTILINE)


@dataclass(frozen=True)
class MatchReport:
    cited_keys: list[str]
    bib_keys: list[str]
    missing_references: list[str]
    unused_references: list[str]
    unkeyed_citation_signals: list[dict[str, object]]


def parse_bib_keys(paths: list[Path]) -> set[str]:
    keys: set[str] = set()
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="replace")
        keys.update(match.group(1).strip() for match in BIB_ENTRY_RE.finditer(text))
    return keys


def keyed_citations(signals: list[CitationSignal]) -> tuple[set[str], list[CitationSignal]]:
    cited: set[str] = set()
    unkeyed: list[CitationSignal] = []

    for signal in signals:
        if signal.kind in {"tex", "pandoc"}:
            cited.update(signal.keys)
        else:
            unkeyed.append(signal)
    return cited, unkeyed


def build_report(manuscript_paths: list[Path], bib_paths: list[Path]) -> MatchReport:
    signals: list[CitationSignal] = []
    for path in manuscript_paths:
        signals.extend(extract_from_file(path))

    cited, unkeyed = keyed_citations(signals)
    bib_keys = parse_bib_keys(bib_paths)

    return MatchReport(
        cited_keys=sorted(cited),
        bib_keys=sorted(bib_keys),
        missing_references=sorted(cited - bib_keys),
        unused_references=sorted(bib_keys - cited),
        unkeyed_citation_signals=[
            {
                "file": signal.file,
                "line": signal.line,
                "column": signal.column,
                "kind": signal.kind,
                "raw": signal.raw,
                "risk_hint": signal.risk_hint,
            }
            for signal in unkeyed
        ],
    )


def human_report(report: MatchReport) -> str:
    lines = [
        f"Cited keys: {len(report.cited_keys)}",
        f"Bibliography keys: {len(report.bib_keys)}",
        f"Missing references: {len(report.missing_references)}",
        f"Unused references: {len(report.unused_references)}",
        f"Unkeyed citation signals: {len(report.unkeyed_citation_signals)}",
    ]

    if report.missing_references:
        lines.append("")
        lines.append("Missing references:")
        lines.extend(f"- {key}" for key in report.missing_references)

    if report.unused_references:
        lines.append("")
        lines.append("Unused references:")
        lines.extend(f"- {key}" for key in report.unused_references)

    if report.unkeyed_citation_signals:
        lines.append("")
        lines.append("Unkeyed signals to review:")
        for item in report.unkeyed_citation_signals:
            lines.append(
                f"- {item['file']}:{item['line']}:{item['column']} "
                f"{item['kind']} {item['raw']} ({item['risk_hint']})"
            )

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manuscripts", nargs="+", help="Manuscript files to inspect")
    parser.add_argument("--bib", action="append", required=True, help="BibTeX/BibLaTeX file")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    report = build_report(
        [Path(path) for path in args.manuscripts],
        [Path(path) for path in args.bib],
    )

    if args.json:
        print(json.dumps(asdict(report), indent=2, ensure_ascii=False))
    else:
        print(human_report(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

