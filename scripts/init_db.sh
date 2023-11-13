#!/bin/bash

# Check if some_database exists
psql -t -c "SELECT 1 FROM pg_database WHERE datname='some_database'" | grep -q 1 || psql -c "CREATE DATABASE some_database"
# Grant privileges
psql -c "GRANT ALL PRIVILEGES ON DATABASE some_database TO postgres"