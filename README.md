# calypso

**Calypso** is an AI-powered assistant that replicates the workflows of a data scientist. It enables users to chat with a bot that performs data analysis, classification, forecasting, sentiment analysis, and more—all through natural language. This project is aimed at demonstrating the end-to-end ML lifecycle with modern MLOps practices.

---

## Tech Stack

- **Frontend:** Streamlit (MVP), React + TypeScript (future)
- **Backend:** FastAPI, Python 3.10+
- **LLM Agent Framework:** LangChain, LangGraph
- **Experiment Tracking:** Weights & Biases (W&B)
- **Observability / Tracing:** Braintrust

---

## Machine Learning Lifecycle

Calypso covers the full ML lifecycle:

1. **Problem Scoping:**
   - Natural language to: SQL, EDA, forecasting, classification, sentiment, visualization

2. **Data Curation & Preprocessing:**
   - Dataset ingestion from CSV or SQL
   - Cleaning, transformation, feature engineering

3. **Modeling & Fine-Tuning:**
   - Use of pre-trained models with SFT and RL
   - Support for classical models (e.g., Prophet, XGBoost) and LLMs

4. **Evaluation:**
   - Modular eval scripts with test cases and scoring functions
   - Auto-eval using GPT-as-judge, accuracy checks, semantic evals

5. **Deployment:**
   - FastAPI backend containerized with Docker
   - GCP Cloud Run or Hugging Face Spaces deployment

6. **Monitoring & Iteration:**
   - Braintrust traces and logs
   - W&B for training/eval metrics
   - Setup for continuous improvement and model retraining

---

## Project Structure

```
calypso/
├── api/                      # FastAPI app for model serving
├── agent/                    # LangChain/LLM agent logic
├── data/                     # Sample datasets and data loading utils
├── eval/                     # Evaluation metrics and test cases
├── notebooks/                # Prototyping and experiments
├── ui/                       # Streamlit app (MVP frontend)
├── scripts/                  # Training, tuning, and batch jobs
├── tests/                    # Unit and integration tests
├── Dockerfile                # Container definition
├── .env.example              # Environment variable template
├── README.md                 # You are here
└── requirements.txt          # Python dependencies
```

---

## Key Features

### Natural Language Interface
- Ask questions like: *"Show me revenue by region for 2023"*
- LLM translates to SQL/Pandas and returns result with chart/table

### Forecasting & Classification
- Built-in models for time-series forecasting and binary/multiclass classification
- Supports Prophet, XGBoost, scikit-learn, and LLM classifiers

### Sentiment Analysis & Text Tasks
- Detect tone and polarity of text data using LLMs

### Evaluation Loop
- Modular eval suite with JSON test cases
- Tracks performance across SFT and RL iterations with W&B

### MLOps & Monitoring
- All model runs, metrics, and artifacts tracked with W&B
- Braintrust logs for real-time inspection and LLM traceability

---

## Running Locally

### Prerequisites
- Python 3.10+
- uv (Python package manager)
- Docker (optional, for deployment)
- Weights & Biases account

#### Installing uv

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Alternative (using pip):**
```bash
pip install uv
```

#### Initialize and run the app

```bash
# Clone repo
$ git clone https://github.com/danielruales/calypso.git
$ cd calypso

# Create virtual environment
$ uv venv
$ source .venv/bin/activate

# Install dependencies
$ uv sync

# Run Streamlit app
$ streamlit run ui/app.py
```

---

## Scripts & Tasks

- `scripts/train_sft.py` – Supervised fine-tuning script
- `scripts/reward_tuning.py` – Reinforcement Learning with human feedback (RLHF)
- `scripts/eval.py` – Evaluation runner with multiple test cases
- `scripts/trace_agent.py` – Log agent traces to Braintrust

---

## Future Considerations

- The agent should eventually have a memory to remember the user's prefered styles.
- The agent could benefit from a cache of previous questions and answers to avoid recacling the same question.
- More complex database structures would need more advanced metadata and potential RAG solutions to answer questions effectively.
- A deep research agent could be added for more open ended and complex questions.