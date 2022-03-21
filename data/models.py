from dataclasses import dataclass, asdict, is_dataclass
import json


class DataJSONEncoder(json.JSONEncoder):
    """Enable json.dumps() with nested data classes."""
    def default(self, o):
        if is_dataclass(o):
            return asdict(o)
        return super().default(o)


@dataclass
class CancerStats:
    """Observed vs expected cancer incidents, with
    standardized incidence ratio, confidence intervals,
    and significance."""
    observed: float
    expected: float
    sir: float  # standardized_incidence_ratio
    ci_low: float  # confidence_intervals
    ci_high: float
    significant: bool # if there are confidence intervals


@dataclass
class CancerData:
    """Cancer Statistics divided by sex."""
    male: CancerStats
    female: CancerStats
    combined: CancerStats
