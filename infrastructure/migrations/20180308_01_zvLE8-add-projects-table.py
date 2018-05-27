"""
add projects table
"""

from yoyo import step

__depends__ = {}

steps = [
    step("CREATE TABLE projects (name VARCHAR(512) PRIMARY KEY, downloads INT)", "DROP TABLE projects"),
]
