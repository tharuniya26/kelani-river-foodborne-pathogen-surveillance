"""Descriptive summaries; percentages denote detection, never bacterial load."""
from .data_processing import published_data


def ranked_sites(frame=None):
    data = published_data(frame)
    return data.sort_values(["pathogen", "detection_proportion", "anatomical_site"],
                            ascending=[True, False, True])


def percentage_point_range(frame=None):
    data = published_data(frame)
    return (data.groupby("pathogen").detection_percentage.max()
            - data.groupby("pathogen").detection_percentage.min()).rename("range_pp")


def site_totals(frame=None):
    """Sum of detection events across groups, not unique positive fish."""
    data = published_data(frame)
    return data.groupby("anatomical_site").positive_count.sum().rename("detection_events")
