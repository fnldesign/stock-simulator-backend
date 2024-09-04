# routes/routes.py

from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
from flask_cors import CORS
from services.exchange_service import ExchangeService
from services.symbol_service import SymbolService
from config.log_config import setup_logging
from services.stock_simulator_service import StockSimulatorService
from config.config import Config
import pandas as pd

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize logging
setup_logging(log_dir=app.config.get('LOG_DIR', 'logs'))

# Corrected Swagger configuration with headers and other necessary settings
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'swagger',
            "route": '/swagger.json',
            "rule_filter": lambda rule: True,  # all endpoints included
            "model_filter": lambda tag: True,  # all models included
        }
    ],
    "static_url_path": "/swagger_static",  # Explicitly define static path
    "swagger_ui": True,
    "specs_route": "/swagger",  # Changed to custom route for Swagger UI
    "title": "Stock Simulator API Swagger"  # Set the browser tab title here
}

# Updated Swagger Template with Custom Title and Definitions
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Stock Simulator API Swagger",  # Custom title in UI
        "description": "API documentation for Stock Investment Simulator",
        "version": "1.0.0",
        "contact": {
            "name": "Support",
            "url": "http://www.example.com/support",
        },
    },
    "basePath": "/",  # Base path for API
    "schemes": ["http", "https"],
    "definitions": {  # Adding schema definitions here
        "SimulationRequestSchema": {
            "type": "object",
            "properties": {
                "exchange": {
                    "type": "string",
                    "example": "NASDAQ"
                },
                "symbol": {
                    "type": "string",
                    "example": "AAPL"
                },
                "start_date": {
                    "type": "string",
                    "format": "date",
                    "example": "2023-01-01"
                },
                "end_date": {
                    "type": "string",
                    "format": "date",
                    "example": "2023-09-01"
                },
                "start_value": {
                    "type": "number",
                    "example": 1000
                }
            },
            "required": ["exchange", "symbol", "start_date", "end_date", "start_value"]
        },
        "SimulationResultSchema": {
            "type": "object",
            "properties": {
                "start_value": {
                    "type": "number",
                    "example": 1000
                },
                "end_value": {
                    "type": "number",
                    "example": 1100.5
                },
                "growth_rate": {
                    "type": "number",
                    "format": "float",
                    "example": 10.05
                },
                "value_change": {
                    "type": "number",
                    "example": 100.5
                },
                "ohlcv_data": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "Date": {
                                "type": "string",
                                "format": "date-time",
                                "example": "2023-01-01 00:00:00"
                            },
                            "Open": {
                                "type": "number",
                                "example": 150.00
                            },
                            "High": {
                                "type": "number",
                                "example": 155.00
                            },
                            "Low": {
                                "type": "number",
                                "example": 148.00
                            },
                            "Close": {
                                "type": "number",
                                "example": 152.00
                            },
                            "Volume": {
                                "type": "integer",
                                "example": 100000
                            }
                        }
                    }
                }
            }
        }
    }
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)

# Initialize service classes
exchange_service = ExchangeService()
symbol_service = SymbolService()
simulator = StockSimulatorService(app.config['VALID_EXCHANGES'])

@app.route('/api/health', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'Backend is healthy'
        }
    }
})
def health_check():
    app.logger.info('Health check endpoint was called.')
    return jsonify({"status": "UP"}), 200

@app.route('/api/exchanges', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'A list of valid exchanges',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'string'
                }
            }
        }
    }
})
def get_exchanges():
    try:
        app.logger.info('Fetching list of valid exchanges.')
        exchanges = exchange_service.get_valid_exchanges()
        return jsonify(exchanges), 200
    except Exception as e:
        app.logger.error(f"Error fetching exchanges: {str(e)}")
        return jsonify({"error": "Failed to fetch exchanges"}), 500

@app.route('/api/symbols', methods=['GET'])
@swag_from({
    'parameters': [
        {
            'name': 'exchange',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'Exchange to retrieve symbols for (e.g., NASDAQ, NYSE, TSX.TO, etc.)'
        }
    ],
    'responses': {
        200: {
            'description': 'A list of valid symbols for the specified exchange',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'string'
                }
            }
        },
        400: {
            'description': 'Invalid exchange specified or error occurred'
        }
    }
})
def get_symbols():
    """
    Get a list of valid symbols for a specific exchange.
    """
    exchange = request.args.get('exchange')
    if not exchange:
        app.logger.error('Exchange parameter is missing.')
        return jsonify({"error": "Exchange parameter is required"}), 400

    try:
        symbols = symbol_service.get_symbols_for_exchange(exchange)
        return jsonify(symbols), 200
    except ValueError as e:
        app.logger.error(f"Error fetching symbols for exchange {exchange}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/simulate', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                '$ref': '#/definitions/SimulationRequestSchema'
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Simulation result with historical data',
            'schema': {
                '$ref': '#/definitions/SimulationResultSchema'
            }
        },
        400: {
            'description': 'Validation error'
        },
        500: {
            'description': 'Unexpected server error'
        }
    }
})
def simulate():
    try:
        data = request.json
        app.logger.info(f"Simulate endpoint called with data: {data}")
        result = simulator.simulate_investment(
            data['exchange'],
            data['symbol'],
            data['start_date'],
            data['end_date'],
            float(data['start_value'])
        )

        # Format OHLCV data with two decimal points and formatted dates using pandas
        for ohlcv in result['ohlcv_data']:
            ohlcv['Open'] = round(ohlcv['Open'], 2)
            ohlcv['High'] = round(ohlcv['High'], 2)
            ohlcv['Low'] = round(ohlcv['Low'], 2)
            ohlcv['Close'] = round(ohlcv['Close'], 2)
            # Format the date using pandas to handle timezone conversion
            ohlcv['Date'] = pd.to_datetime(ohlcv['Date']).strftime('%Y-%m-%d %H:%M:%S')

        app.logger.info(f"Simulation successful: {result}")
        return jsonify({"success": True, "result": result}), 200
    except ValueError as e:
        app.logger.warning(f"Validation error in simulation: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"Unexpected error in simulation: {str(e)}")
        return jsonify({"success": False, "error": "An unexpected error occurred"}), 500
