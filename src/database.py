import os

import psycopg2
from dotenv import load_dotenv
from llama_index.vector_stores.postgres import PGVectorStore
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

load_dotenv()

db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASS")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")


def get_database_connection(db_name=None):
    return psycopg2.connect(
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
        dbname=db_name,
    )


def create_database():
    conn = get_database_connection()
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    with conn.cursor() as c:
        # Terminate other connections
        c.execute(
            f"""
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity
            WHERE datname = '{db_name}' AND pid <> pg_backend_pid();
        """
        )

        # Recreate the database
        c.execute(f"DROP DATABASE IF EXISTS {db_name}")
        c.execute(f"CREATE DATABASE {db_name}")

    conn.close()


def get_pg_vector_store(table_name: str = "embeddings"):
    return PGVectorStore.from_params(
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_user,
        password=db_password,
        table_name=table_name,
        embed_dim=1536,  # nomic=768, openai=1536
        hnsw_kwargs={
            "hnsw_m": 16,
            "hnsw_ef_construction": 64,
            "hnsw_ef_search": 40,
            "hnsw_dist_method": "vector_cosine_ops",
        },
    )


def create_candidates_table():
    conn = get_database_connection(db_name)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS candidates (
            file_name TEXT PRIMARY KEY,
            name TEXT,
            profession TEXT,
            years_of_experience INT,
            summary TEXT
        )
    """
    )
    conn.commit()
    cur.close()
    conn.close()


def save_candidate_details(data):
    conn = get_database_connection(db_name)
    cur = conn.cursor()

    cur.execute(
        """
            INSERT INTO candidates (file_name, name, profession, years_of_experience)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (file_name) DO UPDATE
            SET name = EXCLUDED.name,
                profession = EXCLUDED.profession,
                years_of_experience = EXCLUDED.years_of_experience
        """,
        (
            data.get("file_name"),
            data.get("name"),
            data.get("profession"),
            data.get("years_of_experience"),
        ),
    )

    conn.commit()
    cur.close()
    conn.close()


def get_candidates():
    conn = get_database_connection(db_name)
    cur = conn.cursor()
    cur.execute(
        "SELECT file_name, name, profession, years_of_experience FROM candidates"
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return rows


def update_candidate_summary(file_name, summary):
    conn = get_database_connection(db_name)
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE candidates
        SET summary = %s
        WHERE file_name = %s
        """,
        (summary, file_name),
    )
    conn.commit()
    cur.close()
    conn.close()


def get_candidate_details(file_name):
    conn = get_database_connection(db_name)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT name, profession, years_of_experience, summary
        FROM candidates
        WHERE file_name = %s
        """,
        (file_name,),
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return {
            "name": row[0],
            "profession": row[1],
            "years_of_experience": row[2],
            "summary": row[3],
        }
    return None
