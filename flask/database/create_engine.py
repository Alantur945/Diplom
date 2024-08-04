from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import create_engine

import config

engine = create_engine(url=config.SQLALCHEMY_DATABASE_URL)    
   