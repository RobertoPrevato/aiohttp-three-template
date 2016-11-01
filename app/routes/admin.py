from aiohttp import web
from app.responses import not_implemented

async def dashboard(request):
    return web.Response(text="dashboard")


async def login(request):
    """
    Handles a post request for login to the administrative area.
    """
    return not_implemented()


def setup_admin_routes(app):
    prefix = "/admin"
    app.router.add_get(prefix, dashboard)
    app.router.add_get(prefix + "/", dashboard)
    app.router.add_post(prefix + "/login", login)
