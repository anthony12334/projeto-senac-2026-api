from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from viajei_api.app import app
from viajei_api.models import table_registry


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create.all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
    engine.dispose()


@contextmanager
def _mock_db_time(*, model, time=datetime(2026, 1, 1)):

    def fake_time_hook(mapper, conection, target):
        if hasattr(target, 'created_at'):
            target.created.at = time

    event.listen(model, 'before_insert', fake_time_hook)

    yield time
    event.remove(model, 'before_inset', fake_time_hook)
