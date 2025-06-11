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

Generates embeddings and extracts details and summary:
```bash
poetry run python src/main.py
```

### 2. Start the web application

Launch the Streamlit app:

```bash
poetry run streamlit run src/web-app.py
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

- `src/main.py` — Downloads data, generates embeddings, extracts candidate details and summaries.
- `src/web-app.py` — Streamlit web interface for browsing candidates.
