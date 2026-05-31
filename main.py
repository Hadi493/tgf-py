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

async def forward_msg(msg, dest):
    try:
        if not msg:
            return None
        dest_entity = await client.get_entity(dest)
        forwarded = await client.forward_messages(
            entity=dest_entity, messages=msg.id, from_peer=msg.chat_id
        )
        print(f"Forwarded from: {msg.chat.title} | {msg.chat.username}")
        await asyncio.sleep(sleep_time)
        return forwarded
    except Exception as e:
        print(f"Error: {e}")
        return None


async def forward_album(msgs, dest):
    try:
        if not msgs:
            return None
        dest_entity = await client.get_entity(dest)
        msg_ids = [m.id for m in msgs]
        chat_id = msgs[0].chat_id
        forwarded = await client.forward_messages(
            entity=dest_entity, messages=msg_ids, from_peer=chat_id
        )
        print(f"Forwarded album ({len(msgs)} media) from: {msgs[0].chat.title} | {msgs[0].chat.username}")
        await asyncio.sleep(sleep_time)
        return forwarded
    except Exception as e:
        print(f"Error forwarding album: {e}")
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

            albums = {}
            standalone = []
            for new_msg in new_msgs:
                if not new_msg:
                    continue
                key = f"{new_msg.chat_id}_{new_msg.id}"
                if new_msg.date.strftime('%Y:%m:%d') != current_msg_date or key in current_msgs_keys:
                    continue
                if new_msg.grouped_id:
                    albums.setdefault((new_msg.chat_id, new_msg.grouped_id), []).append(new_msg)
                else:
                    standalone.append(new_msg)

            for group in albums.values():
                await forward_album(group, destination)
                for msg in group:
                    k = f"{msg.chat_id}_{msg.id}"
                    current_msgs_keys.add(k)
                    save_history(k)

            for new_msg in standalone:
                await forward_msg(new_msg, destination)
                k = f"{new_msg.chat_id}_{new_msg.id}"
                current_msgs_keys.add(k)
                save_history(k)
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(5)
            continue

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
