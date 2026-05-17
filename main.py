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
history = 'history.txt'
sleep_time = 10
destination = 'me'
channels = [
    "@channel1",
    "@channel2",
    "@channel3"
]

client = TelegramClient('session-name', api_id, api_hash)

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
        async for msg in client.iter_messages(channels, limit=5):
            msgs.append(msg)
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
        print(f"Forwarded msg ID: {msg.id}")
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
            await asyncio.sleep(sleep_time)
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(5)
            return None

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
