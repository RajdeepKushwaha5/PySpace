import sqlite3
from pathlib import Path
from .utils import logger


class WorkspaceManager:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS workspaces (
                    id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE NOT NULL,
                    path TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            logger.info("Initialized workspace database")

    def create_workspace(self, name: str, path: str):
        with sqlite3.connect(self.db_path) as conn:
            try:
                conn.execute(
                    "INSERT INTO workspaces (name, path) VALUES (?, ?)", (name, path)
                )
                conn.commit()
                logger.info(f"Created workspace '{name}' at {path}")
                return True
            except sqlite3.IntegrityError:
                logger.error(f"Workspace '{name}' already exists")
                return False

    def list_workspaces(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT name, path, created_at FROM workspaces")
            return [
                {"name": row[0], "path": row[1], "created_at": row[2]}
                for row in cursor.fetchall()
            ]

    def get_workspace(self, name: str):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT path FROM workspaces WHERE name = ?", (name,))
            row = cursor.fetchone()
            return row[0] if row else None

    def delete_workspace(self, name: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM workspaces WHERE name = ?", (name,))
            conn.commit()
            logger.info(f"Deleted workspace '{name}'")
