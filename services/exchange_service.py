# services/exchange_service.py

class ExchangeService:
    def __init__(self):
        # Define the valid exchanges
        self.valid_exchanges = ["NASDAQ", "NYSE", "TSX", "LSE", "HKEX", "TSE", "ASX", "FRA", "BSE", "NSE"]

    def get_valid_exchanges(self):
        """
        Returns a list of valid exchanges.
        """
        return self.valid_exchanges
