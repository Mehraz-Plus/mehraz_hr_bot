from telethon import TelegramClient, events
from telethon.tl.types import PeerUser
from env import env
import helper
from mongo import Mongo
import polib
import os

# Environment detection
if env == 'live':
    import config_live
    config = config_live
elif env == 'dev':
    import config_dev
    config = config_dev
else:
    import config_test
    config = config_test

# Load message file
msg = {}
for entry in polib.pofile('msg_' + config.language + '.po'):
    msg[entry.msgid] = entry.msgstr

# Connect to database
db = Mongo(config.db_host, config.db_port, config.db_name)

# Initialize Telegram client
if config.proxy:
    bot = TelegramClient(session=config.session_name, api_id=config.api_id, api_hash=config.api_hash,
                         proxy=(config.proxy_protocol, config.proxy_host, config.proxy_port))
else:
    bot = TelegramClient(session=config.session_name, api_id=config.api_id, api_hash=config.api_hash)


@bot.on(events.NewMessage(pattern='/start', incoming=True))
async def start(event):
    welcome_msg = f"{msg.get('welcome')}.\n\n{msg.get('info')}.\n"
    welcome_buttons = helper.get_start_buttons(msg, config)
    await event.respond(welcome_msg, buttons=welcome_buttons)
    raise events.StopPropagation


@bot.on(events.NewMessage(incoming=True))
async def forward_to_admin(event):
    try:
        for admin in config.admin_list:
            await bot.forward_messages(admin, event.message)
        await event.respond(f"{msg.get('thanks')}! {msg.get('sent_successfully')}.")
    except Exception as e:
        print(f"Failed to forward message: {e}")
    raise events.StopPropagation





# Connect to Telegram and run in a loop
try:
    print('bot starting...')
    bot.start(bot_token=config.bot_token)
    print('bot started')
    bot.run_until_disconnected()
finally:
    print('never runs in async mode!')