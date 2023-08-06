"""Darts forecast class, representing a future forecast.

Is initialized with a number of time steps to forecast from the end of the
interface's target series.
"""
from shutil import ExecError
from darts import TimeSeries
from darts.models.forecasting.forecasting_model import ForecastingModel
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from darts.metrics import mape


class DartsForecast:
    """The Darts forecast class, representing a future forecast.

    An instance of a Darts forecast is produced from the Darts interface, which
    manages all the data used by backtests and forecasts. Initialize a forecast
    with reference to a model, and the model is deployed on the interface's
    data. See kwargs for values you can pass into the forecast.
    """

    model: ForecastingModel
    forecast: TimeSeries
    kwargs: dict[str, any] = {
        "n": 10,
        "num_samples": 1,
    }

    def __init__(self, source, model: ForecastingModel, **kwargs):
        """Initialize a Darts forecast given a model and specifications.

        Once a forecast is run, its forecast is saved and it may be replotted
        or re-run at any point. This also allows you to change the covariates
        used in your interface and have them reflected in the forecast for the
        kwargs set in this forecast.

        Args:
            source (DartsInterface): The interface from which to draw data.
            model (ForecastingModel): A Darts model to use for predictions
            n (int) = 1: How many time steps to forecast
            num_samples (int) = 1: __description__
            ...
        """
        self.source = source
        self.model = model
        self.kwargs = self.kwargs | kwargs
        self.forecast = None

    # runs the backtest using darts, and prints the MAPE
    def run(self, **kwargs):
        _kwargs = dict(
            past_covariates=self.source.past_covariates,
            future_covariates=self.source.future_covariates
        ) | kwargs
        self.forecast = self.model.predict(
            series=self.source.target_ts,
            **_kwargs,
            **self.kwargs
        )

    # ---------------------------------------------------------------------------- #
    #                                 VISUALIZATION                                #
    # ---------------------------------------------------------------------------- #

    # plotting the backtest shows actual vs. prediction
    def plot(self, components=None, actual_ts=None, future_opacity: float = 0.1):
        # get the source fig
        title = "Forecast: {} with kwargs={}".format(
            self.source.target_ts.time_index[-1], self.kwargs
        )
        fig = self.source.plot(
            components,
            future_begins_at=self.source.target_ts.time_index[-1],
            future_opacity=future_opacity,
            title=title,
        )
        # add actual trace, if it exists
        if actual_ts:
            for _, c in enumerate(actual_ts._xa.component[:10]):
                comp_name = c.values
                comp_name = "ACTUAL: {}".format(str(c.values))
                comp = actual_ts._xa.sel(component=c)
                fig.append_trace(
                    go.Scatter(
                        x=actual_ts.time_index,
                        y=comp.values[:, 0],
                        mode="lines",
                        line=dict(color=px.colors.qualitative.Plotly[0]),
                        showlegend=False,
                        name=comp_name,
                    ),
                    row=1,
                    col=1,
                )

        # add prediction trace
        for _, c in enumerate(self.forecast._xa.component[:10]):
            comp_name = c.values
            comp_name = "PRED: {}".format(str(c.values))
            comp = self.forecast._xa.sel(component=c)
            fig.append_trace(
                go.Scatter(
                    x=self.forecast.time_index,
                    y=comp.values[:, 0],
                    mode="lines",
                    name=comp_name,
                    line=dict(
                        color=px.colors.qualitative.Plotly[8],
                    ),
                ),
                row=1,
                col=1,
            )

        # show the display
        return fig
