from abc import ABC, abstractmethod

from tkinter import ttk


class Viewport(ABC):
    @abstractmethod
    def __init__(self, frameroot: ttk.Frame) -> None:
        pass
