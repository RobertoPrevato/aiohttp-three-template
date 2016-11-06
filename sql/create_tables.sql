--
DROP TABLE IF EXISTS app_user_login_attempt CASCADE;
DROP TABLE IF EXISTS app_user_session CASCADE;
DROP TABLE IF EXISTS app_user CASCADE;
DROP TABLE IF EXISTS admin_user_login_attempt CASCADE;
DROP TABLE IF EXISTS admin_user_session CASCADE;
DROP TABLE IF EXISTS admin_user_role CASCADE;
DROP TABLE IF EXISTS admin_role CASCADE;
DROP TABLE IF EXISTS admin_user CASCADE;

-- tables for public area users
CREATE TABLE app_user(
  id SERIAL PRIMARY KEY,
  email VARCHAR(50) NOT NULL,
  username VARCHAR(50) NOT NULL,
  hashed_password CHAR(68) NOT NULL,
  salt CHAR(50),
  creation_time TIMESTAMP NOT NULL,
  password_reset_key UUID NULL,
  confirmation_key UUID NULL
);

CREATE TABLE app_user_login_attempt(
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES app_user(id),
  creation_time TIMESTAMP NOT NULL,
  client_ip VARCHAR(50) NOT NULL,
  client_info TEXT NULL
);

CREATE TABLE app_user_session(
  id SERIAL PRIMARY KEY,
  guid UUID NOT NULL,
  user_id INTEGER REFERENCES app_user(id),
  anonymous BOOLEAN NOT NULL,
  creation_time TIMESTAMP NOT NULL,
  expiration_time TIMESTAMP NOT NULL,
  client_ip VARCHAR(50) NOT NULL,
  client_info TEXT NULL,
  UNIQUE(guid)
);

-- tables for admin area users
CREATE TABLE admin_user(
  id SERIAL PRIMARY KEY,
  email VARCHAR(50) NOT NULL,
  username VARCHAR(50) NOT NULL,
  hashed_password CHAR(68) NOT NULL,
  salt CHAR(50),
  creation_time TIMESTAMP NOT NULL,
  password_reset_key UUID NULL,
  confirmation_key UUID NULL
);

CREATE TABLE admin_user_login_attempt(
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES admin_user(id),
  creation_time TIMESTAMP NOT NULL,
  client_ip VARCHAR(50) NOT NULL,
  client_info TEXT NULL
);

CREATE TABLE admin_user_session(
  id SERIAL PRIMARY KEY,
  guid UUID NOT NULL,
  user_id INTEGER REFERENCES app_user(id),
  anonymous BOOLEAN NOT NULL,
  creation_time TIMESTAMP NOT NULL,
  expiration_time TIMESTAMP NOT NULL,
  client_ip VARCHAR(50) NOT NULL,
  client_info TEXT NULL,
  UNIQUE (guid)
);

CREATE TABLE admin_role(
  id SERIAL PRIMARY KEY,
  key_name VARCHAR(50) NOT NULL,
  description VARCHAR(250) NULL,
  UNIQUE (key_name)
);

CREATE TABLE admin_user_role(
  id SERIAL PRIMARY KEY,
  admin_user_id INTEGER REFERENCES admin_user(id),
  admin_role_id INTEGER REFERENCES admin_role(id),
  UNIQUE (admin_user_id, admin_role_id)
);