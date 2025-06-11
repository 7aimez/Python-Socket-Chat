import asyncio
import websockets
import json

clients = {}
last_messages = []

async def handler(websocket, path):
    nickname = None
    try:
        async for message in websocket:
            data = json.loads(message)
            if data["type"] == "nickname":
                nickname = data["data"]
                clients[websocket] = nickname
                # Send last messages to new client
                for msg in last_messages:
                    await websocket.send(msg)
                join_msg = f"👋 {nickname} joined the chat."
                formatted = f"\n------------------------------\n{join_msg}\n------------------------------\n"
                last_messages.append(formatted)
                if len(last_messages) > 10:
                    last_messages.pop(0)
                for client in clients:
                    await client.send(formatted)
            elif data["type"] == "message":
                chat_msg = f"{nickname}: {data['data']}"
                formatted = f"\n------------------------------\n{chat_msg}\n------------------------------\n"
                last_messages.append(formatted)
                if len(last_messages) > 10:
                    last_messages.pop(0)
                for client in clients:
                    await client.send(formatted)
    finally:
        if nickname:
            leave_msg = f"💨 {nickname} left the chat."
            formatted = f"\n------------------------------\n{leave_msg}\n------------------------------\n"
            last_messages.append(formatted)
            if len(last_messages) > 10:
                last_messages.pop(0)
            for client in clients:
                await client.send(formatted)
        if websocket in clients:
            del clients[websocket]

start_server = websockets.serve(handler, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()