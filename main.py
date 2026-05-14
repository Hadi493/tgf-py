import os
import datetime
from dotenv import load_dotenv
from telethon import utils
from telethon.sync import TelegramClient, events
from telethon.tl.functions.messages import GetHistoryRequest

load_dotenv()

api_id = os.getenv('API_ID')
import asyncio
api_hash = os.getenv('API_HASH')

client = TelegramClient('cyber-green', api_id, api_hash)

async def get_last_msg(channel_name):
    try:
        entity = await client.get_entity(channel_name)
        async for msg in client.iter_messages(entity, limit=1):
            return msg
    except Exception as e:
        print(f"Error: {e}")
        return None

async def forward_msg(msg, dest):
    try:
        if not msg:
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
    current_msg_id = None

    while True:
        try:
            new_msg = await get_last_msg({"@CyberGreenNews")

            if new_msg:
                print(f"[{datetime.datetime.now()}] Latest msg ID: {new_msg.id}")

                if new_msg.id != current_msg_id:
                    print(f"New msg detected")
                    print(f"   Text: {new_msg.text[:80] if new_msg.text else 'No text'}...")

                    await forward_msg(new_msg, 'me')

                    current_msg_id = new_msg.id

                else:
                    print("No new msg detected")

            await asyncio.sleep(5)

        except Exception as e:
            print(f"Error: {e}")
            return None


if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
        client.run_until_disconnected()
