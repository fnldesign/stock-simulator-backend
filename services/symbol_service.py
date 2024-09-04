# services/symbol_service.py

import yfinance as yf

class SymbolService:
    def __init__(self):
        pass

    def get_symbols_for_exchange(self, exchange):
        """
        Fetches a list of symbols for a specific exchange using yfinance.

        :param exchange: The exchange for which to fetch symbols.
        :return: A list of symbols for the given exchange.
        """
        try:
            # Fetch all symbols for the given exchange using yfinance
            tickers = yf.Tickers(f"{exchange}.*")
            symbols = [ticker.ticker for ticker in tickers.tickers.values()]
            return symbols
        except Exception as e:
            raise ValueError(f"Failed to fetch symbols for exchange {exchange}: {str(e)}")
