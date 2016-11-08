-- Database: aiohttp

-- DROP DATABASE aiohttp;

CREATE DATABASE aiohttp
  WITH OWNER = postgres
       ENCODING = "UTF8"
       TABLESPACE = pg_default
       LC_COLLATE = "en_US.UTF-8"
       LC_CTYPE = "en_US.UTF-8"
       CONNECTION LIMIT = -1;

COMMENT ON DATABASE aiohttp
  IS "aiohttp three template database";