from typing import Any
from pathlib import Path

import tkinter as tk
from tkinter import ttk

from application import Viewport
from application import User, Logingscreen, Registrationscreen


class ShopApplication:
    SCREEN_WIDTH = 1080
    SCREEN_HEIGHT = 720
    BACKGROUND_COLOR = "#090960"
    FOREGROUND_COLOR = "#63768D"
    BUTTONS_COLOR = "#8AC6D0"
    FONT_COLOR = "#FFFFFF"

    def __init__(self) -> None:
        self.user = User.NOT_LOGGED

        self.root = tk.Tk()
        self.root.title("Sklep Elektroniczny")
        self.root.geometry(f"{self.SCREEN_WIDTH}x{self.SCREEN_HEIGHT}")
        self.root.configure(bg=self.BACKGROUND_COLOR)

        self.appFrame = tk.Frame(self.root, bg=self.BACKGROUND_COLOR)
        self.appFrame.pack(expand=True)

        self.style = ttk.Style()
        self.style.configure(
            "Blue.TFrame",
            background=self.BACKGROUND_COLOR,
            borderwidth=2,
            relief="solid"
        )

        self.content = Logingscreen(self.appFrame, self.login, self.register)

    def login(self) -> None:
        if isinstance(self.content, Logingscreen):
            login = self.content.loginEntry.get()
            password = self.content.passwordEntry.get()

            self.user = User.Login(login, password)
            if not self.user.isLogedIn:
                self.content.validationLabel.configure(text="Nie prawidłowe dane logowania")
        elif isinstance(self.content, Registrationscreen):
            self._changeViewport(Logingscreen, self.login, self.register)

    def register(self) -> None:
        if isinstance(self.content, Logingscreen):
            self._changeViewport(Registrationscreen, self.login, self.register)
        elif isinstance(self.content, Registrationscreen):
            if self.content.passwordEntry1.get() != self.content.passwordEntry2.get():
                self.content.validationLabel.configure(text="Hasła się nie zgadzają")
            userSpec = User.UserSpec(
                self.content.fnameEntry.get(),
                self.content.lnameEntry.get(),
                self.content.ageEntry.get(),
                self.content.addressEntry.get(),
                self.content.emailEntry.get(),
                self.content.loginEntry.get()
            )
    
            self.user = User.Register(userSpec, self.content.passwordEntry1.get())
            if self.user.isLogedIn is False:
                self.content.validationLabel.configure(text="Użytkownik już istnieje")

    def showApp(self) -> None:
        self.appFrame = tk.Frame(self.root, bg=self.BACKGROUND_COLOR)
        self.appFrame.pack(expand=True)

        self.appContent = ttk.Frame(self.appFrame)
        self.appContent.pack()

        self.welcomeLabel = ttk.Label(self.appContent, text=f"Witaj, {self.user.login}!")
        self.welcomeLabel.grid(row=0, column=0, pady=10)

    def run(self) -> None:
        self.root.mainloop()

    def _changeViewport(self, viewport: Viewport, *args: Any, **kwargs: Any) -> None:
        self.appFrame.pack_forget()
        self.appFrame.pack(expand=True)
        self.content = viewport(self.appFrame, *args, **kwargs)

if __name__ == "__main__":
    app = ShopApplication()
    app.run()
