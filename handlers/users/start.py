import sqlite3

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.LanguageKeyboards import language, Main_Menu_uz, Main_Menu_ru
from data.config import ADMINS
from loader import dp, dbu, bot
from utils.misc.dict import sonlar


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    name = message.from_user.full_name
    # Foydalanuvchini bazaga qo'shamiz
    try:
        dbu.add_user(id=message.from_user.id,
                     name=name)
    except sqlite3.IntegrityError as err:
        i = 1
        # await bot.send_message(chat_id=ADMINS[0], text=err)

    await message.answer(f"Assalomu aleykum, {message.from_user.full_name}! \n"
                         f"Apple Music botiga xush kelibsiz!!!\n\n"
                         f"/start - Botni ishga tushirish\n"
                         f"/help - Yordamnn\n"
                         f"/like - Sevimli musiqalar")
    await message.answer('Tilni tanlang👇👇👇', reply_markup=language)
    count = len(dbu.select_all_users())
    s = ""
    username = (await dp.bot.get_me()).username
    for i in str(count):
        s += sonlar.get(i, i)
    if count <= 100:
        if count % 10 == 0:
            await bot.send_message(chat_id=ADMINS[0],
                                   text=f'✅Tabriklaymiz sizning obunchilaringiz soni {s} ta bo\'ldi🥳🥳🥳'
                                        f'🔥 @{username.capitalize()}')
    elif count <= 1000:
        if count % 100 == 0:
            await bot.send_message(chat_id=ADMINS[0],
                                   text=f'✅Tabriklaymiz sizning obunchilaringiz soni {s} ta bo\'ldi🥳🥳🥳'
                                        f'🔥 @{username.capitalize()}')
    else:
        if count % 1000 == 0:
            await bot.send_message(chat_id=ADMINS[0],
                                   text=f'✅Tabriklaymiz sizning obunchilaringiz soni {s} ta bo\'ldi🥳🥳🥳\n\n'
                                        f'🔥 @{username.capitalize()}')
    await state.finish()


@dp.message_handler(text='Bosh menu', state='*')
@dp.message_handler(text='/menu', state='*')
async def bot_start(message: types.Message, state: FSMContext):
    user = dbu.select_user(id=message.from_user.id)
    if user[2] == 'uz':
        await message.answer('Asosiy menu', reply_markup=Main_Menu_uz)
    else:
        await message.answer('Главное меню', reply_markup=Main_Menu_ru)
    await state.finish()


@dp.message_handler(text='Главное меню', state='*')
async def bot_start(message: types.Message, state: FSMContext):
    await message.answer('Главное меню', reply_markup=Main_Menu_ru)
    await state.finish()
