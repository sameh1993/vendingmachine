import os
import mysql.connector


class DatabaseManager:

    def __init__(self, **overrides):
            self.config = {
                "host": os.getenv("DB_HOST", "localhost"),
                "port": int(os.getenv("DB_PORT", "3306")),
                "user": os.getenv("DB_USER", "root"),
                "password": os.getenv("DB_PASSWORD", ""),
                "database": os.getenv("DB_NAME", "vendingmachine"),
                "charset": "utf8mb4",
                "collation": "utf8mb4_unicode_ci",
                "autocommit": False,
                "connection_timeout": int(os.getenv("DB_TIMEOUT", "10")),
                "use_pure": True,
            }
            self.config.update(**overrides)
            self.connection = mysql.connector.connect(**self.config)
            

    def cursor(self, dictionary=True):
        return self.connection.cursor(dictionary=dictionary)
