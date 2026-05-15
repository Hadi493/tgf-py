import os
import datetime
from dotenv import load_dotenv
from telethon import utils
from telethon.sync import TelegramClient, events
from telethon.tl.functions.messages import GetHistoryRequest
import asyncio

load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
sleep_time = 0
destination = 'yourDestinationChanneORID'
channels = [
    "@channel1",
    "@channel2",
    "@channel3"
]

client = TelegramClient('session-name', api_id, api_hash)

async def get_last_msg(channels):
    try:
        msgs = []
        for channel in channels:
            async for msg in client.iter_messages(channel, limit=1):
                msgs.append(msg)
                print(msgs)
        return msgs

    except Exception as e:
        print(f"Error: {e}")
        return None

async def forward_msg(msg, dest):
    try:
        if not msg:
            print(msg)
            return None

        dest_entity = await client.get_entity(dest)
        forwarded = await client.forward_messages(
            entity = dest_entity,
            messages = msg.id,
            from_peer = msg.chat_id
        )
        print(f"Msg forwarded from: {msg.id}")
        return forwarded
    except Exception as e:
        print(f"Error: {e}")
        return None

async def main():
    print("Starting....")

    current_msg_ids = []
    current_msg_date = datetime.datetime.now(datetime.timezone.utc).strftime('%Y:%m:%d %H:%M')
    while True:
        try:
            new_msgs = await get_last_msg(channels)
            for new_msg in new_msgs:
                print(new_msg)
                if new_msg:
                    print(f"[{datetime.datetime.now(datetime.timezone.utc).strftime('%Y:%m:%d %H:%M')}]: Latest msg Date: {new_msg.date.strftime('%Y:%m:%d %H:%M')}\n")
                    if new_msg.date.strftime('%Y:%m:%d %H:%M') in current_msg_date and new_msg.id not in current_msg_ids:
                        print(f"New updated msg\n")
                        print(f"   Text: {new_msg.text[:80] if new_msg.text else 'No text'}...\n")
                        await forward_msg(new_msg, destination)
                        current_msg_ids.append(new_msg.id)
                    else:
                        print("No new msg detected\n")
                await asyncio.sleep(sleep_time)
        except Exception as e:
            print(f"Error: {e}")
            return None

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
        client.run_until_disconnected()
