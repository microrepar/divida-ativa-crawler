import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

HERE = Path(__name__).parent

(HERE / 'data' / 'external').mkdir(parents=True, exist_ok=True)
(HERE / 'data' / 'interim').mkdir(parents=True, exist_ok=True)
(HERE / 'data' / 'processed').mkdir(parents=True, exist_ok=True)
(HERE / 'data' / 'raw').mkdir(parents=True, exist_ok=True)

(HERE / 'resources' / 'images').mkdir(parents=True, exist_ok=True)
(HERE / 'resources' / 'images_error').mkdir(parents=True, exist_ok=True)

class Config:

    URL = os.getenv('URL')

    USUARIO = os.getenv('USUARIO')
    SENHA   = os.getenv('SENHA')
    
    ANO_INICIAL = 2023
    ANO_FINAL   = 2023

    MAX_WAIT    = None
    DIR_DESTINO = Path.home() / 'divida_ativa' / '2023-12-28'
    DIR_DESTINO.mkdir(parents=True, exist_ok=True)
