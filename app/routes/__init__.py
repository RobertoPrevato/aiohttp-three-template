from .public import setup_public_routes
from .admin import setup_admin_routes


def setup_routes(app, project_root):
    setup_public_routes(app)
    setup_admin_routes(app)
    app.router.add_static("/",
                          path=str(project_root / "static"),
                          name="static")