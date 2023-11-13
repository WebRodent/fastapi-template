#!/usr/bin/env python3

import sys
import time
from urllib.parse import urlparse

import psycopg2
from psycopg2 import InterfaceError, OperationalError


def check_db_connection(conn_str, max_attempts, retry_delay_seconds):
    url = urlparse(conn_str)
    host, port = url.hostname, url.port
    user, password = url.username, url.password
    dbname = url.path[1:]  # remove the leading '/'

    attempt = 1
    while attempt <= max_attempts:
        try:
            conn = psycopg2.connect(
                host=host, port=port, user=user, password=password, dbname=dbname
            )
            conn.close()
            print(f"Successfully connected to the database at {host}:{port}/{dbname}")
            return True
        except OperationalError as oe:
            # Checking for specific error messages
            if "authentication failed" in str(oe):
                print(
                    "Authentication failed. Please check your username and/or password."
                )
            elif f'database "{dbname}" does not exist' in str(oe):
                print(f"Database '{dbname}' does not exist.")
            else:
                print(f"Operational error: {oe}")
        except InterfaceError as ie:
            print(f"Interface error (possible connectivity issue): {ie}")
        except Exception as e:
            print(f"Unexpected error: {e}")

        if attempt == max_attempts:
            print(f"Attempt {attempt} failed and there are no more attempts left!")
            return False
        else:
            print(
                f"Attempt {attempt} failed!"
                + f" Waiting {retry_delay_seconds} seconds before trying again."
            )
            attempt += 1
            time.sleep(retry_delay_seconds)
    return False


if __name__ == "__main__":
    print(f"Received arguments: {sys.argv}")
    if len(sys.argv) != 4:
        print(
            "Usage: wait-for-it.py <connection_string> <max_attempts>"
            + " <retry_delay_seconds>"
        )
        sys.exit(1)

    conn_str, max_attempts, retry_delay_seconds = (
        sys.argv[1],
        int(sys.argv[2]),
        int(sys.argv[3]),
    )

    success = check_db_connection(conn_str, max_attempts, retry_delay_seconds)
    sys.exit(0 if success else 1)
