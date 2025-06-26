import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import EnumFilter
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

API_TOKEN = os.getenv('API_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))

bot = Bot(API_TOKEN)
dp = Dispatcher()

@dp.message(commands=['start'])
async def start_cmd(msg: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('🛑 Жалоба', callback_data='typ_complaint')],
        [InlineKeyboardButton('⚠️ Репорт', callback_data='typ_report')],
        [InlineKeyboardButton('💡 Предложение', callback_data='typ_suggestion')],
    ])
    await msg.answer('Что отправляем?', reply_markup=kb)

@dp.callback_query()
async def cb_handler(c: types.CallbackQuery):
    t = c.data.split('_')[1]
    await c.message.answer('Напиши текст:')
    dp.data = dp.data if hasattr(dp, 'data') else {}
    dp.data[c.from_user.id] = t
    await c.answer()

@dp.message()
async def forward_msg(msg: types.Message):
    t = getattr(dp, 'data', {}).pop(msg.from_user.id, 'message')
    types_ = {'complaint':'🛑', 'report':'⚠️', 'suggestion':'💡'}
    line = f"{types_.get(t,'📩')} {t.capitalize()} от @{msg.from_user.username or msg.from_user.first_name}:\n\n{msg.text}"
    await bot.send_message(ADMIN_ID, line)
    await msg.answer('Отправлено!')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
