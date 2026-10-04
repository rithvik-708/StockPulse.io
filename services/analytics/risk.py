import numpy as np
from typing import Dict

def calculate_portfolio_exposure(positions: Dict[str, float], prices: Dict[str, float]) -> dict:
    total_exposure = 0.0
    exposures = {}
    
    for symbol, qty in positions.items():
        price = prices.get(symbol, 0.0)
        exposure = abs(qty * price)
        exposures[symbol] = exposure
        total_exposure += exposure
        
    return {
        "total_exposure": total_exposure,
        "asset_concentration": {sym: (exp / total_exposure) if total_exposure > 0 else 0 for sym, exp in exposures.items()}
    }

def calculate_historical_var(returns_array: list, confidence_level: float = 95.0) -> float:
    """
    Calculates Historical Value at Risk (VaR).
    returns_array: List or numpy array of historical portfolio returns.
    """
    if not returns_array:
        return 0.0
    
    percentile = 100 - confidence_level
    var = np.percentile(returns_array, percentile)
    
    # VaR is typically expressed as a positive number representing the loss
    return -var if var < 0 else 0.0
