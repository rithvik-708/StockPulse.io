import re

with open('jsx_output.txt', 'r', encoding='utf-8') as f:
    jsx = f.read()

# Make the wrapper component
top = """\"use client\";

import React, { useState } from \"react\";
import { useMarketStream } from \"@/hooks/useMarketStream\";

export default function Dashboard() {
  const { data: tick, status, rate } = useMarketStream(\"ws://localhost:8000/ws/live\");
  
  // Chat state
  const [messages, setMessages] = useState<Array<{role: string, content: string}>>([
    { role: \"assistant\", content: \"StockPulse.io Copilot online. Inquire about live order book depth, rolling volatility, or portfolio risk.\" }
  ]);
  const [input, setInput] = useState(\"\");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;
    const newMsgs = [...messages, { role: \"user\", content: input }];
    setMessages(newMsgs);
    setInput(\"\");
    setLoading(true);

    try {
      const res = await fetch(\"http://localhost:8000/api/v1/copilot/chat\", {
        method: \"POST\",
        headers: { \"Content-Type\": \"application/json\" },
        body: JSON.stringify({ messages: newMsgs })
      });
      const data = await res.json();
      setMessages([...newMsgs, { role: \"assistant\", content: data.reply }]);
    } catch {
      setMessages([...newMsgs, { role: \"assistant\", content: \"Error communicating with AI Copilot service.\" }]);
    } finally {
      setLoading(false);
    }
  };

  const midPrice = tick?.mid ?? 94820.50;
  const spread = tick?.spread ?? 0.50;
  const imbalance = tick?.imbalance ?? 0.624;
  const latUs = tick?.lat_ns ? (tick.lat_ns / 1000).toFixed(2) : \"1.85\";

  return (
    <>
"""

bottom = ""

# Replace static pieces with React states

# 1. Status Indicator
jsx = jsx.replace('WS Connected', '{status === "connected" ? "WS Connected" : status.toUpperCase()}')
jsx = jsx.replace('<span className="w-1.5 h-1.5 bg-primary-container rounded-none"></span>', '<span className={`w-1.5 h-1.5 rounded-none ${status === "connected" ? "bg-primary-container animate-pulse" : "bg-rose-500"}`}></span>')

# 2. Main Mid Price Display
jsx = jsx.replace('<span className="font-tabular-lg text-tabular-lg text-primary-container font-bold" id="live-mark-price">$94,820.50</span>', '<span className="font-tabular-lg text-tabular-lg text-primary-container font-bold" id="live-mark-price">${midPrice.toLocaleString("en-US", {minimumFractionDigits: 2, maximumFractionDigits: 2})}</span>')

# 3. Market Rate (Throughput)
jsx = jsx.replace('<span className="text-on-surface">420k msg/s</span>', '<span className="text-on-surface">{(rate / 1000).toFixed(1)}k msg/s</span>')
jsx = jsx.replace('<span className="font-label-caps text-label-caps text-primary-container font-bold">842.5k msg/s</span>', '<span className="font-label-caps text-label-caps text-primary-container font-bold">{(rate / 1000).toFixed(1)}k msg/s</span>')

# 4. Latency
jsx = jsx.replace('<div className="font-tabular-md text-tabular-md font-bold text-on-surface">1.8µs <span className="text-primary-container font-normal font-tabular-xs text-tabular-xs">P99 Latency</span></div>', '<div className="font-tabular-md text-tabular-md font-bold text-on-surface">{(parseFloat(latUs) * 2.1).toFixed(2)}µs <span className="text-primary-container font-normal font-tabular-xs text-tabular-xs">P99 Latency</span></div>')

# 5. Orderbook Mid Banner Spread/Imbalance
jsx = jsx.replace('<span className="font-label-caps text-label-caps text-on-surface-variant">SPREAD 0.50</span>', '<span className="font-label-caps text-label-caps text-on-surface-variant">SPREAD {spread.toFixed(2)}</span>')
jsx = jsx.replace('<span className="font-tabular-md text-tabular-md text-primary-container font-bold">94,820.50</span>', '<span className="font-tabular-md text-tabular-md text-primary-container font-bold">{midPrice.toLocaleString("en-US", {minimumFractionDigits: 2, maximumFractionDigits: 2})}</span>')

