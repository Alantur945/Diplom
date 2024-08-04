# создаем движок SqlAlchemy
# from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
# from sqlalchemy import create_engine
# from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


# import config


# engine = create_async_engine(url=config.SQLALCHEMY_DATABASE_URL, echo=True)
# sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

# def create_sync_engine():
#     engine = create_engine(url=config.DB_SYNC_DRIVER + config.DB_URL)    
#     return engine


# engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
# Session = async_sessionmaker(engine, expire_on_commit=False)

# #создаем базовый класс для моделей
# class Model(DeclarativeBase): pass

# async def create_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Model.metadata.create_all)

# async def delete_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Model.metadata.drop_all)