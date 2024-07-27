import os

from dotenv import load_dotenv

load_dotenv("evaluation_metrics/openai.env")

AZURE_DEPLOYMENT = os.getenv("AZURE_DEPLOYMENT")
API_KEY = os.getenv("API_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
API_VERSION = os.getenv("API_VERSION")
