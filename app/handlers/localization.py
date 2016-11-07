"""
 Copyright 2016, Roberto Prevato roberto.prevato@gmail.com

 This module contains functions for the server side localization strategy.
 It includes functions to support different cultures for each application area (e.g. public area, admin area, etc.).

 The recognized standard to implement localization in Python application is using Babel http://babel.pocoo.org.
 However, using Babel requires knowledge that is outside of the scope of this project template (extraction, compilation,
 babel.cfg, etc.).
 Therefore in this project template is shown a simpler model, supporting only scoped translations and demonstrating
 the implementation of a custom Jinja2 helper to obtain localized strings.
"""
from app.translations.regional import regional
from core.exceptions import ArgumentNullException


def get_text(language, key, default=None):
    if not language:
        raise ArgumentNullException("language")

    if language not in regional:
        return "Missing regional for `{}`".format(language)

    reg = regional[language]
    parts = key.split(".")
    v = reg
    for part in parts:
        if part not in v:
            return "Missing translation for `{}`".format(key) if default is None else default
        v = v[part]
    return v


class InvalidCultureException(Exception):
    """
    Exception risen when a GET request has an invalid culture.
    """


def parse_accept_language(value):
    languages = value.split(",")
    locale_q_pairs = []
    for language in languages:
        if language.split(";")[0] == language:
            # no q => q = 1
            locale_q_pairs.append((language.strip(), "1"))
    else:
        locale = language.split(";")[0].strip()
        q = language.split(";")[1].split("=")[1]
        locale_q_pairs.append((locale, q))
    return locale_q_pairs


def get_best_culture(request, area):
    """
    Returns the best default culture to serve a client.
    It checks the accept-culture header of the request, if present; and compares it with the application's supported
    cultures. It fallbacks to the area default culture or the application global default culture.

    :param request: request object.
    :param area: the name of the application area.
    :return: default culture.
    """
    app = request.app
    config = app.config
    area = config.areas[area]
    if not area:
        raise RuntimeError("The area '{}' is not configured in the application configuration file.".format(area))

    supported_cultures = area.cultures
    try:
        default_culture = area.get("default_culture", config.default_culture)
    except KeyError:
        # default_culture is not configured neither for area nor global configuration.
        raise RuntimeError("Cannot determine the default culture for area {}."
                           "Either configure an area default_culture or a global default_culture".format(area))
    accept_language = request.headers.get("Accept-Language")
    if not accept_language:
        # the request does not include an Accept-Language header; so we can only return our default culture.
        return default_culture

    client_languages = parse_accept_language(accept_language)
    for language, _ in client_languages:
        if language in supported_cultures:
            return language
        # no language was found, try again but considering only the first part of strings (language without full locale)
        if "-" in language:
            part_without_locale = language.split("-")[0]
            if part_without_locale in supported_cultures:
                return part_without_locale
    return default_culture
