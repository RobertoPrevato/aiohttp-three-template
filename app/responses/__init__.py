from aiohttp import web

PLAIN_TYPE = "text/plain"
JSON_TYPE = "application/json"


def not_implemented():
    return web.Response(text="Not implemented",
                        status=500,
                        content_type=PLAIN_TYPE)


def bad_request():
    return web.Response(text="Bad request",
                        status=400,
                        content_type=PLAIN_TYPE)


def unauthorized():
    return web.Response(text="Unauthorized",
                        status=401,
                        content_type=PLAIN_TYPE)


def forbidden():
    return web.Response(text="Forbidden",
                        status=403,
                        content_type=PLAIN_TYPE)


def not_found():
    return web.Response(text="Not found",
                        status=404,
                        content_type=PLAIN_TYPE)


def not_modified():
    return web.Response(text="Not mofidifed",
                        status=304,
                        content_type=PLAIN_TYPE)



