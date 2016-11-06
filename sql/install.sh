#!/usr/bin/env bash
sudo -u postgres psql -c "DROP DATABASE IF EXISTS aiohttpthree"
sudo -u postgres psql -c "DROP ROLE IF EXISTS aiohttpthree_user"
sudo -u postgres psql -c "CREATE USER aiohttpthree_user WITH PASSWORD 'aiohttpthree_user';"
sudo -u postgres psql -c "CREATE DATABASE aiohttpthree ENCODING 'UTF8';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE aiohttpthree TO aiohttpthree_user;"

cat sql/create_tables.sql | sudo -u postgres psql -d aiohttpthree -a
cat sql/sample_data.sql | sudo -u postgres psql -d aiohttpthree -a