from aiopg.sa import create_engine

__all__ = ["bootstrap"]

dbclient = None

def get_client():
    """
    Returns the database client initialized for the application.
    """
    global dbclient
    return dbclient


async def close_pg():
    global dbclient
    dbclient.close()
    await dbclient.wait_closed()


async def bootstrap(configuration, loop):
    """
    Creates the database client for the application.
    """
    global dbclient
    dbclient = await init_postgres(configuration["postgres"], loop)


async def init_postgres(conf, loop):
    """
    Initializes a database client for the application.
    """
    engine = await create_engine(
        database=conf["database"],
        user=conf["user"],
        password=conf["password"],
        host=conf["host"],
        port=conf["port"],
        minsize=conf["minsize"],
        maxsize=conf["maxsize"],
        loop=loop)
    return engine