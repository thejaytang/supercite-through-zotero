#!/usr/bin/env python3
"""Generate a first-pass Markdown citation audit summary."""

from __future__ import annotations

import argparse
from pathlib import Path

from extract_citation_signals import CitationSignal, extract_from_file
from match_citations_references import MatchReport, build_report


def risk_for_signal(signal: CitationSignal) -> int:
    if signal.cluster_size >= 7:
        return 3
    if signal.cluster_size >= 5:
        return 2
    if signal.near_paragraph_end and signal.cluster_size >= 3:
        return 2
    if signal.cluster_size >= 3:
        return 1
    return 0


def citation_rows(signals: list[CitationSignal]) -> list[str]:
    rows: list[str] = []
    for signal in signals:
        risk = risk_for_signal(signal)
        if risk == 0:
            continue
        location = f"{Path(signal.file).name}:{signal.line}"
        issue = "large citation cluster" if signal.cluster_size >= 5 else "citation placement review"
        basis = signal.risk_hint
        suggestion = "Check whether all sources support one narrow claim; split or group by source role if needed."
        rows.append(
            f"| {location} | {risk} | medium | {issue} | {basis} | {suggestion} |"
        )
    return rows


def consistency_rows(report: MatchReport) -> list[str]:
    rows: list[str] = []
    for key in report.missing_references:
        rows.append(
            f"| `{key}` | 3 | missing reference | cited in manuscript but absent from bibliography | Search Zotero or confirm removal. |"
        )
    for key in report.unused_references:
        rows.append(
            f"| `{key}` | 1 | unused reference | present in bibliography but not cited by key | Confirm whether it should be cited or removed. |"
        )
    return rows


def render_markdown(signals: list[CitationSignal], report: MatchReport | None) -> str:
    risky_rows = citation_rows(signals)
    missing_count = len(report.missing_references) if report else 0
    unused_count = len(report.unused_references) if report else 0
    risky_count = len(risky_rows)

    lines = [
        f"整体判断：检测到 {len(signals)} 个 citation signal；"
        f"{risky_count} 个需要人工复核的位置；"
        f"{missing_count} 个缺失参考文献；{unused_count} 个未引用参考文献。"
    ]

    lines.append("")
    lines.append("## In-text citation audit")
    if risky_rows:
        lines.append("| 位置 | 风险 | 置信度 | 问题 | 判断依据 | 建议 |")
        lines.append("|---|---:|---|---|---|---|")
        lines.extend(risky_rows)
    else:
        lines.append("未发现明显的大型 citation cluster。仍需结合 source content 判断引用是否真实支持 claim。")

    if report:
        lines.append("")
        lines.append("## Citation-reference consistency")
        rows = consistency_rows(report)
        if rows:
            lines.append("| 项目 | 风险 | 状态 | 说明 | 建议 |")
            lines.append("|---|---:|---|---|---|")
            lines.extend(rows)
        else:
            lines.append("按 cite key 检查，正文引用和 BibTeX 条目一致。")

        if report.unkeyed_citation_signals:
            lines.append("")
            lines.append("## Needs source check")
            lines.append("| 位置 | 引用 | 原因 | 需要材料 |")
            lines.append("|---|---|---|---|")
            for item in report.unkeyed_citation_signals:
                location = f"{Path(str(item['file'])).name}:{item['line']}"
                raw = str(item["raw"]).replace("|", "\\|")
                reason = str(item["risk_hint"]).replace("|", "\\|")
                lines.append(
                    f"| {location} | {raw} | {reason}; no cite key available for BibTeX matching | Zotero item or reference-list entry |"
                )

    lines.append("")
    lines.append("## Recommended next actions")
    lines.append("- Search Zotero first for missing or unkeyed references.")
    lines.append("- Verify source support only after abstracts, notes, PDFs, or indexed full text are available.")
    lines.append("- Import or modify Zotero records only after explicit confirmation.")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manuscripts", nargs="+", help="Manuscript files to inspect")
    parser.add_argument("--bib", action="append", help="Optional BibTeX/BibLaTeX file")
    args = parser.parse_args()

    manuscript_paths = [Path(path) for path in args.manuscripts]
    signals: list[CitationSignal] = []
    for path in manuscript_paths:
        signals.extend(extract_from_file(path))

    report = None
    if args.bib:
        report = build_report(manuscript_paths, [Path(path) for path in args.bib])

    print(render_markdown(signals, report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

