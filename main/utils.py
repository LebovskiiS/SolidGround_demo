import json
from pathlib import Path
# from main.models import MusicTrack  # Music functionality moved to frontend
from DjangoProject.settings import MUSIC_FILE_PATH
from .logger import logger
from . import exceptions

# Music functionality moved to frontend
# def load_music_from_file():
#
#     file_path = Path(MUSIC_FILE_PATH)
#
#     if not file_path.exists():
#         logger.error(f'{file_path} not found.')
#         raise FileNotFoundError
#
#     with open(file_path, 'r', encoding='utf-8') as f:
#         try:
#             music_data = json.load(f)
#         except json.JSONDecodeError as e:
#             logger.error('Error in structure of JSON file:', {e})
#             raise exceptions.InvalidJSONStructure
#
#
#     for track in music_data:
#         track_name = track.get("name")
#         track_url = track.get("url")
#
#         obj, created = MusicTrack.objects.update_or_create(
#             name=track_name,
#             defaults={"url": track_url}
#         )
#
#         if created:
#             logger.info(f"New track added: {track_name}")
#         else:
#             logger.info(f'Track updated {track_name}')
