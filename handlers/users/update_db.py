from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from keyboards.default.LanguageKeyboards import Main_Menu_uz, Main_Menu_ru
from loader import dp, dbu, dbp, bot


@dp.message_handler(text='🇺🇿UZ')
async def language(message: types.Message):
    await message.answer('Siz o\'zbek tilini tanladingiz!!!', reply_markup=ReplyKeyboardRemove())
    dbu.update_language(language='uz', id=message.from_user.id)
    username = (await dp.bot.get_me()).username
    await bot.send_video(chat_id=message.from_user.id, video='https://t.me/foto_va_mp3lar_olami_575/121',
                         caption=f'Qo\'llanma\n\n🔥 @{username.capitalize()}')
    await message.answer('Bu bot sizning musiqalaringizni playlistlarga bo\'lib saqlash uchun juda foydali bot. Bu '
                         'ayniqsa iPhone telefon ishlatadiganlarga foydasi tegadi chunki apple music programmasi '
                         'pullik bu esa telegramdagi musiqalarni playlist sifatida saqlaydi.',
                         reply_markup=Main_Menu_uz)


@dp.message_handler(text='🇷🇺RU')
async def language(message: types.Message):
    await message.answer('Вы выбрали узбекский!!!', reply_markup=ReplyKeyboardRemove())
    dbu.update_language(language='ru', id=message.from_user.id)
    username = (await dp.bot.get_me()).username
    await bot.send_video(chat_id=message.from_user.id, video='https://t.me/foto_va_mp3lar_olami_575/122',
                         caption=f'Руководство\n\n🔥 @{username.capitalize()}')
    await message.answer('Этот бот очень полезен для хранения вашей музыки в плейлистах. Это особенно полезно для '
                         'пользователей iPhone, потому что приложение Apple Music платное, которое сохраняет музыку в '
                         'телеграмме в виде плейлиста. ', reply_markup=Main_Menu_ru)


@dp.message_handler(text='🎵 Playlistlar')
@dp.message_handler(text='🎵 Плейлисты')
async def playlists(message: types.Message):
    id_user = message.from_user.id
    user = dbu.select_user(id=id_user)
    if user[2] == 'uz':
        if not user[3]:
            await message.answer('❌Sizda hozircha playlistlar mavjud emas!!!')
        else:
            user_playlists = user[3].split()
            keyboard = []
            a = []
            c = []
            d = []
            e = []
            back = [KeyboardButton(text='Bosh menu')]
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
            keyboard.append(back)
            playlists = ReplyKeyboardMarkup(keyboard=keyboard,
                                            resize_keyboard=True)
            await message.answer('🎧Sizning playlistlaringiz', reply_markup=playlists)
    else:
        if not user[3]:
            await message.answer('❌У вас еще нет плейлистов!!!')
        else:
            user_playlists = user[3].split()
            keyboard = []
            a = []
            c = []
            d = []
            e = []
            back = [KeyboardButton(text='Главное меню')]
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
            keyboard.append(back)
            playlists = ReplyKeyboardMarkup(keyboard=keyboard,
                                            resize_keyboard=True)
            await message.answer('🎧Ваши плейлисты', reply_markup=playlists)