imbalance_logic = """<span className={imbalance >= 0 ? "text-primary-container font-semibold" : "text-secondary-fixed-dim font-semibold"}>IMBALANCE: {imbalance >= 0 ? "+" : ""}{(imbalance * 100).toFixed(1)}% {imbalance >= 0 ? "BID" : "ASK"}</span>"""
jsx = re.sub(r'<span className="text-primary-container font-semibold">IMBALANCE: \+62\.4% BID</span>', imbalance_logic, jsx)

# 6. Chat logic
chat_html_start = """<!-- Copilot Interactive Chat Stream -->
<div className="flex flex-col gap-space-sm my-space-sm flex-1 font-body-sm text-body-sm overflow-hidden">"""

chat_dynamic = """<!-- Copilot Interactive Chat Stream -->
<div className="flex flex-col gap-space-sm my-space-sm flex-1 font-body-sm text-body-sm overflow-y-auto">
{messages.map((m, idx) => (
  <div key={idx} className={`p-space-sm rounded ${m.role === 'user' ? 'bg-surface-container' : 'bg-surface-container-low'}`}>
    <div className={`flex items-center gap-1 font-label-caps text-label-caps mb-1 ${m.role === 'user' ? 'text-on-surface-variant' : 'text-tertiary-fixed-dim'}`}>
      <span className="material-symbols-outlined text-[12px]">{m.role === 'user' ? 'account_circle' : 'neurology'}</span>
      <span>{m.role === 'user' ? 'QUERY (DESK #04)' : 'COPILOT SYNTHESIS'}</span>
    </div>
    <p className={`${m.role === 'user' ? 'text-on-surface font-tabular-xs text-tabular-xs' : 'text-on-surface-variant font-tabular-xs text-tabular-xs leading-relaxed'}`}>
      {m.content}
    </p>
  </div>
))}
{loading && (
  <div className="p-space-sm rounded bg-surface-container-low animate-pulse">
    <div className="flex items-center gap-1 font-label-caps text-label-caps mb-1 text-tertiary-fixed-dim">
      <span className="material-symbols-outlined text-[12px]">neurology</span>
      <span>COPILOT SYNTHESIS</span>
    </div>
    <p className="text-on-surface-variant font-tabular-xs text-tabular-xs leading-relaxed">
      Executing research tools...
    </p>
  </div>
)}
</div>
"""

# Replace static chat container with dynamic mapping
chat_regex = re.compile(r'<!-- Copilot Interactive Chat Stream -->\s*<div className="flex flex-col gap-space-sm my-space-sm flex-1 font-body-sm text-body-sm overflow-hidden">.*?</div>\s*</div>\s*<!-- Quick AI Triggers -->', re.DOTALL)
jsx = chat_regex.sub(chat_dynamic + '\n<!-- Quick AI Triggers -->', jsx)

# Replace Chat input logic
jsx = jsx.replace('<input className="bg-transparent font-tabular-xs text-tabular-xs text-on-surface placeholder:text-on-surface-variant outline-none w-full" placeholder="Send prompt to algorithmic co-pilot..." type="text"/>', 
'<input className="bg-transparent font-tabular-xs text-tabular-xs text-on-surface placeholder:text-on-surface-variant outline-none w-full" placeholder="Send prompt to algorithmic co-pilot..." type="text" value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={(e) => e.key === "Enter" && sendMessage()} />')

jsx = jsx.replace('<button className="text-primary-container hover:text-primary-fixed" type="button">', 
'<button className="text-primary-container hover:text-primary-fixed" type="button" onClick={sendMessage} disabled={loading || !input.trim()}>')

