"""
add projects downloads_per_day table
"""

from yoyo import step

__depends__ = {}

CREATE_DOWNLOADS_TABLE = """
    CREATE TABLE downloads_per_day (
        name VARCHAR(512) REFERENCES projects(name),
        date DATE NOT NULL,
        downloads INT NOT NULL
    )
"""

steps = [
    step(CREATE_DOWNLOADS_TABLE, "DROP TABLE downloads_per_day"),
]