@dp.message_handler(text='🎶 Playlist yaratish')
@dp.message_handler(text='🎶 Создать плейлист')
async def create(message: types.Message, state: FSMContext):
    user = dbu.select_user(id=message.from_user.id)
    if user[3]:
        user_playlists = user[3].split()
        length = len(user_playlists)
    else:
        length = 0
    if length == 10:
        if user[2] == 'uz':
            await message.answer(
                '‼️Siz boshqa playlist yarata olmaysiz. Sizga berilgan limit tugadi. Agar yaratmoqchi bo\'lsangiz \n'
                '/del_playlist buyrug\'idan foydalanib xoxlagan playlistingizni o\'chirgan holda boshqa yaratishingiz '
                'mumkin!!!')
        else:
            await message.answer('Вы не можете создать другой список воспроизведения. Предоставленный вам лимит истек. '
                                 'Если вы хотите создать, вы можете создать еще один, удалив любой список '
                                 'воспроизведения, который хотите, с помощью команды /del_playlist')
    else:
        if user[2] == 'uz':
            await message.answer('Playlistga nom bering: ', reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer('Назовите плейлист: ', reply_markup=ReplyKeyboardRemove())
        await state.set_state('playlist')


@dp.message_handler(state='playlist')
async def playl(message: types.Message, state: FSMContext):
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
        await state.finish()
    else:
        user_playlists = user[3] + ' ' + playlist
        dbu.update_playlists(playlists=user_playlists, id=message.from_user.id)
        if user[2] == 'uz':
            await message.answer(f'✅{playlist} nomli playlist yaratildi', reply_markup=Main_Menu_uz)
        else:
            await message.answer(f'✅ Создан плейлист с названием {playlist}', reply_markup=Main_Menu_ru)
        await state.finish()


@dp.message_handler(commands='del_playlist', state='*')
async def delete(message: types.Message, state: FSMContext):
    id_user = message.from_user.id
    user = dbu.select_user(id=id_user)
    if user[2] == 'uz':
        user_playlists = user[3].split()
        length = len(user_playlists)
        keyboard = []
        if length == 0:
            await message.answer('❌Sizda hozircha playlistlar mavjud emas!!!')
        else:
            a = []
            c = []
            d = []
            e = []
            back = [KeyboardButton(text='Bosh menu')]
            for playlist in user_playlists:
                if len(a) < 3:
                    b = KeyboardButton(text=f'{playlist}')
                    a.append(b)
                elif len(a) == 3 and len(c) < 3:
                    b = KeyboardButton(text=f'{playlist}')
                    c.append(b)
                elif len(a) == 3 and len(c) == 3 and len(d) < 3:
                    b = KeyboardButton(text=f'{playlist}')
                    d.append(b)
                elif len(a) == 3 and len(c) == 3 and len(d) == 3 and len(e) < 3:
                    b = KeyboardButton(text=f'{playlist}')
                    e.append(b)
            keyboard.append(a)
            keyboard.append(c)
            keyboard.append(d)
            keyboard.append(e)
            keyboard.append(back)
            playlists = ReplyKeyboardMarkup(keyboard=keyboard,
                                            resize_keyboard=True)
            await message.answer('‼️O\'chirmoqchi bo\'lgan playlistingizni tanlang', reply_markup=playlists)
    else:
        user_playlists = user[3].split()
        length = len(user_playlists)
        keyboard = []
        if length == 0:
            await message.answer('❌У вас еще нет плейлистов!!!')
        else:
            a = []
            c = []
            d = []
            e = []
            back = [KeyboardButton(text='Главное меню')]
            for playlist in user_playlists:
                if len(a) < 3:
                    b = KeyboardButton(text=f'{playlist}')
                    a.append(b)
                elif len(a) == 3 and len(c) < 3:
                    b = KeyboardButton(text=f'{playlist}')
                    c.append(b)
                elif len(a) == 3 and len(c) == 3 and len(d) < 3:
                    b = KeyboardButton(text=f'{playlist}')
                    d.append(b)
                elif len(a) == 3 and len(c) == 3 and len(d) == 3 and len(e) < 3:
                    b = KeyboardButton(text=f'{playlist}')
                    e.append(b)
            keyboard.append(a)
            keyboard.append(c)
            keyboard.append(d)
            keyboard.append(e)
            keyboard.append(back)
            playlists = ReplyKeyboardMarkup(keyboard=keyboard,
                                            resize_keyboard=True)
            await message.answer('‼️Выберите плейлист, который хотите удалить', reply_markup=playlists)
    await state.set_state('delete')


@dp.message_handler(state='delete')
async def delet(message: types.Message, state: FSMContext):
    user = dbu.select_user(id=message.from_user.id)
    playl = message.text
    p_lists = user[3].split()
    p_lists.remove(playl)
    S = ''
    for p in p_lists:
        S += ' ' + p
    dbu.update_playlists(playlists=S, id=message.from_user.id)
    all_musics = dbp.select_all_musics()
    for music in all_musics:
        if music[2] == message.from_user.id and music[5] == f'🎧 {playl}':
            dbp.delete_music(music_id=music[0])
    id_user = message.from_user.id
    user = dbu.select_user(id=id_user)
    if user[2] == 'uz':
        await message.answer(f'{playl} nomli playlist o\'chirildi!', reply_markup=Main_Menu_uz)
    else:
        await message.answer(f'Плейлист с названием {playl} удален!', reply_markup=Main_Menu_ru)
    await state.finish()
