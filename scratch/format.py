import re

html = """
<aside class="fixed left-0 top-0 h-screen w-16 bg-surface-container-lowest flex flex-col justify-between py-space-sm z-50 shadow-[0_1px_8px_rgba(0,0,0,0.4)]"><div class="flex flex-col items-center gap-space-md w-full"><div class="h-10 w-full flex items-center justify-center"><img alt="StockPulse Brand Logo" class="h-8 w-auto object-contain" src="https://lh3.googleusercontent.com/aida/AEtjO1Vv5wuNs_lN61Ta91ZAqEEAEbPgpQy4TPj64lnd0K_-d258fGa3S4RoxVUv_7LLzNUIsWyjU5vngi57_mrZyoM-ER23GwN2eoKInyFmCCfXpO5zg2-apW7PjzCjgEUwmVKMWBMqvdvPgBnQS1z1DLpYm2dzQ8B7shfIiADtI6-_Ed-sKODqZkMGOCLU0taiBj2CmeNwOkS4dqj2ymIX_dDt0S8fMiysxgfHXkcQyma5Mw"/></div><nav class="flex flex-col items-center gap-space-xs w-full px-space-xs" data-active-classes="bg-surface-container-high text-primary-container"><a aria-current="page" class="flex flex-col items-center justify-center w-full h-10 rounded transition-colors bg-surface-container-high text-primary-container" data-path="terminal-dashboard" href="#" title="Terminal Dashboard"><span class="material-symbols-outlined text-[20px]">terminal</span><span class="font-label-caps text-label-caps uppercase mt-0.5">Term</span></a><a class="flex flex-col items-center justify-center w-full h-10 rounded text-on-surface-variant hover:bg-surface-container hover:text-on-surface transition-colors" data-path="order-book-depth" href="#" title="Order Book &amp; DOM"><span class="material-symbols-outlined text-[20px]">layers</span><span class="font-label-caps text-label-caps uppercase mt-0.5">Book</span></a><a class="flex flex-col items-center justify-center w-full h-10 rounded text-on-surface-variant hover:bg-surface-container hover:text-on-surface transition-colors" data-path="quant-signals" href="#" title="Quant Alpha Signals"><span class="material-symbols-outlined text-[20px]">bolt</span><span class="font-label-caps text-label-caps uppercase mt-0.5">Quant</span></a><a class="flex flex-col items-center justify-center w-full h-10 rounded text-on-surface-variant hover:bg-surface-container hover:text-on-surface transition-colors" data-path="ai-copilot" href="#" title="Algorithmic AI Copilot"><span class="material-symbols-outlined text-[20px]">smart_toy</span><span class="font-label-caps text-label-caps uppercase mt-0.5">Copilot</span></a><a class="flex flex-col items-center justify-center w-full h-10 rounded text-on-surface-variant hover:bg-surface-container hover:text-on-surface transition-colors" data-path="system-health" href="#" title="Telemetry &amp; Cluster Health"><span class="material-symbols-outlined text-[20px]">dns</span><span class="font-label-caps text-label-caps uppercase mt-0.5">Infra</span></a><a class="flex flex-col items-center justify-center w-full h-10 rounded text-on-surface-variant hover:bg-surface-container hover:text-on-surface transition-colors" data-path="settings-execution" href="#" title="Execution Parameters &amp; Settings"><span class="material-symbols-outlined text-[20px]">tune</span><span class="font-label-caps text-label-caps uppercase mt-0.5">Config</span></a></nav></div><div class="flex flex-col items-center gap-space-sm w-full px-space-xs"><div class="flex flex-col items-center justify-center w-full py-space-xs rounded bg-surface-container-low text-center" title="Active Cluster: US-EAST (Alpha-01)"><div class="flex items-center gap-1"><span class="inline-block w-1.5 h-1.5 bg-primary-container rounded-none animate-pulse"></span><span class="font-label-caps text-label-caps text-on-surface-variant uppercase">USE-1</span></div><span class="font-tabular-xs text-tabular-xs text-primary-container">ALPHA</span></div><div class="flex flex-col items-center justify-center w-full py-space-xs rounded bg-surface-container-low text-center" title="Risk Budget: Nominal 12.4%"><span class="font-label-caps text-label-caps text-on-surface-variant uppercase">Risk</span><span class="font-tabular-xs text-tabular-xs text-tertiary-fixed-dim">NOMINAL</span></div><a class="flex items-center justify-center w-full h-8 rounded text-on-surface-variant hover:bg-surface-container hover:text-on-surface transition-colors" data-path="api-documentation" href="#" title="Documentation &amp; API Specs"><span class="material-symbols-outlined text-[18px]">menu_book</span></a></div></aside><div class="pl-16"><header class="fixed top-0 left-16 right-0 h-14 bg-surface-container-lowest/95 backdrop-blur-md z-40 flex flex-col justify-between shadow-[0_1px_8px_rgba(0,0,0,0.5)]"><div class="h-6 w-full overflow-hidden bg-surface-container flex items-center px-space-md gap-space-xl"><div class="flex items-center gap-space-xs shrink-0"><span class="font-label-caps text-label-caps text-primary-container uppercase tracking-wider">MARKETS L2</span><span class="material-symbols-outlined text-[12px] text-on-surface-variant">rss_feed</span></div><div class="flex items-center gap-space-xl overflow-x-hidden whitespace-nowrap font-tabular-xs text-tabular-xs"><div class="flex items-center gap-space-xs"><span class="text-on-surface font-semibold">BTC/USDT</span><span class="text-primary-container">$92,450.20</span><span class="text-primary-container">+3.42%</span></div><div class="flex items-center gap-space-xs"><span class="text-on-surface font-semibold">ETH/USDT</span><span class="text-primary-container">$3,412.80</span><span class="text-primary-container">+1.85%</span></div><div class="flex items-center gap-space-xs"><span class="text-on-surface font-semibold">SOL/USDT</span><span class="text-secondary-fixed-dim">$188.40</span><span class="text-secondary-fixed-dim">-0.74%</span></div><div class="flex items-center gap-space-xs"><span class="text-on-surface font-semibold">NVDA</span><span class="text-primary-container">$142.25</span><span class="text-primary-container">+4.11%</span></div><div class="flex items-center gap-space-xs"><span class="text-on-surface font-semibold">SPX</span><span class="text-primary-container">$5,982.10</span><span class="text-primary-container">+0.28%</span></div><div class="flex items-center gap-space-xs"><span class="text-on-surface font-semibold">NQ</span><span class="text-primary-container">$21,114.50</span><span class="text-primary-container">+0.62%</span></div></div></div><div class="h-8 w-full px-space-md flex items-center justify-between gap-space-md bg-surface-container-low"><div class="flex items-center gap-space-lg"><div class="flex items-center gap-space-sm bg-surface-container-highest px-space-md py-space-xs rounded"><span class="font-headline-sm text-headline-sm text-on-surface tracking-tight">BTC/USDT Perp</span><span class="font-label-caps text-label-caps px-space-xs rounded bg-surface-container text-tertiary-fixed-dim">100X</span><span class="font-tabular-xs text-tabular-xs text-on-surface-variant">Vol: $4.82B</span><span class="font-tabular-xs text-tabular-xs text-primary-container">Idx: $92,450.20</span></div><div class="hidden xl:flex items-center gap-space-md font-tabular-xs text-tabular-xs text-on-surface-variant"><div class="flex items-center gap-1"><span class="w-1.5 h-1.5 bg-primary-container rounded-none"></span><span class="text-on-surface">WS Connected</span></div><div class="flex items-center gap-1"><span class="text-on-surface-variant">Kafka:</span><span class="text-primary-container">0ms</span></div><div class="flex items-center gap-1"><span class="text-on-surface-variant">L2:</span><span class="text-on-surface">420k msg/s</span></div><div class="flex items-center gap-1"><span class="text-on-surface-variant">MemTick:</span><span class="text-on-surface">1.2GB</span></div></div></div><div class="flex items-center gap-space-md"><div class="flex items-center gap-1 bg-surface-container px-space-sm py-space-xs rounded font-tabular-xs text-tabular-xs text-primary-container"><span class="material-symbols-outlined text-[14px]">speed</span><span>4µs NY4</span></div><button class="flex items-center text-on-surface-variant hover:text-on-surface transition-colors p-space-xs rounded hover:bg-surface-container" title="Toggle Sound Telemetry" type="button"><span class="material-symbols-outlined text-[16px]">volume_up</span></button><button class="flex items-center gap-1 text-on-surface-variant hover:text-on-surface transition-colors px-space-sm py-space-xs rounded bg-surface-container text-label-caps font-label-caps uppercase" title="Switch Tile Layout" type="button"><span class="material-symbols-outlined text-[14px]">dashboard_customize</span><span>Matrix 4x</span></button><div class="flex items-center gap-space-sm pl-space-sm"><div class="flex flex-col text-right hidden sm:flex"><span class="font-label-caps text-label-caps text-tertiary-fixed-dim uppercase leading-none">Citadel Alpha</span><span class="font-tabular-xs text-tabular-xs text-on-surface-variant leading-none mt-0.5">Desk #04</span></div><img alt="Profile" class="w-8 h-8 rounded-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBmuTop0Nd7x9i2zAhB8jdoTyjW6PTOhYe0CMzZ73j1W-ij_LTozGtBcSkF0NrslroWVrsz064jiMIF7NwLnPy6vEj6DIO91c4EJ5xb-OyOstecuGggdw-6vMWOxtaJhPE3N9_vEgSFF0Jjcw8JbSP6ddv3-LdJ1-OfVZnRZiEOdwi21Ajad0kDjVBsvSt7_se6E4ncJb0wo0U12PW95hjT5O7mWxz1CXSa0BvSGHWF"/></div></div></div></header><main class="w-full pt-14 bg-surface-container-lowest min-h-screen"><div class="flex flex-col w-full text-on-surface">
<!-- TOP TERMINAL METRIC RIBBON -->
<div class="w-full bg-surface-container-lowest px-space-md py-space-sm shadow-md">
<div class="flex flex-col xl:flex-row xl:items-center justify-between gap-space-md">
<!-- Instrument Core Specs -->
<div class="flex items-center flex-wrap gap-space-lg">
<div class="flex items-center gap-space-md">
<div class="flex items-center gap-space-xs">
<span class="w-2 h-2 bg-primary-container animate-pulse"></span>
<span class="font-headline-md text-headline-md tracking-tight text-primary font-bold">BTC/USDT</span>
<span class="font-label-caps text-label-caps px-space-xs py-0.5 bg-surface-container-high text-tertiary-fixed-dim">PERPETUAL</span>
</div>
<div class="flex items-baseline gap-space-sm pl-space-xs">
<span class="font-tabular-lg text-tabular-lg text-primary-container font-bold" id="live-mark-price">$94,820.50</span>
<span class="font-tabular-sm text-tabular-sm text-primary-container">+$3,240.20 (+3.54%)</span>
</div>
</div>
<div class="flex items-center gap-space-md font-tabular-xs text-tabular-xs text-on-surface-variant">
<div class="flex flex-col">
<span class="font-label-caps text-label-caps text-on-surface-variant">24H HIGH</span>
<span class="text-on-surface font-medium">$95,100.00</span>
</div>
<div class="flex flex-col">
<span class="font-label-caps text-label-caps text-on-surface-variant">24H LOW</span>
<span class="text-on-surface font-medium">$91,240.00</span>
</div>
<div class="flex flex-col">
<span class="font-label-caps text-label-caps text-on-surface-variant">24H TURNOVER</span>
<span class="text-on-surface font-medium">$5.41B</span>
</div>
<div class="flex flex-col">
<span class="font-label-caps text-label-caps text-on-surface-variant">FUNDING (02:14:32)</span>
<span class="text-primary-container font-medium">+0.0102%</span>
</div>
<div class="flex flex-col">
<span class="font-label-caps text-label-caps text-on-surface-variant">OPEN INTEREST</span>
<span class="text-tertiary-fixed-dim font-medium">84,219 BTC</span>
</div>
</div>
</div>
<!-- Quick Execution & Preset Switches -->
<div class="flex items-center gap-space-sm self-start xl:self-auto flex-wrap">
<div class="flex items-center bg-surface-container-high rounded p-0.5">
<span class="font-label-caps text-label-caps px-space-sm py-space-xs text-primary-container bg-surface-container font-bold">CROSS 50X</span>
<button class="font-label-caps text-label-caps px-space-sm py-space-xs text-on-surface-variant hover:text-on-surface transition-colors uppercase" type="button">ISOLATED</button>
</div>
<div class="flex items-center gap-space-xs">
<button class="px-space-md py-1 bg-surface-container hover:bg-surface-container-high text-on-surface font-label-caps text-label-caps rounded transition-colors uppercase" type="button">Limit</button>
<button class="px-space-md py-1 bg-surface-container hover:bg-surface-container-high text-on-surface font-label-caps text-label-caps rounded transition-colors uppercase" type="button">Market</button>
<button class="px-space-md py-1 bg-surface-container hover:bg-surface-container-high text-tertiary-fixed-dim font-label-caps text-label-caps rounded transition-colors uppercase" type="button">TWAP</button>
<button class="px-space-md py-1 bg-surface-container hover:bg-surface-container-high text-tertiary-fixed-dim font-label-caps text-label-caps rounded transition-colors uppercase" type="button">VWAP</button>
<button class="px-space-md py-1 bg-surface-container hover:bg-surface-container-high text-tertiary-fixed-dim font-label-caps text-label-caps rounded transition-colors uppercase" type="button">Iceberg</button>
</div>
<div class="flex items-center gap-space-xs pl-space-xs">
<button class="bg-primary-container hover:bg-primary-fixed text-on-primary font-tabular-sm text-tabular-sm font-bold px-space-md py-1 rounded shadow-sm transition-colors" type="button">
            BUY / LONG
          </button>
<button class="bg-secondary-container hover:bg-on-secondary-fixed-variant text-on-secondary-container font-tabular-sm text-tabular-sm font-bold px-space-md py-1 rounded shadow-sm transition-colors" type="button">
            SELL / SHORT
          </button>
</div>
</div>
</div>
</div>
<!-- WORKSPACE MATRIX (Bento Layout) -->
<div class="grid grid-cols-1 lg:grid-cols-12 gap-gutter p-gutter bg-surface-container-high min-h-[calc(100vh-8.5rem)]">
<!-- COLUMN 1 & 2: CHART DOMAIN (7 Cols) -->
<div class="lg:col-span-7 flex flex-col gap-gutter">
<!-- MAIN CANDLESTICK / DEPTH ENGINE -->
<div class="bg-surface-container-lowest flex flex-col h-[520px] shadow-sm relative">
<!-- Chart Controls Ribbon -->
<div class="flex items-center justify-between px-space-md py-space-xs bg-surface-container-low">
<div class="flex items-center gap-space-md">
<div class="flex items-center gap-0.5 bg-surface-container-lowest p-0.5 rounded">
<button class="font-tabular-xs text-tabular-xs px-2 py-0.5 text-on-surface-variant hover:text-on-surface" type="button">1s</button>
<button class="font-tabular-xs text-tabular-xs px-2 py-0.5 bg-surface-container-high text-primary-container font-bold rounded" type="button">1m</button>
<button class="font-tabular-xs text-tabular-xs px-2 py-0.5 text-on-surface-variant hover:text-on-surface" type="button">5m</button>
<button class="font-tabular-xs text-tabular-xs px-2 py-0.5 text-on-surface-variant hover:text-on-surface" type="button">15m</button>
<button class="font-tabular-xs text-tabular-xs px-2 py-0.5 text-on-surface-variant hover:text-on-surface" type="button">1h</button>
<button class="font-tabular-xs text-tabular-xs px-2 py-0.5 text-on-surface-variant hover:text-on-surface" type="button">4h</button>
<button class="font-tabular-xs text-tabular-xs px-2 py-0.5 text-on-surface-variant hover:text-on-surface" type="button">1D</button>
</div>
<div class="h-3 w-px bg-surface-container-highest"></div>
<div class="flex items-center gap-space-xs font-label-caps text-label-caps">
<span class="text-tertiary-fixed-dim bg-surface-container px-1.5 py-0.5 rounded">EMA 20/50/200</span>
<span class="text-tertiary-fixed-dim bg-surface-container px-1.5 py-0.5 rounded">BOLL (20,2)</span>
<span class="text-primary-container bg-surface-container px-1.5 py-0.5 rounded">POC: $94,620</span>
<span class="text-on-surface-variant bg-surface-container px-1.5 py-0.5 rounded">VWAP</span>
</div>
</div>
<div class="flex items-center gap-space-xs">
<button class="font-label-caps text-label-caps px-space-sm py-1 bg-surface-container-high text-primary-container rounded" type="button">CANDLES</button>
<button class="font-label-caps text-label-caps px-space-sm py-1 bg-surface-container text-on-surface-variant hover:text-on-surface rounded" type="button">DEPTH 3D</button>
<button class="font-label-caps text-label-caps px-space-sm py-1 bg-surface-container text-on-surface-variant hover:text-on-surface rounded" type="button">ORDER FLOW</button>
</div>
</div>
<!-- Floating OHLC Realtime HUD -->
<div class="px-space-md py-space-xs flex items-center justify-between text-on-surface-variant font-tabular-xs text-tabular-xs bg-surface-container-lowest/80 backdrop-blur-sm z-10">
<div class="flex items-center gap-space-md flex-wrap">
<span>O: <strong class="text-on-surface">94,780.00</strong></span>
<span>H: <strong class="text-primary-container">94,850.50</strong></span>
<span>L: <strong class="text-secondary-fixed-dim">94,750.00</strong></span>
<span>C: <strong class="text-primary-container">94,820.50</strong></span>
<span>VOL: <strong class="text-on-surface">1,420.48 BTC</strong></span>
</div>
<div class="flex items-center gap-space-sm font-label-caps text-label-caps">
<span class="text-primary-container">SPREAD: $0.50 (0.0005%)</span>
<span class="text-on-surface-variant">AGGREGATOR: L2 SYNTHETIC</span>
</div>
</div>
<!-- Inline SVG Candlestick & Volume Canvas -->
<div class="relative flex-1 w-full overflow-hidden bg-surface-container-lowest">
<svg class="w-full h-full" fill="none" preserveaspectratio="none" viewbox="0 0 900 420">
<defs>
<lineargradient id="volGreenGrad" x1="0" x2="0" y1="0" y2="1">
<stop offset="0%" stop-color="#00ff88" stop-opacity="0.45"></stop>
<stop offset="100%" stop-color="#00ff88" stop-opacity="0.05"></stop>
</lineargradient>
<lineargradient id="volRedGrad" x1="0" x2="0" y1="0" y2="1">
<stop offset="0%" stop-color="#ff334b" stop-opacity="0.45"></stop>
<stop offset="100%" stop-color="#ff334b" stop-opacity="0.05"></stop>
</lineargradient>
<lineargradient id="vwapGlow" x1="0" x2="1" y1="0" y2="0">
<stop offset="0%" stop-color="#4cd7f6" stop-opacity="0.2"></stop>
<stop offset="100%" stop-color="#4cd7f6" stop-opacity="0.9"></stop>
</lineargradient>
</defs>
<!-- Horizontal Grid Lines -->
<line stroke="#1d2026" stroke-dasharray="4,4" stroke-width="1" x1="0" x2="900" y1="60" y2="60"></line>
<line stroke="#1d2026" stroke-dasharray="4,4" stroke-width="1" x1="0" x2="900" y1="120" y2="120"></line>
<line stroke="#1d2026" stroke-dasharray="4,4" stroke-width="1" x1="0" x2="900" y1="180" y2="180"></line>
<line stroke="#1d2026" stroke-dasharray="4,4" stroke-width="1" x1="0" x2="900" y1="240" y2="240"></line>
<line stroke="#1d2026" stroke-dasharray="4,4" stroke-width="1" x1="0" x2="900" y1="300" y2="300"></line>
<!-- Price Scale Coordinates On Canvas -->
<text fill="#849585" font-family="JetBrains Mono" font-size="10" x="840" y="58">95,000</text>
<text fill="#849585" font-family="JetBrains Mono" font-size="10" x="840" y="118">94,900</text>
<text fill="#849585" font-family="JetBrains Mono" font-size="10" x="840" y="178">94,800</text>
<text fill="#849585" font-family="JetBrains Mono" font-size="10" x="840" y="238">94,700</text>
<text fill="#849585" font-family="JetBrains Mono" font-size="10" x="840" y="298">94,600</text>
<!-- VWAP Curvature Line -->
<path d="M 30 220 Q 240 200, 450 175 T 840 145" fill="none" stroke="url(#vwapGlow)" stroke-width="1.75"></path>
<!-- Bollinger Band Envelope -->
<path d="M 30 180 Q 250 160, 480 130 T 840 100" fill="none" stroke="#849585" stroke-opacity="0.3" stroke-width="1"></path>
<path d="M 30 260 Q 250 240, 480 210 T 840 190" fill="none" stroke="#849585" stroke-opacity="0.3" stroke-width="1"></path>
<!-- Candlesticks (Sequence of high precision candles) -->
<!-- 1 Bullish -->
<line stroke="#00ff88" stroke-width="1.5" x1="50" x2="50" y1="190" y2="240"></line>
<rect fill="#00ff88" height="32" width="12" x="44" y="200"></rect>
<!-- 2 Bearish -->
<line stroke="#ff334b" stroke-width="1.5" x1="90" x2="90" y1="185" y2="235"></line>
<rect fill="#ff334b" height="24" width="12" x="84" y="195"></rect>
<!-- 3 Bullish -->
<line stroke="#00ff88" stroke-width="1.5" x1="130" x2="130" y1="170" y2="225"></line>
<rect fill="#00ff88" height="35" width="12" x="124" y="180"></rect>
<!-- 4 Bullish -->
<line stroke="#00ff88" stroke-width="1.5" x1="170" x2="170" y1="160" y2="210"></line>
<rect fill="#00ff88" height="30" width="12" x="164" y="170"></rect>
<!-- 5 Bearish -->
<line stroke="#ff334b" stroke-width="1.5" x1="210" x2="210" y1="165" y2="220"></line>
<rect fill="#ff334b" height="35" width="12" x="204" y="175"></rect>
<!-- 6 Bearish -->
<line stroke="#ff334b" stroke-width="1.5" x1="250" x2="250" y1="190" y2="250"></line>
<rect fill="#ff334b" height="42" width="12" x="244" y="200"></rect>
<!-- 7 Bullish (Absorption) -->
<line stroke="#00ff88" stroke-width="1.5" x1="290" x2="290" y1="195" y2="260"></line>
<rect fill="#00ff88" height="25" width="12" x="284" y="210"></rect>
<!-- 8 Bullish -->
<line stroke="#00ff88" stroke-width="1.5" x1="330" x2="330" y1="175" y2="230"></line>
<rect fill="#00ff88" height="38" width="12" x="324" y="185"></rect>
<!-- 9 Bullish Spike -->
<line stroke="#00ff88" stroke-width="1.5" x1="370" x2="370" y1="145" y2="200"></line>
<rect fill="#00ff88" height="40" width="12" x="364" y="155"></rect>
<!-- 10 Bearish Pullback -->
<line stroke="#ff334b" stroke-width="1.5" x1="410" x2="410" y1="150" y2="195"></line>
<rect fill="#ff334b" height="22" width="12" x="404" y="160"></rect>
<!-- 11 Bullish Consolidation -->
<line stroke="#00ff88" stroke-width="1.5" x1="450" x2="450" y1="140" y2="185"></line>
<rect fill="#00ff88" height="25" width="12" x="444" y="150"></rect>
<!-- 12 Bullish Rally -->
<line stroke="#00ff88" stroke-width="1.5" x1="490" x2="490" y1="120" y2="175"></line>
<rect fill="#00ff88" height="35" width="12" x="484" y="130"></rect>
<!-- 13 Bullish Push -->
<line stroke="#00ff88" stroke-width="1.5" x1="530" x2="530" y1="105" y2="160"></line>
<rect fill="#00ff88" height="30" width="12" x="524" y="115"></rect>
<!-- 14 Bearish Exhaustion -->
<line stroke="#ff334b" stroke-width="1.5" x1="570" x2="570" y1="110" y2="170"></line>
<rect fill="#ff334b" height="35" width="12" x="564" y="125"></rect>
<!-- 15 Bullish Pin-Bar -->
<line stroke="#00ff88" stroke-width="1.5" x1="610" x2="610" y1="125" y2="190"></line>
<rect fill="#00ff88" height="15" width="12" x="604" y="135"></rect>
<!-- 16 Bullish Surge -->
<line stroke="#00ff88" stroke-width="1.5" x1="650" x2="650" y1="95" y2="155"></line>
<rect fill="#00ff88" height="38" width="12" x="644" y="110"></rect>
<!-- 17 Bearish Retest -->
<line stroke="#ff334b" stroke-width="1.5" x1="690" x2="690" y1="100" y2="148"></line>
<rect fill="#ff334b" height="22" width="12" x="684" y="112"></rect>
<!-- 18 Bullish Continuation -->
<line stroke="#00ff88" stroke-width="1.5" x1="730" x2="730" y1="80" y2="135"></line>
<rect fill="#00ff88" height="32" width="12" x="724" y="92"></rect>
<!-- 19 Current Live Active Candle -->
<line stroke="#00ff88" stroke-width="2" x1="770" x2="770" y1="75" y2="128"></line>
<rect class="animate-pulse" fill="#00ff88" height="28" width="12" x="764" y="84"></rect>
<!-- Live Horizontal Price Line stretching across chart -->
<line opacity="0.9" stroke="#00ff88" stroke-dasharray="5,3" stroke-width="1.2" x1="0" x2="840" y1="84" y2="84"></line>
<rect fill="#00ff88" height="20" rx="2" width="64" x="836" y="74"></rect>
<text fill="#00210c" font-family="JetBrains Mono" font-size="10.5" font-weight="700" x="840" y="88">94,820.50</text>
<!-- Real-time Pulsing Dot on Current Candlestick -->
<circle cx="770" cy="84" fill="#00ff88" r="3.5"></circle>
<circle class="animate-ping" cx="770" cy="84" opacity="0.6" r="7" stroke="#00ff88" stroke-width="1"></circle>
<!-- Bottom Volume Histogram Section (Height: 80px) -->
<line stroke="#1d2026" stroke-width="1" x1="0" x2="900" y1="340" y2="340"></line>
<text fill="#849585" font-family="JetBrains Mono" font-size="9" x="12" y="352">VOL (BTC) - L2 SYNC</text>
<rect fill="url(#volGreenGrad)" height="40" width="12" x="44" y="375"></rect>
<rect fill="url(#volRedGrad)" height="30" width="12" x="84" y="385"></rect>
<rect fill="url(#volGreenGrad)" height="50" width="12" x="124" y="365"></rect>
<rect fill="url(#volGreenGrad)" height="45" width="12" x="164" y="370"></rect>
<rect fill="url(#volRedGrad)" height="55" width="12" x="204" y="360"></rect>
<rect fill="url(#volRedGrad)" height="65" width="12" x="244" y="350"></rect>
<rect fill="url(#volGreenGrad)" height="35" width="12" x="284" y="380"></rect>
<rect fill="url(#volGreenGrad)" height="50" width="12" x="324" y="365"></rect>
<rect fill="url(#volGreenGrad)" height="70" width="12" x="364" y="345"></rect>
<rect fill="url(#volRedGrad)" height="37" width="12" x="404" y="378"></rect>
<rect fill="url(#volGreenGrad)" height="43" width="12" x="444" y="372"></rect>
<rect fill="url(#volGreenGrad)" height="60" width="12" x="484" y="355"></rect>
<rect fill="url(#volGreenGrad)" height="53" width="12" x="524" y="362"></rect>
<rect fill="url(#volRedGrad)" height="63" width="12" x="564" y="352"></rect>
<rect fill="url(#volGreenGrad)" height="33" width="12" x="604" y="382"></rect>
<rect fill="url(#volGreenGrad)" height="73" width="12" x="644" y="342"></rect>
<rect fill="url(#volRedGrad)" height="45" width="12" x="684" y="370"></rect>
<rect fill="url(#volGreenGrad)" height="65" width="12" x="724" y="350"></rect>
<rect fill="url(#volGreenGrad)" height="71" width="12" x="764" y="344"></rect>
</svg>
</div>
<!-- Cumulative Depth Wall Miniature Overlay (Bottom Corner Anchor) -->
<div class="absolute bottom-3 left-3 bg-surface-container-low/90 backdrop-blur-md p-space-sm rounded w-72 shadow-xl">
<div class="flex items-center justify-between text-label-caps font-label-caps text-on-surface-variant mb-1">
<span>CUMULATIVE DEPTH (BID vs ASK)</span>
<span class="text-primary-container">SPREAD: $0.50</span>
</div>
<div class="h-10 w-full flex items-end gap-1">
<!-- Bids Wall -->
<div class="w-1/2 h-full flex items-end justify-end gap-0.5">
<div class="w-2 bg-primary-container/20 h-2"></div>
<div class="w-2 bg-primary-container/30 h-4"></div>
<div class="w-2 bg-primary-container/40 h-6"></div>
<div class="w-2 bg-primary-container/60 h-8"></div>
<div class="w-2 bg-primary-container h-full"></div>
</div>
<!-- Spread mid line -->
<div class="w-0.5 bg-surface-bright h-full"></div>
<!-- Asks Wall -->
<div class="w-1/2 h-full flex items-end justify-start gap-0.5">
<div class="w-2 bg-secondary-container h-7"></div>
<div class="w-2 bg-secondary-container/60 h-5"></div>
<div class="w-2 bg-secondary-container/40 h-4"></div>
<div class="w-2 bg-secondary-container/30 h-3"></div>
<div class="w-2 bg-secondary-container/20 h-1"></div>
</div>
</div>
<div class="flex justify-between font-tabular-xs text-tabular-xs text-on-surface-variant mt-1">
<span class="text-primary-container">Bids: 1,840 BTC</span>
<span class="text-secondary-fixed-dim">Asks: 1,120 BTC</span>
</div>
</div>
</div>
<!-- RECENT EXECUTION TAPE (Under chart for institutional sub-second audit) -->
<div class="bg-surface-container-lowest p-space-sm flex flex-col shadow-sm">
<div class="flex items-center justify-between px-space-xs pb-space-xs bg-surface-container-low px-space-sm py-1">
<div class="flex items-center gap-space-sm">
<span class="material-symbols-outlined text-[16px] text-primary-container">receipt_long</span>
<span class="font-label-caps text-label-caps uppercase tracking-wider text-on-surface">Live Market Trades Tape</span>
<span class="font-tabular-xs text-tabular-xs text-on-surface-variant">420 Ticks/sec</span>
</div>
<span class="font-label-caps text-label-caps text-primary-container">WS: HIGH DENSITY REALTIME</span>
</div>
<div class="grid grid-cols-4 px-space-sm py-1 font-label-caps text-label-caps text-on-surface-variant bg-surface-container-lowest">
<span>TIME (UTC-0)</span>
<span class="text-right">PRICE (USDT)</span>
<span class="text-right">SIZE (BTC)</span>
<span class="text-right">SIDE</span>
</div>
<div class="flex flex-col font-tabular-xs text-tabular-xs overflow-hidden max-h-36">
<div class="grid grid-cols-4 px-space-sm py-0.5 hover:bg-surface-container transition-colors items-center bg-primary-container/10">
<span class="text-on-surface-variant">14:32:01.428912</span>
<span class="text-right text-primary-container font-semibold">94,820.50</span>
<span class="text-right text-on-surface">2.4180</span>
<span class="text-right font-label-caps text-label-caps text-primary-container font-bold">BUY</span>
</div>
<div class="grid grid-cols-4 px-space-sm py-0.5 hover:bg-surface-container transition-colors items-center">
<span class="text-on-surface-variant">14:32:01.398104</span>
<span class="text-right text-primary-container font-semibold">94,820.50</span>
<span class="text-right text-on-surface">0.8500</span>
<span class="text-right font-label-caps text-label-caps text-primary-container font-bold">BUY</span>
</div>
<div class="grid grid-cols-4 px-space-sm py-0.5 hover:bg-surface-container transition-colors items-center bg-secondary-container/10">
<span class="text-on-surface-variant">14:32:01.312005</span>
<span class="text-right text-secondary-fixed-dim font-semibold">94,820.00</span>
<span class="text-right text-on-surface">5.1200</span>
<span class="text-right font-label-caps text-label-caps text-secondary-fixed-dim font-bold">SELL</span>
</div>
<div class="grid grid-cols-4 px-space-sm py-0.5 hover:bg-surface-container transition-colors items-center">
<span class="text-on-surface-variant">14:32:01.298711</span>
<span class="text-right text-primary-container font-semibold">94,820.50</span>
<span class="text-right text-on-surface">0.1420</span>
<span class="text-right font-label-caps text-label-caps text-primary-container font-bold">BUY</span>
</div>
<div class="grid grid-cols-4 px-space-sm py-0.5 hover:bg-surface-container transition-colors items-center">
<span class="text-on-surface-variant">14:32:01.210452</span>
<span class="text-right text-primary-container font-semibold">94,820.50</span>
<span class="text-right text-on-surface">1.0000</span>
<span class="text-right font-label-caps text-label-caps text-primary-container font-bold">BUY</span>
</div>
<div class="grid grid-cols-4 px-space-sm py-0.5 hover:bg-surface-container transition-colors items-center">
<span class="text-on-surface-variant">14:32:01.194510</span>
<span class="text-right text-secondary-fixed-dim font-semibold">94,820.00</span>
<span class="text-right text-on-surface">0.4500</span>
<span class="text-right font-label-caps text-label-caps text-secondary-fixed-dim font-bold">SELL</span>
</div>
</div>
</div>
</div>
<!-- COLUMN 3: ORDER BOOK DEPTH LADDER (2.5 / ~3 Cols equivalent) -->
<div class="lg:col-span-2 flex flex-col bg-surface-container-lowest shadow-sm h-full">
<!-- Order Book Telemetry Header -->
<div class="p-space-sm bg-surface-container-low flex flex-col gap-0.5">
<div class="flex items-center justify-between">
<span class="font-label-caps text-label-caps uppercase text-on-surface font-semibold tracking-wider">L2 Depth Ladder</span>
<span class="font-tabular-xs text-tabular-xs text-primary-container font-medium">12µs LATENCY</span>
</div>
<div class="flex items-center justify-between font-label-caps text-label-caps text-on-surface-variant">
<span>TICK: 18.4kHz</span>
<span>BINANCE FUT</span>
</div>
</div>
<!-- DOM Ladder Table Head -->
<div class="grid grid-cols-3 px-space-sm py-1 font-label-caps text-label-caps text-on-surface-variant bg-surface-container-lowest">
<span>PRICE (USDT)</span>
<span class="text-right">SIZE</span>
<span class="text-right">TOTAL</span>
</div>
<!-- ASKS (Red / descending to spread) -->
<div class="flex flex-col overflow-hidden font-tabular-xs text-tabular-xs">
<!-- Ask Row 8 -->
<div class="relative grid grid-cols-3 px-space-sm py-0.5 items-center hover:bg-surface-container">
<div class="absolute right-0 top-0 bottom-0 bg-secondary-container/15" style="width: 82%;"></div>
<span class="text-secondary-fixed-dim font-semibold z-10">94,830.00</span>
<span class="text-right text-on-surface z-10">4.120</span>
<span class="text-right text-on-surface-variant z-10">24.89</span>
</div>
<!-- Ask Row 7 -->
<div class="relative grid grid-cols-3 px-space-sm py-0.5 items-center hover:bg-surface-container">
<div class="absolute right-0 top-0 bottom-0 bg-secondary-container/15" style="width: 71%;"></div>
<span class="text-secondary-fixed-dim font-semibold z-10">94,828.50</span>
<span class="text-right text-on-surface z-10">3.850</span>
<span class="text-right text-on-surface-variant z-10">20.77</span>
</div>
<!-- Ask Row 6 -->
<div class="relative grid grid-cols-3 px-space-sm py-0.5 items-center hover:bg-surface-container">
<div class="absolute right-0 top-0 bottom-0 bg-secondary-container/15" style="width: 59%;"></div>
<span class="text-secondary-fixed-dim font-semibold z-10">94,827.00</span>
<span class="text-right text-on-surface z-10">1.940</span>
<span class="text-right text-on-surface-variant z-10">16.92</span>
</div>
<!-- Ask Row 5 -->
<div class="relative grid grid-cols-3 px-space-sm py-0.5 items-center hover:bg-surface-container">
<div class="absolute right-0 top-0 bottom-0 bg-secondary-container/15" style="width: 48%;"></div>
<span class="text-secondary-fixed-dim font-semibold z-10">94,825.50</span>
<span class="text-right text-on-surface z-10">5.420</span>
<span class="text-right text-on-surface-variant z-10">14.98</span>
</div>
<!-- Ask Row 4 -->
<div class="relative grid grid-cols-3 px-space-sm py-0.5 items-center hover:bg-surface-container">
<div class="absolute right-0 top-0 bottom-0 bg-secondary-container/15" style="width: 32%;"></div>
<span class="text-secondary-fixed-dim font-semibold z-10">94,824.00</span>
<span class="text-right text-on-surface z-10">2.180</span>
<span class="text-right text-on-surface-variant z-10">9.56</span>
</div>
<!-- Ask Row 3 -->
<div class="relative grid grid-cols-3 px-space-sm py-0.5 items-center hover:bg-surface-container">
<div class="absolute right-0 top-0 bottom-0 bg-secondary-container/15" style="width: 26%;"></div>
<span class="text-secondary-fixed-dim font-semibold z-10">94,823.00</span>
<span class="text-right text-on-surface z-10">3.410</span>
<span class="text-right text-on-surface-variant z-10">7.38</span>
</div>
<!-- Ask Row 2 -->
<div class="relative grid grid-cols-3 px-space-sm py-0.5 items-center hover:bg-surface-container">
<div class="absolute right-0 top-0 bottom-0 bg-secondary-container/15" style="width: 14%;"></div>
<span class="text-secondary-fixed-dim font-semibold z-10">94,822.00</span>
<span class="text-right text-on-surface z-10">1.250</span>
<span class="text-right text-on-surface-variant z-10">3.97</span>
</div>
<!-- Ask Row 1 (Best Ask) -->
<div class="relative grid grid-cols-3 px-space-sm py-0.5 items-center hover:bg-surface-container">
<div class="absolute right-0 top-0 bottom-0 bg-secondary-container/15" style="width: 9%;"></div>
<span class="text-secondary-fixed-dim font-semibold z-10">94,821.00</span>
<span class="text-right text-on-surface z-10">2.720</span>
<span class="text-right text-on-surface-variant z-10">2.72</span>
</div>
</div>
<!-- MID-MARKET SPREAD BANNER -->
<div class="my-space-xs px-space-sm py-1.5 bg-surface-container flex flex-col gap-0.5 shadow-inner">
<div class="flex items-center justify-between">
<div class="flex items-center gap-space-xs">
<span class="font-tabular-md text-tabular-md text-primary-container font-bold">94,820.50</span>
<span class="material-symbols-outlined text-[16px] text-primary-container">arrow_upward</span>
</div>
<span class="font-label-caps text-label-caps text-on-surface-variant">SPREAD 0.50</span>
</div>
<div class="flex items-center justify-between font-label-caps text-label-caps">
<span class="text-primary-container font-semibold">IMBALANCE: +62.4% BID</span>
<span class="text-on-surface-variant">RATIO 1.66</span>
</div>
</div>
<!-- BIDS (Green / descending from spread) -->
<div class="flex flex-col overflow-hidden font-tabular-xs text-tabular-xs">
<!-- Bid Row 1 (Best Bid) -->
<div class="relative grid grid-cols-3 px-space-sm py-0.5 items-center hover:bg-surface-container">
<div class="absolute right-0 top-0 bottom-0 bg-primary-container/15" style="width: 12%;"></div>
<span class="text-primary-container font-semibold z-10">94,820.00</span>
<span class="text-right text-on-surface z-10">3.510</span>
<span class="text-right text-on-surface-variant z-10">3.51</span>
</div>
<!-- Bid Row 2 -->
<div class="relative grid grid-cols-3 px-space-sm py-0.5 items-center hover:bg-surface-container">
<div class="absolute right-0 top-0 bottom-0 bg-primary-container/15" style="width: 25%;"></div>
<span class="text-primary-container font-semibold z-10">94,819.00</span>
<span class="text-right text-on-surface z-10">4.180</span>
<span class="text-right text-on-surface-variant z-10">7.69</span>
</div>
<!-- Bid Row 3 -->
<div class="relative grid grid-cols-3 px-space-sm py-0.5 items-center hover:bg-surface-container">
<div class="absolute right-0 top-0 bottom-0 bg-primary-container/15" style="width: 41%;"></div>
<span class="text-primary-container font-semibold z-10">94,818.00</span>
<span class="text-right text-on-surface z-10">6.240</span>
<span class="text-right text-on-surface-variant z-10">13.93</span>
</div>
<!-- Bid Row 4 -->
<div class="relative grid grid-cols-3 px-space-sm py-0.5 items-center hover:bg-surface-container">
<div class="absolute right-0 top-0 bottom-0 bg-primary-container/15" style="width: 52%;"></div>
<span class="text-primary-container font-semibold z-10">94,817.00</span>
<span class="text-right text-on-surface z-10">2.910</span>
<span class="text-right text-on-surface-variant z-10">16.84</span>
</div>
<!-- Bid Row 5 -->
<div class="relative grid grid-cols-3 px-space-sm py-0.5 items-center hover:bg-surface-container">
<div class="absolute right-0 top-0 bottom-0 bg-primary-container/15" style="width: 68%;"></div>
<span class="text-primary-container font-semibold z-10">94,815.50</span>
<span class="text-right text-on-surface z-10">8.400</span>
<span class="text-right text-on-surface-variant z-10">25.24</span>
</div>
<!-- Bid Row 6 -->
<div class="relative grid grid-cols-3 px-space-sm py-0.5 items-center hover:bg-surface-container">
<div class="absolute right-0 top-0 bottom-0 bg-primary-container/15" style="width: 79%;"></div>
<span class="text-primary-container font-semibold z-10">94,814.00</span>
<span class="text-right text-on-surface z-10">3.750</span>
<span class="text-right text-on-surface-variant z-10">28.99</span>
</div>
<!-- Bid Row 7 -->
<div class="relative grid grid-cols-3 px-space-sm py-0.5 items-center hover:bg-surface-container">
<div class="absolute right-0 top-0 bottom-0 bg-primary-container/15" style="width: 88%;"></div>
<span class="text-primary-container font-semibold z-10">94,812.50</span>
<span class="text-right text-on-surface z-10">4.200</span>
<span class="text-right text-on-surface-variant z-10">33.19</span>
</div>
<!-- Bid Row 8 -->
<div class="relative grid grid-cols-3 px-space-sm py-0.5 items-center hover:bg-surface-container">
<div class="absolute right-0 top-0 bottom-0 bg-primary-container/15" style="width: 98%;"></div>
<span class="text-primary-container font-semibold z-10">94,810.00</span>
<span class="text-right text-on-surface z-10">12.800</span>
<span class="text-right text-on-surface-variant z-10">45.99</span>
</div>
</div>
</div>
<!-- COLUMN 4: QUANT ENGINE & AI COPILOT (3 Cols) -->
<div class="lg:col-span-3 flex flex-col gap-gutter">
<!-- PANEL 4A: QUANT SIGNAL ENGINE & RISK GAUGES -->
<div class="bg-surface-container-lowest p-space-sm flex flex-col shadow-sm">
<div class="flex items-center justify-between pb-space-xs bg-surface-container-low px-space-sm py-1">
<div class="flex items-center gap-space-xs">
<span class="material-symbols-outlined text-[16px] text-tertiary-fixed-dim">bolt</span>
<span class="font-label-caps text-label-caps uppercase text-on-surface font-semibold">Python Signal Engine</span>
</div>
<span class="font-label-caps text-label-caps text-on-surface-variant">JIT v4.2.0</span>
</div>
<!-- Portfolio VaR Metric Card -->
<div class="mt-space-sm bg-surface-container p-space-sm rounded flex items-center justify-between">
<div class="flex flex-col">
<span class="font-label-caps text-label-caps text-on-surface-variant">1-DAY 99% VaR (PARAMETRIC)</span>
<span class="font-tabular-md text-tabular-md text-on-surface font-bold">$184,200 <span class="text-primary-container text-tabular-xs font-normal">(2.41% NAV)</span></span>
<span class="font-label-caps text-label-caps text-primary-container mt-0.5">STATUS: SAFE REGIME</span>
</div>
<div class="w-12 h-12 relative flex items-center justify-center">
<svg class="w-full h-full -rotate-90" viewbox="0 0 36 36">
<path class="text-surface-container-highest" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="currentColor" stroke-width="3"></path>
<path class="text-primary-container" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="currentColor" stroke-dasharray="24, 100" stroke-linecap="round" stroke-width="3"></path>
</svg>
<span class="absolute font-tabular-xs text-tabular-xs font-bold text-on-surface">2.4%</span>
</div>
</div>
<!-- Active Quantitative Signals -->
<div class="flex flex-col gap-1 mt-space-sm">
<!-- Signal 1 -->
<div class="flex items-center justify-between bg-surface-container-low px-space-sm py-1 rounded">
<div class="flex flex-col">
<span class="font-label-caps text-label-caps text-on-surface">Momentum Breakout (H1)</span>
<span class="font-tabular-xs text-tabular-xs text-on-surface-variant">Target: $96,200 · Stop: $93,900</span>
</div>
<div class="flex flex-col items-end">
<span class="font-label-caps text-label-caps px-space-xs py-0.5 bg-primary-container text-on-primary font-bold rounded">BUY 89.4%</span>
</div>
</div>
<!-- Signal 2 -->
<div class="flex items-center justify-between bg-surface-container-low px-space-sm py-1 rounded">
<div class="flex flex-col">
<span class="font-label-caps text-label-caps text-on-surface">Order Flow Delta (S30)</span>
<span class="font-tabular-xs text-tabular-xs text-on-surface-variant">Delta: +412.8 BTC · CVD Spike</span>
</div>
<div class="flex flex-col items-end">
<span class="font-label-caps text-label-caps px-space-xs py-0.5 bg-primary-container text-on-primary font-bold rounded">AGGRESSIVE</span>
</div>
</div>
<!-- Signal 3 -->
<div class="flex items-center justify-between bg-surface-container-low px-space-sm py-1 rounded">
<div class="flex flex-col">
<span class="font-label-caps text-label-caps text-on-surface">Perp-Spot Basis Arbitrage</span>
<span class="font-tabular-xs text-tabular-xs text-on-surface-variant">Basis: +14.2 bps · Low Variance</span>
</div>
<div class="flex flex-col items-end">
<span class="font-label-caps text-label-caps px-space-xs py-0.5 bg-tertiary-fixed-dim text-on-tertiary font-bold rounded">SPREAD LONG</span>
</div>
</div>
</div>
<!-- Quant Metrics Grid -->
<div class="grid grid-cols-3 gap-1 mt-space-sm font-tabular-xs text-tabular-xs">
<div class="bg-surface-container p-1 rounded flex flex-col text-center">
<span class="font-label-caps text-label-caps text-on-surface-variant">SHARPE</span>
<span class="text-primary-container font-bold">3.42</span>
</div>
<div class="bg-surface-container p-1 rounded flex flex-col text-center">
<span class="font-label-caps text-label-caps text-on-surface-variant">SORTINO</span>
<span class="text-primary-container font-bold">4.88</span>
</div>
<div class="bg-surface-container p-1 rounded flex flex-col text-center">
<span class="font-label-caps text-label-caps text-on-surface-variant">MAX DD</span>
<span class="text-secondary-fixed-dim font-bold">-4.12%</span>
</div>
</div>
</div>
<!-- PANEL 4B: AI RESEARCH COPILOT -->
<div class="bg-surface-container-lowest p-space-sm flex flex-col flex-1 shadow-sm">
<div class="flex items-center justify-between pb-space-xs bg-surface-container-low px-space-sm py-1">
<div class="flex items-center gap-space-xs">
<span class="material-symbols-outlined text-[16px] text-tertiary-fixed-dim">smart_toy</span>
<span class="font-label-caps text-label-caps uppercase text-on-surface font-semibold">Quant Copilot v2.4</span>
</div>
<span class="font-label-caps text-label-caps px-1 bg-surface-container text-tertiary-fixed-dim rounded">LLAMA-3 70B · 48ms</span>
</div>
<!-- Copilot Interactive Chat Stream -->
<div class="flex flex-col gap-space-sm my-space-sm flex-1 font-body-sm text-body-sm overflow-hidden">
<div class="bg-surface-container p-space-sm rounded">
<div class="flex items-center gap-1 font-label-caps text-label-caps text-on-surface-variant mb-1">
<span class="material-symbols-outlined text-[12px]">account_circle</span>
<span>QUERY (DESK #04)</span>
</div>
<p class="text-on-surface text-tabular-xs font-tabular-xs">
              Order book imbalance and whale absorption signal for BTC perpetuals?
            </p>
</div>
<div class="bg-surface-container-low p-space-sm rounded">
<div class="flex items-center justify-between font-label-caps text-label-caps text-tertiary-fixed-dim mb-1">
<div class="flex items-center gap-1">
<span class="material-symbols-outlined text-[12px]">neurology</span>
<span>SYNTHESIS COMPLETE</span>
</div>
<span class="text-primary-container">+3.8σ BUY CVD</span>
</div>
<p class="text-on-surface-variant font-tabular-xs text-tabular-xs leading-relaxed">
              Binance L2 indicates Bid skew is <strong class="text-primary-container">+62.4%</strong> concentrated at $94,600-$94,750 (2,140 BTC wall). Engine detected whale absorption of 480 BTC at $94,780 via Iceberg execution in the last 4 minutes.
            </p>
<div class="mt-1.5 p-1 bg-surface-container rounded text-tabular-xs font-tabular-xs text-primary-container font-medium">
              Recommendation: Favorable R:R for momentum scalp; tight invalidation at $94,550.
            </div>
</div>
</div>
<!-- Quick AI Triggers -->
<div class="flex items-center gap-1 flex-wrap mb-space-xs">
<button class="font-label-caps text-label-caps px-1.5 py-0.5 bg-surface-container hover:bg-surface-container-high text-on-surface-variant hover:text-on-surface rounded transition-colors" type="button">Explain CVD</button>
<button class="font-label-caps text-label-caps px-1.5 py-0.5 bg-surface-container hover:bg-surface-container-high text-on-surface-variant hover:text-on-surface rounded transition-colors" type="button">Detect Spoofing</button>
<button class="font-label-caps text-label-caps px-1.5 py-0.5 bg-surface-container hover:bg-surface-container-high text-on-surface-variant hover:text-on-surface rounded transition-colors" type="button">Kelly Bet Size</button>
</div>
<!-- Chat Input Dock -->
<div class="flex items-center gap-space-xs bg-surface-container px-space-sm py-1 rounded">
<input class="bg-transparent font-tabular-xs text-tabular-xs text-on-surface placeholder:text-on-surface-variant outline-none w-full" placeholder="Send prompt to algorithmic co-pilot..." type="text"/>
<button class="text-primary-container hover:text-primary-fixed" type="button">
<span class="material-symbols-outlined text-[18px]">send</span>
</button>
</div>
</div>
</div>
</div>
<!-- BOTTOM FULL-WIDTH DOCKED TELEMETRY & ZERO-ALLOCATION SYSTEM HEALTH (Grafana Mini Console) -->
<div class="w-full bg-surface-container-lowest p-space-sm mt-gutter shadow-md">
<div class="flex items-center justify-between pb-space-xs px-space-sm bg-surface-container-low">
<div class="flex items-center gap-space-md">
<div class="flex items-center gap-space-xs">
<span class="w-2 h-2 bg-primary-container"></span>
<span class="font-label-caps text-label-caps uppercase text-on-surface font-semibold tracking-wider">Infrastructure Telemetry &amp; Zero-Allocation Hot Path</span>
</div>
<span class="font-label-caps text-label-caps text-on-surface-variant">3 NODES HEALTHY · 0 DROPPED PACKETS</span>
</div>
<div class="flex items-center gap-space-md font-tabular-xs text-tabular-xs text-on-surface-variant">
<span>SOLARFLARE EF_VI ACTIVE</span>
<span>KERNEL BYPASS ON</span>
<span class="text-primary-container">UPTIME 99.999%</span>
</div>
</div>
<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-5 gap-gutter p-gutter bg-surface-container-high">
<!-- Node 1: Kafka Engine -->
<div class="bg-surface-container-lowest p-space-sm flex flex-col justify-between">
<div class="flex items-center justify-between">
<span class="font-label-caps text-label-caps text-on-surface-variant">KAFKA CLUSTER</span>
<span class="font-label-caps text-label-caps text-primary-container font-bold">842.5k msg/s</span>
</div>
<!-- Sparkline representation -->
<div class="h-6 w-full my-1">
<svg class="w-full h-full" preserveaspectratio="none" viewbox="0 0 100 24">
<path d="M0,18 Q20,12 40,15 T80,8 L100,5" fill="none" stroke="#4cd7f6" stroke-width="1.5"></path>
</svg>
</div>
<div class="flex items-center justify-between font-tabular-xs text-tabular-xs text-on-surface-variant">
<span>Partitions: 64</span>
<span>Lag: 0</span>
</div>
</div>
<!-- Node 2: C++ Zero-Alloc SPSC -->
<div class="bg-surface-container-lowest p-space-sm flex flex-col justify-between">
<div class="flex items-center justify-between">
<span class="font-label-caps text-label-caps text-on-surface-variant">C++ SPSC QUEUES</span>
<span class="font-label-caps text-label-caps text-primary-container font-bold">LOCK-FREE</span>
</div>
<div class="my-1">
<div class="font-tabular-md text-tabular-md font-bold text-on-surface">1.8µs <span class="text-primary-container font-normal font-tabular-xs text-tabular-xs">P99 Latency</span></div>
</div>
<div class="flex items-center justify-between font-tabular-xs text-tabular-xs text-on-surface-variant">
<span>Max Jitter: 0.4µs</span>
<span>Heap: 0 B</span>
</div>
</div>
<!-- Node 3: Redis In-Memory State -->
<div class="bg-surface-container-lowest p-space-sm flex flex-col justify-between">
<div class="flex items-center justify-between">
<span class="font-label-caps text-label-caps text-on-surface-variant">REDIS PUB/SUB</span>
<span class="font-label-caps text-label-caps text-primary-container font-bold">100% HIT</span>
</div>
<div class="my-1">
<div class="font-tabular-md text-tabular-md font-bold text-on-surface">0.24ms <span class="text-tertiary-fixed-dim font-normal font-tabular-xs text-tabular-xs">RTT Core</span></div>
</div>
<div class="flex items-center justify-between font-tabular-xs text-tabular-xs text-on-surface-variant">
<span>Mem: 4.1GB / 32GB</span>
<span>Clients: 180</span>
</div>
</div>
<!-- Node 4: Solarflare FPGA NIC -->
<div class="bg-surface-container-lowest p-space-sm flex flex-col justify-between">
<div class="flex items-center justify-between">
<span class="font-label-caps text-label-caps text-on-surface-variant">SOLARFLARE NIC</span>
<span class="font-label-caps text-label-caps text-primary-container font-bold">OPENONLOAD</span>
</div>
<div class="my-1">
<div class="font-tabular-md text-tabular-md font-bold text-on-surface">0.000% <span class="text-primary-container font-normal font-tabular-xs text-tabular-xs">Drop Rate</span></div>
</div>
<div class="flex items-center justify-between font-tabular-xs text-tabular-xs text-on-surface-variant">
<span>SFP28: 25GbE</span>
<span>Tx: 18.2M pps</span>
</div>
</div>
<!-- Node 5: WS Broadcaster -->
<div class="bg-surface-container-lowest p-space-sm flex flex-col justify-between">
<div class="flex items-center justify-between">
<span class="font-label-caps text-label-caps text-on-surface-variant">WS BROADCAST</span>
<span class="font-label-caps text-label-caps text-primary-container font-bold">14,290 PEERS</span>
</div>
<div class="my-1">
<div class="font-tabular-md text-tabular-md font-bold text-on-surface">1.4 Gbps <span class="text-tertiary-fixed-dim font-normal font-tabular-xs text-tabular-xs">Egress</span></div>
</div>
<div class="flex items-center justify-between font-tabular-xs text-tabular-xs text-on-surface-variant">
<span>Backpressure: 0</span>
<span>SSL Offload</span>
</div>
</div>
</div>
</div>
</div>
"""

