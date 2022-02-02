from peewee import fn

from loader import dbp


class Musics:
    def __init__(self, searched_text):
        self.searched_text = searched_text

    def Search_Music(self, limit=False, offset=0):
        if offset:
            return [i for i in
                    dbp.select().where(fn.Lower(dbp.title).contains(self.searched_text)).limit().offset(offset)]
        else:
            return [i for i in
                    dbp.select_music(playlist=self.searched_text)]

    def Search_Inline_Music(self, offset=False, types=False):
        if types:
            return dbp.select().where(fn.Lower(dbp.title).contains(self.searched_text)).count()
        if type(offset) == int:
            return [i for i in
                    dbp.select().where(fn.Lower(dbp.title).contains(self.searched_text)).limit(50).offset(
                        offset - 1)]

    def All_Music(self):
        return dbp.select().where(dbp.title.contains(self.searched_text)).count()
