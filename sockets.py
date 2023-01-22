import json
import socketio
from utils import config
from utils.utils import generate_short_id
from datetime import datetime
from db import db
from serializers import message_serializer


mgr = socketio.AsyncRedisManager(config.REDIS_URL)
sio = socketio.AsyncServer(
    async_mode="asgi", client_manager=mgr, cors_allowed_origins="*"
)

# establishes a connection with the client
@sio.on("connect")
async def connect(sid, env, auth):
    if auth:
        room_id = auth["room_id"]
        print("SocketIO connect")
        sio.enter_room(sid, room_id)
        await sio.emit("connect", f"Connected as {sid}")
    else:
        raise ConnectionRefusedError("no auth token")


@sio.on("message")
async def print_message(sid, data):
    print("Socket ID", sid)
    data = json.loads(data)
    room_id = data["room_id"]
    # room = await Room.objects.aget(id=room_id)
    # print(room)
    message_data = {
        "sender_id": data["sender_id"],
        "sender_name": data["sender_name"],
        "message": data["message"],
        "timestamp": datetime.utcnow(),
        "short_id": generate_short_id(),
        "room_id": room_id,
    }
    db.messages.insert_one(message_data)
    message = message_serializer(
        db.messages.find_one({"short_id": message_data["short_id"]})
    )
    await sio.emit("new_message", message, room=room_id)


@sio.on("disconnect")
async def disconnect(sid):
    print("SocketIO disconnect")


# extra events
@sio.on("left")
async def left_room(sid, data):
    sio.leave_room(sid, "feed")
    await sio.emit("user_left", f"{data} left", room="world")
    print(f"{sid} Left")


@sio.on("joined")
async def joined(sid, data):
    await sio.emit("user_joined", f"{data} connected", room="world")
    print(f"{data} Connected")
