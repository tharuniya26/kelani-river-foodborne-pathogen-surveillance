"""Marginal Wilson intervals; paired comparisons need linked specimen data."""
from math import sqrt
from scipy.stats import norm
from .data_processing import published_data


def wilson_interval(positive, total, confidence=0.95):
    if not isinstance(positive, int) or not isinstance(total, int) or total <= 0 or not 0 <= positive <= total:
        raise ValueError("Counts must be valid integers")
    if not 0 < confidence < 1:
        raise ValueError("Confidence must be between zero and one")
    z = norm.ppf((1 + confidence) / 2)
    p = positive / total
    denominator = 1 + z*z/total
    center = (p + z*z/(2*total)) / denominator
    radius = z * sqrt(p*(1-p)/total + z*z/(4*total*total)) / denominator
    if positive == 0:
        return 0.0, float(min(1, center+radius))
    if positive == total:
        return float(max(0, center-radius)), 1.0
    return float(max(0, center-radius)), float(min(1, center+radius))


def interval_table(frame=None):
    data = published_data(frame)
    bounds = [wilson_interval(int(row.positive_count), int(row.total_count))
              for row in data.itertuples()]
    data["wilson_low"] = [x[0] for x in bounds]
    data["wilson_high"] = [x[1] for x in bounds]
    return data


def gut_denominator_sensitivity():
    """Two literal source readings; 22/25 conflicts with its printed 81.48%."""
    return {27: 22/27, 25: 22/25}
