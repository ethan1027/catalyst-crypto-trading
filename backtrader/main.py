from configparser import ConfigParser
from datetime import datetime
from alpaca_backtrader_api import AlpacaStore, AlpacaData, AlpacaBroker
import backtrader as bt
from backtrader.cerebro import Cerebro
from backtrader.indicator import Indicator
from backtrader.indicators.stochastic import Stochastic
from backtrader.sizers.percents_sizer import AllInSizerInt

config = ConfigParser()
config.read('alpaca-creds.ini')
paper_creds = config['PAPER']
key_id = paper_creds['API_KEY']
secret_key=paper_creds['SECRET_KEY']
paper = paper_creds.getboolean('PAPER')

stocks = ['TSLA', 'MSTR', 'MSFT', 'AAPL', 'GME', 'AMD', 'AAL']
cerebro = Cerebro()

store = AlpacaStore(
  key_id=key_id,
  secret_key=secret_key,
  paper=paper
)

if not paper:
  broker = AlpacaBroker()
  broker.set_cash(5000)
  cerebro.setbroker(broker)

fromdate = datetime(2020, 10, 1)
todate = datetime(2021, 1, 20)

for stock in stocks:
  data = AlpacaData(dataname=stock, historical=True, fromdate=fromdate, todate=todate, timeframe=bt.TimeFrame.Days)
  cerebro.adddata(data)

cerebro.addobserver(bt.observers.Broker)
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot()