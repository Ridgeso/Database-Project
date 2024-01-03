from typing import Callable

from pathlib import Path

import tkinter as tk
from tkinter import ttk, filedialog


class RoadSignGuesser:
    SCREEN_WIDTH = 1080
    SCREEN_HEIGHT = 720
    BACKGROUND_COLOR = "#090960"
    FOREGROUND_COLOR = "#63768D"
    BUTTONS_COLOR = "#8AC6D0"
    FONT_COLOR = "#FFFFFF"

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Sklep Elektroniczny")
        self.root.geometry(f"{self.SCREEN_WIDTH}x{self.SCREEN_HEIGHT}")
        self.root.configure(bg=self.BACKGROUND_COLOR)

        self.appFrame = tk.Frame(self.root, bg=self.BACKGROUND_COLOR)
        self.appFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def Run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    app = RoadSignGuesser()
    app.Run()
