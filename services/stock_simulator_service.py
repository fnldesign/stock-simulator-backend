import yfinance as yf
from flask import current_app as app
import pandas as pd

class StockSimulatorService:
    def __init__(self, valid_exchanges):
        self.valid_exchanges = valid_exchanges

    def validate_stock(self, exchange, symbol):
        if exchange not in self.valid_exchanges:
            return False
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            return 'symbol' in info and info['symbol'] == symbol
        except Exception as e:
            app.logger.error(f"Error validating stock: {str(e)}")
            return False

    def simulate_investment(self, exchange, symbol, start_date, end_date, start_value):
        if not self.validate_stock(exchange, symbol):
            raise ValueError("Invalid exchange or stock symbol")

        stock = yf.Ticker(symbol)
        hist = stock.history(start=start_date, end=end_date)

        if hist.empty:
            raise ValueError("No historical data available for the given date range")

        # Compute change Data
        change_df=hist[['Close']].round(2)
        change_df.reset_index()

        # Convert the 'Index' column to datetime format and format it as yyyy-MM-dd
        change_df.index=pd.to_datetime(change_df.index, utc=True).strftime('%Y-%m-%d')
        
        change_df['Change']=change_df['Close'].pct_change(fill_method='ffill')
        # Fill the first value in the 'Change' column with the second value
        change_df['Change'].iloc[0] = change_df['Change'].iloc[1]
        # Round the results to two decimal places
        change_df['Change'] = change_df['Change'].round(2)

        # Compute percent change acumulado
        change_df['Cumulative_Return'] = (change_df['Close'].div(change_df['Close'].iloc[0]) - 1) * 100
        change_df['Cumulative_Return'] = change_df['Cumulative_Return'].round(2)

        # Extract OHLCV data for candlestick chart
        ohlcv_data = hist[['Open', 'High', 'Low', 'Close', 'Volume']].reset_index().to_dict('records')
        change_data=change_df[['Close', 'Change','Cumulative_Return']].reset_index().to_dict('records')

        start_price = hist['Close'].iloc[0]
        end_price = hist['Close'].iloc[-1]

        growth_rate = (end_price - start_price) / start_price
        end_value = start_value * (1 + growth_rate)
        value_change = end_value - start_value
        
        return {
            "start_value": start_value,
            "end_value": round(end_value, 2),
            "growth_rate": round(growth_rate * 100, 2),
            "value_change": round(value_change, 2),
            "ohlcv_data": ohlcv_data,  # Include OHLCV data for candlestick chart
            "change_data": change_data
        }
