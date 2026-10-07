import json
import os
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import redis.asyncio as redis
from analytics.risk import calculate_portfolio_exposure, calculate_historical_var
from ai.copilot import run_copilot

app = FastAPI(title="Stock Pulse API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True
)

# Mock portfolio for risk calculations
MOCK_PORTFOLIO = {"BTCUSDT": 1.5, "ETHUSDT": 10.0}

@app.get("/api/v1/orderbook/{symbol}")
async def get_orderbook(symbol: str):
    data = await redis_client.get(f"market:l1:{symbol}")
    return json.loads(data) if data else {"error": "No data available"}

@app.get("/api/v1/features/{symbol}")
async def get_features(symbol: str):
    data = await redis_client.get(f"market:features:{symbol}")
    return json.loads(data) if data else {"error": "No data available"}

@app.get("/api/v1/risk")
async def get_risk():
    # Fetch latest prices for exposure calculation
    prices = {}
    for symbol in MOCK_PORTFOLIO.keys():
        data = await redis_client.get(f"market:l1:{symbol}")
        if data:
            prices[symbol] = json.loads(data).get("mid", 0.0)
            
    exposure_metrics = calculate_portfolio_exposure(MOCK_PORTFOLIO, prices)
    
    # Mock historical returns array for VaR
    mock_returns = [-0.01, 0.02, -0.005, -0.03, 0.015, -0.02] 
    var_95 = calculate_historical_var(mock_returns)
    
    return {
        "exposure": exposure_metrics,
        "var_95_pct": var_95 * 100,
        "leverage": 1.2 # Mocked
    }

@app.websocket("/ws/live")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    pubsub = redis_client.pubsub()

    try:
        await pubsub.subscribe("market_updates")
    except Exception:
        # Redis not available — keep connection alive with heartbeats only
        try:
            while True:
                await websocket.send_json({"type": "heartbeat", "status": "waiting_for_data"})
                await asyncio.sleep(5)
        except WebSocketDisconnect:
            return

    async def receive_loop():
        try:
            while True:
                await websocket.receive()
        except WebSocketDisconnect:
            pass

    async def send_loop():
        try:
            while True:
                try:
                    message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=5.0)
                    if message and message.get("type") == "message":
                        data = message["data"]
                        if not isinstance(data, str):
                            data = str(data)
                        await websocket.send_text(data)
                    elif not message:
                        # No data yet — send a heartbeat to keep the connection alive
                        await websocket.send_json({"type": "heartbeat", "status": "no_data"})
                except asyncio.TimeoutError:
                    await websocket.send_json({"type": "heartbeat", "status": "no_data"})
                except Exception:
                    await asyncio.sleep(1)
                await asyncio.sleep(0.01)
        except WebSocketDisconnect:
            pass

    recv_task = asyncio.create_task(receive_loop())
    send_task = asyncio.create_task(send_loop())
    
    try:
        done, pending = await asyncio.wait(
            [recv_task, send_task],
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()
    finally:
        try:
            await pubsub.unsubscribe("market_updates")
        except Exception:
            pass

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

@app.post("/api/v1/copilot/chat")
async def copilot_chat(request: ChatRequest):
    formatted = [{"role": m.role, "content": m.content} for m in request.messages]
    reply = await run_copilot(formatted)
    return {"reply": reply}
