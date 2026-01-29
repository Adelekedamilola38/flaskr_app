import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db
# from flaskr.db import init_db


with open(os.path.join(os.path.dirname(__file__), "..", "flaskr", "schema.sql")) as f:
    _schema_sql = f.read()


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        "TESTING": True,
        "DATABASE": db_path,
    })

    

    with app.app_context():
        get_db().executescript(_schema_sql)

        
    # or initialize database instead of reading db schema file
    # with flaskr.app_context():
    #      init_db()

    yield app


    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()