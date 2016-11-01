

async def close_pg(app):
    app["db"].close()
    await app["db"].wait_closed()


def bootstrap(app, loop):
    # create connection to the database
    #db = await init_postgres(conf["postgres"], loop)
    #app["db"] = db # ??
    pass


async def init_db(conf, loop):
    pass
    """
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
        loop=loop)
    return engine
    """