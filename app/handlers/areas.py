"""
 Copyright 2016, Roberto Prevato roberto.prevato@gmail.com

 This module contains functions for the organization of code into logical areas.
"""
from functools import wraps, partial
from aiohttp.web import Request, HTTPFound, HTTPForbidden, HTTPUnauthorized
from app import configuration
from core import require_params
from core.encryption.aes import AesEncryptor
from .cookies import CookieToken
from .localization import get_text, get_best_culture, InvalidCultureException
from .security.antiforgery import issue_aft, validate_aft, InvalidAntiforgeryTokenException
request_context_key = "aiohttp_jinja2_context"


class Area:
    """
    Unlike the middleware, which is applied globally on an application object, Area is designed to be applied on groups
    of route handlers, to separate the application into logical areas.

    Area allows to specify localization strategy and membership logic for different areas of the application.
    For example, the public area of a website may be implemented in few languages, whereas the administrative area
    supports only one language.
    """
    def __init__(self, name, membership_provider=None, fallback_url=None):
        require_params(name=name)
        if not configuration.areas:
            raise RuntimeError("The configuration section 'areas' is not configured in the application configuration.")
        try:
            area_config = configuration.areas[name]
        except KeyError:
            raise RuntimeError("The '{}' area is not configured in the application configuration.".format(name))

        if membership_provider:
            # the area must define a session cookie key
            for property_name in {"session_cookie_name",
                                  "encryption_key"}:
                if not area_config.get(property_name):
                    raise RuntimeError("The '{}' area does not define its '{}'.".format(name, property_name))

        self.name = name
        self.fallback_url = fallback_url
        self.config = area_config
        self.secure_cookies = configuration.secure_cookies
        self.membership = membership_provider

    def get_fallback_url(self, request):
        """
        Returns the redirect url used for this area, when a redirection is required (due to an invalid url).
        For example, when a user types a non supported culture inside the page url culture parameter.
        """
        tail = self.fallback_url or "/"
        if not tail.startswith("/"):
            tail = "/" + tail
        return "/" + get_best_culture(request, self.name) + tail

    def auth(self, roles=None):
        """
        Requires authentication to access a resource.

        :param roles: sufficient roles (if None, simply requires a non-anonymous user).
        :return: decorated function.
        """
        area_name = self.name
        def decorator(f):
            # (The user of this function is not using it properly)
            @wraps(f)
            async def wrapped(request):
                # set the area property inside the request object
                try:
                    user = request.user
                except AttributeError:
                    # the user of this method is not using it in the intended way
                    raise RuntimeError("The 'user' property is not set in the request object."
                                       "Use the {0}.auth decorator after a '{0}' decorator".format(area_name))
                if not user or user.authenticated is False:
                    raise HTTPUnauthorized()

                if roles and not user.has_any_role(roles):
                    raise HTTPUnauthorized()
                return await f(request)
            return wrapped
        return decorator

    @staticmethod
    def get_client_ip(request):
        peername = request.transport.get_extra_info("peername")
        if peername is not None:
            host, port = peername
            return host
        return None

    async def before_request(self, request):
        """
        Applies the initial setup logic on a request object:
        authentication on the basis of area-logic; and selection of the request localization (the best language to serve
        the client)

        :param request: a new request object
        """
        # validate the antiforgery token, if necessary
        validate_aft(request)

        await self._authenticate_user(request)
        self._apply_localization(request)

        # set the request context key; used by Jinja2 Rendering engine (due to aiohttp-jinja2 implementation)
        # this grants access to information inside the templates
        request[request_context_key] = {
            "user": request.user,
            "culture": request.culture,
            "antiforgery": partial(issue_aft, request),
            "_": partial(get_text, request.culture)  # function for localization of strings inside template
        }

    async def initialize_anonymous_session(self, request: Request):
        """
        Initializes an anonymous session for the given request.

        :param request: incoming request to a resource that is related to this logical area.
        """
        client_ip = self.get_client_ip(request)
        result = await self.membership.initialize_anonymous_session(client_ip,
                                                                    client_data=request.headers.get("User-Agent"))

        # set a flag to set a session cookie
        session = result.session
        session_cookie_name = self.config.session_cookie_name
        encryption_key = self.config.encryption_key
        session_cookie_value = AesEncryptor.encrypt(str(session.guid), encryption_key)

        request.set_session_cookie = True
        request.cookies_to_set.append(CookieToken(session_cookie_name,
                                                  session_cookie_value,
                                                  httponly=True,
                                                  secure=self.secure_cookies))
        # store user and session information in the request object
        request.user = result.principal
        request.session = session

    async def _authenticate_user(self, request : Request):
        """
        If the area features membership, it invokes the methods of the underlying membership provider to authenticate
        the user, supporting anonymous authentication.

        :param request: request to authenticate.
        """
        request.user = None
        encryption_key = self.config.encryption_key
        membership = self.membership
        set_anonymous_session = False

        if self.membership:
            # does the request contains the session cookie for this area?
            session_cookie_name = self.config.session_cookie_name
            session_key = request.cookies.get(session_cookie_name)
            if session_key:
                # try to load the session
                # decrypt the session key
                success, session_guid = AesEncryptor.try_decrypt(session_key, encryption_key)
                if success:
                    # try to perform login by session key
                    success, result = await membership.try_login_by_session_key(session_guid)
                    if success:
                        # result is a principal object
                        request.user = result.principal
                        request.session = result.session
                    else:
                        # the login by session cookie failed: the session could be expired
                        set_anonymous_session = True
                else:
                    # session key decryption failed
                    set_anonymous_session = True
            else:
                # the request does not contain a session cookie for this area
                set_anonymous_session = True

        if set_anonymous_session:
            # initialize an anonymous session
            await self.initialize_anonymous_session(request)
        return self

    def get_default_culture(self):
        """
        Returns the default culture for this area.
        """
        if "default_culture" in self.config:
            return self.config.default_culture
        return configuration.default_culture

    def _is_supported_culture(self, culture):
        """
        Returns true if the given culture is supported for this area, false otherwise.

        :param culture: culture to check.
        :return: boolean
        """
        if not culture:
            return False
        cultures = self.config.cultures or configuration.cultures
        return culture in cultures

    def _get_culture_for_request(self, request):
        """
        Gets the culture to use for a given request.
        """
        if "GET" == request.method:
            culture = request.match_info.get("culture")
            if culture:
                if not self._is_supported_culture(culture):
                    # the given culture is not supported; the user could have changed a url by hand
                    # raise an exception to redirect to a proper url
                    raise InvalidCultureException()
                return culture

        user = request.user
        if user and not user.anonymous and self._is_supported_culture(user.culture):
            return user.culture

        if "POST" == request.method:
            # check custom headers
            culture_header = request.headers.get("X-Request-Culture")
            if self._is_supported_culture(culture_header):
                return culture_header

        culture_cookie = request.cookies.get("culture")
        if self._is_supported_culture(culture_cookie):
            return culture_cookie

    def _apply_localization(self, request):
        """
        Sets the best locale for the request object (used when preparing the response), applying the server side
        localization strategy.

        :param request: request for which the culture must be set.
        """
        request.culture = self._get_culture_for_request(request)
        return self

    def __call__(self, f):
        """
        Applies area initialization logic to a request handling function, for example by loading user session.

        :param f: the request handler to be decorated.
        :return: a wrapped request handler that loads user information.
        """
        @wraps(f)
        async def wrapped(request):
            # set the area property inside the request object
            request.area = self.name
            try:
                await self.before_request(request)
            except InvalidCultureException:
                # redirect to a proper url
                return HTTPFound(self.get_fallback_url(request))
            except InvalidAntiforgeryTokenException:
                raise HTTPForbidden()

            return await f(request)
        return wrapped
