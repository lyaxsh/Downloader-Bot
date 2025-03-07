from datetime import datetime, timedelta

import psycopg2
from psycopg2.extras import RealDictCursor

import config


class DataBase:

    def __init__(self):
        self.connect = psycopg2.connect(config.db_auth)
        self.cursor = self.connect.cursor()
        self.reconnect()
        self.create_tables()

    def reconnect(self):
        if self.connect:
            self.connect.close()
        self.connect = psycopg2.connect(config.db_auth, cursor_factory=RealDictCursor)
        self.connect.autocommit = True
        self.cursor = self.connect.cursor()

    def create_tables(self):
        create_downloaded_files_table = """
            CREATE TABLE IF NOT EXISTS public.downloaded_files (
                id BIGINT GENERATED BY DEFAULT AS IDENTITY NOT NULL,
                url TEXT NOT NULL,
                file_id TEXT NOT NULL,
                date_added TIMESTAMP WITH TIME ZONE NULL DEFAULT (now() AT TIME ZONE 'gmt+3'),
                file_type TEXT NULL,
                CONSTRAINT downloaded_files_pkey PRIMARY KEY (id),
                CONSTRAINT downloaded_files_url_key UNIQUE (url)
            ) TABLESPACE pg_default;
            """

        create_users_table = """
            CREATE TABLE IF NOT EXISTS public.users (
                user_id BIGINT GENERATED BY DEFAULT AS IDENTITY NOT NULL,
                user_name TEXT NULL,
                user_username TEXT NULL,
                chat_type TEXT NULL,
                language TEXT NULL,
                status TEXT NULL,
                captions TEXT NOT NULL DEFAULT 'off',
                CONSTRAINT users_pkey PRIMARY KEY (user_id)
            ) TABLESPACE pg_default;
            """

        try:

            with self.connect:
                self.cursor.execute(create_downloaded_files_table)
                self.cursor.execute(create_users_table)
                print("Tables created or exist")
        except psycopg2.OperationalError as e:
            print(f"Error: {e}")
            pass

    async def add_users(self, user_id, user_name, user_username, chat_type, language, status):
        try:
            with self.connect:
                self.cursor.execute(
                    """INSERT INTO users (user_id, user_name, user_username, chat_type, language, status) 
                    VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (user_id) DO NOTHING;""",
                    (user_id, user_name, user_username, chat_type, language, status))

        except psycopg2.OperationalError as e:
            print(e)
            pass

    async def delete_user(self, user_id):
        try:
            with self.connect:
                self.cursor.execute(
                    "DELETE FROM users WHERE user_id = %s;",
                    (user_id,))
        except psycopg2.OperationalError as e:
            print(e)
            pass

    async def user_count(self):
        try:
            with self.connect:
                self.cursor.execute("SELECT COUNT(*) FROM users")
                return self.cursor.fetchone()[0]
        except psycopg2.OperationalError as e:
            print(e)
            pass

    async def active_user_count(self):
        try:
            with self.connect:
                self.cursor.execute("SELECT COUNT(*) FROM users WHERE status = 'active'")
                return self.cursor.fetchone()[0]
        except psycopg2.OperationalError as e:
            print(e)
            pass

    async def inactive_user_count(self):
        try:
            with self.connect:
                self.cursor.execute("SELECT COUNT(*) FROM users WHERE status != 'active'")
                return self.cursor.fetchone()[0]
        except psycopg2.OperationalError as e:
            print(e)
            pass

    async def all_users(self):
        try:
            with self.connect:
                self.cursor.execute("SELECT user_id FROM users")
                return self.cursor.fetchall()

        except psycopg2.OperationalError as e:
            print(e)
            pass

    async def user_exist(self, user_id):
        try:
            with self.connect:
                self.cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
                return self.cursor.fetchall()

        except psycopg2.OperationalError as e:
            print(e)
            pass

    async def user_update_name(self, user_id, user_name, user_username):
        try:
            with self.connect:
                self.cursor.execute("UPDATE users SET user_username = %s, user_name = %s WHERE user_id = %s",
                                    (user_username, user_name, user_id))
        except psycopg2.OperationalError as e:
            print(e)
            pass

    async def get_user_captions(self, user_id):
        try:
            with self.connect:
                self.cursor.execute("SELECT captions FROM users WHERE user_id = %s", (user_id,))
                return self.cursor.fetchone()[0]

        except psycopg2.OperationalError as e:
            print(e)
            pass

    async def update_captions(self, captions, user_id):
        try:
            with self.connect:
                self.cursor.execute("UPDATE users SET captions = %s WHERE user_id = %s",
                                    (captions, user_id))
        except psycopg2.OperationalError as e:
            print(e)
            pass

    async def set_inactive(self, user_id):
        try:
            with self.connect:
                self.cursor.execute("UPDATE users SET status = %s WHERE user_id = %s", ("inactive", user_id))
        except psycopg2.OperationalError as e:
            print(e)
            pass

    async def set_active(self, user_id):
        try:
            with self.connect:
                self.cursor.execute("UPDATE users SET status = %s WHERE user_id = %s", ("active", user_id))
        except psycopg2.OperationalError as e:
            print(e)
            pass

    async def status(self, user_id):
        try:
            with self.connect:
                self.cursor.execute("SELECT DISTINCT status FROM users WHERE user_id = %s", (user_id,))
                return self.cursor.fetchone()[0]
        except psycopg2.OperationalError as e:
            print(e)
            pass

    async def get_user_info(self, user_id):
        try:
            with self.connect:
                self.cursor.execute(
                    "SELECT user_name, user_username, status FROM users WHERE user_id = %s",
                    (user_id,))
                return self.cursor.fetchone()
        except psycopg2.OperationalError as e:
            print(e)
            pass

    async def get_user_info_username(self, user_username):
        try:
            with self.connect:
                self.cursor.execute(
                    "SELECT user_name, user_id, status FROM users WHERE user_username = %s",
                    (user_username,))
                return self.cursor.fetchone()
        except psycopg2.OperationalError as e:
            print(e)
            pass

    async def get_all_users_info(self):
        try:
            with self.connect:
                self.cursor.execute(
                    "SELECT user_id, chat_type, user_name, user_username, language, status, referrer_id FROM users")
                return self.cursor.fetchall()
        except psycopg2.OperationalError as e:
            print(e)
            pass

    async def ban_user(self, user_id):
        try:
            with self.connect:
                self.cursor.execute("UPDATE users SET status = %s WHERE user_id = %s", ("ban", user_id))
        except psycopg2.OperationalError as e:
            print(e)
            pass

    async def add_file(self, url, file_id, file_type):
        try:
            with self.connect:
                self.cursor.execute("INSERT INTO downloaded_files (url, file_id, file_type) VALUES (%s, %s, %s)",
                                    (url, file_id, file_type))
        except psycopg2.OperationalError as e:
            print(e)
            pass

    async def get_file_id(self, url):
        try:
            with self.connect:
                self.cursor.execute("SELECT file_id FROM downloaded_files WHERE url = %s", (url,))
                return self.cursor.fetchall()
        except psycopg2.OperationalError as e:
            print(e)
            pass

    async def get_downloaded_files_count(self, period: str):
        try:
            with self.connect:
                if period == 'Week':
                    start_date = datetime.now() - timedelta(weeks=1)
                    query = """
                    SELECT DATE(date_added) AS date, COUNT(*) 
                    FROM downloaded_files 
                    WHERE date_added >= %s 
                    GROUP BY DATE(date_added)
                    ORDER BY DATE(date_added)
                    """
                    self.cursor.execute(query, (start_date,))
                elif period == 'Month':
                    start_date = datetime.now() - timedelta(days=30)
                    query = """
                    SELECT DATE(date_added) AS date, COUNT(*) 
                    FROM downloaded_files 
                    WHERE date_added >= %s 
                    GROUP BY DATE(date_added)
                    ORDER BY DATE(date_added)
                    """
                    self.cursor.execute(query, (start_date,))
                elif period == 'Year':
                    start_date = datetime.now() - timedelta(days=365)
                    query = """
                    SELECT DATE(date_added) AS date, COUNT(*) 
                    FROM downloaded_files 
                    WHERE date_added >= %s 
                    GROUP BY DATE(date_added)
                    ORDER BY DATE(date_added)
                    """
                    self.cursor.execute(query, (start_date,))

                result = self.cursor.fetchall()
                # Перетворюємо результат у потрібний формат
                return {row[0].strftime('%Y-%m-%d'): row[1] for row in result}
        except Exception as e:
            print("Error:", e)
