# Pyro

Pyro is a chatbot that contains vectors of the entire python 3.12 documentation. Backed up by GPT 4.o ask any question
regarding python and it will try to answer those questions thanks to the Weviate vector database and Langchain based RAG
pipeline.

## Motivation
I noticed that there aren't many examples on how to deploy via docker compose
a **FastAPI** backend  backed by a self-hosted **Weaviate** vector store, and a streamlit chat application.  
The interaction with Azure OpenAI happens through **langchain**.


## Quickstart

The API exposes 2 endpoints:

- **/files/upload**: a POST with a .pdf document to store in a weaviate
  collection.

- **/files/query**: a GET with a question to ask based on the uploaded
  documents. The response will be streamed back to the user.

### 1) Set the environment

Create a .env in the project root folder in order to set up the environment variables:

```text
WEAVIATE_SERVICE_NAME=weaviate
FASTAPI_PORT=8000
WEAVIATE_PORT=8080
WEAVIATE_COLLECTION = Document
WEAVIATE_DROP_COLLECTION = False
OPENAI_API_TYPE = azure
OPENAI_API_VERSION = 2023-07-01-preview
OPENAI_DEPLOYMENT_NAME=
OPENAI_API_KEY = 
OPENAI_API_BASE =
```

If those ports are not in use then you can leave these variables as
they are, you just need to set **OPENAI_DEPLOYMENT_NAME**, **OPEN_API_KEY** & **OPEN_API_BASE**
with the values you can find on the Azure dashboard of your
Azure Open AI resource deployment.

### 2) Docker compose

```shell
docker compose up --build
```

Once it is done, you can check if everything is working fine by
making a GET to the following endpoint:

```text
http://localhost:8000/health
```

If you get an OK message than you are ready to go.

### FastApi Swagger Docs

You can go the openAPI swagger docs
endpoint and start testing the API:

```text
http://localhost:8000/docs
```

### Streamlit Chat App

You can go to this endpoint to access the chat app.

```text
http://localhost:8501
```
