# Candidate CV Summarizer

This application processes candidate resumes, generates summaries, and provides a Streamlit web interface to browse candidate profiles.

## Prerequisites

- Python 3.9+
- [Poetry](https://python-poetry.org/docs/#installation)
- PostgreSQL (for vector store)
- Ollama or OpenAI API key for embeddings and summaries

## Setup

1. **Clone the repository**
2. **Install dependencies:**
```bash
poetry install
```
3. **Set up environment variables:**
   - Configure your database connection and any required API keys in a `.env` file or as environment variables.
4. **Prepare the database:**
   - Ensure PostgreSQL is running and accessible.
   - The scripts will create tables as needed.

## Usage

### 1. Download and process resumes

Run the embedding and details extraction script:
```bash
poetry run python src/1-embeddings.py
```

### 2. Generate summaries

Run the summary generation script:

```bash
poetry run python src/2-summary.py
```

### 3. Start the web application

Launch the Streamlit app:

```bash
poetry run streamlit run src/3-web-app.py
```

Open the provided URL in your browser to view and interact with the candidate list.

## Debugging

1. **Enable Debug Mode**

   To enable debug mode call `enable_debug_mode()` at the top of the file.

2. **Start Phoenix UI**

   Run the following command to launch the Phoenix tracing dashboard:

   ```bash
   poetry run phoenix serve
   ```

## Project Structure

- `src/1-embeddings.py` — Downloads data, generates embeddings, extracts candidate details.
- `src/2-summary.py` — Generates summaries for each candidate.
- `src/3-web-app.py` — Streamlit web interface for browsing candidates.
