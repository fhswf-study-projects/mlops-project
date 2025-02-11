import os

import psycopg2

from app.constants import EnvConfig


class PostgresClient:
    _instance = None

    def __new__(cls):
        """Returns the singleton instance or creates a new one if not existend"""
        if cls._instance is None:
            cls._instance = super(PostgresClient, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Init class variables needed to establish a connection to the database"""
        self.client = psycopg2.connect(os.environ[EnvConfig.DB_CONNECTION.value])

    def get_cursor(self):
        return self.client.cursor()
