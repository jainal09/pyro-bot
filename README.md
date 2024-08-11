# Pyro
<div align="center">
  <img src="https://github.com/jainal09/pyro-bot/assets/34179361/5d494fb4-5721-42f7-b463-cd12e8e3c86c" alt="pyro-logo" width="400"/>
  <br>
</div>

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Dependency Management: Poetry](https://img.shields.io/badge/Dependency%20Managment-Poetry-blue?logo=python&logoColor=yellow)](https://python-poetry.org/) [![Formatter and Linter: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT) [![python: 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-311/)

Pyro is a chatbot that contains vectors of the entire python 3.12 documentation. Backed up by GPT 4.o ask any question
regarding python and it will try to answer those questions thanks to the Weviate vector database and Langchain based RAG
pipeline.

## Demo Video 📺

### Introduction

Click on the image below to watch the demo video on YouTube:

[![Youtube Video](https://img.youtube.com/vi/OK6J-1NPIxM/0.jpg)](https://www.youtube.com/watch?v=OK6J-1NPIxM)

### Complete Presentation
[![Youtube Video](https://img.youtube.com/vi/34xLpdBvdQg&t=12s/0.jpg)](https://www.youtube.com/watch?v=34xLpdBvdQg&t=12s)




## Sneak Peak

https://github.com/user-attachments/assets/b6af98c8-ba10-4f52-8202-287c69bd42bf

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

### Setting the environment

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

### Starting Services

```text
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

### Lint
Lint the code using ruff:

```text
ruff check --fix .
```

## Dataset
The pdf folder contains the entire python 3.12 documentation. Upload each pdf through the streamlit UI to index it to the vector db.

To index all the pdfs run the following script:

```text
poetry run index_dataset.py
```

## Metrics
Refer to the documentation in [evaluation_metrics/README.md](evaluation_metrics/README.md)
