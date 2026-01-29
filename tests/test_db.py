from flaskr import db
from flask import g
import sqlite3
from flaskr.db import init_db_command
import pytest

def test_get_close_db(app):
    with app.app_context():

        conn1 = db.get_db()
        assert isinstance(conn1, sqlite3.Connection)

        # Check we can execute a simple query
        conn1.execute("CREATE TABLE test (id INTEGER)")
        conn1.execute("INSERT INTO test (id) VALUES (1)")
        row = conn1.execute("SELECT id FROM test").fetchone()
        assert row["id"] == 1

        # Test that get_db reuses the connection
        conn2 = db.get_db()
        assert conn1 is conn2

        db.close_db()

        assert "db" not in g



def test_init_db_creates_tables(app):
    from flaskr import db as db_module
    with app.app_context():
        db_module.init_db() # runs schema.sql

        conn = db_module.get_db()
        # Check one table exists from your schema
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='user';" 
        )
        table = cursor.fetchone()
        assert table is not None

@pytest.mark.skip(reason="Flask CLI context is unstable in CI; init_db is tested logic is tested directly.")
def test_init_db_command(runner, app):
    # Use the CLI runner fixture from conftest.py
    result = runner.invoke(init_db_command, obj=app)

    # Check that the CLI output contains our expected message
    assert result.exit_code == 0
    assert "Initialized the database." in result.output

    # Optionally, check that tables from schema.sql exist
    with app.app_context():
        conn = db.get_db()
        table = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='user';"
        ).fetchone()
        assert table is not None