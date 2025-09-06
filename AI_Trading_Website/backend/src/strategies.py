from typing import Dict, List, Tuple, Optional

# Function to detect Fair Value Gaps (FVG)
def detect_fvg(klines: List[Dict]) -> List[Tuple[str, float, float]]:
    fvg_zones = []
    for i in range(1, len(klines)):
        prev = klines[i-1]
        curr = klines[i]
        if curr['low'] > prev['high']:
            fvg_zones.append(('gap_up', prev['high'], curr['low']))
        elif curr['high'] < prev['low']:
            fvg_zones.append(('gap_down', curr['high'], prev['low']))
    return fvg_zones

# Function to check if price is near a liquidity zone
def check_liquidity_zone(price: float, liquidity_zones: List[float], threshold: float = 0.0015) -> bool:
    for zone in liquidity_zones:
        if abs(price - zone) / zone < threshold:
            return True
    return False

# Function to calculate RSI (Relative Strength Index)
def calculate_rsi(closes: List[float], period: int = 14) -> List[float]:
    if len(closes) < period + 1:
        return [50.0] * len(closes)  # Return neutral RSI if not enough data
    
    deltas = [closes[i] - closes[i-1] for i in range(1, len(closes))]
    seed = deltas[:period]
    up = sum(d for d in seed if d >= 0) / period
    down = -sum(d for d in seed if d < 0) / period
    rs = up/down if down != 0 else 0
    rsi = [0.0] * len(closes)
    rsi[:period] = [100. - 100./(1. + rs)] * period

    for i in range(period, len(closes)):
        delta = deltas[i-1]
        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up * (period - 1) + upval) / period
        down = (down * (period - 1) + downval) / period
        rs = up/down if down != 0 else 0
        rsi[i] = 100. - 100./(1. + rs)

    return rsi

