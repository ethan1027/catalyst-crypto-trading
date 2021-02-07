import backtrader as bt
from backtrader.indicators.macd import MACD
from backtrader.indicators.stochastic import Stochastic
from backtrader.strategy import Strategy

class GenesisStrat(Strategy):
  def __init__(self):
    self.stoch = Stochastic()
    self.macd = MACD()

  def next(self):