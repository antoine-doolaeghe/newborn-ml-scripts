import os
import tempfile

import pytest

from newborn_communicator_api import newborn_communicator


@pytest.fixture
def client():
    db_fd, newborn_communicator.app.config['DATABASE'] = tempfile.mkstemp()
    newborn_communicator.app.config['TESTING'] = True
    client = newborn_communicator.app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(newborn_communicator.app.config['DATABASE'])


def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/run')
    assert b'No entries here so far' in rv.data
