from aiohttp import web
from aiohttp_jinja2 import render_template
from app.responses import not_implemented
from app.handlers.areas import Area
from app.handlers.localization import get_best_culture
from bll.public.membership import PublicMembershipProvider

public = Area("public", membership_provider=PublicMembershipProvider())


@public
async def index(request):
    """
    Returns the main page of the public area.
    """
    return render_template("index.html", request, {})


@public
@public.auth()
async def account_dashboard(request):
    """
    This is an example to show how the authentication logic works and can be required.

    Since the method is decorated by public.auth, only authenticated users have access to this resource.
    Authentication logic is implemented inside the PublicMembershipProvider, from the business logic layer.
    """
    return web.Response(text="Hello World")


async def index_with_culture(request):
    """
    Redirects to the index page with culture information.
    """
    culture = request.match_info.get("culture")
    if not culture:
        culture = get_best_culture(request, area="public")
    return web.HTTPFound("/" + culture + "/")


@public
async def login(request):
    """
    Handles a login POST request for the public area of the application.
    """
    return not_implemented()


def setup_public_routes(app):
    # GET requests to pages should include a culture code: this is the most elegant solution for localization strategy
    # In production, the redirection should be performed by the HTTP Proxy server (not by aiohttp).
    # But at least during development, it's convenient to setup a redirection also in aiohttp.
    # Having a redirection handler also in aiohttp doesn't hurt anyway.
    #
    # Other kind of requests (POST, etc.) should instead read the culture from a custom header set in AJAX requests,
    # which allow for a simplified model.
    culture = "/{culture:\w{2}?}"
    app.router.add_get("/", index_with_culture)
    app.router.add_get(culture, index_with_culture)
    app.router.add_get(culture + "/", index)

    app.router.add_get(culture + "/account", account_dashboard)
    app.router.add_get(culture + "/account/", account_dashboard)

    app.router.add_post("/login", login)