from datetime import datetime
from aiohttp_jinja2 import get_env
from .resources import resources
from app import configuration


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

    def res(*args):
        return resources(args,
                         development=conf.development,
                         cache_seed=conf.cache_seed)

    try:
        ga_token = configuration.google_analytics
    except KeyError:
        ga_token = None

    def google_analytics():
        return ga_token

    helpers = {
        "copy": get_copy,
        "google_analytics": google_analytics,
        "resources": res
    }

    env.globals.update(helpers)
