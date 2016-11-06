import asyncio
import logging
import pathlib
import jinja2
import aiohttp_jinja2
from aiohttp import web
from app import configuration
from app.routes import setup_routes
from app.helpers.global_helpers import setup_global_helpers
from app.handlers.cookies import cookies_middleware
from dal import bootstrap as bootstrap_dal


PROJ_ROOT = pathlib.Path(__file__).parent


async def init(loop):
    # setup application and extensions
    app = web.Application(loop=loop)

    setattr(app, "config", configuration)
    # configure jinja 2 rendering engine
    aiohttp_jinja2.setup(app, loader=jinja2.PackageLoader("app", "templates"))
    setup_global_helpers(app)

    await bootstrap_dal(configuration, loop)

    # setup routes
    setup_routes(app, PROJ_ROOT)
    # setup middlewares
    app.middlewares.append(cookies_middleware)

    host, port = configuration.host, configuration.port
    return app, host, port


def main():
    # init logging
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    app, host, port = loop.run_until_complete(init(loop))
    web.run_app(app, host=host, port=port)


if __name__ == "__main__":
    main()