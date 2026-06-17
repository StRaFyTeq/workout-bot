import asyncio
import os
import logging
from aiohttp import web  # Импортируем веб-сервер
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Включаем логирование, чтобы в Render было видно каждую ошибку
logging.basicConfig(level=logging.INFO)

# Твой рабочий токен бота
TOKEN = "8955221421:AAGQncSWAJBnKxnJ_rm9Z6B90ITxR_G9X0U"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Словарь с упражнениями и анатомическими акцентами
exercises = {
    "Спина": [
        {"name": "Подтягивания", "target": "Широчайшие мышцы (работа в ширину, верхний отдел) и большая круглая мышца"},
        {"name": "Горизонтальная тяга", "target": "Толщина спины, ромбовидные мышцы, середина и низ трапециевидных"},
        {"name": "Вертикальная тяга", "target": "Верхний и наружный отделы широчайших (формирование V-силуэта)"},
        {"name": "Становая тяга", "target": "Вся задняя мышечная цепь: разгибатели спины, ягодичные и бицепс бедра"}
    ],
    "Бицепс": [
        {"name": "Подъем штанги на бицепс (EZ-гриф)", "target": "Обе головки бицепса (общая масса) + плечевая мышца (брахиалис)"},
        {"name": "Молотки с гантелями", "target": "Плечелучевая мышца (предплечье) и брахиалис (выталкивает бицепс наружу, давая пик)"}
    ],
    "Грудь": [
        {"name": "Жим лежа", "target": "Средний и нижний отделы большой грудной мышцы, трицепс, передняя дельта"},
        {"name": "Жим гантелей на наклонной скамье", "target": "Верхний отдел грудных мышц (ключичная порция), передняя дельта"},
        {"name": "Бабочка", "target": "Внутренний край и отчетливое сведение большой грудной мышцы (изолированная проработка)"}
    ],
    "Трицепс": [
        {"name": "Французский жим", "target": "Длинная головка трицепса (задает основной объем руки сзади при взгляде сбоку)"},
        {"name": "Разгибание рук на блоке", "target": "Латеральная (внешняя) и медиальная головки трицепса (формирование подковы)"},
        {"name": "Жим узким хватом", "target": "Внутренняя и латеральная головки трицепса, передняя дельта, общая масса рук"}
    ],
    "Ноги": [
        {"name": "Приседания со штангой", "target": "Квадрицепсы (все четыре головки), ягодичные мышцы, приводящие мышцы бедра"},
        {"name": "Жим ногами", "target": "Квадрицепсы (при узкой постановке) или ягодицы и бицепс бедра (при высокой постановке ног на платформу)"},
        {"name": "Разгибания ног", "target": "Изолированный акцент на квадрицепсы (прямая и латеральная широкая мышца бедра / «капля»)"},
        {"name": "Сгибания ног", "target": "Изолированная проработка бицепса бедра (двуглавая, полусухожильная и полуперепончатая мышцы)"}
    ]
}

def get_muscle_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Спина", callback_data="Спина")],
        [InlineKeyboardButton(text="Бицепс", callback_data="Бицепс")],
        [InlineKeyboardButton(text="Грудь", callback_data="Грудь")],
        [InlineKeyboardButton(text="Трицепс", callback_data="Трицепс")],
        [InlineKeyboardButton(text="Ноги", callback_data="Ноги")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Выбери группу мышц для тренировки:", reply_markup=get_muscle_keyboard())

# ИСПРАВЛЕНО: Теперь мы строго проверяем список строк через list(exercises.keys())
@dp.callback_query(lambda callback: callback.data in list(exercises.keys()))
async def show_exercises(callback: types.CallbackQuery):
    muscle = callback.data
    
    ex_list = []
    for item in exercises[muscle]:
        ex_list.append(f"💪 {item['name']}\n🎯 Акцент: {item['target']}\n")
        
    text = f"🏋️‍♂️ Упражнения на группу [{muscle}]:\n\n" + "\n".join(ex_list)
    
    await callback.message.answer(text)
    await callback.answer()

# --- ХИТРОСТЬ ДЛЯ RENDER ---
async def handle_root(request):
    return web.Response(text="Бот запущен и работает 24/7!")

async def start_dummy_server():
    app = web.Application()
    app.router.add_get('/', handle_root)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    await start_dummy_server()  # Сначала запускаем веб-заглушку
    print("Бот запущен и готов к работе...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
