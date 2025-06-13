# Candidate CV Summarizer

This application processes candidate resumes, generates summaries, and provides a Streamlit web interface to browse candidate profiles.

## Setup

1. Clone the repository
2. Copy `.env.example` file to `.env` and update values.
3. Run docker compose to build and start the application:
   ```bash
   docker compose up
   ```
4. Open [http://localhost:8501/](http://localhost:8501/) in your browser to view and interact with the candidate list.

## Project Structure

- `src/main.py` — Downloads data, generates embeddings, extracts candidate details and summaries.
- `src/web-app.py` — Streamlit web interface for browsing candidates.
