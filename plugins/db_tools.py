from pyrogram import Client, filters
from database.users_chats_db import db


@Client.on_message(filters.command("dbclean"))
async def db_clean(client, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:**\n"
            "/dbclean users\n"
            "/dbclean premium\n"
            "/dbclean thumbs\n"
            "/dbclean prefixes\n"
            "/dbclean suffixes\n"
            "/dbclean all"
        )

    target = message.command[1].lower()

    msg = await message.reply_text("🧹 Cleaning database...")

    try:

        collections = await db.list_collection_names()

        if target == "all":
            for col in collections:
                await db[col].delete_many({})
            await msg.edit("✅ Database fully cleaned!")
            return

        if target in collections:
            await db[target].delete_many({})
            await msg.edit(f"✅ `{target}` cleaned successfully!")
        else:
            await msg.edit("❌ Collection not found.")

    except Exception as e:
        await msg.edit(f"❌ Error:\n{e}")


@Client.on_message(filters.command("dbstats"))
async def db_stats(client, message):

    msg = await message.reply_text("📊 Checking database...")

    try:
        collections = await db.list_collection_names()

        text = "**MongoDB Stats**\n\n"

        for col in collections:
            count = await db[col].count_documents({})
            text += f"{col} : {count}\n"

        await msg.edit(text)

    except Exception as e:
        await msg.edit(f"❌ Error:\n{e}")