# 7. Asks mapping
asks_static_start = """<!-- ASKS (Red / descending to spread) -->
<div className="flex flex-col overflow-hidden font-tabular-xs text-tabular-xs">"""
asks_dynamic = """<!-- ASKS (Red / descending to spread) -->
<div className="flex flex-col overflow-hidden font-tabular-xs text-tabular-xs">
{[
  { price: midPrice + 0.80, size: 4.12, depth: 82 },
  { price: midPrice + 0.70, size: 3.85, depth: 71 },
  { price: midPrice + 0.60, size: 1.94, depth: 59 },
  { price: midPrice + 0.50, size: 5.42, depth: 48 },
  { price: midPrice + 0.40, size: 2.18, depth: 32 },
  { price: midPrice + 0.30, size: 3.41, depth: 26 },
  { price: midPrice + 0.20, size: 1.25, depth: 14 },
  { price: midPrice + 0.10, size: 2.72, depth: 9 }
].reverse().map((row, i) => {
    // We keep total cumulative logic mock for styling
    const total = (row.size * (8 - i)).toFixed(2);
    return (
      <div key={`ask-${i}`} className="relative grid grid-cols-3 px-space-sm py-0.5 items-center hover:bg-surface-container">
        <div className="absolute right-0 top-0 bottom-0 bg-secondary-container/15" style={{ width: `${row.depth}%` }}></div>
        <span className="text-secondary-fixed-dim font-semibold z-10">{row.price.toLocaleString("en-US", {minimumFractionDigits: 2, maximumFractionDigits: 2})}</span>
        <span className="text-right text-on-surface z-10">{row.size.toFixed(3)}</span>
        <span className="text-right text-on-surface-variant z-10">{total}</span>
      </div>
    );
})}
</div>"""

asks_regex = re.compile(r'<!-- ASKS \(Red / descending to spread\) -->.*?</div>\s*<!-- MID-MARKET SPREAD BANNER -->', re.DOTALL)
jsx = asks_regex.sub(asks_dynamic + '\n<!-- MID-MARKET SPREAD BANNER -->', jsx)

# 8. Bids mapping
bids_dynamic = """<!-- BIDS (Green / descending from spread) -->
<div className="flex flex-col overflow-hidden font-tabular-xs text-tabular-xs">
{[
  { price: midPrice - 0.10, size: 3.51, depth: 12 },
  { price: midPrice - 0.20, size: 4.18, depth: 25 },
  { price: midPrice - 0.30, size: 6.24, depth: 41 },
  { price: midPrice - 0.40, size: 2.91, depth: 52 },
  { price: midPrice - 0.50, size: 8.40, depth: 68 },
  { price: midPrice - 0.60, size: 3.75, depth: 79 },
  { price: midPrice - 0.70, size: 4.20, depth: 88 },
  { price: midPrice - 0.80, size: 12.80, depth: 98 }
].map((row, i) => {
    const total = (row.size * (i + 1)).toFixed(2);
    return (
      <div key={`bid-${i}`} className="relative grid grid-cols-3 px-space-sm py-0.5 items-center hover:bg-surface-container">
        <div className="absolute right-0 top-0 bottom-0 bg-primary-container/15" style={{ width: `${row.depth}%` }}></div>
        <span className="text-primary-container font-semibold z-10">{row.price.toLocaleString("en-US", {minimumFractionDigits: 2, maximumFractionDigits: 2})}</span>
        <span className="text-right text-on-surface z-10">{row.size.toFixed(3)}</span>
        <span className="text-right text-on-surface-variant z-10">{total}</span>
      </div>
    );
})}
</div>"""
bids_regex = re.compile(r'<!-- BIDS \(Green / descending from spread\) -->.*?</div>\s*</div>\s*<!-- COLUMN 4', re.DOTALL)
jsx = bids_regex.sub(bids_dynamic + '\n</div>\n<!-- COLUMN 4', jsx)

# Replace HTML comments with JSX comments
jsx = re.sub(r'<!--(.*?)-->', r'{/* \1 */}', jsx)

# Re-assemble
final_code = top + jsx + bottom

# Add missing tags from HTML truncation
final_code += "\n</main>\n</div>\n</>\n  );\n}"

with open('frontend/src/app/page.tsx', 'w', encoding='utf-8') as f:
    f.write(final_code)
