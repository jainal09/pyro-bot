from evaluation_metrics.config import (
    API_KEY,
    API_VERSION,
    AZURE_DEPLOYMENT,
    AZURE_ENDPOINT,
)
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=API_KEY,
    azure_endpoint=AZURE_ENDPOINT,
    api_version=API_VERSION,
    azure_deployment=AZURE_DEPLOYMENT,
)

def query_openai(messages: list):
    response = client.chat.completions.create(
        model= AZURE_DEPLOYMENT,
        messages= messages
    )
    return response.choices[0].message.content
