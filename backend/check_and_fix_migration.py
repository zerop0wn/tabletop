"""
Utility script to backfill critical schema changes for legacy databases.

Some production databases were created before Alembic migrations were
introduced, so this script performs the minimum ALTER TABLE statements
needed to keep them compatible with the current application models.
"""
from app.database import SessionLocal, engine
from sqlalchemy import inspect, text


def ensure_column(table_name: str, column_name: str, alter_statement: str) -> None:
    """Add the column via raw SQL if it does not already exist."""
    inspector = inspect(engine)
    columns = [col["name"] for col in inspector.get_columns(table_name)]

    print(f"Current columns in {table_name}: {columns}")

    if column_name in columns:
        print(f"✔ {column_name} already exists on {table_name}.")
        return

    print(f"Adding missing column {column_name} to {table_name}...")
    with engine.connect() as conn:
        conn.execute(text(alter_statement))
        conn.commit()
    print(f"✔ {column_name} added successfully.")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        ensure_column(
            "scenario_phase_artifacts",
            "team_role",
            "ALTER TABLE scenario_phase_artifacts ADD COLUMN team_role VARCHAR",
        )
        ensure_column(
            "scenario_phases",
            "gm_prompt_questions",
            "ALTER TABLE scenario_phases ADD COLUMN gm_prompt_questions JSONB",
        )
    finally:
        db.close()

