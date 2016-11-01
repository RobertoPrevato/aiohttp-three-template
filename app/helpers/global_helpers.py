from datetime import datetime
from aiohttp_jinja2 import get_env
from .resources import resources

def setup_global_helpers(app):
    env = get_env(app)
    conf = app.config
    # set global helpers for Jinja 2
    def get_copy():
        """
        Returns the copyright string for the application.
        """
        now = datetime.now()
        return "Copyright &copy; {} {}".format(now.year, conf.site.copyright)

    def antiforgery():
        """
        Returns an antiforgery-token.
        """
        return "TODO"

    def res(*args):
        return resources(args,
                         development=conf.development,
                         cache_seed=conf.cache_seed)

    helpers = {
        "copy": get_copy,
        "antiforgery": antiforgery,
        "resources": res
    }

    env.globals.update(helpers)
