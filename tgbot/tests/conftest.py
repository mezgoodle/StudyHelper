import os

import pytest


@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown_database():
    db_file_name = "database.db"
    if os.path.exists(db_file_name):
        os.remove(db_file_name)
    yield
    os.remove(db_file_name)
