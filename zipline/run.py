import argparse
import pytz
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import pandas_datareader.data as yahoo_reader

from zipline import run_algorithm
from zipline.data import bundles
import zipline.protocol
from zipline.api import order_target_percent, symbol
from zipline.utils.calendars import get_calendar

from talib import STOCH, MA_Type

def get_benchmark(symbol=None, start=None, end=None):
  bm = yahoo_reader.DataReader(symbol,
              'yahoo',
              pd.Timestamp(start),
              pd.Timestamp(end))['Close']
  bm.index = bm.index.tz_localize('UTC')
  return bm.pct_change(periods=1).fillna(0)


def initialize(context):
  equities = ["TSLA", "BAC"]
  context.equities = [symbol(equity) for equity in equities]
  context.count = 0


def handle_data(context, data):
  context.count += 1
  if context.count < 60:
    return
  context.count = 0
  for equity in context.equities:
    trailing_window: pd.DataFrame = data.history(equity, ['high', 'low', 'close'], 60 * 30, '1m')
    if trailing_window.isnull().values.any():
      return
    hour_trailing_window = trailing_window.resample('60T').last()
    # print(hour_trailing_window)
    slowk, slowd = STOCH(hour_trailing_window['high'], hour_trailing_window['low'], hour_trailing_window['close'], 14, 3, 0, 14, 0)
    if slowk.values[-1] > slowd.values[-1]:
      allocation = round(1 / (len(context.portfolio.positions) + 1), 2)
      order_target_percent(equity, allocation)
    else:
      order_target_percent(equity, 0)



def before_trading_start(context, data):
  pass


def analyze(context, perf: pd.DataFrame):
  fig, axes = plt.subplots(1, 1, figsize=(16, 7), sharex=True)
  perf['algorithm_period_return'].plot(color='blue')
  perf['benchmark_period_return'].plot(color='red')
  plt.legend(['Algo', 'Benchmark'])
  plt.ylabel("Returns", color='black', size=20)
  plt.show()


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='run zipline backtest')
  parser.add_argument('-b', '--bundle', default='alpaca_api', dest='bundle')
  args = parser.parse_args()

  bundle_name = args.bundle
  bundle_data = bundles.load(bundle_name)

  # Set the trading calendar
  trading_calendar = get_calendar('NYSE')

  start = pd.Timestamp(datetime(2020, 11, 30, tzinfo=pytz.UTC))
  end = pd.Timestamp(datetime(2021, 2, 8, tzinfo=pytz.UTC))

  r = run_algorithm(
    start=start,
    end=end,
    initialize=initialize,
    capital_base=100000,
    handle_data=handle_data,
    benchmark_returns=get_benchmark(symbol="SPY",
                                    start=start.date().isoformat(),
                                    end=end.date().isoformat()),
    bundle=bundle_name,
    broker=None,
    state_filename="./demo.state",
    trading_calendar=trading_calendar,
    before_trading_start=before_trading_start,
    analyze=analyze,
    data_frequency='minute'
  )