import os
from dotenv import load_dotenv

load_dotenv()

GEMININ_API_KEY = os.getenv('GEMININ_API_KEY')
GEMINI_MODEL = os.getenv('GEMINI_MODEL','gemini-3.5-flash')

if not GEMININ_API_KEY:
    raise RuntimeError(
        'GEMINI_API_KEY is not set, please add it into .env file.'
    )