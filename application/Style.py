from tkinter import Misc, ttk


class ShopStyle(ttk.Style):
    SCREEN_WIDTH = 1080
    SCREEN_HEIGHT = 720
    BACKGROUND_COLOR = "#090960"
    FOREGROUND_COLOR = "#63768D"
    BUTTONS_COLOR = "#8AC6D0"
    FONT_COLOR = "#FFFFFF"

    def __init__(self, master: Misc | None = None) -> None:
        super().__init__(master)
        
        super().configure(
            "Blue.TFrame",
            background=self.BACKGROUND_COLOR,
            borderwidth=2,
            relief="solid"
        )
        
        super().configure(
            "Red.TFrame",
            background="#FF0000",
            borderwidth=2,
            relief="solid"
        )
