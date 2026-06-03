#!/usr/bin/env python3
"""Extract citation-like signals from academic manuscript text.

This script is intentionally conservative. It finds likely citation structures
for review; it does not decide whether sources support claims.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence


TEX_CITE_RE = re.compile(
    r"\\(?P<cmd>[A-Za-z]*cite[A-Za-z]*|parencite|textcite|autocite|footcite)"
    r"(?:\s*\[[^\]]*\])*"
    r"\s*\{(?P<keys>[^{}]+)\}"
)
PANDOC_BRACKET_RE = re.compile(r"\[(?P<body>[^\]]*@[-A-Za-z0-9_:.]+[^\]]*)\]")
PANDOC_KEY_RE = re.compile(r"@(?P<key>[-A-Za-z0-9_:.]+)")
NUMERIC_CLUSTER_RE = re.compile(r"\[(?P<body>\s*\d+(?:\s*(?:,|-|;)\s*\d+)*\s*)\]")
AUTHOR_YEAR_PAREN_RE = re.compile(
    r"\((?P<body>[^()\n]*(?:19|20)\d{2}[a-z]?[^()\n]*)\)"
)
AUTHOR_YEAR_TEXTUAL_RE = re.compile(
    r"\b(?P<author>[A-Z][A-Za-z'`-]+(?:\s+et\s+al\.)?)\s*"
    r"\((?P<year>(?:19|20)\d{2}[a-z]?)\)"
)


@dataclass(frozen=True)
class CitationSignal:
    file: str
    line: int
    column: int
    kind: str
    raw: str
    keys: list[str]
    cluster_size: int
    paragraph_index: int
    sentence_index: int
    near_paragraph_end: bool
    risk_hint: str


def split_paragraphs(text: str) -> list[tuple[int, str]]:
    paragraphs: list[tuple[int, str]] = []
    start = 0
    current: list[str] = []
    current_start = 0

    for line_no, line in enumerate(text.splitlines(), start=1):
        if line.strip():
            if not current:
                current_start = line_no
            current.append(line)
        elif current:
            paragraphs.append((current_start, "\n".join(current)))
            current = []

    if current:
        paragraphs.append((current_start, "\n".join(current)))

    if not paragraphs and text.strip():
        paragraphs.append((1, text))

    return paragraphs


def sentence_index_for_offset(paragraph: str, offset: int) -> int:
    before = paragraph[:offset]
    endings = re.findall(r"[.!?](?:\s+|$)", before)
    return len(endings) + 1


def line_col_for_offset(text: str, offset: int) -> tuple[int, int]:
    line = text.count("\n", 0, offset) + 1
    last_newline = text.rfind("\n", 0, offset)
    column = offset + 1 if last_newline < 0 else offset - last_newline
    return line, column


def normalize_key_list(raw: str) -> list[str]:
    keys = []
    for part in re.split(r"[,;]\s*", raw):
        cleaned = part.strip()
        if cleaned:
            keys.append(cleaned)
    return keys


def split_author_year_items(body: str) -> list[str]:
    parts = [part.strip() for part in re.split(r";", body) if part.strip()]
    if len(parts) > 1:
        return parts
    year_hits = re.findall(r"(?:19|20)\d{2}[a-z]?", body)
    return [body.strip()] if year_hits else []


def risk_hint(kind: str, keys: Sequence[str], near_paragraph_end: bool, raw: str) -> str:
    size = len(keys)
    if kind in {"tex", "pandoc", "author_year", "numeric"} and size >= 5:
        return "large citation cluster; check whether sources support one narrow claim"
    if near_paragraph_end and size >= 3:
        return "paragraph-end cluster; check for citation dumping"
    if re.search(r"\b(however|whereas|while|although|and|but)\b", raw, re.I) and size >= 3:
        return "multi-part sentence; check claim-source alignment"
    return "review placement"


def collect_matches(pattern: re.Pattern[str], paragraph: str) -> Iterable[re.Match[str]]:
    yield from pattern.finditer(paragraph)


def extract_from_text(text: str, file_label: str = "<stdin>") -> list[CitationSignal]:
    signals: list[CitationSignal] = []
    paragraphs = split_paragraphs(text)
    global_offset = 0

    for paragraph_index, (start_line, paragraph) in enumerate(paragraphs, start=1):
        paragraph_start = text.find(paragraph, global_offset)
        if paragraph_start < 0:
            paragraph_start = 0
        global_offset = paragraph_start + len(paragraph)

        match_specs: list[tuple[str, re.Match[str], list[str]]] = []

        for match in collect_matches(TEX_CITE_RE, paragraph):
            keys = normalize_key_list(match.group("keys"))
            match_specs.append(("tex", match, keys))

        for match in collect_matches(PANDOC_BRACKET_RE, paragraph):
            keys = [m.group("key") for m in PANDOC_KEY_RE.finditer(match.group("body"))]
            match_specs.append(("pandoc", match, keys))

        for match in collect_matches(NUMERIC_CLUSTER_RE, paragraph):
            body = match.group("body")
            numbers = [part.strip() for part in re.split(r"[,;]\s*", body) if part.strip()]
            match_specs.append(("numeric", match, numbers))

        for match in collect_matches(AUTHOR_YEAR_PAREN_RE, paragraph):
            body = match.group("body")
            items = split_author_year_items(body)
            if items:
                match_specs.append(("author_year", match, items))

        for match in collect_matches(AUTHOR_YEAR_TEXTUAL_RE, paragraph):
            key = f"{match.group('author')} {match.group('year')}"
            match_specs.append(("textual_author_year", match, [key]))

        seen: set[tuple[int, int, str]] = set()
        for kind, match, keys in sorted(match_specs, key=lambda item: item[1].start()):
            identity = (match.start(), match.end(), kind)
            if identity in seen:
                continue
            seen.add(identity)

            absolute_offset = paragraph_start + match.start()
            line, column = line_col_for_offset(text, absolute_offset)
            near_end = match.end() >= max(len(paragraph) - 80, int(len(paragraph) * 0.8))
            raw = match.group(0)
            signals.append(
                CitationSignal(
                    file=file_label,
                    line=line,
                    column=column,
                    kind=kind,
                    raw=raw,
                    keys=keys,
                    cluster_size=len(keys),
                    paragraph_index=paragraph_index,
                    sentence_index=sentence_index_for_offset(paragraph, match.start()),
                    near_paragraph_end=near_end,
                    risk_hint=risk_hint(kind, keys, near_end, raw),
                )
            )

    return signals


def extract_from_file(path: Path) -> list[CitationSignal]:
    text = path.read_text(encoding="utf-8", errors="replace")
    return extract_from_text(text, str(path))


def summarize(signals: Sequence[CitationSignal]) -> str:
    by_kind: dict[str, int] = {}
    large_clusters = 0
    paragraph_end_clusters = 0
    for signal in signals:
        by_kind[signal.kind] = by_kind.get(signal.kind, 0) + 1
        if signal.cluster_size >= 5:
            large_clusters += 1
        if signal.near_paragraph_end and signal.cluster_size >= 3:
            paragraph_end_clusters += 1

    lines = [
        f"Total citation signals: {len(signals)}",
        "By kind: "
        + (", ".join(f"{kind}={count}" for kind, count in sorted(by_kind.items())) or "none"),
        f"Large clusters (>=5 items): {large_clusters}",
        f"Paragraph-end clusters (>=3 items): {paragraph_end_clusters}",
    ]

    if signals:
        lines.append("")
        lines.append("Signals:")
    for signal in signals:
        key_text = ", ".join(signal.keys)
        lines.append(
            f"- {signal.file}:{signal.line}:{signal.column} "
            f"{signal.kind} size={signal.cluster_size} keys=[{key_text}] "
            f"hint={signal.risk_hint}"
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", help="Manuscript files to inspect")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    signals: list[CitationSignal] = []
    for file_name in args.files:
        signals.extend(extract_from_file(Path(file_name)))

    if args.json:
        print(json.dumps([asdict(signal) for signal in signals], indent=2, ensure_ascii=False))
    else:
        print(summarize(signals))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

