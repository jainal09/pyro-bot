# Evaluation Metrics


https://github.com/user-attachments/assets/16fe6f14-dffe-48f4-8a0f-0df5f4348fa5


## Generating Evaluation Metrics

### Environment Setup

1. cd into the `evaluation_metrics` directory.
```bash
cd evaluation_metrics
```
2. Install the required packages.
```bash
poetry install
```
3. Activate the virtual environment.
```bash
poetry shell
```
### Environment Variables
1. Create a `openai.env` file in this `evaluation_metrics` directory.
2. Add the following environment variables to the `openai.env` file.
```bash
API_KEY=YOUR_OPENAI_API_KEY
AZURE_ENDPOINT=YOUR_AZURE_ENDPOINT
API_VERSION=2024-02-01
AZURE_DEPLOYMENT=YOUR_AZURE_DEPLOYMENT
```
### Running the Evaluation Script
1. Get Back to the root directory.
> Make sure the virtual environment is activated for the `evaluation_metrics` directory before cd'ing back to the root directory.
```bash
cd ..
```
2. Run the evaluation script.
```bash
python -m evaluation_metrics.calculate_metrics
```
## Retrieval Martrics

| Metric                | Description                                                                            | Value |
|-----------------------|----------------------------------------------------------------------------------------|-------|
| Context Precision     | Measures the proportion of relevant context among the retrieved context                | 0.84  |
| Context Recall        | Measures the proportion of relevant context that is successfully retrieved             | 0.84  |
| Context Relevance     | Assesses the relevance of the retrieved context to the given query or information need | 0.85  |
| Context Entity Recall | Measures the proportion of relevant entities that are successfully retrieved           | 0.69  |
| Noise Robustness      | Evaluates the ability of the retrieval system to handle noisy or irrelevant context    | 0.64  |


## Generation Metrics

| Metric                    | Description                                                                             | Value   |
|---------------------------|-----------------------------------------------------------------------------------------|---------|
| Faithfulness              | Measure the accuracy and reliability of the generated answers.                          | 0.76    |
| Answer Relevance          | Evaluate the relevance of the generated answers to the user's query.                    | 0.87    |
| Information Integration   | Assess the ability to integrate and present information cohesively.                     | 0.8     |
| Counterfactual Robustness | Test the robustness of the system against counterfactual or contradictory queries.      | 0.52    |
| Negative Rejection        | Measure the system's ability to reject and handle negative or inappropriate queries.    | 1       |
| Latency                   | Measure the response time of the system from receiving a query to delivering an answer. | 0.15 ms |



