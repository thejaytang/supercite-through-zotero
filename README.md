# supercite through zotero

**supercite through zotero** is a Zotero-first skill for auditing academic citations and reference lists. It helps AI assistants review citation placement, catch suspicious reference problems, and route final citation work through Zotero instead of letting an LLM invent bibliography entries.

The core idea is simple: use AI for audit and reasoning, use Zotero as the citation fact layer.

## Why this exists

AI tools can help with academic writing, but citation work is fragile. Common failure modes include:

- hallucinated references;
- DOI or metadata mismatches;
- citations that do not support the claim they are attached to;
- large end-of-sentence or end-of-paragraph citation piles;
- missing bibliography entries;
- unused references;
- manual bibliographies that drift away from Zotero.

This skill is designed for researchers, students, editors, and reviewers who want AI help without giving up citation control.

## What it checks

- **In-text citation placement**: finds possible citation dumping, oversized citation clusters, and claim-source alignment issues.
- **Legitimate multi-source synthesis**: does not blindly reject multiple citations when several papers support the same narrow claim.
- **Citation-reference consistency**: compares manuscript cite keys against BibTeX/BibLaTeX entries.
- **Reference authenticity workflow**: separates verified records, metadata mismatches, unresolved entries, and possible fabricated references.
- **Zotero-first routing**: asks the assistant to search or import through Zotero before inserting final references.

## Repository layout

```text
skills/supercite-through-zotero/
|-- SKILL.md
|-- agents/openai.yaml
|-- references/
|   |-- citation-placement-rubric.md
|   |-- reference-integrity-rubric.md
|   |-- zotero-first-workflow.md
|   `-- output-format.md
`-- scripts/
    |-- extract_citation_signals.py
    |-- match_citations_references.py
    `-- summarize_reference_audit.py
```

## Install in Codex

From Codex, ask:

```text
Install the skill from https://github.com/thejaytang/supercite-through-zotero/tree/main/skills/supercite-through-zotero
```

Or install with the Codex skill installer helper:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo thejaytang/supercite-through-zotero \
  --path skills/supercite-through-zotero
```

Restart Codex after installation so the new skill is loaded.

## Use it

Invoke the skill explicitly:

```text
Use $supercite-through-zotero to audit my manuscript citations through Zotero.
```

Typical requests:

```text
Use $supercite-through-zotero to check whether my LaTeX citations match references.bib.
```

```text
Use $supercite-through-zotero to find possible citation dumping in this literature review.
```

```text
Use $supercite-through-zotero to prepare a Zotero-first plan for fixing missing references.
```

## Local script examples

Extract citation signals:

```bash
python3 skills/supercite-through-zotero/scripts/extract_citation_signals.py paper.tex
```

Compare cite keys with a bibliography:

```bash
python3 skills/supercite-through-zotero/scripts/match_citations_references.py paper.tex --bib references.bib
```

Generate a first-pass Markdown audit:

```bash
python3 skills/supercite-through-zotero/scripts/summarize_reference_audit.py paper.tex --bib references.bib
```

## Zotero-first policy

The skill is intentionally strict about final references:

- AI should not invent references.
- AI should not silently import or modify Zotero records.
- New records should be confirmed before import.
- Final manuscript citations should come from Zotero, Better BibTeX, or the user's verified reference library.
- Word and Google Docs citations should normally be inserted through the official Zotero plugin, not recreated as plain text by AI.

## Good fit

This skill is useful for:

- literature reviews;
- journal articles;
- theses and dissertations;
- grant drafts;
- LaTeX or Markdown manuscripts with BibTeX/BibLaTeX;
- Zotero-based writing workflows;
- checking AI-assisted drafts for citation problems.

## Limits

The bundled scripts are offline structural checks. They do not prove that a source supports a claim. Source-support verification needs abstracts, notes, indexed full text, PDFs, or trusted external metadata sources.

The skill is designed to make uncertainty visible instead of hiding it.

## License

MIT
