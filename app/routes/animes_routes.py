from flask import Blueprint
from app.controllers import animes_controllers

bp_animes = Blueprint("anime", __name__, url_prefix="/animes")

bp_animes.get("")(animes_controllers.getAnimes)
bp_animes.get("/<int:anime_id>")(animes_controllers.getAnimesById)
bp_animes.post("")(animes_controllers.postAnimes)
bp_animes.patch("/<int:anime_id>")(animes_controllers.patchAnimes)
bp_animes.delete("/<int:anime_id>")(animes_controllers.deleteAnime)