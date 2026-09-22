import os

from dotenv import load_dotenv


load_dotenv()


METALS_DEV_API_KEY = os.getenv("METALS_DEV_API_KEY")

METALS_DEV_BASE_URL = os.getenv(
    "METALS_DEV_BASE_URL",
    "https://api.metals.dev/v1"
)
