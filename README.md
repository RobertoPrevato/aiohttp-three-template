# aiohttp-three-template
Project template for three-tier web applications using Python aiohttp for the presentation layer.

[![Homepage](https://robertoprevato.github.io/demos/aiohttp-template/homepage.png)](https://robertoprevato.github.io/demos/aiohttp-template/homepage.png)

## Project template features
* Project skeleton ready to use, to start a three tier web application using [aiohttp](http://aiohttp.readthedocs.io/en/stable/web.html) for its presentation layer.
* Strategy to organize the application into areas (e.g. public, admin, etc.).
* Support for different localization and authentication strategies based on application area.
* Authentication and authorization strategies.
* Server side localization strategy (e.g. supported cultures by application area, culture code in routes, etc.).
* Culture code in url route; logic to validate culture and redirect when a request hits a non supported culture.
* Code organization to use YAML configuration file for the application.
* Session management strategy, supporting anonymous users sessions and storing client information (user-agent).
* Authentication and authorization strategies abstracted from presentation layer, including anonymous authentication.
* Antiforgery token validation strategy (session based, dual token technique; for AJAX requests and regular form posts).
* Login mechanism protected against brute forcing (stores login attempts in DB).
* DB based sessions strategy, supporting multiple instances of the application, behind load balancers.
* Instructions for PostgreSQL setup.
* Script to create PostgreSQL tables for accounts, sessions, login attempts (public area and administrative area).
* Custom error pages.
* Strategy to use secure cookies (HTTPS only) by configuration file.
* Strategy to show or hide error details by configuration.
* Strategy to activate / deactivate serving of static files by configuration file.
* Strategy to force client reload of JavaScript and CSS files by configuration file.
* Integration with Google Analytics, by configuration file.

## Objectives
The main objectives behind aiohttp-three-template are:

* to contribute to the Python community and to pay homage to the great job done by [aiohttp developers](http://aiohttp.readthedocs.io/en/stable/). Their task is important because they are developing the most modern Python competitor to other event-based web servers.
* offering a beginners' friendly introduction to web applications development: showing all the basic features of common web applications (server side rendering engine with implementation of custom helpers, localization strategy, authentication and authorization strategy, session management, antiforgery token validation, JS and CSS bundling and minification strategy, support for multiple application areas, code organization into logical layers)
* providing a ready to use project template rich in features, but not too opinionated

## Documentation

* [How to set up the development environment](https://github.com/RobertoPrevato/aiohttp-three-template/wiki/Preparing-the-environment)
* [How to set up a PostgreSQL instance](https://github.com/RobertoPrevato/aiohttp-three-template/wiki/PostgreSQL-setup)
* [How to bundle and minify CSS and JavaScript files.](https://github.com/RobertoPrevato/aiohttp-three-template/wiki/Bundling-and-minification)

## Branches
* [empty-project](https://github.com/RobertoPrevato/aiohttp-three-template/tree/empty-project): empty template without any authentication strategy, but including code organization and JavaScript bundling and minification strategy, LESS compilation and integration with Grunt.
* [master](https://github.com/RobertoPrevato/aiohttp-three-template/tree/master): template with all features listed above.

## Why exactly PostgreSQL?
PostgreSQL seems to be the best supported DBMS for use with the latest versions of Python and its features for concurrency (asyncio), including the convenient async / await syntax.
