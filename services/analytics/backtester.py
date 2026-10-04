import pandas as pd
import numpy as np

def run_backtest(historical_data: pd.DataFrame, imbalance_threshold: float = 0.2) -> dict:
    """
    Expects DataFrame with columns: ['timestamp', 'close', 'imbalance', 'momentum']
    """
    df = historical_data.copy()
    
    # 1. Generate Signals (Vectorized)
    df['signal'] = 0
    df.loc[(df['imbalance'] > imbalance_threshold) & (df['momentum'] > 0), 'signal'] = 1
    df.loc[(df['imbalance'] < -imbalance_threshold) & (df['momentum'] < 0), 'signal'] = -1
    
    # Position is held until signal changes (forward fill active positions)
    df['position'] = df['signal'].replace(0, np.nan).ffill().fillna(0)
    
    # 2. Calculate Returns
    df['market_return'] = df['close'].pct_change()
    df['strategy_return'] = df['position'].shift(1) * df['market_return']
    
    # 3. Apply Transaction Costs (5 bps per trade)
    trade_cost = 0.0005 
    df['trades'] = df['position'].diff().abs()
    df['strategy_return'] -= (df['trades'] * trade_cost)
    
    df['cumulative_return'] = (1 + df['strategy_return']).cumprod()
    
    # 4. Compute Metrics
    total_return = df['cumulative_return'].iloc[-1] - 1 if not df.empty else 0
    
    # Annualized Sharpe (assuming high frequency, e.g., minute data)
    periods_per_year = 365 * 24 * 60 
    mean_ret = df['strategy_return'].mean()
    std_ret = df['strategy_return'].std()
    sharpe = (mean_ret / std_ret) * np.sqrt(periods_per_year) if std_ret > 0 else 0
    
    # Max Drawdown
    running_max = df['cumulative_return'].cummax()
    drawdown = (df['cumulative_return'] - running_max) / running_max
    max_drawdown = drawdown.min()
    
    # Win Rate
    winning_trades = len(df[df['strategy_return'] > 0])
    total_active_periods = len(df[df['strategy_return'] != 0])
    win_rate = winning_trades / total_active_periods if total_active_periods > 0 else 0
    
    return {
        "total_return_pct": total_return * 100,
        "sharpe_ratio": sharpe,
        "max_drawdown_pct": max_drawdown * 100,
        "win_rate_pct": win_rate * 100,
        "total_trades": int(df['trades'].sum())
    }
