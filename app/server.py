import asyncio
import logging
import pathlib
import jinja2
import aiohttp_jinja2
from aiohttp import web
from core.configuration import Configuration
from app.routes import setup_routes
from app.helpers.global_helpers import setup_global_helpers
from dal import bootstrap as bootstrap_dal


PROJ_ROOT = pathlib.Path(__file__).parent


async def init(loop):
    # load config from yaml file in current dir
    conf = Configuration.from_yaml(str(pathlib.Path(".") / "config.yaml"))

    # setup application and extensions
    app = web.Application(loop=loop)

    setattr(app, "config", conf)
    aiohttp_jinja2.setup(app, loader=jinja2.PackageLoader("app", "templates"))
    setup_global_helpers(app)

    bootstrap_dal(app, loop)

    # setup routes
    setup_routes(app, PROJ_ROOT)
    # TODO
    #setup_middlewares(app)

    host, port = conf.host, conf.port
    return app, host, port


def main():
    # init logging
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    app, host, port = loop.run_until_complete(init(loop))
    web.run_app(app, host=host, port=port)


if __name__ == "__main__":
    main()