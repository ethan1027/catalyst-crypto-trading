import argparse
import pytz
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import pandas_datareader.data as yahoo_reader

from zipline.utils.calendars import get_calendar
from zipline.api import order_target, order_target_percent, symbol
from zipline.data import bundles
from zipline import run_algorithm

from talib import STOCH, MA_Type

def get_benchmark(symbol=None, start=None, end=None):
  bm = yahoo_reader.DataReader(symbol,
              'yahoo',
              pd.Timestamp(start),
              pd.Timestamp(end))['Close']
  bm.index = bm.index.tz_localize('UTC')
  return bm.pct_change(periods=1).fillna(0)


def initialize(context):
  context.equity = symbol("TSLA")


def handle_data(context, data):
  trailing_window = data.history(context.equity, ['high', 'low', 'close'], 30, '1d')
  if trailing_window.isnull().values.any():
    return
  slowk, slowd = STOCH(trailing_window['high'], trailing_window['low'], trailing_window['close'], 14, 3, 0, 14, 0)
  if slowk.values[-1] > slowd.values[-1]:
    order_target_percent(context.equity, 1)
  else:
    order_target_percent(context.equity, 0)



def before_trading_start(context, data):
  pass


def analyze(context, perf):
  fig, axes = plt.subplots(1, 1, figsize=(16, 7), sharex=True)
  perf.algorithm_period_return.plot(color='blue')
  perf.benchmark_period_return.plot(color='red')

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
    bundle='alpaca_api',
    broker=None,
    state_filename="./demo.state",
    trading_calendar=trading_calendar,
    before_trading_start=before_trading_start,
    analyze=analyze,
    data_frequency='daily'
  )