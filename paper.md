---
title: "boltpy: A Python toolkit for multi-source literature dataset construction"
tags:
  - Python
  - literature review
  - systematic review
  - metadata harvesting
  - bibliographic APIs
  - deduplication
authors:
  - name: "Filippo Civilini"
    affiliation: 1
affiliations:
  - name: "University of Bologna"
    index: 1
date: 2026-02-04
bibliography: paper.bib
---

## Summary

Growth in scholarly publishing increases the manual effort required to assemble comprehensive literature datasets and raises the risk of missing relevant evidence when searches are fragmented across platforms [@europeancommission2024; @khabsa2014]. boltpy is an open-source Python toolkit that automates early-stage retrieval, metadata harmonization, and deduplication. It queries multiple sources, aggregates records into a unified schema, and removes duplicates via a multi-stage pipeline (DOI-based, exact normalized-title, fuzzy title matching). boltpy exports a full dataset and an ASReview LAB–aligned table with key screening fields (title, abstract, authors, year, DOI, URL), and reports PRISMA-style stage-wise record counts for documenting preprocessing decisions, crucial for modern reviews [@vandeschoot2021; @page2021].

## Statement of need

Systematic and narrative literature reviews are increasingly difficult by the growth in scientific output. Review teams often need to search multiple platforms, then manually harmonize metadata fields (e.g., title, abstract, year, DOI, URL) and remove duplicates before screening. Deduplication is non-trivial because the same record can appear with small metadata differences across sources (e.g., punctuation or encoding differences in titles, missing DOIs, or inconsistent author strings).

boltpy was developed to address this workflow bottleneck by providing an automated way to: (i) query multiple scholarly sources, (ii) aggregate results into a single normalized dataset with consistent fields, (iii) deduplicate records through a transparent multi-stage pipeline, and (iv) export datasets that can be directly used for screening and downstream analysis. From a practical workflow perspective, boltpy is intended to be used immediately after defining keywords and selecting which sources to query. Users define the list of keywords, select the APIs to be queried, set ceilings on the number of results collected per keyword for each source (with a configurable default), and provide API credentials where required. They can then run a single function to obtain a merged, deduplicated dataset and exported files.

## State of the field

Several existing libraries focus on retrieving metadata from a single scholarly API. For example, habanero is a Python client for the Crossref search API [@chamberlain2025], while PyAlex provides a lightweight Python interface to the OpenAlex API [@debruin2025]. In R, openalexR supports retrieval of bibliographic records from OpenAlex [@aria2024]. boltpy differs in that it is designed specifically for multi-source harvesting and preprocessing: it supports Crossref, Elsevier Scopus (API key required), PubMed, arXiv, OpenAlex, Europe PMC, and Zenodo, producing a single consolidated dataset before screening.

Related tools also target adjacent steps in literature workflows rather than multi-source metadata deduplication. For example, PyPaperRetriever focuses on finding and downloading lawfully available PDFs given identifiers such as DOI or PubMed IDs [@turner2025]. boltpy instead targets the earlier dataset construction stage: collecting and consolidating metadata across multiple sources and removing duplicates, so that screening can proceed on a clean record set, helping researchers to save a lot of time in gathering data.

## Software design

boltpy is organized into three components that mirror the user workflow: configuration and orchestration, source providers, and post-processing with export.

**Configuration and orchestration.**
Search parameters are captured in a single configuration object (`HarvestConfig`). This object specifies the keyword list, the set of APIs to query, optional API keys, per-source ceilings (with a configurable default), concurrency settings (`max_workers`), and export options (output directory, file naming prefix, and which exports to write). In addition, `HarvestConfig` supports an optional global publication-date window (`from_pub_date`, `until_pub_date`; ISO 8601 “YYYY-MM-DD”) that is applied consistently across all selected providers. The main entry point (`harvest`) iterates over keywords and dispatches API calls for the selected sources. For each keyword, calls are executed concurrently across sources using a thread pool.

