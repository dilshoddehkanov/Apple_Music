from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

language = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🇺🇿UZ'),
            KeyboardButton(text='🇷🇺RU'),
        ],
    ],
    resize_keyboard=True
)

Main_Menu_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🎵 Playlistlar'),
            KeyboardButton(text='🎵 Barcha Musiqalar')
        ],
        [
            KeyboardButton(text='🎶 Playlist yaratish')
        ],
    ],
    resize_keyboard=True
)

Main_Menu_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🎵 Плейлисты'),
            KeyboardButton(text='🎵 Вся музыка')
        ],
        [
            KeyboardButton(text='🎶 Создать плейлист')
        ],
    ],
    resize_keyboard=True
)
