from os import getenv

from dotenv import load_dotenv


def load_env_credentials():
    """
    Bot api and AI api are necessary for correct functioning.
    You can obtain bot token via BotFather in telegram.
    I got my API token for AI from openrouter.ai so i'd recommend you doing it same way.
    While not required, it is recommended to restrict AI respond length to 50-80 for better experience.
    For R34 and Femboy you may put whatever tags you want (check available tags on rule34.xxx)
    Have fun!
    """
    load_dotenv()
    return {
        "BOT_API_TOKEN": getenv("BOT_API_TOKEN"),
        "AI_API_TOKEN": getenv("AI_API_TOKEN"),
        "R34_TAGS": getenv("R34_TAGS"),
        "FEMBOY_TAGS": getenv("FEMBOY_TAGS"),
        "AI_PROMPT": getenv("AI_PROMPT"),
    }
