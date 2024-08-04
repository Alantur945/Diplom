from sqlalchemy.orm import declarative_base

Base = declarative_base()


def generate_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)