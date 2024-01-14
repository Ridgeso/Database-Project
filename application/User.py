from typing import Self, Callable
from hashlib import sha256

import tkinter as tk
from tkinter import ttk

from .Interface import Viewport
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
        

class Loggingscreen(Viewport):
    def __init__(self, frameroot: ttk.Frame, onLogin: Callable, onRegistration: Callable) -> None:
        self.loggingScreen = ttk.Frame(frameroot, style="Blue.TFrame")
        self.loggingScreen.place(relx=0.5, rely=0.5)
        self.loggingScreen.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.loginLabel = ttk.Label(self.loggingScreen, text="Login:")
        self.loginLabel.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.loginEntry = ttk.Entry(self.loggingScreen)
        self.loginEntry.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.passwordLabel = ttk.Label(self.loggingScreen, text="Hasło:")
        self.passwordLabel.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        self.passwordEntry = ttk.Entry(self.loggingScreen, show="*")
        self.passwordEntry.grid(row=1, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.subbmitButton = ttk.Button(self.loggingScreen, text="Zaloguj", command=onLogin)
        self.subbmitButton.grid(row=2, column=0, columnspan=2, pady=10)

        self.registrationButton = ttk.Button(self.loggingScreen, text="Zarejestruj się", command=onRegistration)
        self.registrationButton.grid(row=3, column=1, columnspan=1, padx=5, pady=5, sticky=tk.E)

        self.validationLabel = ttk.Label(self.loggingScreen, text="")
        self.validationLabel.grid(row=4, columnspan=2, padx=5, pady=5)


class Registrationscreen(Viewport):
    def __init__(self, frameroot: ttk.Frame, onRegistration: Callable) -> None:
        self.registrationScreen = ttk.Frame(frameroot, style="Blue.TFrame")
        self.registrationScreen.place(relx=0.5, rely=0.5)
        self.registrationScreen.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.emailLabel = ttk.Label(self.registrationScreen, text="Email:")
        self.emailLabel.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.emailLntry = ttk.Entry(self.registrationScreen)
        self.emailLntry.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.loginLabel = ttk.Label(self.registrationScreen, text="Login:")
        self.loginLabel.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.loginEntry = ttk.Entry(self.registrationScreen)
        self.loginEntry.grid(row=1, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.passwordLabel = ttk.Label(self.registrationScreen, text="Hasło:")
        self.passwordLabel.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.passwordEntry = ttk.Entry(self.registrationScreen, show="*")
        self.passwordEntry.grid(row=2, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.passwordLabel = ttk.Label(self.registrationScreen, text="Potwierdz Hasło:")
        self.passwordLabel.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.passwordEntry = ttk.Entry(self.registrationScreen, show="*")
        self.passwordEntry.grid(row=3, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.fnameLabel = ttk.Label(self.registrationScreen, text="Imię:")
        self.fnameLabel.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.fnameEntry = ttk.Entry(self.registrationScreen, show="*")
        self.fnameEntry.grid(row=4, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.lnameLabel = ttk.Label(self.registrationScreen, text="Nazwisko:")
        self.lnameLabel.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.lnameEntry = ttk.Entry(self.registrationScreen)
        self.lnameEntry.grid(row=5, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.ageLabel = ttk.Label(self.registrationScreen, text="Wiek")
        self.ageLabel.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        self.ageEntry = ttk.Entry(self.registrationScreen)
        self.ageEntry.grid(row=6, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.addressLabel = ttk.Label(self.registrationScreen, text="Adres")
        self.addressLabel.grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)
        self.addressEntry = ttk.Entry(self.registrationScreen)
        self.addressEntry.grid(row=7, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.subbmitButton = ttk.Button(self.registrationScreen, text="Zarejestruj", command=onRegistration)
        self.subbmitButton.grid(row=8, column=0, columnspan=2, pady=10)
        

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
