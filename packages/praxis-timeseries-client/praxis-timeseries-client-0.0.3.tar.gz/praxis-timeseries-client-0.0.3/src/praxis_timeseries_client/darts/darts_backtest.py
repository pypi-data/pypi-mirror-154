"""Darts backtest class, representing a historical forecast.

Is initialized with a date, a forecast horizon, a stride, and various other
settings, and saves the eventual forecast so it can be replotted 
"""
from shutil import ExecError
from darts import TimeSeries
from darts.models.forecasting.forecasting_model import ForecastingModel
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from darts.metrics import mape


class DartsBacktest:
    """The Darts backtest class, representing a historical forecast.

    An instance of a Darts backtest is produced from the Darts interface, which
    manages all the data used by backtests and forecasts. Initialize a backtest
    with reference to a model, and the model is deployed on the interface's
    data. See kwargs for values you can pass into the backtest.
    """

    model: ForecastingModel
    forecast: TimeSeries
    mape: float
    kwargs: dict[str, any] = {
        "num_samples": 1,
        "train_length": None,
        "start": 0.5,
        "forecast_horizon": 1,
        "stride": 1,
        "retrain": False,
        "overlap_end": False,
        "last_points_only": True,
        "verbose": False,
    }

    def __init__(self, source, model: ForecastingModel, **kwargs):
        """Initialize a Darts backtest given a model and specifications.

        Once a backtest is run, its forecast is saved and it may be replotted
        or re-run at any point. This also allows you to change the covariates
        used in your interface and have them reflected in the backtest for the
        kwargs set in this backtest.

        Args:
            source (DartsInterface): The interface from which to draw data.
            model (ForecastingModel): A Darts model to use for predictions
            num_samples (int) = 1: __description__
            train_length (int) = None: If retraining the model, how many datapoints to use
            start (float or pd.Timestamp) = 0.5: When to begin the backtest
            forecast_horizon (int) = 1: How many time stamps to forecast at each stride
            stride (int) = 1: The stride of the backtest
            retrain (boolean) = False: Whether or not to retrain the model at each step
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
        self.forecast = self.model.historical_forecasts(
            self.source.target_ts,
            **_kwargs,
            **(self.kwargs)
        )
        self.mape = mape(self.forecast, self.source.target_ts)
        print("MAPE = {:.2f}%".format(self.mape))
        return self.mape
    
    # ---------------------------------------------------------------------------- #
    #                                 VISUALIZATION                                #
    # ---------------------------------------------------------------------------- #

    # plotting the backtest shows actual vs. prediction
    def plot(self, components=None, future_opacity: float = 0.5):
        # if the backtest hasn't been run, return an error
        if not self.forecast:
            raise ExecError("Please run the backtest before plotting it!")
        # get the source fig
        title = "Backtest: {} - MAPE = {:.2f}%".format(self.kwargs["start"], self.mape)
        fig = self.source.plot(
            components,
            future_begins_at=self.kwargs["start"],
            future_opacity=future_opacity,
            title=title,
        )
        # add prediction trace
        for _, c in enumerate(self.forecast._xa.component[:10]):
            comp_name = c.values
            comp_name = "PRED: {}".format(
                self.source.target_ts._xa.component[int(comp_name)].values
            )
            comp = self.forecast._xa.sel(component=c)
            fig.append_trace(
                go.Scatter(
                    x=self.forecast.time_index,
                    y=comp.values[:, 0],
                    mode="lines",
                    name=comp_name,
                    line=dict(
                        color=px.colors.qualitative.Plotly[6],
                    ),
                ),
                row=1,
                col=1,
            )

        # show the display
        return fig
