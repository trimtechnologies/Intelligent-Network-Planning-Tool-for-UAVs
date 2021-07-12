from dotenv import load_dotenv
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
ENV_FILE = os.path.join(BASE_DIR, "../../../../.env")
load_dotenv(dotenv_path=ENV_FILE)

DATABASE_NAME = os.getenv("DATABASE_NAME")
SAVE_LOGS_IN_DATABASE = os.getenv("SAVE_LOGS_IN_DATABASE")
ENVIRONMENT = os.getenv("ENVIRONMENT")


def get_env_keys():
    """
    This function read the .env file and get all env keys from the file
    :return: list Return the .env keys
    """
    env_vars = []
    with open(ENV_FILE) as f:
        for line in f:
            if not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                env_vars.append(key)

    return env_vars
