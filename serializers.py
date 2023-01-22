
def message_serializer(a) -> dict:
    return {
        "id": str(a["_id"]),
        "sender_id": a["sender_id"],
        "sender_name": a["sender_name"],
        "message": a["message"],
        "timestamp": (a["timestamp"]).strftime("%a. %I:%M %p"),
        "short_id": a["short_id"],
        "room_id": a["room_id"],
    }
