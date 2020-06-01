# settings.py
import os
from pathlib import Path  # python3 only
from dotenv import load_dotenv


class Settings:
    def __init__(self, env_path: str = "") -> None:
        if len(env_path) == 0:
            env_path = Path('.') / '.env'

        load_dotenv(dotenv_path=env_path)

    def get(self, variable: str):
        return os.getenv(variable)
