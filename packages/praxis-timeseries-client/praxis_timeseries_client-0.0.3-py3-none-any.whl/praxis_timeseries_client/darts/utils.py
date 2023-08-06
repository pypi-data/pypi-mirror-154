"""
Helper functions for Darts operations
"""
import pandas as pd
from darts import TimeSeries


def stack_timeseries(
    timeseries: list[TimeSeries], time_col: str = "date"
) -> TimeSeries:
    """Concatenates multiple timeseries on the range of the first in the list"""
    stacked = timeseries[0].pd_dataframe().reset_index()
    components = list(timeseries[0].components)
    for i in range(len(timeseries) - 1):
        stacked = pd.merge(
            stacked, timeseries[1 + i].pd_dataframe(), on=time_col, how="left"
        )
        components.extend(list(timeseries[1 + i].components))
    return TimeSeries.from_dataframe(
        stacked,
        time_col=time_col,
        value_cols=components,
        freq=timeseries[0].freq,
        fillna_value=0
    )
