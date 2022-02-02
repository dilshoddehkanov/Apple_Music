from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text

from keyboards.default.LanguageKeyboards import Main_Menu_uz, Main_Menu_ru
from loader import dp, dbp, dbu


@dp.message_handler(content_types=types.ContentType.AUDIO)
async def audio_take(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    music_id = message.audio.file_id
    title = message.audio.title
    name = message.audio.performer
    all_musics = dbp.select_all_musics()
    if all_musics:
        music = all_musics[-1]
        mes_id = music[0] + 1
    else:
        mes_id = 0
    await state.update_data(
        {'mes_id': mes_id}
    )
    dbp.add_music(music_id=mes_id, music=music_id, id=user_id, artist_name=name, title=title)
    user = dbu.select_user(id=user_id)
    if user[2] == 'uz':
        if not user[3]:
            # user_playlists = user[3].split()
            # length = len(user_playlists)
            # keyboard = []
            # if length == 0:
            create = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text='🎵 Playlist yaratish')
                    ],
                ],
                resize_keyboard=True
            )
            await message.answer('❌Sizda hozircha playlistlar mavjud emas!!!', reply_markup=create)
            await state.set_state('music_add')
        else:
            a = []
            c = []
            d = []
            e = []
            user_playlists = user[3].split()
            keyboard = []
            create = [KeyboardButton(text='🎵 Playlist yaratish')]
            for playlist in user_playlists:
                if len(a) < 3:
                    b = KeyboardButton(text=f'🎧 {playlist}')
                    a.append(b)
                elif len(a) == 3 and len(c) < 3:
                    b = KeyboardButton(text=f'🎧 {playlist}')
                    c.append(b)
                elif len(a) == 3 and len(c) == 3 and len(d) < 3:
                    b = KeyboardButton(text=f'🎧 {playlist}')
                    d.append(b)
                elif len(a) == 3 and len(c) == 3 and len(d) == 3 and len(e) < 3:
                    b = KeyboardButton(text=f'🎧 {playlist}')
                    e.append(b)
            keyboard.append(a)
            keyboard.append(c)
            keyboard.append(d)
            keyboard.append(e)
            keyboard.append(create)
            playlists = ReplyKeyboardMarkup(keyboard=keyboard,
                                            resize_keyboard=True)
            await message.answer('🎧Musiqani qo\'shish uchun playlist tanlang!', reply_markup=playlists)
            await state.set_state('music_add')
    else:
        user_playlists = user[3].split()
        length = len(user_playlists)
        keyboard = []
        if length == 0:
            create = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text='🎵 Создать плейлист')
                    ],
                ],
                resize_keyboard=True
            )
            await message.answer('❌У вас еще нет плейлистов!!!', reply_markup=create)
            await state.set_state('music_add')
        else:
            a = []
            c = []
            d = []
            e = []
            create = [KeyboardButton(text='🎵 Создать плейлист')]
            for playlist in user_playlists:
                if len(a) < 3:
                    b = KeyboardButton(text=f'🎧 {playlist}')
                    a.append(b)
                elif len(a) == 3 and len(c) < 3:
                    b = KeyboardButton(text=f'🎧 {playlist}')
                    c.append(b)
                elif len(a) == 3 and len(c) == 3 and len(d) < 3:
                    b = KeyboardButton(text=f'🎧 {playlist}')
                    d.append(b)
                elif len(a) == 3 and len(c) == 3 and len(d) == 3 and len(e) < 3:
                    b = KeyboardButton(text=f'🎧 {playlist}')
                    e.append(b)
            keyboard.append(a)
            keyboard.append(c)
            keyboard.append(d)
            keyboard.append(e)
            keyboard.append(create)
            playlists = ReplyKeyboardMarkup(keyboard=keyboard,
                                            resize_keyboard=True)
            await message.answer('🎧Выберите плейлист, чтобы добавить музыку!', reply_markup=playlists)
            await state.set_state('music_add')


@dp.message_handler(text='🎵 Playlist yaratish', state='music_add')
@dp.message_handler(text='🎵 Создать плейлист', state='music_add')
async def add_mus(message: types.MessageEntity, state: FSMContext):
    user = dbu.select_user(id=message.from_user.id)
    if user[3]:
        user_playlists = user[3].split()
        length = len(user_playlists)
        if length == 10:
            if user[2] == 'uz':
                await message.answer(
                    '‼️Siz boshqa playlist yarata olmaysiz. Sizga berilgan limit tugadi. Agar yaratmoqchi bo\'lsangiz \n'
                    '/del_playlist buyrug\'idan foydalanib xoxlagan playlistingizni o\'chirgan holda boshqa yaratishingiz '
                    'mumkin yoki oldingi playlistlaringizdan birortasiga joylang!!!')
            else:
                await message.answer(
                    'Вы не можете создать другой список воспроизведения. Предоставленный вам лимит истек. Если вы хотите '
                    'создать, вы можете использовать команду /del_playlist, чтобы удалить любой список воспроизведения, '
                    'который вы хотите, и создать другой, или вставить его в один из ваших предыдущих списков '
                    'воспроизведения!!!')
        else:
            if user[2] == 'uz':
                await message.answer('Playlistga nom bering: ', reply_markup=ReplyKeyboardRemove())
            else:
                await message.answer('Назовите плейлист: ', reply_markup=ReplyKeyboardRemove())
            await state.set_state('playlist2')
    else:
        if user[2] == 'uz':
            await message.answer('Playlistga nom bering: ', reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer('Назовите плейлист: ', reply_markup=ReplyKeyboardRemove())
        await state.set_state('playlist2')


@dp.message_handler(state='playlist2')
async def create_playl(message: types.Message, state: FSMContext):
    playlist_ = message.text
    play = playlist_.split()
    if len(play) == 1:
        playlist = playlist_
    else:
        playlist = ''
        for i in play:
            if playlist:
                playlist = playlist + '_' + i
            else:
                playlist = i
    user = dbu.select_user(id=message.from_user.id)
    if user[3] == None:
        dbu.update_playlists(playlists=playlist, id=message.from_user.id)
    else:
        user_playlists = user[3] + ' ' + playlist
        dbu.update_playlists(playlists=user_playlists, id=message.from_user.id)
        if user[2] == 'uz':
            await message.answer(f'✅🎧 {playlist} nomli playlist yaratildi')
        else:
            await message.answer(f'✅ Создан плейлист с названием 🎧 {playlist}')
    data = await state.get_data()
    music_id = data.get('mes_id')
    dbp.update_music_playlist(playlist=f'🎧 {playlist}', music_id=music_id)
    if user[2] == 'uz':
        await message.answer(f'✅Musiqa 🎧 {playlist} ga qo\'shildi', reply_markup=Main_Menu_uz)
    else:
        await message.answer(f'✅Музыка добавлена в 🎧 {playlist}', reply_markup=Main_Menu_ru)
    await state.finish()


@dp.message_handler(Text(contains='🎧 ', ignore_case=True), state='music_add')
async def addp(message: types.Message, state: FSMContext):
    playlist = message.text
    user = dbu.select_user(id=message.from_user.id)
    data = await state.get_data()
    music_id = data.get('mes_id')
    dbp.update_music_playlist(playlist=playlist, music_id=music_id)
    if user[2] == 'uz':
        await message.answer(f'✅Musiqa {playlist} ga qo\'shildi', reply_markup=Main_Menu_uz)
    else:
        await message.answer(f'✅Музыка добавлена в {playlist}', reply_markup=Main_Menu_ru)
    await state.finish()
