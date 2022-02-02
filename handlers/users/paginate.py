from re import sub

from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import hbold, quote_html

from utils.misc.functions import split_list
from loader import dp, dbp, dbu

from keyboards.inline.Inlinekeyboards import music_keyboard


@dp.callback_query_handler(text_startswith=['next', 'prev'])
async def __search_music(query: CallbackQuery):
    all_musics = dbp.select_all_musics()
    musics = []
    for music in all_musics:
        music = list(music)
        if music[2] == query.message.reply_to_message.from_user.id and music[5] == query.message.reply_to_message.text:
            musics.append(music)

    now_page = query.data.replace('next', '') if query.data.startswith('next') else query.data.replace('prev', '')
    prev_page = int(now_page) - 1
    next_page = int(now_page) + 1

    # search_playlist = musics.Search_Music(int(now_page) if query.data.startswith('next') else prev_page)
    if query.data.startswith('next'):
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
            keyboard_markup.row(InlineKeyboardButton('⬅', callback_data=f'prev{prev_page}'))
        keyboard_markup.insert(InlineKeyboardButton('ALL', callback_data=f'all{query.message.reply_to_message.text}'))
        keyboard_markup.insert(InlineKeyboardButton('❌', callback_data='delete'))
        if 10 < result_count and result_count > int(now_page) * 10:
            keyboard_markup.insert(InlineKeyboardButton('➡', callback_data=f'next{next_page}'))
        await query.message.edit_text(send_text,
                                      reply_markup=keyboard_markup)


@dp.callback_query_handler(text_startswith=['delete'])
async def _delete_message(query: CallbackQuery):
    await query.message.delete()


@dp.callback_query_handler(text_startswith=['music'])
async def music_take(query: CallbackQuery):
    username = (await dp.bot.get_me()).username
    music_id = query.data.replace('music', '')
    music = dbp.select_music(music_id=music_id)
    await query.message.reply_audio(music[1], reply_markup=music_keyboard(music_id),
                                    caption=f"🔥 @{username.capitalize()}")
