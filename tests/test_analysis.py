from math import isclose
import pytest
from src.data_processing import load_data, published_data, validate_data
from src.statistical_analysis import wilson_interval, gut_denominator_sensitivity

EXPECTED = {
    "Staphylococcus spp.": (27, 27, 15, 22),
    "Salmonella spp.": (11, 9, 10, 4),
    "Shigella spp.": (9, 15, 11, 5),
}
SITES = ("Skin", "Mouth", "Gills", "Gut")


def test_source_counts_and_arithmetic():
    rows = published_data()
    for group, counts in EXPECTED.items():
        for site, count in zip(SITES, counts):
            row = rows.loc[(rows.pathogen == group) & (rows.anatomical_site == site)].iloc[0]
            assert row.positive_count == count and row.total_count == 27
            assert isclose(row.detection_percentage, 100*count/27)
    assert len(load_data()) == 25


def test_invalid_counts():
    rows = published_data()
    rows.loc[rows.index[0], "positive_count"] = 28
    with pytest.raises(ValueError): validate_data(rows)


def test_wilson_boundaries():
    assert wilson_interval(0, 27)[0] == 0
    assert wilson_interval(27, 27)[1] == 1
    assert 0 < wilson_interval(27, 27)[0] < 1
    assert isclose(gut_denominator_sensitivity()[25], .88)
