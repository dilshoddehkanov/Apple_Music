import sqlite3


class Music_db:
    def __init__(self, path_to_db="Musics.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_musics(self):
        sql = """
        CREATE TABLE Musics (
            Music_id int NOT NULL UNIQUE,
            Music varchar(255) NOT NULL,
            id int NOT NULL,
            Artist_name varchar(30) NOT NULL,
            Title varchar(30) NOT NULL,
            Playlist varchar(255),
            Liked varchar(10),
            PRIMARY KEY (Music_id)
            );
"""
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_music(self, music_id: int, music: str, id: int, artist_name: str, title: str, liked: str = None,
                  playlist: str = None, ):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO Musics(Music_id, Music, id, Artist_name, Title, Liked, Playlist) VALUES(?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(music_id, music, id, artist_name, title, liked, playlist), commit=True)

    def select_all_musics(self):
        sql = """
        SELECT * FROM Musics
        """
        return self.execute(sql, fetchall=True)

    def select_music(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Musics WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_musics(self):
        return self.execute("SELECT COUNT(*) FROM Musics;", fetchone=True)

    def update_music_playlist(self, playlist, music_id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Musics SET Playlist=? WHERE Music_id=?
        """
        return self.execute(sql, parameters=(playlist, music_id), commit=True)

    def update_liked(self, liked, music_id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Musics SET Liked=? WHERE Music_id=?
        """
        return self.execute(sql, parameters=(liked, music_id), commit=True)

    def delete_musics(self):
        self.execute("DELETE FROM Musics WHERE TRUE", commit=True)

    def delete_music(self, music_id):
        sql = f"""
        DELETE FROM Musics WHERE Music_id={music_id}
        """
        return self.execute(sql, commit=True)

def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
