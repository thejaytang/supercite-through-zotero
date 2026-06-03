---
name: supercite-through-zotero
description: Zotero-first audit workflow for academic in-text citations, reference lists, citation dumping, source-reference consistency, and reference authenticity. Use when the user asks to check manuscript citations, verify references, avoid AI-like citation piles, reconcile citations with a bibliography, or route citation insertion and metadata correction through Zotero.
---

# supercite through zotero

Use this skill to audit academic citations and reference lists with Zotero as the primary fact layer. The agent may inspect, match, and recommend, but it must not fabricate references or silently write records into Zotero.

## Core Position

Zotero library records are the preferred source of truth for inserted citations and final bibliography generation. Internet search results, LLM memory, and loose reference strings are candidates only. They must be verified before being treated as manuscript references.

## Non-Negotiable Rules

- Do not invent references, DOI values, authors, years, page ranges, findings, or source support.
- Do not claim a reference supports a manuscript claim unless source content, an abstract, notes, or indexed full text is available.
- Do not treat every multi-reference cluster as a problem. Several sources may legitimately support the same narrow claim.
- Do not write to Zotero, import records, modify Zotero metadata, or attach files unless the user explicitly asks for that write action or confirms the exact records.
- Prefer Zotero insertion/export for final citations. Do not hand-build a final Word bibliography when Zotero fields are expected.
- Preserve the user's citation style unless the user asks to convert it.

## Workflow

1. Identify the manuscript format, citation style, and requested strictness.
   - For `.tex`, `.md`, `.txt`, and `.bib`, use the bundled scripts when useful.
   - For `.docx`, use a document workflow for text extraction and visual review, but do not fake Zotero field citations.
2. Run a citation signal pass.
   - Use `scripts/extract_citation_signals.py` to find TeX cite commands, Pandoc cite keys, author-year clusters, and numeric clusters.
   - Use `scripts/match_citations_references.py` when a `.bib` file is available.
   - Use `scripts/summarize_reference_audit.py` for a first-pass Markdown report.
3. Audit in-text citation placement.
   - Read `references/citation-placement-rubric.md` for citation dumping and multi-source synthesis rules.
   - Split claims before moving citations. Keep legitimate source clusters when they support one precise claim.
4. Check citation-reference consistency.
   - Confirm every cited key or visible citation has a matching reference-list entry.
   - Flag uncited bibliography entries, duplicate records, mismatched author/year values, and malformed entries.
5. Route verification through Zotero.
   - If a Zotero plugin/skill/tool is available, search the local Zotero library before external lookup.
   - If an item is present in Zotero, use its item key, cite key, DOI, title, creators, and year as the manuscript candidate.
   - If an item is missing, prepare candidate metadata for user confirmation before importing.
   - Read `references/zotero-first-workflow.md` before any Zotero import or citation insertion plan.
6. Audit reference authenticity and metadata.
   - Read `references/reference-integrity-rubric.md` for status labels and field checks.
   - Use external databases only as verification sources, not as automatic replacements.
7. Report results in layers.
   - Use `references/output-format.md` for compact tables and status labels.
   - Separate placement issues, consistency issues, Zotero routing actions, and authenticity issues.

## Script Quick Start

```bash
python3 supercite-through-zotero/scripts/extract_citation_signals.py paper.tex --json
python3 supercite-through-zotero/scripts/match_citations_references.py paper.tex --bib references.bib
python3 supercite-through-zotero/scripts/summarize_reference_audit.py paper.tex --bib references.bib
```

## Zotero Integration Guidance

When a Zotero integration is available, use it for library search, BibTeX export, cite key insertion, and confirmed imports. Keep the distinction clear:

- Zotero item keys identify records inside Zotero.
- BibTeX keys or citation keys identify entries in `.bib`, LaTeX, Markdown, or Pandoc drafts.

For Word and Google Docs, give the user a Zotero insertion plan with record titles and locations. The final field insertion should normally be done through Zotero's official word processor integration.

## Output Standard

Start with a short overall judgment. Then provide only the relevant sections:

- `In-text citation audit`
- `Citation-reference consistency`
- `Zotero routing`
- `Reference authenticity`
- `Needs source check`
- `Recommended next actions`

Use risk levels:

- `0`: no issue or acceptable practice
- `1`: minor style or clarity issue
- `2`: likely citation integrity issue
- `3`: high-risk mismatch, missing reference, or possible fabricated source

Use confidence labels: `low`, `medium`, `high`.
