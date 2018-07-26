from sqlite3 import connect, Row
from os.path import isfile
from typing import List
from glob import glob


class Database:
    """A wrapper around access to local sqlite databases."""

    def __init__(self, path_to_sqlite_file: str):
        """(The path can be relative. :3)"""

        self.location = glob(path_to_sqlite_file)[0]

        # If the file doesn't exist, raise an exception.
        if not self.location or not isfile(self.location):
            raise RuntimeError(
                f"Yo, your database file {self.location} is missing!"
            ))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            log.error(exc_type, exc_value, traceback)
        return self

    def query(self, query_text, *args) -> List[dict]:
        """
        Runs a query against the sqlite database. Returns a list of
        dict objects, so you can totally access values like this!
        result[0]["column_name"] -> value
        """
        # Open a new connection in autocommit mode.
        with connect(self.location, isolation_level=None) as conn:
            conn.row_factory = Row
            cursor = conn.cursor()
            cursor.execute(query_text, args)

            return [
                Datastore._dict_from_row(row)
                for row in cursor.fetchall()
            ]

    @staticmethod
    def _dict_from_row(row):
        return dict(zip(row.keys(), row))
