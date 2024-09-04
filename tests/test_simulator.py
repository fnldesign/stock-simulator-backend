import pytest
from services.stock_simulator_service import StockSimulatorService

@pytest.fixture
def simulator():
    valid_exchanges = ["B3", "NYSE", "NASDAQ", "LSE", "TSE", "HKSE"]
    return StockSimulatorService(valid_exchanges)

def test_validate_stock(simulator):
    # Assuming 'AAPL' is a valid stock symbol for 'NASDAQ'
    assert simulator.validate_stock("NASDAQ", "AAPL") is True

    # Invalid stock symbol
    assert simulator.validate_stock("NASDAQ", "INVALID") is False

def test_simulate_investment(simulator):
    result = simulator.simulate_investment("NASDAQ", "AAPL", "2023-01-01", "2023-09-01", 1000)
    
    assert "start_value" in result
    assert "end_value" in result
    assert "growth_rate" in result
    assert "value_change" in result
    assert "ohlcv_data" in result
    assert len(result["ohlcv_data"]) > 0

def test_invalid_exchange(simulator):
    with pytest.raises(ValueError):
        simulator.simulate_investment("INVALID", "AAPL", "2023-01-01", "2023-09-01", 1000)

def test_no_historical_data(simulator):
    with pytest.raises(ValueError):
        simulator.simulate_investment("NASDAQ", "AAPL", "1900-01-01", "1900-01-02", 1000)
