"""
 Copyright 2016, Roberto Prevato roberto.prevato@gmail.com

 This module contains utility functions to set cookies. The request object is extended with two lists:
 cookies_to_set and cookies_to_unset; which are used after the preparation of the response to add or delete cookies.
"""
from core import require_params


class CookieToken:
    def __init__(self, name, value, path="/", expires=None, domain=None, max_age=None, secure=None, httponly=None):
        require_params(name=name, value=value)
        if isinstance(value, bytes):
            value = value.decode("utf-8")
        self.name = name
        self.value = value
        self.path = path
        self.expires = expires
        self.domain = domain
        self.max_age = max_age
        self.secure = secure
        self.httponly = httponly


async def cookies_middleware(app, handler):
    async def cookies_middleware_handler(request):
        # sets arrays in the request object, that can be manipulated to insert or remove cookies for the response.
        request.cookies_to_set = []
        request.cookies_to_unset = []
        response = await handler(request)

        for to_set in request.cookies_to_set:
            response.set_cookie(to_set.name,
                                to_set.value,
                                path=to_set.path,
                                expires=to_set.expires,
                                domain=to_set.domain,
                                max_age=to_set.max_age,
                                secure=to_set.secure,
                                httponly=to_set.httponly,
                                version=None)

        for to_unset in request.cookies_to_unset:
            if isinstance(to_unset, str):
                response.del_cookie(to_unset)
            if isinstance(to_unset, CookieToken):
                response.del_cookie(to_unset.name)
            raise RuntimeError("Cookies to unset must be of str or CookieToken type.")

        return response
    return cookies_middleware_handler