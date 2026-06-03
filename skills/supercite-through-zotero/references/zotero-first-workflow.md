# Zotero-First Workflow

Use this reference before planning Zotero writes or citation insertion.

## Principle

All final manuscript citations should point to records that the user can inspect in Zotero. AI-generated reference strings are not final references.

## Read-Only Steps

1. Search the local Zotero library by title, author, DOI, PMID, arXiv ID, or cite key.
2. Compare the manuscript citation with Zotero metadata.
3. Export or inspect BibTeX only when needed for LaTeX, Markdown, Pandoc, or CI checks.
4. Use Zotero full text or attachments only when the user asks for source-content verification or support checking.

## Confirmed Write Steps

Ask for confirmation before:

- importing BibTeX or RIS records into Zotero;
- changing existing Zotero metadata;
- adding tags, notes, collections, or attachments;
- inserting cite keys into drafts when the edit is not already explicitly requested.

The confirmation should identify the exact title, identifier, destination collection when known, and reason for import.

## Missing Item Handling

When a manuscript cites an item that is not in Zotero:

1. Mark it as `not in Zotero`.
2. Search trusted external metadata sources if the user permits or if network lookup is part of the task.
3. Prepare a candidate record with title, creators, year, venue, DOI or other identifier, and source URL.
4. Ask before importing.
5. After import, use Zotero or Better BibTeX to generate the final cite key.

## Word and Google Docs

Do not manually recreate Zotero field citations. Provide an insertion plan:

- paragraph or sentence location;
- Zotero title or item key;
- citation role;
- exact claim supported;
- whether source content was checked.

The user should insert the final citation through Zotero's official word processor integration unless an available tool can safely create real Zotero fields.

