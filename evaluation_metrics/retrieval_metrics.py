from urllib.parse import quote

import markdown
import numpy as np
import requests
from bs4 import BeautifulSoup
from evaluation_metrics.open_ai_service import query_openai
from tqdm import tqdm


def preprocess_markdown(markdown_text):
    """Convert markdown to plain text."""
    html = markdown.markdown(markdown_text)
    text = BeautifulSoup(html, features="html.parser").get_text()
    return text.strip()


def context_precision(query, retrieved_context, relevant_contexts):
    """Measure how accurately the retrieved context matches the user's query."""
    response = query_openai(
        messages=[
            {
                "role": "system",
                "content": """
             We are evaluating a RAG Pipeline. You will get the user query, 
            list of retrieved_context and a list of relevant_contexts.
             You need to calculate the context_precision. The context_precision is the 
             Measure how accurately the retrieved context matches the user's query.
            """,
            },
            {
                "role": "user",
                "content": f"""
             Query: {query},
             Retrieved Context List: {retrieved_context},
             Relevant Context List: {relevant_contexts},
             """,
            },
            {
                "role": "system",
                "content": """You just have to return a single float value. The value should be between 0 and 1.""",
            },
        ],
    )
    return float(response)


def context_recall(query, retrieved_context, relevant_contexts):
    """Evaluate the ability to retrieve all relevant contexts for the user's query."""
    response = query_openai(
        messages=[
            {
                "role": "system",
                "content": """
             We are evaluating a RAG Pipeline. You will get query, the list of retrieved_context and a list of \
            relevant_contexts.
             You need to calculate the context_recall. The context_recall is the 
             Evaluate the ability to retrieve all relevant contexts for the user's query.
            """,
            },
            {
                "role": "user",
                "content": f"""
            Query: {query},
             Retrieved Context List: {retrieved_context},
             Relevant Context List: {relevant_contexts},
             """,
            },
            {
                "role": "system",
                "content": """You just have to return a single float value. The value should be between 0 and 1.""",
            },
        ],
    )
    return float(response)


def context_relevance(retrieved_context, query):
    """Assess the relevance of the retrieved context to the user's query."""
    response = query_openai(
        messages=[
            {
                "role": "system",
                "content": """
             We are evaluating a RAG Pipeline. You will get the retrieved_context and the user query.
             You need to calculate the context_relevance. The context_relevance is the 
             Assess the relevance of the retrieved context to the user's query.
            """,
            },
            {
                "role": "user",
                "content": f"""
             Retrieved Context: {retrieved_context},
             Query: {query},
             """,
            },
            {
                "role": "system",
                "content": """You just have to return a single float value. The value should be between 0 and 1.""",
            },
        ],
    )
    return float(response)


def context_entity_recall(retrieved_context, relevant_entities):
    """
    Determine the ability to recall relevant entities within the context.
    """
    response = query_openai(
        messages=[
            {
                "role": "system",
                "content": """
                We are evaluating a RAG Pipeline. You will get the retrieved_context and a list of relevant_entities.
                You need to calculate the context_entity_recall. The context_entity_recall is the
                Determine the ability to recall relevant entities within the context.
            """,
            },
            {
                "role": "user",
                "content": f"""
                Retrieved Context: {retrieved_context},
                Relevant Entities: {relevant_entities},
            """,
            },
            {
                "role": "system",
                "content": """You just have to return a single float value. The value should be between 0 and 1.""",
            },
        ],
    )
    return float(response)


def noise_robustness(api_function, noisy_queries, clean_queries):
    """Test the system's ability to handle noisy or irrelevant inputs."""
    noisy_results = [
        preprocess_markdown(api_function(query)) for query in noisy_queries
    ]
    clean_results = [
        preprocess_markdown(api_function(query)) for query in clean_queries
    ]

    response = query_openai(
        messages=[
            {
                "role": "system",
                "content": """
                We are evaluating a RAG Pipeline. You will get the noisy_results, clean_results and clean_queries.
                You need to calculate the noise_robustness. The noise_robustness is the
                Measure the robustness of the system against noisy queries.
            """,
            },
            {
                "role": "user",
                "content": f"""
                Noisy Results: {noisy_results},
                Clean Results: {clean_results},
                Clean Queries: {clean_queries},
            """,
            },
            {
                "role": "system",
                "content": """You just have to return a single float value. The value should be between 0 and 1.""",
            },
        ],
    )
    return float(response)


def generate_noisy_queries(queries):
    """Generate noisy versions of the input queries."""
    noisy_queries = []
    for query in queries:
        # Simulate typos
        noisy = "".join(c if np.random.random() > 0.1 else "" for c in query)
        # Add random Python-related terms
        python_terms = ["function", "class", "method", "list", "dict", "tuple"]
        noisy += " " + np.random.choice(python_terms)
        noisy_queries.append(noisy)
    return noisy_queries


def query_api(question, temperature=0.7, n_docs=10):
    """Query the API and return the markdown response."""
    url = f"http://localhost:8000/files/query?question={quote(question)}&temperature={temperature}&n_docs={n_docs}"
    response = requests.get(url, headers={"accept": "application/json"}, stream=True)
    response.raise_for_status()
    return response.text


def evaluate_retrieval_metrics(test_queries, ground_truth):
    results = {
        "context_precision": [],
        "context_recall": [],
        "context_relevance": [],
        "context_entity_recall": [],
    }

    # Calculate total steps (queries + 1 for noise robustness)
    total_steps = len(test_queries) + 1

    # Create progress bar
    progress_bar = tqdm(total=total_steps, desc="Calculating Retrieval metrics")

    # Main evaluation loop
    for query, truth in zip(test_queries, ground_truth, strict=False):
        retrieved_context = query_api(query)
        results["context_precision"].append(
            context_precision(query, retrieved_context, truth["relevant_contexts"])
        )
        results["context_recall"].append(
            context_recall(query, retrieved_context, truth["relevant_contexts"])
        )
        results["context_relevance"].append(context_relevance(retrieved_context, query))
        results["context_entity_recall"].append(
            context_entity_recall(retrieved_context, truth["relevant_entities"])
        )
        progress_bar.update(1)

    # Generate noisy queries and calculate noise robustness
    noisy_queries = generate_noisy_queries(test_queries)
    results["noise_robustness"] = noise_robustness(
        query_api, noisy_queries, test_queries
    )
    progress_bar.update(1)

    # Close the progress bar
    progress_bar.close()

    return {
        metric: round(np.mean(scores).item(), 2) for metric, scores in results.items()
    }
