"""
* Copyright 2016, Roberto Prevato roberto.prevato@gmail.com
* https://github.com/RobertoPrevato/aiohttp-three-template
*
* AJAX decorator: enforces AJAX requests to access a resource.
*
* Licensed under the MIT license:
* http://www.opensource.org/licenses/MIT
"""
from functools import wraps
from app.requests import is_ajax
from aiohttp.web import HTTPNotFound


def ajax(f):
    """
    Enforces the use of AJAX requests to access a resource. (Raises HTTPNotFound otherwise)
    """
    @wraps(f)
    async def wrapped(request):
        if not is_ajax(request):
            raise HTTPNotFound()

        return await f(request)
    return wrapped