import asyncio
import os
from aiohttp import web  # Импортируем веб-сервер
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8955221421:AAGQncSWAJBnKxnJ_rm9Z6B90ITxR_G9X0U"

bot = Bot(token=TOKEN)
dp = Dispatcher()

exercises = {
    "спина": ["Подтягивания", "Горизонталья тяга", "Вертикальная тяга", "Становая тяга"],
    "бицепс": ["Подъем штанги на бицепс (EZ - гриф предпочтителен)", "Молотки с гантелями"],
    "грудь": ["Жим лежа", "Жим гантелй на наклонной скамье", "Бабочка"],
    "трицепс": ["Французский жим", "Разгибание рук на блоке", "Жим узким хватом"],
    "ноги": ["Приседания со штангой", "Жим ногами", "Разгибания ног", "Сгибания ног"]
}

def get_muscle_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Спина", callback_data="спина")],
        [InlineKeyboardButton(text="Бицепс", callback_data="бицепс")],
        [InlineKeyboardButton(text="Грудь", callback_data="грудь")],
        [InlineKeyboardButton(text="Трицепс", callback_data="трицепс")],
        [InlineKeyboardButton(text="Ноги", callback_data="ноги")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Выбери группу мышц для тренировки:", reply_markup=get_muscle_keyboard())

@dp.callback_query(F.data.in_(exercises.keys()))
async def show_exercises(callback: types.CallbackQuery):
    muscle = callback.data
    ex_list = "\n".join([f"- {ex}" for ex in exercises[muscle]])
    await callback.message.answer(f"Упражнения на {muscle}:\n\n{ex_list}")
    await callback.answer()

# --- ХИТРОСТЬ ДЛЯ RENDER ---
# Эта функция создает пустую веб-страницу, чтобы Render видел, что бот "жив"
async def handle_root(request):
    return web.Response(text="Бот запущен и работает 24/7!")

async def start_dummy_server():
    app = web.Application()
    app.router.add_get('/', handle_root)
    runner = web.AppRunner(app)
    await runner.setup()
    # Render сам передает нужный ему порт в переменную окружения PORT
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    await start_dummy_server() # Сначала запускаем веб-заглушку
    print("Бот запущен и готов к работе...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
