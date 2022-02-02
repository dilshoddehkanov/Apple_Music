import asyncio
import sqlite3

from aiogram.dispatcher import FSMContext
from openpyxl import Workbook
from aiogram import types
from aiogram.types import InputFile, ReplyKeyboardRemove

from data.config import ADMINS
from loader import dp, dbu, bot, dbp
from utils.misc.dict import sonlar


@dp.message_handler(text="/allusers", user_id=ADMINS)
async def get_all_users(message: types.Message):
    wb = Workbook()
    ws = wb.active
    ws.title = "Foydalanuvchilar ro'yxati"

    SQL_QUERY = "select * from Musics"

    conn = sqlite3.connect('data/Musics.db')
    c = conn.cursor()

    c.execute(SQL_QUERY)

    row = c.fetchall()

    column_list = []
    for column_name in c.description:
        column_list.append(column_name[0])
    ws.append(column_list)

    for result in row:
        ws.append(list(result))

    wb.save("Users.xlsx")
    file = InputFile(path_or_bytesio='Users.xlsx')
    count = len(dbu.select_all_users())
    s = ""
    for i in str(count):
        s += sonlar.get(i, i)
    username = (await dp.bot.get_me()).username
    await message.answer_document(file, caption=f'\n▶️Foydalanuvchilar soni👉    {s}ta\n'
                                                f'▶️Ishga tushirilgan vaqti:   <b>18/01/2022</b>\n'
                                                f'▶️Dasturchi: @iDekUz\n\n'
                                                f'🔥 @{username.capitalize()}')


@dp.message_handler(text="/reklama", user_id=ADMINS)
async def send_add_to_all(message: types.Message, state: FSMContext):
    await message.answer('Reklama uchun rasm yuboring', reply_markup=ReplyKeyboardRemove())
    await state.set_state('rek_photo')


@dp.message_handler(content_types=types.ContentType.PHOTO, state='rek_photo')
async def add_photo(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(
        {'photo_id': photo_id}
    )
    await message.answer('Reklama matnini yuboring')
    await state.set_state('rek_add')


@dp.message_handler(state='rek_add')
async def rek_adddd(message: types.Message, state: FSMContext):
    text = message.text
    data = await state.get_data()
    photo_id = data.get('photo_id')
    users = dbu.select_all_users()
    try:
        for user in users:
            user_id = user[0]
            await bot.send_photo(chat_id=user_id, photo=photo_id, caption=text)
            await asyncio.sleep(0.05)
    except:
        i = 0
    await state.finish()


@dp.message_handler(text="/cleandb", user_id=ADMINS)
async def get_all_users(message: types.Message):
    dbu.delete_users()
    dbp.delete_musics()
    await message.answer("Baza tozalandi!")


@dp.message_handler(text='/video', user_id=ADMINS)
async def send_video(message: types.Message):
    username = (await dp.bot.get_me()).username

    users = dbu.select_all_users()
    try:
        for user in users:
            user_id = user[0]
            await bot.send_video(chat_id=user_id, video='https://t.me/foto_va_mp3lar_olami_575/121',
                                 caption=f'Qo\'llanma\n\n🔥 @{username.capitalize()}')
            await asyncio.sleep(0.05)
    except:
        i = 0
