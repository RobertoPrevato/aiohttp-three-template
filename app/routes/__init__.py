from .public import setup_public_routes
from .admin import setup_admin_routes
from app import configuration


def setup_routes(app, project_root):
    setup_public_routes(app)
    setup_admin_routes(app)

    if configuration.serve_static:
        # the application server is also used to serve static files
        # this is commonly true during development, while in a production environment static files are usually
        # served by an HTTP Proxy server like Nginx (or Apache, or IIS, Kestrel, etc.)
        app.router.add_static("/",
                              path=str(project_root / "static"),
                              name="static")