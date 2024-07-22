from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

from openagent.conf.env import settings
from openagent.db.models import Base

url = settings.DB_CONNECTION

if not database_exists(url):
    create_database(url)
engine = create_engine(url, connect_args={"options": "-c timezone=utc"})
Base.metadata.create_all(bind=engine)  # type: ignore

DBSession = sessionmaker(bind=engine)
