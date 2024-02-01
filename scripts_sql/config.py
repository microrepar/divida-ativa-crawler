# https://pypi.org/project/python-dotenv/

import os
from dotenv import load_dotenv
# from pathlib import Path

# here = Path.cwd() 
# env = here / '.env'

load_dotenv()  # take environment variables from .env.

DATA_DOWNLOAD = os.getenv('DATA_DOWNLOAD')