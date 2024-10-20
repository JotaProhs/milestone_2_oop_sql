import sqlite3


class DatabaseConnection:
    """
    Class to create a database connection object that will handle a context
    manager to do CRUD action in the SQLite db.
    """
    def __init__(self, host: str):
        """
        Initialize the database object with a parameter host
        :param host: name of the database file
        """
        self.host = host
        self.connection = None
        self.cursor = None

    def __enter__(self) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
        """
        creates and returns the connection and the cursor object.
        :return: a tuple containing both objects created.
        """
        self.connection = sqlite3.connect(self.host)
        self.cursor = self.connection.cursor()
        return self.connection, self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """
        Validate if there has been an error and if there has been an error,
        the db will close without commiting. Otherwise, it will commit and
        then close.
        :param exc_type: Not None when there is an error.
        :param exc_val: Not None when there is an error
        :param exc_tb: Not None when there is an error
        :return: None
        """
        if exc_type or exc_val or exc_tb:
            self.connection.close()
            return True

        else:
            self.connection.commit()
            self.connection.close()
