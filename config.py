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
    
    ANO_INICIAL   = os.getenv('ANO_INICIAL')
    ANO_FINAL     = os.getenv('ANO_FINAL')
    DATA_DOWNLOAD = os.getenv('DATA_DOWNLOAD')

    MAX_WAIT    = None
    DIR_DESTINO = Path.home() / 'divida_ativa' / DATA_DOWNLOAD
    DIR_DESTINO.mkdir(parents=True, exist_ok=True)

    (HERE / 'data' / 'processed' / DATA_DOWNLOAD).mkdir(parents=True, exist_ok=True)