# Simple conversions for JSX
html = html.replace('class="', 'className="')
html = re.sub(r'<input([^>]*[^/])>', r'<input\1/>', html)
html = re.sub(r'<img([^>]*[^/])>', r'<img\1/>', html)
html = re.sub(r'<br>', r'<br/>', html)
html = re.sub(r'<hr>', r'<hr/>', html)
html = html.replace('viewbox', 'viewBox')
html = html.replace('stroke-width', 'strokeWidth')
html = html.replace('stroke-opacity', 'strokeOpacity')
html = html.replace('stroke-dasharray', 'strokeDasharray')
html = html.replace('stroke-linecap', 'strokeLinecap')
html = html.replace('stop-color', 'stopColor')
html = html.replace('stop-opacity', 'stopOpacity')
html = html.replace('preserveaspectratio', 'preserveAspectRatio')
html = html.replace('lineargradient', 'linearGradient')
html = html.replace('font-family', 'fontFamily')
html = html.replace('font-size', 'fontSize')
html = html.replace('font-weight', 'fontWeight')

# Style attribute fixes (e.g. style="width: 82%;")
html = re.sub(r'style="width:\s*(\d+(?:\.\d+)?)%;"', r'style={{ width: "\1%" }}', html)

with open('jsx_output.txt', 'w', encoding='utf-8') as f:
    f.write(html)
