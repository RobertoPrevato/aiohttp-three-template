from aiohttp import web
from aiohttp_jinja2 import render_template
from app.responses import not_implemented


async def index(request):
    """
    Returns the main page.
    """
    return render_template("index.html", request, {})


async def login(request):
    """
    Handles a login POST request for the public area of the application.
    """
    return not_implemented()


def setup_public_routes(app):
    app.router.add_get("/", index)
    app.router.add_post("/login", login)