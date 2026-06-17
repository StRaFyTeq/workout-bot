import asyncio
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Вставь сюда свой ТОКЕН из @BotFather
TOKEN = "8955221421:AAGQncSWAJBnKxnJ_rm9Z6B90ITxR_G9X0U"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Словарь с базой данных
exercises = {
    "Спина": ["Подтягивания", "Горизонтальная тяга", "Вертикальная тяга", "Становая тяга"],
    "Бицепс": ["Подъем штанги", "Молотки с гантелями"],
    "Грудь": ["Жим лежа", "Жим на наклонной", "Бабочка"],
    "Трицепс": ["Французский жим", "Разгибание на блоке", "Жим узким хватом"],
    "Ноги": ["Приседания", "Жим ногами", "Разгибания", "Сгибания"]
}

def get_keyboard():
    buttons = [[InlineKeyboardButton(text=m, callback_data=m)] for m in exercises.keys()]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Выбери мышцу:", reply_markup=get_keyboard())

@dp.callback_query(lambda c: c.data in exercises.keys())
async def show(callback: types.CallbackQuery):
    text = f"Упражнения на {callback.data}:\n" + "\n".join([f"- {e}" for e in exercises[callback.data]])
    await callback.message.answer(text)
    await callback.answer()

# Веб-заглушка для Render
async def handle(request): return web.Response(text="OK")

async def main():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.environ.get("PORT", 8080)))
    await site.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
