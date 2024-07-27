import time
from urllib.parse import quote

import numpy as np
import requests
from evaluation_metrics.open_ai_service import query_openai
from evaluation_metrics.retrieval_metrics import preprocess_markdown, query_api as query_rag
from tqdm import tqdm


def query_api(question, temperature=0.7, n_docs=10):
    """Query the API and return the markdown response and latency."""
    start_time = time.time()
    response = query_rag(question, temperature=temperature, n_docs=n_docs)
    latency = time.time() - start_time
    return preprocess_markdown(response), latency

def faithfulness(generated_answer, ground_truth):
    """Measure the accuracy and reliability of the generated answers."""
    response = query_openai(
        messages=[
            {
                "role": "system",
                "content": """
                We are evaluating a RAG Pipeline. You will get the generated_answer and ground_truth.
                You need to calculate the faithfulness. The faithfulness is the degree to which the generated answer \
                matches the ground truth.
            """,
            },
            {
                "role": "user",
                "content": f"""
                Generated Answer: {generated_answer},
                Ground Truth: {ground_truth},
            """,
            },
            {
                "role": "system",
                "content": """You just have to return a single float value. The value should be between 0 and 1.""",
            },
        ],
    )
    return float(response)


def answer_relevance(generated_answer, query):
    """Evaluate the relevance of the generated answers to the user's query."""
    response = query_openai(
        messages=[
            {
                "role": "system",
                "content": """
                We are evaluating a RAG Pipeline. You will get the generated_answer and query.
                You need to calculate the answer_relevance. The answer_relevance is the degree to which the generated \
                answer is relevant to the user's query.
            """,
            },
            {
                "role": "user",
                "content": f"""
                Generated Answer: {generated_answer},
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

def information_integration(generated_answer):
    """Assess the ability to integrate and present information cohesively."""
    response = query_openai(
        messages=[
            {
                "role": "system",
                "content": """
                We are evaluating a RAG Pipeline. You will get the generated_answer.
                You need to calculate the information_integration. The information_integration is the ability to \
                integrate and present information cohesively.
            """,
            },
            {
                "role": "user",
                "content": f"""
                Generated Answer: {generated_answer},
            """,
            },
            {
                "role": "system",
                "content": """You just have to return a single float value. The value should be between 0 and 1.""",
            },
        ],
    )
    return float(response)

def counterfactual_robustness(api_function, original_query, counterfactual_query):
    """Test the robustness of the system against counterfactual or contradictory queries."""
    original_answer, _ = api_function(original_query)
    counterfactual_answer, _ = api_function(counterfactual_query)

    response = query_openai(
        messages=[
            {
                "role": "system",
                "content": """
                We are evaluating a RAG Pipeline. You will get the original_answer, counterfactual_answer and the \
                original_query.
                You need to calculate the counterfactual_robustness. The counterfactual_robustness is the ability of \
                the system to handle counterfactual or contradictory queries.
            """,
            },
            {
                "role": "user",
                "content": f"""
                Original Answer: {original_answer},
                Counterfactual Answer: {counterfactual_answer},
                Original Query: {original_query},
            """,
            },
            {
                "role": "system",
                "content": """You just have to return a single float value. The value should be between 0 and 1.""",
            },
        ],
    )

    return float(response)

def negative_rejection(api_function, negative_query):
    """Measure the system's ability to reject and handle negative or inappropriate queries."""
    answer, _ = api_function(negative_query)
    return answer.strip().lower() == "i can't answer this question."




def evaluate_generation_metrics(test_queries, ground_truth, counterfactual_queries, negative_queries):
    results = {
        'faithfulness': [],
        'answer_relevance': [],
        'information_integration': [],
        'counterfactual_robustness': [],
        'negative_rejection': [],
        'latency': []
    }

    # Calculate total steps (queries + 1 for noise robustness)
    total_steps = len(test_queries) + len(counterfactual_queries) + len(negative_queries)

    # Create progress bar
    progress_bar = tqdm(total=total_steps, desc="Calculating Generation Metrics", unit="step")

    for query, truth in zip(test_queries, ground_truth, strict=False):
        generated_answer, latency = query_api(query)

        results['faithfulness'].append(faithfulness(generated_answer, truth))
        results['answer_relevance'].append(answer_relevance(generated_answer, query))
        results['information_integration'].append(information_integration(generated_answer))
        results['latency'].append(latency)
        progress_bar.update(1)

    for original, counterfactual in counterfactual_queries:
        results['counterfactual_robustness'].append(
            counterfactual_robustness(query_api, original, counterfactual)
        )
        progress_bar.update(1)

    for negative_query in negative_queries:
        results['negative_rejection'].append(
            negative_rejection(query_api, negative_query)
        )
        progress_bar.update(1)



    return {metric: round(np.mean(scores).item(), 2) for metric, scores in results.items()}
