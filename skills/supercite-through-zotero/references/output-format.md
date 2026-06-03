# Output Format

Keep reports compact and layered. Do not mix structural citation issues with reference authenticity issues.

## Overall Judgment

Use one paragraph:

```markdown
整体判断：...
```

## In-Text Citation Audit

```markdown
| 位置 | 风险 | 置信度 | 问题 | 判断依据 | 建议 |
|---|---:|---|---|---|---|
| P2 S3 | 2 | medium | citation dumping | 一个句子包含多个 claim，但所有引用集中在句末。 | 拆句并把引用移到对应 claim 后。 |
```

## Citation-Reference Consistency

```markdown
| 项目 | 风险 | 状态 | 说明 | 建议 |
|---|---:|---|---|---|
| smith2020 | 3 | missing reference | 正文引用存在，但 .bib 中无条目。 | 从 Zotero 查找或确认是否删除该引用。 |
```

## Zotero Routing

```markdown
| 条目 | Zotero 状态 | 动作 | 需要确认 |
|---|---|---|---|
| Attention Is All You Need | found | use Zotero/Better BibTeX cite key | no |
| Unknown reference string | not found | prepare candidate import | yes |
```

## Reference Authenticity

```markdown
| 条目 | 状态 | 证据源 | 字段差异 | 建议 |
|---|---|---|---|---|
| ... | metadata mismatch | Crossref | year differs | Check edition/version before final bibliography. |
```

## Needs Source Check

Use when source content is required:

```markdown
| 位置 | 引用 | 原因 | 需要材料 |
|---|---|---|---|
| P4 S2 | Lee 2021 | 需要确认文献是否支持具体机制性 claim。 | abstract or full text |
```