**Provider layer.**
Each supported source is implemented as a provider function, and a provider registry maps API names (e.g., "crossref", "openalex") to these functions to enable uniform dispatch. Providers return lists of records that are mapped into a shared schema so results from different sources can be combined. Elsevier Scopus is handled as a special case: if no API key is provided via the configuration (or the `ELSEVIER_API_KEY` environment variable), the Scopus provider is skipped and returns no records for that source. When a publication-date window is provided, each provider applies the same bounds during retrieval where supported; in cases where provider interfaces primarily expose publication year in the returned metadata, filtering is applied at year resolution derived from the provided dates.

**Post-processing, deduplication, and export.**
After provider calls complete, records are loaded into a pandas `DataFrame` and coerced into an expected set of fields (with missing columns created as empty strings). The pipeline then applies staged filtering and deduplication. Records with both empty title and empty abstract are removed; DOIs are normalized; and duplicates are removed sequentially using (i) exact matching on normalized DOI when present, (ii) exact matching on a normalized title representation, and (iii) fuzzy title-based matching using a configurable similarity threshold. The function returns a `HarvestResult` containing (i) the full deduplicated `DataFrame`, (ii) an ASReview-oriented `DataFrame` restricted to {title, abstract, authors, year, doi, url}, (iii) a dictionary of stage-wise record counts and per-source counts, and (iv) optional output file paths when writing exports to disk.

## Research impact statement

boltpy is intended to improve the practical feasibility of comprehensive literature reviews by reducing the manual effort required to retrieve records from multiple sources, harmonize heterogeneous metadata, remove duplicates, and prepare a screening-ready dataset. By reducing time and manual effort for multi-source retrieval and preprocessing, boltpy can help researchers assemble a more comprehensive initial set of retrieved records, reducing the likelihood that relevant studies are missed due to reliance on a single index or due to friction in merging results across platforms. The extent of coverage still depends on the chosen sources, search strategy, and API limits, but boltpy aims to make a broad, multi-source identification step easier to execute and reproduce.

boltpy primarily impacts review workflows in three areas:
(1) Multi-source retrieval as a reproducible, scriptable step. Literature searches for evidence synthesis often require querying multiple platforms and consolidating results into a single dataset. boltpy supports multi-source harvesting in one run and encapsulates search settings (keywords, selected APIs, retrieval ceilings, and optional credentials) in a single configuration object. This design makes the identification and preprocessing stage easier to rerun and audit as part of a scripted workflow (e.g., within a version-controlled research repository), rather than relying on manual export/import steps across tools.
(2) Lower-friction integration with machine-learning–aided screening. ASReview provides an open-source active-learning approach to screening that aims to reduce manual reading while supporting transparent, reproducible workflows [@vandeschoot2021]. boltpy contributes at the interface between retrieval and screening by producing an ASReview-compatible dataset automatically (restricted to {title, abstract, authors, year, doi, url}) and by applying deduplication prior to export. This reduces common sources of friction at the start of screening, particularly format alignment and duplicate handling.
(3) Transparent preprocessing outputs for reporting. PRISMA 2020 emphasizes clear reporting of the flow of records from identification through screening and inclusion [@page2021]. boltpy outputs stage-wise record counts (e.g., total collected; remaining after DOI-based deduplication; remaining after exact title-based deduplication; remaining after fuzzy title-based deduplication), which can support documentation of preprocessing decisions. These counts are not a substitute for protocol-level reporting, but they provide structured intermediate information that can be incorporated into PRISMA flow reporting alongside the review’s inclusion/exclusion procedures.

Overall, boltpy’s impact is to make multi-source retrieval and preprocessing more reproducible and less labor-intensive, enabling researchers to start screening from a consolidated dataset that better reflects the breadth of the selected evidence sources.

## AI usage disclosure

The author used generative AI tools to assist with language editing and restructuring of the manuscript. All technical content and final wording were reviewed and validated by the author.

## Acknowledgements
### Funding
The study was realized thanks to the international research project “European youth in education and in transition to the labour market” (EDU-LAB, www.edu-lab-project.eu) funded by the European Commission under the Horizon Europe Programme (Grant Agreement # 101177428).

## References
