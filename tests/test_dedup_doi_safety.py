
import pandas as pd
import pytest

from boltpy.core import (
    deduplicate_doi,
    deduplicate_exact_title,
    deduplicate_fuzzy,
)


def run_pipeline(
    dataframe,
    allow_missing_doi=False,
    threshold=95,
):
    result = deduplicate_doi(dataframe)

    result = deduplicate_exact_title(
        result,
        allow_missing_doi=allow_missing_doi,
    )

    result = deduplicate_fuzzy(
        result,
        threshold=threshold,
        allow_missing_doi=allow_missing_doi,
    )

    return result


def test_same_doi_is_deduplicated():

    df = pd.DataFrame({
        "title": ["Article A", "Article A"],
        "doi": [
            "https://doi.org/10.1234/ABC",
            "10.1234/abc",
        ],
    })

    assert len(run_pipeline(df)) == 1


def test_different_dois_same_title_preserved():

    df = pd.DataFrame({
        "title": ["Mobile Money", "Mobile Money"],
        "doi": ["10.1234/a", "10.1234/b"],
    })

    assert len(run_pipeline(df)) == 2


def test_different_dois_fuzzy_titles_preserved():

    df = pd.DataFrame({
        "title": [
            "Anti-Money Laundering Regulations Part 1",
            "Anti-Money Laundering Regulations Part 2",
        ],
        "doi": ["10.1234/a", "10.1234/b"],
    })

    result = run_pipeline(
        df,
        allow_missing_doi=True,
    )

    assert len(result) == 2


def test_missing_dois_preserved_by_default():

    df = pd.DataFrame({
        "title": ["Mobile Money", "Mobile Money"],
        "doi": ["", ""],
    })

    assert len(run_pipeline(df)) == 2


def test_missing_and_valid_doi_preserved():

    df = pd.DataFrame({
        "title": ["Mobile Money", "Mobile Money"],
        "doi": ["10.1234/a", ""],
    })

    assert len(run_pipeline(df)) == 2

    # Also protected in optional mode.
    assert len(
        run_pipeline(df, allow_missing_doi=True)
    ) == 2


def test_missing_dois_optional_exact_matching():

    df = pd.DataFrame({
        "title": ["Mobile money!", "mobile money"],
        "doi": ["", ""],
    })

    result = run_pipeline(
        df,
        allow_missing_doi=True,
    )

    assert len(result) == 1


def test_missing_dois_optional_fuzzy_matching():

    df = pd.DataFrame({
        "title": [
            "The impact of mobile money in Kenya",
            "The impact of mobile money in KenyA!",
        ],
        "doi": ["", ""],
    })

    result = run_pipeline(
        df,
        allow_missing_doi=True,
        threshold=95,
    )

    assert len(result) == 1


def test_empty_titles_not_merged():

    df = pd.DataFrame({
        "title": ["", ""],
        "doi": ["", ""],
    })

    result = run_pipeline(
        df,
        allow_missing_doi=True,
    )

    assert len(result) == 2


def test_invalid_doi_not_treated_as_identifier():

    df = pd.DataFrame({
        "title": ["Article A", "Article A"],
        "doi": ["nan", "nan"],
    })

    assert len(run_pipeline(df)) == 2


def test_missing_values_none_nan_pdna():

    df = pd.DataFrame({
        "title": ["Article A"] * 3,
        "doi": [None, float("nan"), pd.NA],
    })

    assert len(run_pipeline(df)) == 3


def test_no_transitive_merging():

    df = pd.DataFrame({
        "title": ["Mobile Money"] * 3,
        "doi": [
            "10.1234/a",
            "",
            "10.1234/b",
        ],
    })

    result = run_pipeline(
        df,
        allow_missing_doi=True,
    )

    assert len(result) == 3


def test_doi_versions_are_distinct():

    df = pd.DataFrame({
        "title": ["Article A", "Article A"],
        "doi": [
            "10.5072/article.v1",
            "10.5072/article.v2",
        ],
    })

    result = run_pipeline(
        df,
        allow_missing_doi=True,
    )

    assert len(result) == 2


def test_invalid_threshold_raises():

    df = pd.DataFrame({
        "title": ["Article A"],
        "doi": [""],
    })

    with pytest.raises(ValueError):
        deduplicate_fuzzy(
            df,
            threshold=101,
        )


def test_order_is_preserved():

    df = pd.DataFrame({
        "title": ["A", "B", "C", "D"],
        "doi": [
            "10.1234/a",
            "",
            "10.1234/a",
            "10.1234/d",
        ],
    })

    result = run_pipeline(df)

    assert result["title"].tolist() == [
        "A", "B", "D"
    ]
