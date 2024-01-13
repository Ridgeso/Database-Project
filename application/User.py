from typing import Self
from hashlib import sha256

from sqlMenager import Client


class User:
    class UserSpec:
        def __init__(
            self,
            fname: str,
            lname: str,
            age: str,
            address: str,
            email: str,
            login: str,
        ) -> None:
            self.fname = fname
            self.lname = lname
            self.age = age
            self.address = address    
            self.email = email
            self.login = login
            self.password = None

    NOT_LOGGED = UserSpec(None, None, 0, None, None, None)

    def __init__(self, isLogedIn: bool, userSpec: UserSpec) -> None:
        self.isLogedIn = isLogedIn
        self.fname = userSpec.fname
        self.lname = userSpec.lname
        self.age = int(userSpec.age)
        self.address = userSpec.address
        self.email = userSpec.email
        self.login = userSpec.login

        self.cart = []
    
    @classmethod
    def Login(cls, login: str, password: str) -> Self | None:
        password = cls._encryptPassword(password)

        userSpecNames = (
            "fname",
            "lname",
            "age",
            "address",
            "email",
            "login",
        )
        user = Client().select(
            "client",
            *userSpecNames,
            where = f"login = '{login}' and password = '{password}'"
        )

        if not user:
            return cls(False, cls.NOT_LOGGED)

        userSpec = cls.UserSpec(**{key: val for key, val in zip(userSpecNames, user[0], strict = True)})
        return cls(True, userSpec)
    
    
    @classmethod
    def Register(cls, userSpec: UserSpec, password: str) -> Self:
        userSpec.password = cls._encryptPassword(password)

        success = Client().insert("client", userSpec.__dict__.keys(), [userSpec.__dict__.values()])
        if success:
            return cls(True, userSpec)
        cls(False, cls.NOT_LOGGED)
    
    @staticmethod
    def _encryptPassword(password: str):
        return sha256(password.encode("utf-8"), usedforsecurity=True).hexdigest()
        

if __name__ == '__main__':
    client = Client()

    userSpec = User.UserSpec(
        'Insert',
        'Spec',
        -2,
        'port',
        'sql@server.com',
        'user2'
    )
    newUser = User.Register(userSpec, '12345')
    print("User Registerd")

    user = User.Login("port", "12345")
    print("User:")
    print(f"- fname: {user.fname}")
    print(f"- lname: {user.lname}")
    print(f"- age: {user.age}")
    print(f"- address: {user.address}")
    print(f"- email: {user.email}")
    print(f"- login: {user.login}")

    users = Client().select('client')
    for user in users:
        print(user)

    print("Works")
