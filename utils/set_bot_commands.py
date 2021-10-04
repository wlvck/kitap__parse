from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Ботты іске қосу"),
            types.BotCommand("kitap", "Кітаптар каталогын көрсету"),
            types.BotCommand('about', "Жоба туралы"),
        ]
    )
