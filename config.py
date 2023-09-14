from dataclasses import dataclass
from pathlib import Path
from environs import Env
import sys


@dataclass
class TgBot:
    token: str


@dataclass
class DvmnApi:
    token: str


@dataclass
class Config:
    tgbot: TgBot
    dvmn_api: DvmnApi


def load_config(env_path='') -> Config:
    '''Loading configurations using environment variables from an .env file,
    the path to which should be specified as an argument to the function.
    If the path to the .env is not specified, the function will look for the
    file in the entry point directory.
    Returns an instance of the Config class with the data already filled in.
    '''
    env = Env()
    if not env_path or not Path(env_path).exists():
        env_path = Path(Path.cwd(), '.env')
    try:
        env.read_env(env_path)
    except OSError:
        sys.exit("Error. There is no '.env' file")

    return Config(tgbot=TgBot(token=env('TG_BOT_TOKEN')),
                  dvmn_api=DvmnApi(token=f"Token {env('DVMN_API_TOKEN')}"))
