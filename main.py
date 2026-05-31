import os
import datetime
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
import asyncio
import sys

sys.path.append('config.py')
import config

load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
history = config.history
limit = config.limit
# catch_up = 0 # TODO
sleep_time = config.sleep_time
destination = config.destination
channels = config.channels
session  = config.session

client = TelegramClient(session, api_id, api_hash)

def load_history():
    stored_keys = set()
    if os.path.exists(history):
        with open(history, "r", encoding="utf-8") as hf:
            for line in hf:
                clean_line = line.strip()
                if clean_line:
                    stored_keys.add(clean_line)
    print(f"Loaded {len(stored_keys)} lines of history \n")
    return stored_keys

def save_history(msgs_keys):
    with open(history, "a", encoding="utf-8") as hf:
        hf.write(f"{msgs_keys}\n")

async def get_last_msg(channels):
    if str(channels).strip() == "@":
        return None
    try:
        msgs = []
        async for msg in client.iter_messages(channels, limit=limit):
            msgs.append(msg)
        return msgs
    except Exception as e:
        print(f"Error: {e}")
        return None

async def forward_msg(msg, dest, reply_to=None):
    try:
        if not msg:
            print(msg)
            return None

        dest_entity = await client.get_entity(dest)

        # HACK: Its a very weird way to write like that
        if msg.reply_to_msg_id:
            original_msg = await client.get_messages(msg.chat_id, ids=msg.reply_to_msg_id)

            forwarded_original = await client.forward_messages(
                entity    = dest_entity,
                messages  = msg.id,
                from_peer = msg.chat_id
            )
            if isinstance(forwarded_original, list):
                forwarded_original = forwarded_original[0]

            forwarded = await client.send_message(
                entity   = dest_entity,
                message  = msg.message,
                reply_to = forwarded_original.id,
                file     = msg.media if msg.media else None
            )
        else:
            forwarded = await client.forward_messages(
                entity    = dest_entity,
                messages  = msg.id,
                from_peer = msg.chat_id
            )
        print(f"Forwarded from: {msg.chat.title} | {msg.chat.username}")
        await asyncio.sleep(sleep_time)
        return forwarded
    except Exception as e:
        print(f"Error: {e}")
        return None

async def main():
    print(f"Start monitoring {len(channels)} channels\n")

    current_msgs_keys = load_history()
    while True:
        try:
            current_msg_date = datetime.datetime.now(datetime.timezone.utc).strftime('%Y:%m:%d')
            tasks = [get_last_msg(channel) for channel in channels]
            results = await asyncio.gather(*tasks)

            new_msgs = []
            for result in results:
                if isinstance(result, list):
                    for msg in result:
                        if msg is not None:
                            new_msgs.append(msg)

            for new_msg in new_msgs:
                if new_msg:
                    new_msgs_key = f"{new_msg.chat_id}_{new_msg.id}"
                    if new_msg.date.strftime('%Y:%m:%d') == current_msg_date and new_msgs_key not in current_msgs_keys:
                        await forward_msg(new_msg, destination)
                        current_msgs_keys.add(new_msgs_key)
                        save_history(new_msgs_key)
                    # else:
                    #     print("Monitoring...\n")
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(5)
            continue

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
