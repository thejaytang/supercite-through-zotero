# Reference Integrity Rubric

Use this rubric for reference-list authenticity and metadata checks.

## Status Labels

- `verified`: The record matches a trusted source on title, creators, year, venue, and identifier.
- `metadata mismatch`: The record exists, but one or more important fields differ.
- `partial match`: Some fields match, but the match is not strong enough for verification.
- `unresolved`: No reliable match was found.
- `possible fabricated reference`: The entry combines plausible fields that do not correspond to one real source, or no trace exists in expected databases.
- `needs manual confirmation`: The source type or field requires human review, such as archives, law, translated books, historical editions, or local-language materials.

## Field Priority

Check fields in this order:

1. Stable identifiers: DOI, PMID, PMCID, ISBN, ISSN, arXiv ID, DBLP key.
2. Title.
3. Creators and author order.
4. Publication year.
5. Venue, publisher, proceedings, or journal.
6. Volume, issue, pages, article number.
7. URL and access date for web sources.

## High-Risk Patterns

- DOI resolves to a different title.
- Title and authors appear in separate real papers.
- Year differs from the authoritative record and affects the claim.
- A preprint is cited where a final version exists, without a reason.
- Conference and journal versions are mixed as one entry.
- The bibliography entry has no stable identifier and no reliable database trace.

## Trusted Source Preference

Use discipline-appropriate sources:

- Biomedical and health: PubMed, Crossref, publisher pages, clinical trial registries when relevant.
- Computer science: DBLP, arXiv, ACL Anthology, IEEE/ACM pages, Crossref.
- Social sciences and humanities: Crossref, OpenAlex, library catalogs, publisher pages, ISBN sources, JSTOR or Project MUSE when available.
- Law: official legal databases or jurisdiction-specific citation sources.

External search results are evidence, not automatic truth. Prefer structured identifiers and authoritative records.

