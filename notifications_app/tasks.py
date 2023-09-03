
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import asyncio

def broadcast_notification(data):
    print(data)
    from notifications_app.models import BroadcastNotification
    notification = BroadcastNotification.objects.filter(id = int(data))
    if len(notification)>0:
        notification = notification.first()
        channel_layer = get_channel_layer()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(channel_layer.group_send(
            "notification_broadcast",
            {
                'type': 'send_notification',
                'message': json.dumps(notification.message),
            }))
        notification.sent = True
        notification.save()
        return 'Done'