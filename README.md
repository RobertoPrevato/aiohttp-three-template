# aiohttp-three-template
Project template for Python aiohttp three-tier web applications

[![Homepage](https://robertoprevato.github.io/demos/aiohttp-template/homepage.png)](https://robertoprevato.github.io/demos/aiohttp-template/homepage.png)

## Features
* Project skeleton ready to use, to start a three tier web application using [aiohttp](http://aiohttp.readthedocs.io/en/stable/web.html) for its presentation layer.
* Strategy to organize the application into areas (e.g. public, admin, etc.)
* Support for different localization and authentication strategies based on application area
* Authentication and authorization strategies
* Server side localization strategy (e.g. supported cultures by application area, culture code in routes, etc.)
* Culture code in url route; logic to validate culture and redirect when a request hits a non supported culture
* Code organization to use YAML configuration file for the application
* Session management strategy, supporting anonymous users sessions and storing client information (user-agent)
* Integration with [Babel internationalization library](http://babel.pocoo.org/en/latest/installation.html)
* Authentication and authorization strategies abstracted from presentation layer, including anonymous authentication.
* Antiforgery token validation strategy (session based, dual token technique; for AJAX requests and regular form posts)
* Login mechanism protected against brute forcing (stores login attempts in DB).
* DB based sessions strategy, supporting multiple instances of the application, behind load balancers.
* Instructions for PostgreSQL setup.
* Script to create PostgreSQL tables for accounts, sessions, login attempts (public area and administrative area).
* Custom error pages.
* Strategy to use secure cookies (HTTPS only) by configuration file.
* Strategy to show or hide error details by configuration.
* Strategy to activate / deactivate serving of static files by configuration file.
* Strategy to force client reload of JavaScript and CSS files by configuration file.
* Integration with Google Analytics, by configuration file

## Branches
* [empty-project](https://github.com/RobertoPrevato/aiohttp-three-template/tree/empty-project): empty template without any authentication strategy, but including code organization and JavaScript bundling and minification strategy, LESS compilation and integration with Grunt.
* [master](https://github.com/RobertoPrevato/aiohttp-three-template/tree/master): template with all features listed above.

## Why PostgreSQL?
Currently, PostgreSQL seems to be the best supported DBMS for use with the latest versions of Python and its features for concurrency (asyncio), including the convenient async / await syntax.

## Why not aiohttp-security?
A new implementation of authentication and authorization strategies was preferred because:
1. apparently aiohttp-security doesn't implement salt value for passwords stored in database
2. authentication strategy must be abstracted from front end layer; in aiohttp-security things seem to be single layer (presentation layer, business logic and database access code mixed in single places)
3. one of the objectives was to support the separation of the application into logical areas, each supporting its own authentication logic

