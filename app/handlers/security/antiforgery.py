"""
* Copyright 2016, Roberto Prevato roberto.prevato@gmail.com
* https://github.com/RobertoPrevato/aiohttp-three-template
*
* AntiForgeryToken implementation using the double token strategy, session based
* (generated tokens are session specific).
*
* Licensed under the MIT license:
* http://www.opensource.org/licenses/MIT
"""
import uuid
from core.encryption.aes import AesEncryptor
from app.handlers.cookies import CookieToken
from app import configuration

__all__ = ["InvalidAntiforgeryTokenException", "validate_aft", "issue_aft"]

header_name = "X-AFT"
form_name = "aft"
cookie_name = "aftck"


class InvalidAntiforgeryTokenException(Exception):
    """
    Exception risen when the AFT validation fails.
    """

# request methods ignored for antiforgery validation
AFT_IGNORE_METHODS = {"GET", "OPTIONS", "HEAD"}


def validate_aft(request):
    """
    Validates the AFT of a given request.
    Utilizes dual token strategy (session based encrypted token, issued in both cookie and page);
    sent at each request in both cookie and request header, for ajax requests or form values.
    """
    # ignore get, options, head
    if request.method in AFT_IGNORE_METHODS:
        return

    # requires the request to have a session
    if not request.session:
        raise RuntimeError("Missing session inside the request object; cannot issue an AFT without session.")
    # expect the request session to have a guid
    encryption_key = request.session.guid

    # get the tokens: one is always in the cookie; the second may be inside form or request header
    # request header is more important, assuming that pages implement AJAX requests, rather than form submission
    cookie_token = request.cookies.get(cookie_name)
    second_token = request.headers[header_name] if header_name in request.headers else None

    if second_token is None:
        # try to read from form
        second_token = request.form[form_name] if form_name in request.form else None

    # are the tokens present?
    if not cookie_token or not second_token:
        raise InvalidAntiforgeryTokenException()

    # decrypt the tokens; decryption will fail if the tokens were issued for another session;
    a, cookie_token = AesEncryptor.try_decrypt(cookie_token, encryption_key)
    b, second_token = AesEncryptor.try_decrypt(second_token, encryption_key)

    if not a or not b or not cookie_token or not second_token:
        raise InvalidAntiforgeryTokenException()

    # are the tokens identical?
    if cookie_token != second_token:
        raise InvalidAntiforgeryTokenException()


def issue_aft(request):
    """
    Issues a new session based antiforgery token.

    This solution implements the double token strategy: the same antiforgery token is serialized twice,
    hence producing two different encrypted strings. One is set as response cookie; one is returned to be rendered
    inside the html view.
    """
    # check if the session is defined inside the request
    if not hasattr(request, "session"):
        # missing session context; use the AntiforgeryValidate after the membership provider
        raise ValueError("missing session context")
    encryption_key = str(request.session.guid)

    cookie_token = request.cookies.get(cookie_name)
    if not cookie_token:
        #define a new token
        cookie_token = uuid.uuid1()
    else:
        can_decrypt, value = AesEncryptor.try_decrypt(cookie_token, encryption_key)
        if not can_decrypt:
            cookie_token = uuid.uuid1()
        else:
            # use the same value of before
            cookie_token = value

    # will set a new cookie in the response object
    cookie_token = str(cookie_token)
    encrypted_token = AesEncryptor.encrypt(cookie_token, encryption_key)
    # the cookie will be set in response object inside global_handlers function
    request.cookies_to_set.append(CookieToken(cookie_name,
                                              encrypted_token.decode("utf-8"),
                                              httponly=True,
                                              secure=configuration.secure_cookies))

    # return the token encrypted with AES; many calls always return a different value
    v = AesEncryptor.encrypt(cookie_token, encryption_key)
    return v.decode("utf-8")
