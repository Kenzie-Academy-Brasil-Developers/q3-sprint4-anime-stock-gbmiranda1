from http import HTTPStatus
from flask import request
from app.models.animes_models import Anime
from psycopg2.errors import UniqueViolation, UndefinedTable


def getAnimes():

    if Anime.read_animes():
        anime_columns = ["id", "anime", "released_date", "seasons"]
        serialized_animes = [dict(zip(anime_columns, anime)) for anime in Anime.read_animes()]
        
        return {"data": serialized_animes}, 200
    return {"data": []}, 200


def getAnimesById(anime_id):

    try:
        animes = Anime.animeById(anime_id)
        anime_columns = ["id", "anime", "released_date", "seasons"]
        serialized_animes = dict(zip(anime_columns, animes)) 
        

        return {"data": serialized_animes}, 200

    except (TypeError, UndefinedTable):
        return {"error": "Not Found"}, 404


def postAnimes():
    data = request.get_json()
    notKeys = []
    if "anime" not in data.keys():
        notKeys.append("anime")
    if "released_date" not in data.keys():
        notKeys.append("released_date")   
    if "seasons" not in data.keys():
        notKeys.append("seasons") 

    

    try:
        anime = Anime(**data)
        inserted_anime = anime.postAnime()
        anime_columns = ["id", "anime", "released_date", "seasons"]
        serialized_animes = dict(zip(anime_columns, inserted_anime)) 
        return serialized_animes, HTTPStatus.CREATED
    except UniqueViolation as e:
        return {"error": "anime already in use"}, HTTPStatus.UNPROCESSABLE_ENTITY
    except KeyError:
        return {"available_keys": ["anime", "released_date", "seasons"],
                "not_keys_sended": notKeys}, \
            HTTPStatus.UNPROCESSABLE_ENTITY
    


def patchAnimes(anime_id: str):
    data = request.get_json()
    notKeys = []
    if "anime" not in data.keys():
        notKeys.append("anime")
    if "released_date" not in data.keys():
        notKeys.append("released_date")   
    if "seasons" not in data.keys():
        notKeys.append("seasons") 
    try:
        
        if notKeys:
            raise KeyError
        updated_anime = Anime.updateAnime(anime_id, data)

        if not updated_anime:
            return {"error": "id not found"}, HTTPStatus.NOT_FOUND

        anime_columns = ["id", "anime", "released_date", "seasons"]
        serialized_animes = dict(zip(anime_columns, updated_anime)) 

        return serialized_animes, HTTPStatus.OK
    except KeyError:
        return {"available_keys": ["anime", "released_date", "seasons"],
                "not_keys_sended": notKeys}, \
            HTTPStatus.UNPROCESSABLE_ENTITY

def deleteAnime(anime_id):
    try:
        animes_deleted = Anime.deleteAnime(anime_id)

        anime_columns = ["id", "anime", "released_date", "seasons"]
        serialized_animes = dict(zip(anime_columns, animes_deleted)) 

        return {"data": serialized_animes}, 204

    except (TypeError, UndefinedTable):
        return {"error": "Not Found"}, 404