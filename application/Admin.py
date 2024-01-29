from hashlib import sha256
from collections import namedtuple

import tkinter as tk
from tkinter import ttk

from .Interface import Viewport
from sqlMenager import Client


class Adminscreen(Viewport):
    def __init__(self, frameroot: tk.Frame):
        self.adminScreen = ttk.Frame(frameroot, style="Blue.TFrame")
        self.adminScreen.pack()

        self.mainFrame = ttk.Frame(self.adminScreen, style="Blue.TFrame")
        self.produktFrame = ttk.Frame(self.adminScreen, style="Blue.TFrame")
        self.kategorieFrame = ttk.Frame(self.adminScreen, style="Blue.TFrame")
        self.podkatFrame = ttk.Frame(self.adminScreen, style="Blue.TFrame")
        self.magazynFrame = ttk.Frame(self.adminScreen, style="Blue.TFrame")
        self.opinieFrame = ttk.Frame(self.adminScreen, style="Blue.TFrame")

        self._initMainFrame()
        self._initProduktFrame()
        self._initKategorieFrame()
        self._initPodkatFrame()
        self._initMagazynFrame()
        self._initOpinieFrame()
        
        self.produktFrame.grid_forget()
        self.kategorieFrame.grid_forget()
        self.podkatFrame.grid_forget()
        self.magazynFrame.grid_forget()
        self.opinieFrame.grid_forget()

    def _initMainFrame(self):
        self.mainFrame.grid(row=0, column=0)
        self.mainFrameContent = []

        self.mainFrameContent.append(ttk.Frame(self.mainFrame, style="Blue.TFrame"))
        self.mainFrameContent[0].grid(row=0, column=0)
        
        self.mainFrameContent.append(
            ttk.Button(self.mainFrameContent[0], text="Produkty", command=lambda: (self.mainFrame.grid_forget(), self.produktFrame.grid())))
        self.mainFrameContent.append(
            ttk.Button(self.mainFrameContent[0], text="Kategorie", command=lambda: (self.mainFrame.grid_forget(), self.kategorieFrame.grid())))
        self.mainFrameContent.append(
            ttk.Button(self.mainFrameContent[0], text="Podkategorie", command=lambda: (self.mainFrame.grid_forget(), self.podkatFrame.grid())))
        self.mainFrameContent.append(
            ttk.Button(self.mainFrameContent[0], text="Magazyn", command=lambda: (self.mainFrame.grid_forget(), self.magazynFrame.grid())))
        self.mainFrameContent.append(
            ttk.Button(self.mainFrameContent[0], text="Opinie", command=lambda: (self.mainFrame.grid_forget(), self.opinieFrame.grid())))

        self.mainFrameContent[1].grid(row=0, column=0, pady=10)
        self.mainFrameContent[2].grid(row=1, column=0, pady=10)
        self.mainFrameContent[3].grid(row=2, column=0, pady=10)
        self.mainFrameContent[4].grid(row=3, column=0, pady=10)
        self.mainFrameContent[5].grid(row=4, column=0, pady=10)

    def _initProduktFrame(self):
        self.produktContent = self._getFrame(self.produktFrame)

        self.produktContent.append(ttk.Label(self.produktContent[0], text="Produkty"))

        self.produktContent[2].grid(row=1, column=0, pady=10)

    def _initKategorieFrame(self):
        self.katContent = self._getFrame(self.kategorieFrame)
        
        self.katContent.append(ttk.Label(self.katContent[0], text="Kategorie"))

        self.katContent[2].grid(row=1, column=0, pady=10)


    def _initPodkatFrame(self):
        self.podkatContent = self._getFrame(self.podkatFrame)
        
        self.podkatContent.append(ttk.Label(self.podkatContent[0], text="Podkategorie"))

        self.podkatContent[2].grid(row=1, column=0, pady=10)


    def _initMagazynFrame(self):
        self.magazynContent = self._getFrame(self.magazynFrame)

        self.magazynContent.append(ttk.Label(self.magazynContent[0], text="Magazyn"))

        self.magazynContent[2].grid(row=1, column=0, pady=10)


    def _initOpinieFrame(self):        
        self.opinieContent = self._getFrame(self.opinieFrame)

        self.opinieContent.append(ttk.Label(self.opinieContent[0], text="Opinie"))

        self.opinieContent[2].grid(row=1, column=0, pady=10)
    
    def _getFrame(self, rootFrame):
        rootFrame.grid(row=0, column=0)
        content = []

        content.append(ttk.Frame(rootFrame, style="Blue.TFrame"))
        content[0].grid(row=0, column=0)

        content.append(ttk.Button(content[0], text="Ekran Główny", command=lambda: self._returnToMainScreen(rootFrame)))
        content[1].grid(row=0, column=0)

        return content
    
    def _returnToMainScreen(self, currentFrame):
        currentFrame.grid_forget()
        self.mainFrame.grid()
