from psycopg2 import sql
from app.models import DatabaseConnector

class Anime(DatabaseConnector):
    table_name = "animes"

    def __init__(self, **kwargs):
        self.anime = kwargs["anime"].title()
        self.released_date = kwargs["released_date"]
        self.seasons = kwargs["seasons"]


    @classmethod
    def read_animes(cls):
        # Cria os atributos conn e cur na classe Pai (DatabaseConector)
        cls.get_conn_cur()

        query = "SELECT * FROM animes;"

        cls.cur.execute(query)

        animes = cls.cur.fetchall()

        cls.cur.close()
        cls.conn.close()

        return animes

    @classmethod
    def animeById(cls, anime_id):
        cls.get_conn_cur()
        query = "SELECT * FROM animes WHERE id = %s;"
        cls.cur.execute(query, str(anime_id))
        anime = cls.cur.fetchone()
        print(anime)
        cls.commit_and_close()
        return anime
    
    def postAnime(self):

        self.get_conn_cur()

        query = """
            INSERT INTO animes
                (anime, released_date, seasons)
            VALUES
                (%s, %s, %s)
            RETURNING *
        """

        query_values = tuple(self.__dict__.values())
        # print(f"{query_values=}")

        self.cur.execute(query, query_values)
        # print(f"{self.cur.query=}")

        self.conn.commit()

        inserted_anime = self.cur.fetchone()

        self.cur.close()
        self.conn.close()

        return inserted_anime

    @classmethod
    def updateAnime(cls, anime_id, payload):
        cls.get_conn_cur()

        columns = [sql.Identifier(key) for key in payload.keys()]
        values = [sql.Literal(value) for value in payload.values()]
        sql_anime_id = sql.Literal(anime_id)

        query = sql.SQL(
            """
            UPDATE
                animes
            SET
                ({columns}) = ROW({values})
            WHERE
                id = {id}
            RETURNING *;
            """
        ).format(
            id=sql_anime_id,
            columns=sql.SQL(",").join(columns),
            values=sql.SQL(",").join(values),
        )

        print("=" * 100)
        print(query.as_string(cls.cur))
        print("=" * 100)

        cls.cur.execute(query)

        updated_anime = cls.cur.fetchone()

        cls.commit_and_close()

        return updated_anime
    
    @classmethod
    def deleteAnime(cls, anime_id):
        cls.get_conn_cur()

        query = sql.SQL(
            """
                DELETE FROM 
                    animes 
                WHERE 
                    id = {id} 
                RETURNING 
                    *
                ;
            """).format(id=sql.Literal(str(anime_id)))

        cls.cur.execute(query)

        deleted_anime = cls.cur.fetchone()
        
        cls.commit_and_close()
        return deleted_anime