# Function to calculate MACD (Moving Average Convergence Divergence)
def calculate_macd(closes: List[float], fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> Tuple[List[float], List[float], List[float]]:
    if len(closes) < max(fast_period, slow_period):
        return [0.0] * len(closes), [0.0] * len(closes), [0.0] * len(closes)
    
    # Calculate EMA
    def calculate_ema(data: List[float], period: int) -> List[float]:
        ema = [0.0] * len(data)
        multiplier = 2 / (period + 1)
        ema[0] = data[0]
        for i in range(1, len(data)):
            ema[i] = (data[i] * multiplier) + (ema[i-1] * (1 - multiplier))
        return ema
    
    fast_ema = calculate_ema(closes, fast_period)
    slow_ema = calculate_ema(closes, slow_period)
    macd = [fast_ema[i] - slow_ema[i] for i in range(len(closes))]
    signal = calculate_ema(macd, signal_period)
    histogram = [macd[i] - signal[i] for i in range(len(macd))]
    return macd, signal, histogram

# Function to calculate Bollinger Bands
def calculate_bollinger_bands(closes: List[float], period: int = 20, num_std_dev: float = 2.0) -> Tuple[List[float], List[float], List[float]]:
    if len(closes) < period:
        return closes[:], closes[:], closes[:]
    
    upper_band = []
    middle_band = []
    lower_band = []
    
    for i in range(len(closes)):
        if i < period - 1:
            # Not enough data for full calculation
            upper_band.append(closes[i])
            middle_band.append(closes[i])
            lower_band.append(closes[i])
        else:
            # Calculate SMA and standard deviation for the period
            window = closes[i-period+1:i+1]
            sma = sum(window) / period
            variance = sum((x - sma) ** 2 for x in window) / period
            std_dev = variance ** 0.5
            
            upper_band.append(sma + (std_dev * num_std_dev))
            middle_band.append(sma)
            lower_band.append(sma - (std_dev * num_std_dev))
    
    return upper_band, middle_band, lower_band

# Function to analyze trade signals based on selected strategy
def analyze_trade_signal(klines: List[Dict], strategy: str = "fvg_liquidity") -> Tuple[str, float]:
    if not klines or len(klines) < 20:
        return 'HOLD', 0.0

    closes = [k['close'] for k in klines]
    highs = [k['high'] for k in klines]
    lows = [k['low'] for k in klines]
    volumes = [k['volume'] for k in klines]
    last_close = closes[-1]
    
    # Calculate indicators
    rsi = calculate_rsi(closes)
    macd, signal, histogram = calculate_macd(closes)
    upper_band, middle_band, lower_band = calculate_bollinger_bands(closes)
    
    # Strategy selection
    if strategy == "fvg_liquidity":
        return analyze_fvg_liquidity(klines, rsi, macd, signal, histogram)
    elif strategy == "rsi_macd":
        return analyze_rsi_macd(rsi, macd, signal, histogram, last_close)
    elif strategy == "bollinger_breakout":
        return analyze_bollinger_breakout(closes, upper_band, middle_band, lower_band, rsi)
    else:
        # Default to FVG + Liquidity strategy
        return analyze_fvg_liquidity(klines, rsi, macd, signal, histogram)

# FVG + Liquidity strategy
def analyze_fvg_liquidity(klines: List[Dict], rsi: List[float], macd: List[float], signal: List[float], histogram: List[float]) -> Tuple[str, float]:
    fvg_zones = detect_fvg(klines)
    highs = [k['high'] for k in klines[-10:]]
    lows = [k['low'] for k in klines[-10:]]
    liquidity_zones = highs + lows
    last_close = klines[-1]['close']
    
    # Check RSI for confirmation
    last_rsi = rsi[-1]
    rsi_signal = "oversold" if last_rsi < 30 else "overbought" if last_rsi > 70 else "neutral"
    
    # Check MACD for confirmation
    macd_signal = "bullish" if histogram[-1] > 0 and histogram[-2] < histogram[-1] else "bearish" if histogram[-1] < 0 and histogram[-2] > histogram[-1] else "neutral"
    
    for fvg in fvg_zones:
        fvg_type, low_bound, high_bound = fvg
        if low_bound < last_close < high_bound:
            if check_liquidity_zone(last_close, liquidity_zones):
                if fvg_type == 'gap_down':
                    confidence = 0.85
                    if rsi_signal == "oversold" or macd_signal == "bullish":
                        confidence = 0.95
                    return 'BUY', confidence
                elif fvg_type == 'gap_up':
                    confidence = 0.85
                    if rsi_signal == "overbought" or macd_signal == "bearish":
                        confidence = 0.95
                    return 'SELL', confidence
    
    # Check for potential signals based on RSI and MACD
    if rsi_signal == "oversold" and macd_signal == "bullish":
        return 'BUY', 0.75
    elif rsi_signal == "overbought" and macd_signal == "bearish":
        return 'SELL', 0.75
    
    return 'HOLD', 0.0

# RSI + MACD strategy
def analyze_rsi_macd(rsi: List[float], macd: List[float], signal: List[float], histogram: List[float], last_close: float) -> Tuple[str, float]:
    last_rsi = rsi[-1]
    
    # MACD crossover detection
    macd_crossover = macd[-2] < signal[-2] and macd[-1] > signal[-1]  # Bullish crossover
    macd_crossunder = macd[-2] > signal[-2] and macd[-1] < signal[-1]  # Bearish crossunder
    
    # RSI conditions
    rsi_oversold = last_rsi < 30
    rsi_overbought = last_rsi > 70
    
    # Combined signals
    if rsi_oversold and macd_crossover:
        return 'BUY', 0.9
    elif rsi_overbought and macd_crossunder:
        return 'SELL', 0.9
    elif macd_crossover:
        return 'BUY', 0.7
    elif macd_crossunder:
        return 'SELL', 0.7
    elif rsi_oversold and histogram[-1] > histogram[-2]:
        return 'BUY', 0.6
    elif rsi_overbought and histogram[-1] < histogram[-2]:
        return 'SELL', 0.6
    
    return 'HOLD', 0.0

# Bollinger Bands Breakout strategy
def analyze_bollinger_breakout(closes: List[float], upper_band: List[float], middle_band: List[float], lower_band: List[float], rsi: List[float]) -> Tuple[str, float]:
    last_close = closes[-1]
    prev_close = closes[-2]
    
    # Check if price is breaking out of bands
    upper_breakout = prev_close <= upper_band[-2] and last_close > upper_band[-1]
    lower_breakout = prev_close >= lower_band[-2] and last_close < lower_band[-1]
    
    # Check if price is returning to middle band after touching outer bands
    upper_return = closes[-3] > upper_band[-3] and closes[-2] > upper_band[-2] and last_close < upper_band[-1] and last_close > middle_band[-1]
    lower_return = closes[-3] < lower_band[-3] and closes[-2] < lower_band[-2] and last_close > lower_band[-1] and last_close < middle_band[-1]
    
    # RSI confirmation
    rsi_overbought = rsi[-1] > 70
    rsi_oversold = rsi[-1] < 30
    
    if upper_breakout:
        # Potential continuation of uptrend
        return 'BUY', 0.6
    elif lower_breakout:
        # Potential continuation of downtrend
        return 'SELL', 0.6
    elif upper_return and rsi_overbought:
        # Price returning from upper band with overbought RSI
        return 'SELL', 0.8
    elif lower_return and rsi_oversold:
        # Price returning from lower band with oversold RSI
        return 'BUY', 0.8
    
    return 'HOLD', 0.0

# Function to calculate stop loss levels
def calculate_stop_loss(klines: List[Dict], signal: str, current_price: float) -> float:
    if not klines or len(klines) < 5:
        return 0.0
    
    if signal == 'BUY':
        # For buy signals, set stop loss below recent lows
        recent_lows = [k['low'] for k in klines[-10:]]
        stop_loss = min(recent_lows) * 0.995  # Slightly below the lowest recent low
    elif signal == 'SELL':
        # For sell signals, set stop loss above recent highs
        recent_highs = [k['high'] for k in klines[-10:]]
        stop_loss = max(recent_highs) * 1.005  # Slightly above the highest recent high
    else:
        # For hold signals, no stop loss
        stop_loss = 0.0
    
    return stop_loss

# Function to calculate take profit levels
def calculate_take_profit(klines: List[Dict], signal: str, current_price: float) -> float:
    if not klines or len(klines) < 5 or signal == 'HOLD':
        return 0.0
    
    # Calculate ATR (Average True Range) for dynamic take profit
    true_ranges = []
    for i in range(1, min(15, len(klines))):
        high = klines[-i]['high']
        low = klines[-i]['low']
        prev_close = klines[-i-1]['close']
        true_ranges.append(max(high - low, abs(high - prev_close), abs(low - prev_close)))
    
    atr = sum(true_ranges) / len(true_ranges) if true_ranges else 0
    
    if signal == 'BUY':
        # For buy signals, set take profit above current price based on ATR
        take_profit = current_price + (atr * 3)  # 3x ATR for take profit
    elif signal == 'SELL':
        # For sell signals, set take profit below current price based on ATR
        take_profit = current_price - (atr * 3)  # 3x ATR for take profit
    else:
        take_profit = 0.0
    
    return take_profit