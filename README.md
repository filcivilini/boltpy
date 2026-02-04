# boltpy (BOLT)

**BOLT** = **B**ibliographic **O**rchestration for **L**iterature **T**riage

`boltpy` is a Python toolkit to collect and triage literature results from multiple scholarly sources
(Crossref, OpenAlex, PubMed, arXiv, Europe PMC, Zenodo, and optionally Elsevier Scopus).

It is designed for literature reviews where you want to:
- choose a set of keywords,
- choose which APIs/sources to query,
- provide API keys when required,
- set a maximum number of results per source,
- receive a clean, deduplicated dataset (plus an ASReview-friendly export).

---

## Features

- Multi-source harvesting (select the APIs you want)
- Per-source ceilings (`ceilings={"crossref": 150, "openalex": 200, ...}`)
- Optional API key support # currently only Elsevier Scopus is supported
- Deduplication:
  - DOI-based
  - exact normalized title
  - fuzzy title matching
- Export:
  - full CSV (all fields)
  - ASReview CSV (title/abstract/authors/year/doi/url)
  - PRISMA-style counters (JSON)

---

## Install

pip install boltpy


## Example

from boltpy.core import HarvestConfig, harvest

cfg = HarvestConfig(
    keywords=["Key word 1", "Key word 2", "Key word X"],  #as many keywords as you like
    apis=["crossref", "openalex", "pubmed", "arxiv", "europe_pmc", "zenodo"],
    default_ceiling=100,
    output_dir="outputs",      
    export_prefix="boltpy_demo",

    from_pub_date="1997-01-01",
    until_pub_date="2026-12-31",
)

res = harvest(cfg)

print(res.full.head())
print(res.asreview.head())
print(res.prisma)
print(res.output_paths)

## Community guidelines

- **Contributing:** see [CONTRIBUTING.md](CONTRIBUTING.md)
- **Bug reports & feature requests:** please open a GitHub Issue (include steps to reproduce, expected vs actual behavior, and your environment).
- **Support / questions:** open a GitHub Issue and label it as a question.


