#!/bin/bash
# this is the production start.sh file
# it is used to start the application in the production environment
# it is called by the Dockerfile
# it does the following before starting the application:
# 1. checks if APP_ENV is set to "prod", otherwise it skips the startup procedure, prints a warning and then tries once to start the application
# 2. checks if the database is up and running, through environment variable APP_DATABASE_URL
# 3. uses alembic to upgrade the database to the latest version
# 4. starts the application

poetry config virtualenvs.create false

# method for starting the application
start_app() {
    echo "Starting application"
    poetry run uvicorn app.api:app --host "0.0.0.0" --port $APP_PORT
}

# method for starting the application in development mode
start_app_dev() {
    echo "Starting application in development mode"
    poetry run uvicorn app.api:app --reload --host "0.0.0.0" --port $APP_PORT
}


# method for checking if the database is up and running
check_database() {
    database_url=$APP_DATABASE_URL
    printable_sensored_database_url=$(echo $database_url | sed -E 's/:[^@]+@/:***@/')
    echo "Checking database at $printable_sensored_database_url"
    # try to connect to the database, using the wait-for-it.sh script
    # if the database is not up and running, the script will wait for it to start
    # if the database is up and running, the script will immediately return

    # Pass the components to wait-for-it.py, and run it from the same directory as this script
    #<same parent as this script, which might be "./" for development or "/app/app" for production>/wait-for-it.py $APP_DATABASE_URL 5 3
    pwd=$(pwd)
    poetry run python $pwd/wait-for-it.py $APP_DATABASE_URL 5 3

    # check if the database is up and running
    if [ $? -ne 0 ]; then
        echo "ERROR: Database is not up and running"
        exit 1
    fi
}

# method for upgrading the database
upgrade_database() {
    echo "Upgrading database"
    poetry run alembic upgrade head
}

# 1. check if the database is up and running
check_database

# 2. upgrade the database
upgrade_database

# 3. start the application
if [ "$APP_ENV" = "prod" ]; then
    start_app
else
    echo "WARNING: APP_ENV is not set to 'prod', starting application in development mode"
    start_app_dev
fi
echo "Application exited"