from pathlib import Path
from sys import argv
from getpass import getpass

import tkinter as tk
from tkinter import ttk

from application import Viewport
from application import ShopStyle
from application import User, Logingscreen, Registrationscreen, Shopscreen
from sqlMenager import Client

class ShopApplication:

    def __init__(self):
        if "--god-mode" in argv or "-g" in argv:
            return
        
        self.user = User.NOT_LOGGED

        self.root = tk.Tk()
        self.root.title("Sklep Elektroniczny")
        self.root.geometry(f"{ShopStyle.SCREEN_WIDTH}x{ShopStyle.SCREEN_HEIGHT}")
        self.root.configure(bg=ShopStyle.BACKGROUND_COLOR)

        self.appFrame = tk.Frame(self.root, bg=ShopStyle.BACKGROUND_COLOR)
        self.appFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.style = ShopStyle()

        self.content = Logingscreen(self.appFrame, self.login, self.register)
        # self.content = Shopscreen(self.appFrame, self.getUser)

    def login(self):
        if isinstance(self.content, Logingscreen):
            login = self.content.loginEntry.get()
            password = self.content.passwordEntry.get()

            self.user = User.Login(login, password)
            if self.user.isLogedIn:
                self._changeViewport(Shopscreen, self.getUser)
            else:
                self.content.validationLabel.configure(text="Nie prawidłowe dane logowania")
        elif isinstance(self.content, Registrationscreen):
            self._changeViewport(Logingscreen, self.login, self.register)

    def register(self):
        if isinstance(self.content, Logingscreen):
            self._changeViewport(Registrationscreen, self.login, self.register)
        elif isinstance(self.content, Registrationscreen):
            if self.content.passwordEntry1.get() != self.content.passwordEntry2.get():
                self.content.validationLabel.configure(text="Hasła się nie zgadzają")
            userSpec = User.UserSpec(
                -1,
                self.content.fnameEntry.get(),
                self.content.lnameEntry.get(),
                self.content.ageEntry.get(),
                self.content.addressEntry.get(),
                self.content.emailEntry.get(),
                self.content.loginEntry.get()
            )
    
            self.user = User.Register(userSpec, self.content.passwordEntry1.get())
            if self.user.isLogedIn:
                self._changeViewport(Shopscreen, self.getUser)
            else:
                self.content.validationLabel.configure(text="Użytkownik już istnieje")

    def getUser(self):
        return self.user

    def run(self):
        if "--god-mode" in argv or "-g" in argv:
            self.consoleApp()
        else:
            self.root.mainloop()

    def consoleApp(self):
        ac = None
        while True:
            print("Action:")
            print("     1: Login")
            print("     2: Register")
            if (ac := input()) in ("1", "2"):
                break
        while True:
            if ac == "1":
                login = input("Login: ")
                password = getpass("Password: ")
                self.user = User.Login(login, password)
            else:
                fname = input("fname: ")
                lname = input("lname: ")
                age = input("age: ")
                address = input("address: ")
                email = input("email: ")
                login = input("login: ")
                password = getpass("Password: ")
                userSpec = User.UserSpec(
                    -1,
                    fname,
                    lname,
                    age,
                    address,
                    email,
                    login
                )
                self.user = User.Register(userSpec, password)

            if not self.user.isLogedIn:
                print("Bledne dane")
                continue
            else:
                break
        while (querry := input("Querry: ")) != "exit":
            data = Client().execute(querry)
            for err in Client().getTraceback():
                print(err)
            Client().getTraceback().clear()

            if data:
                for d in data:
                    print(d)

    def _changeViewport(self, viewport: Viewport, *args: Any, **kwargs: Any) -> None:
        self.appFrame.destroy()
        
        self.appFrame = tk.Frame(self.root, bg=ShopStyle.BACKGROUND_COLOR)
        self.appFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.content = viewport(self.appFrame, *args, **kwargs)


if __name__ == "__main__":
    app = ShopApplication()
    app.run()
