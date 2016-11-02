from .public import setup_public_routes
from .admin import setup_admin_routes


def setup_routes(app, project_root):
    setup_public_routes(app)
    setup_admin_routes(app)

    # TODO: setting a route for static files should be done only during development.
    # In a production environment, static files are normally
    # served by an HTTP Proxy server like Nginx (or Apache, or IIS, etc.)
    app.router.add_static("/",
                          path=str(project_root / "static"),
                          name="static")