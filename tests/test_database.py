from app.database import get_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.database import Base
import pytest


def test_get_session():
    result = get_session()
    assert isinstance(result, Session)
    assert result.bind.url.drivername == "mysql+pymysql"