from typing import Callable
from pathlib import Path

import tkinter as tk
from tkinter import ttk

from application import Viewport
from application import User, Loggingscreen, Registrationscreen


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

        self.content = Loggingscreen(self.appFrame, self.loggin, self.register)

    def loggin(self):
        login = self.content.loginEntry.get()
        password = self.content.passwordEntry.get()

        self.user = User.Login(login, password)
        if self.user.isLogedIn:
            self.appFrame.pack_forget()
            self.showApp()
        else:
            self.content.validationLabel.configure(text="Nie prawidłowe dane logowania")

    def register(self):
        if isinstance(self.content, Loggingscreen):
            self._changeViewport(Registrationscreen(self.appFrame, self.register))
        elif isinstance(self.content, Registrationscreen):
            print("Registring")

    def showApp(self):
        self.appFrame = tk.Frame(self.root, bg=self.BACKGROUND_COLOR)
        self.appFrame.pack(expand=True)

        self.appContent = ttk.Frame(self.appFrame)
        self.appContent.pack()

        self.welcomeLabel = ttk.Label(self.appContent, text=f"Witaj, {self.user.login}!")
        self.welcomeLabel.grid(row=0, column=0, pady=10)

    def run(self) -> None:
        self.root.mainloop()

    def _changeViewport(self, viewport: Viewport) -> None:
        self.appFrame.pack_forget()
        self.appFrame.pack(expand=True)
        self.content = viewport

if __name__ == "__main__":
    app = ShopApplication()
    app.run()
