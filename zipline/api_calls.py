import alpaca_trade_api as tradeapi
import pandas as pd
end = pd.Timestamp('2020-09-10', tz='America/New_York').isoformat()
api = tradeapi.REST('PKFHFHI79KOB5UHTRE99', 'ugY9FA1XCmTfkuT4hUJK55pPeUEbc0znhvxFJSeH', base_url='https://paper-api.alpaca.markets') # or use ENV Vars shown below
b = api.get_barset('BAC', 'minute', 30, end=end)
print(b.df)