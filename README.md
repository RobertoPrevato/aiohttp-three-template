# aiohttp-three-template
Project template for three-tier web applications using Python aiohttp for the presentation layer.

[![Homepage](https://robertoprevato.github.io/demos/aiohttp-template/homepage.png)](https://robertoprevato.github.io/demos/aiohttp-template/homepage.png)

## Project template features
* Project skeleton ready to use, to start a three tier web application using [aiohttp](http://aiohttp.readthedocs.io/en/stable/web.html) for its presentation layer.
* Strategy to organize the application into areas (e.g. public, admin, etc.).
* Authentication and authorization strategies.
* Server side localization strategy (e.g. supported cultures by application area, culture code in routes, etc.).
* Culture code in url route; logic to validate culture and redirect when a request hits a non supported culture.
* Code organization to use YAML configuration file for the application.
* Database based session management, supporting anonymous users sessions and storing client information (user-agent).
* Antiforgery token validation (session based, dual token technique; for AJAX requests and regular form posts).
* Instructions for PostgreSQL setup.
* Script to create PostgreSQL tables for accounts, sessions, login attempts (public area and administrative area).
* Strategy to use secure cookies (HTTPS only) by configuration file.
* Strategy to show or hide error details by configuration.
* Strategy to activate / deactivate serving of static files by configuration file.
* Strategy to force refresh of clients cache (JavaScript and CSS files) by configuration file.
* Integration with Google Analytics, by configuration file.

## Documentation

* [How to set up the development environment.](https://github.com/RobertoPrevato/aiohttp-three-template/wiki/Preparing-the-environment)
* [How to set up a PostgreSQL instance.](https://github.com/RobertoPrevato/aiohttp-three-template/wiki/PostgreSQL-setup)
* [How to bundle and minify CSS and JavaScript files.](https://github.com/RobertoPrevato/aiohttp-three-template/wiki/Bundling-and-minification)

## Why exactly PostgreSQL?
PostgreSQL seems to be the best supported DBMS for use with the latest versions of Python and its features for concurrency (asyncio), including the convenient async / await syntax.
