from typing import Any, List

import psycopg2 as sql

try:
    import config
except ImportError as error:
    print("Cannot load data base configurations, make sure 'config.py' exists")
    exit(404)

class ClientMeta(type):
    _instances = {}
    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwds)
        return cls._instances[cls]

class Clien(metaclass=ClientMeta):
    def __init__(self) -> None:
        self.connection = None
        self.cursor = None

        self._connect()
    
    def __del__(self) -> None:
        self._disconect()
    
    def isConected(self) -> None:
        return self.connection is not None

    def select(self):
        querry = "SELECT * FROM projekt.produkty;"

        wyniki = self._executeQuerry(querry)
        print("wyniki")
        print(wyniki)

    def _connect(self) -> None:
        try:
            self.connection = sql.connect(**config.dbConfig)
            self.cursor = self.connection.cursor()

        except sql.Error as error:
            print("Błąd podczas łączenia z bazą danych:", error)

    def _disconect(self) -> None:
        if self.connection:
            self.cursor.close()
            self.connection.close()

    def _executeQuerry(self, querryFormat: str, *querryInstructions: str) -> List | None:
        try:
            self.cursor.execute(querryFormat, querryInstructions)
            return self.cursor.fetchall()
        except sql.Error as error:
            print(f"Problem z zapytaniem: {error}")
            print(querryInstructions)


if __name__ == '__main__':
    sqlClient = Clien()

    if not sqlClient.isConected():
        print("Connection has not been established")
        exit(400)
    print("Connected succesfuly")

    sqlClient.select()
