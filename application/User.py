from hashlib import sha256
from collections import namedtuple

import tkinter as tk
from tkinter import ttk

from .Interface import Viewport
from sqlMenager import Client


class User:
    UserSpec = namedtuple("UserSpec", ("userId", "fname", "lname", "age", "address", "email", "login"))
    NOT_LOGGED = UserSpec(-1, None, None, 0, None, None, None)

    def __init__(self, isLogedIn, userSpec):
        self.isLogedIn = isLogedIn
        self.userId = int(userSpec.userId)
        self.fname = userSpec.fname
        self.lname = userSpec.lname
        self.age = int(userSpec.age)
        self.address = userSpec.address
        self.email = userSpec.email
        self.login = userSpec.login
    
    @classmethod
    def Login(cls, login, password):
        password = cls._encryptPassword(password)

        user = Client().execute(f"SELECT * FROM get_loged_user('{login}', '{password}')")
        if not user:
            return cls(False, cls.NOT_LOGGED)

        user = user[0]
        userSpec = cls.UserSpec(user[0], user[1], user[2], user[3], user[4], user[5], login)
        return cls(True, userSpec)
    
    
    @classmethod
    def Register(cls, userSpec, password):
        password = cls._encryptPassword(password)

        userValues = f"'{userSpec.fname}', '{userSpec.lname}', '{userSpec.age}', '{userSpec.address}', '{userSpec.email}', '{userSpec.login}', '{password}'"
        success = Client().execute(f"SELECT create_user({userValues})")
    
        if success[0][0] != -1:
            userSpec = cls.UserSpec(
                success[0][0],
                userSpec.fname,
                userSpec.lname,
                userSpec.age,
                userSpec.address,
                userSpec.email,
                userSpec.lname
            )
            return cls(True, userSpec)
        return cls(False, cls.NOT_LOGGED)
    
    @staticmethod
    def _encryptPassword(password):
        return sha256(password.encode("utf-8"), usedforsecurity=True).hexdigest()
        

class Logingscreen(Viewport):
    def __init__(self, frameroot, onLogin, onRegistration):
        self.logingScreen = ttk.Frame(frameroot, style="Blue.TFrame")
        self.logingScreen.place(relx=15.5, rely=15.5)
        self.logingScreen.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.loginLabel = ttk.Label(self.logingScreen, text="Login:")
        self.loginLabel.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.loginEntry = ttk.Entry(self.logingScreen)
        self.loginEntry.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.passwordLabel = ttk.Label(self.logingScreen, text="Hasło:")
        self.passwordLabel.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        self.passwordEntry = ttk.Entry(self.logingScreen, show="*")
        self.passwordEntry.grid(row=1, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.subbmitButton = ttk.Button(self.logingScreen, text="Zaloguj", command=onLogin)
        self.subbmitButton.grid(row=2, column=0, columnspan=2, pady=10)

        self.registrationButton = ttk.Button(self.logingScreen, text="Zarejestruj się", command=onRegistration)
        self.registrationButton.grid(row=3, column=1, columnspan=1, padx=5, pady=5, sticky=tk.E)

        self.validationLabel = ttk.Label(self.logingScreen, text="")
        self.validationLabel.grid(row=4, columnspan=2, padx=5, pady=5)


class Registrationscreen(Viewport):
    def __init__(self, frameroot, onLogin, onRegistration):
        self.registrationScreen = ttk.Frame(frameroot, style="Blue.TFrame")
        self.registrationScreen.place(relx=0.5, rely=0.5)
        self.registrationScreen.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.emailLabel = ttk.Label(self.registrationScreen, text="Email:")
        self.emailLabel.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.emailEntry = ttk.Entry(self.registrationScreen)
        self.emailEntry.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.loginLabel = ttk.Label(self.registrationScreen, text="Login:")
        self.loginLabel.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.loginEntry = ttk.Entry(self.registrationScreen)
        self.loginEntry.grid(row=1, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.passwordLabel1 = ttk.Label(self.registrationScreen, text="Hasło:")
        self.passwordLabel1.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.passwordEntry1 = ttk.Entry(self.registrationScreen, show="*")
        self.passwordEntry1.grid(row=2, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.passwordLabel2 = ttk.Label(self.registrationScreen, text="Potwierdz Hasło:")
        self.passwordLabel2.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.passwordEntry2 = ttk.Entry(self.registrationScreen, show="*")
        self.passwordEntry2.grid(row=3, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.fnameLabel = ttk.Label(self.registrationScreen, text="Imię:")
        self.fnameLabel.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.fnameEntry = ttk.Entry(self.registrationScreen)
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

        self.loginButton = ttk.Button(self.registrationScreen, text="Logowanie", command=onLogin)
        self.loginButton.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky=tk.E)
        
        self.validationLabel = ttk.Label(self.registrationScreen, text="")
        self.validationLabel.grid(row=10, columnspan=2, padx=5, pady=5)
        

if __name__ == '__main__':
    client = Client()

    userSpec = User.UserSpec(
        -1,
        'Insert',
        'Spec',
        -2,
        'port',
        'sql@server.com',
        'user2'
    )
    newUser = User.Register(userSpec, '12345')
    print("User Registerd")

    user = User.Login("user", "password")
    print("User:")
    print(f"- id: {user.userId}")
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
