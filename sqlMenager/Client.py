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
    def __call__(cls, *args, **kwds):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwds)
        return cls._instances[cls]

    @staticmethod
    def accumulateErrors(annotation = ""):
        def accumulateTraceback(sqlFuncion):
            @wraps(sqlFuncion)
            def funcWithTraceback(self, *args, **kwargs):
                try:
                    return sqlFuncion(self, *args, **kwargs)
                except postgres.Error as error:
                    _ClientMeta._erroraTraceback.append(
                        (annotation, f"{error.pgcode}: {error} | {error.pgerror}"))
                    self.rollback()
            return funcWithTraceback
        return accumulateTraceback


class Client(metaclass=_ClientMeta):
    def __init__(self):
        self.connection = None
        self.cursor = None

        self._connect()
        self._setSearchPath()
    
    def __del__(self):
        self._disconect()
    
    def isConected(self):
        return self.connection is not None

    def select(self, table, *rows, **settings):
        querry = f"SELECT {'*' if not rows else ', '.join(rows)} FROM {table}";
        querry += self._prepareConditions(settings)
        
        return self._executeQuerry(querry + ';')
    
    def insert(self, table, names, values):
        formatRow = lambda row: '(' + ','.join(f"'{value}'" for value in row) + ')'
        rows = ", ".join(formatRow(row) for row in values)
        querry = f"INSERT INTO {table} ({', '.join(names)}) VALUES {rows};"
        
        self._executeQuerry(querry)

        _ClientMeta._erroraTraceback[-1]
        noFetchError = _ClientMeta._erroraTraceback.pop()
        if noFetchError != ('Querry', 'None: no results to fetch | None'):
            _ClientMeta._erroraTraceback.append(noFetchError)
            return False
        return True
    
    def execute(self, querry):
        return self._executeQuerry(querry)

    def getTraceback(self):
        return _ClientMeta._erroraTraceback

    def rollback(self):
        self.connection.rollback()
        self._setSearchPath()

    def _setSearchPath(self):
        self.cursor.execute("SET SEARCH_PATH TO projekt;")

    def _prepareConditions(self, settings):
        if settings is None:
            return ';'
        
        querry = ""
        if (joins := settings.get("join", None)) is not None:
            for join in joins:
                querry += f" JOIN {join[0]} ON {join[1]}"
        if (where := settings.get("where", None)) is not None:
            querry += f" WHERE {where} "
        if (groupBy := settings.get("groupBy", None)) is not None:
            querry += f" GROUP BY {groupBy} "
        if (having := settings.get("having", None)) is not None:
            querry += f" HAVING {having} "
        if (orderBy := settings.get("orderBy", None)) is not None:
            querry += f" ORDER BY {orderBy} "

        return querry + ';'

    @_ClientMeta.accumulateErrors("Connection")
    def _connect(self):
        self.connection = postgres.connect(**config.dbConfig)
        self.cursor = self.connection.cursor()

    def _disconect(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()

    @_ClientMeta.accumulateErrors("Querry")
    def _executeQuerry(self, querryFormat):
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
