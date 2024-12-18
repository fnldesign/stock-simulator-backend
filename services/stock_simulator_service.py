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
        change_df = hist[['Close']].round(2)
        change_df.reset_index(inplace=True)

        # Convert the 'Date' column to datetime format and format it as yyyy-MM-dd
        change_df['Date'] = pd.to_datetime(change_df['Date'], utc=True).dt.strftime('%Y-%m-%d')

        # Preencher valores NaN em 'Close'
        change_df['Close'] = change_df['Close'].fillna(method='ffill').fillna(0)

        # Calcular mudança percentual
        change_df['Change'] = change_df['Close'].pct_change()

        # Substituir NaN em 'Change' e garantir o primeiro valor como 0.0
        change_df['Change'] = change_df['Change'].fillna(0)
        change_df.loc[0, 'Change'] = 0.0

        # Arredondar 'Change' para duas casas decimais
        change_df['Change'] = change_df['Change'].round(2)

        # Calcular retorno acumulado
        change_df['Cumulative_Return'] = (change_df['Close'].div(change_df['Close'].iloc[0]) - 1) * 100
        change_df['Cumulative_Return'] = change_df['Cumulative_Return'].fillna(0).round(2)

        # Extrair dados de OHLCV para o gráfico de candlestick
        ohlcv_data = hist[['Open', 'High', 'Low', 'Close', 'Volume']].reset_index().to_dict('records')

        # Formatar os campos no array change_data
        change_data = change_df[['Date', 'Close', 'Change', 'Cumulative_Return']].to_dict('records')

        start_price = hist['Close'].iloc[0]
        end_price = hist['Close'].iloc[-1]

        growth_rate = (end_price - start_price) / start_price if start_price != 0 else 0
        end_value = start_value * (1 + growth_rate)
        value_change = end_value - start_value

        return {
            "start_value": start_value,
            "end_value": round(end_value, 2),
            "growth_rate": round(growth_rate * 100, 2),
            "value_change": round(value_change, 2),
            "ohlcv_data": ohlcv_data,
            "change_data": change_data
        }
