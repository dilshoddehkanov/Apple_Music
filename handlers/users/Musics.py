from re import sub

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, quote_html

from loader import dp, dbp, dbu
from utils.misc.functions import split_list


@dp.message_handler(Text(contains='🎧 ', ignore_case=True))
async def music_ddd(message: types.Message):
    all_musics = dbp.select_all_musics()
    musics = []
    for music in all_musics:
        music = list(music)
        if music[2] == message.from_user.id and music[5] == message.text:
            musics.append(music)
    now_page = 1
    musics_ = musics[:10]
    id_user = message.from_user.id
    user = dbu.select_user(id=id_user)
    if len(musics_) > 0:
        result_count = len(musics)
        now_pages = int(now_page) * 10 if int(now_page) * 10 < result_count else result_count
        show_count_mp3 = int(now_page) * 10 - 9
        if user[2] == 'uz':
            send_text = f'<b>Natijalar {show_count_mp3} - {now_pages} {result_count} dan \n\n</b>'
        else:
            send_text = f'<b> Результаты {show_count_mp3} - {now_pages} от {result_count} \n\n</b>'
        keyboard_markup = InlineKeyboardMarkup()
        row_btns = []
        n = 1

        for music_ in musics_:
            row_btns.append(
                InlineKeyboardButton(f'{n}', callback_data=f'music{music_[0]}')
            )
            title = sub('(\(@[A-Z_a-z0-9]+\))/(@[A-Z_a-z0-9]+)', '', music_[3] + ' - ' + music_[4])
            send_text += f'{hbold(n)}. {quote_html(title)}\n'
            n += 1
        for i in list(split_list(row_btns)):
            keyboard_markup.row(*i)
        keyboard_markup.row(InlineKeyboardButton('ALL', callback_data=f'all{message.text}'))
        keyboard_markup.insert(InlineKeyboardButton('❌', callback_data='delete'))
        if result_count > 10:
            keyboard_markup.insert(InlineKeyboardButton('➡️', callback_data='next2'))
        await message.reply(send_text, reply_markup=keyboard_markup)
    else:
        if user[2] == 'uz':
            await message.reply('🚫 Bu playlistda hech narsa topilmadi')
        else:
            await message.reply('🚫 Ничего не найдено в этом плейлисте')
