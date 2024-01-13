from typing import Any, List, Tuple, Callable, Self
from functools import wraps

import psycopg2 as postgres

try:
    from sqlMenager import config
except ImportError as error:
    print("Cannot load data base configurations, make sure 'config.py' exists")
    exit(404)


class _ClientMeta(type):
    _instances = {}
    _erroraTraceback = []
    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwds)
        return cls._instances[cls]

    @staticmethod
    def accumulateErrors(annotation: str = "") -> Callable[[Any], Any]:
        def accumulateTraceback(sqlFuncion: Callable[[Any], Any]) -> Callable[[Any], Any]:
            @wraps(sqlFuncion)
            def funcWithTraceback(self: Self, *args: Any, **kwargs: Any) -> Any:
                try:
                    return sqlFuncion(self, *args, **kwargs)
                except postgres.Error as error:
                    _ClientMeta._erroraTraceback.append((annotation, f"{error.pgcode}: {error} | {error.pgerror}"))
                    self.rollback()
            return funcWithTraceback
        return accumulateTraceback


class Client(metaclass=_ClientMeta):
    def __init__(self) -> None:
        self.connection = None
        self.cursor = None

        self._connect()
        self._setSearchPath()
    
    def __del__(self) -> None:
        self._disconect()
    
    def isConected(self) -> bool:
        return self.connection is not None

    def select(self, table: str, *rows: str, **settings: dict[str, str]) -> List:
        querry = f"SELECT {'*' if not rows else ', '.join(rows)} FROM {table}";
        querry += self._prepareConditions(settings)
        
        return self._executeQuerry(querry + ';')
    
    def insert(self, table: str, names: Tuple[str], values: List[Tuple]) -> None:
        formatRow = lambda row: '(' + ','.join(f"'{value}'" for value in row) + ')'
        rows = ", ".join(formatRow(row) for row in values)
        querry = f"INSERT INTO {table} ({', '.join(names)}) VALUES {rows};"
        
        self._executeQuerry(querry)

        _ClientMeta._erroraTraceback[-1]
        noFetchError = _ClientMeta._erroraTraceback.pop()
        if noFetchError != ('Querry', 'None: no results to fetch | None'):
            _ClientMeta._erroraTraceback.append(noFetchError)
        
    def getTraceback(self) -> List:
        return _ClientMeta._erroraTraceback

    def rollback(self):
        self.connection.rollback()
        self._setSearchPath()

    def _setSearchPath(self):
        self.cursor.execute("SET SEARCH_PATH TO projekt;")

    def _prepareConditions(self, settings: dict[str, str]) -> str:
        if settings is None:
            return ';'
        
        querry = ""
        if (where := settings.get("where", None)) is not None:
            querry += f" WHERE {where} "

        return querry + ';'

    @_ClientMeta.accumulateErrors("Connection")
    def _connect(self) -> None:
        self.connection = postgres.connect(**config.dbConfig)
        self.cursor = self.connection.cursor()

    def _disconect(self) -> None:
        if self.connection:
            self.cursor.close()
            self.connection.close()

    @_ClientMeta.accumulateErrors("Querry")
    def _executeQuerry(self, querryFormat: str) -> List | None:
        self.cursor.execute(querryFormat)
        self.connection.commit()
        return self.cursor.fetchall()


if __name__ == '__main__':
    sqlClient = Client()

    if not sqlClient.isConected():
        print("Connection has not been established")
        exit(400)
    print("Connected succesfuly")

    sqlClient.select('produkty')
