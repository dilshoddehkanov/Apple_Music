from loader import dbp, dbu
from re import sub

from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import hbold, quote_html

from utils.misc.functions import split_list

from loader import dp


@dp.callback_query_handler(text_startswith=['like'])
async def _playlist(query: CallbackQuery):
    data = query.data
    music_id = data.replace('like', '')
    music = dbp.select_music(music_id=music_id)
    id_user = query.from_user.id
    user = dbu.select_user(id=id_user)
    if user[2] == 'uz':
        if not music[6]:
            dbp.update_liked(music_id=music_id, liked='liked')
            await query.answer("❤️ Sizning sevimli musiqalaringizga qo'shildi (/like)")
        else:
            dbp.update_liked(music_id=music_id, liked='')
            await query.answer("💔  Sevimli musiqalaringizdan o'chirildi")
    else:
        if not music[6]:
            dbp.update_liked(music_id=music_id, liked='liked')
            await query.answer("❤️ Добавлено в вашу любимую музыку (/like)")
        else:
            dbp.update_liked(music_id=music_id, liked='')
            await query.answer("💔  Удалено из любимой музыки")


@dp.message_handler(commands=['like'])
async def _playlists(message: Message):
    now_page = 1
    all_musics = dbp.select_all_musics()
    musics = []
    for music in all_musics:
        music = list(music)
        if music[2] == message.from_user.id and music[6] == 'liked':
            musics.append(music)
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
            send_text = f'<b>Результаты {show_count_mp3} - {now_pages} от {result_count} \n\n</b>'
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

        keyboard_markup.row(InlineKeyboardButton('ALL', callback_data=f'allliked'))
        keyboard_markup.insert(InlineKeyboardButton('❌', callback_data='delete'))
        if result_count > 10:
            keyboard_markup.insert(InlineKeyboardButton('➡️', callback_data='like_next2'))
        await message.reply(send_text, reply_markup=keyboard_markup)
    else:
        if user[2] == 'uz':
            await message.reply('🚫 Sevimli musiqalarda hech narsa topilmadi')
        else:
            await message.reply('🚫 Ничего не найдено в вашей любимой музыке')


@dp.callback_query_handler(text_startswith=['like_next', 'like_prev'])
async def __search_music(query: CallbackQuery):
    all_musics = dbp.select_all_musics()
    musics = []
    for music in all_musics:
        music = list(music)
        if music[2] == query.message.reply_to_message.from_user.id and music[6] == 'liked':
            musics.append(music)

    now_page = query.data.replace('like_next', '') if query.data.startswith('like_next') else query.data.replace(
        'like_prev', '')
    prev_page = int(now_page) - 1
    next_page = int(now_page) + 1

    # search_playlist = musics.Search_Music(int(now_page) if query.data.startswith('next') else prev_page)
    if query.data.startswith('like_next'):
        search_playlist = int(now_page)
    else:
        search_playlist = prev_page
    musics_ = musics[(int(now_page) - 1) * 10:int(now_page) * 10]
    id_user = query.message.reply_to_message.from_user.id
    user = dbu.select_user(id=id_user)
    if len(musics_) > 0:
        result_count = int(len(musics))
        now_pages = int(now_page) * 10 if int(now_page) * 10 < result_count else result_count
        show_count_mp3 = int(now_page) * 10 - 9
        if user[2] == 'uz':
            send_text = f"<b>Natijalar {show_count_mp3}-{now_pages} {result_count} dan\n\n</b>"
        else:
            send_text = f"<b>Результаты {show_count_mp3} - {now_pages} от {result_count}\n\n</b>"
        keyboard_markup = InlineKeyboardMarkup()
        n = 1
        row_btns = []
        for i in musics_:
            row_btns.append(
                InlineKeyboardButton(f"{n}", callback_data=f"music{i[0]}")
            )
            title = sub('(\(@[A-Z_a-z0-9]+\))|(@[A-Z_a-z0-9]+)', '', i[3] + ' - ' + i[4])

            send_text += f"{hbold(n)}. {quote_html(title)}\n"
            n += 1
        for i in list(split_list(row_btns)):
            keyboard_markup.row(*i)
        if prev_page != 0:
            keyboard_markup.row(InlineKeyboardButton('⬅', callback_data=f'like_prev{prev_page}'))
        keyboard_markup.insert(InlineKeyboardButton('ALL', callback_data='allliked'))
        keyboard_markup.insert(InlineKeyboardButton('❌', callback_data='delete'))
        if 10 < result_count and result_count > int(now_page) * 10:
            keyboard_markup.insert(InlineKeyboardButton('➡', callback_data=f'like_next{next_page}'))
        await query.message.edit_text(send_text,
                                      reply_markup=keyboard_markup)
