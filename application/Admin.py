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

        self._initMainFrame()
        self._initProduktFrame()
        self._initKategorieFrame()
        self._initPodkatFrame()
        self._initMagazynFrame()
        
        self.produktFrame.grid_forget()
        self.kategorieFrame.grid_forget()
        self.podkatFrame.grid_forget()
        self.magazynFrame.grid_forget()

    def _initMainFrame(self):
        self.mainFrame.grid(row=0, column=0)
        self.mainFrameContent = {}

        self.mainFrameContent['mainFrame'] = ttk.Frame(self.mainFrame, style="Blue.TFrame")
        self.mainFrameContent['mainFrame'].grid(row=0, column=0)
        
        self.mainFrameContent['BIG_ADMIN_LABEL'] = ttk.Label(self.mainFrameContent['mainFrame'], text="WITAJ WIELKI ADMINIE")
        self.mainFrameContent['produkty'] = ttk.Button(self.mainFrameContent['mainFrame'], text="Produkty", command=lambda: (self.mainFrame.grid_forget(), self.produktFrame.grid()))
        self.mainFrameContent['kategorie'] = ttk.Button(self.mainFrameContent['mainFrame'], text="Kategorie", command=lambda: (self.mainFrame.grid_forget(), self.kategorieFrame.grid()))
        self.mainFrameContent['podkategorie'] = ttk.Button(self.mainFrameContent['mainFrame'], text="Podkategorie", command=lambda: (self.mainFrame.grid_forget(), self.podkatFrame.grid()))
        self.mainFrameContent['magazyn'] = ttk.Button(self.mainFrameContent['mainFrame'], text="Magazyn", command=lambda: (self.mainFrame.grid_forget(), self.magazynFrame.grid()))

        self.mainFrameContent['BIG_ADMIN_LABEL'].grid(row=0, column=0, padx=10, pady=10)
        self.mainFrameContent['produkty'].grid(row=1, column=0, pady=10)
        self.mainFrameContent['kategorie'].grid(row=2, column=0, pady=10)
        self.mainFrameContent['podkategorie'].grid(row=3, column=0, pady=10)
        self.mainFrameContent['magazyn'].grid(row=4, column=0, pady=10)

    def _initProduktFrame(self):
        self.produktContent = self._getFrame(self.produktFrame)

        self.produktContent["mainLabel"] = ttk.Label(self.produktContent["frame"], text="Produkty")
        self.produktContent["entryFrame"] = ttk.Frame(self.produktContent["frame"], style="Blue.TFrame")

        self.produktContent["appendLabel"] = ttk.Label(self.produktContent["entryFrame"], text="Dodaj Produkt")
        self.produktContent["mainEntry"] = (
            ttk.Label(self.produktContent["entryFrame"], text="Nazwa:"),
            ttk.Entry(self.produktContent["entryFrame"]),
        )
        self.produktContent["prizeEntry"] = (
            ttk.Label(self.produktContent["entryFrame"], text="Cena:"),
            ttk.Entry(self.produktContent["entryFrame"])
        )
        self.produktContent["opisEntry"] = (
            ttk.Label(self.produktContent["entryFrame"], text="Producent:"),
            ttk.Entry(self.produktContent["entryFrame"]),
            ttk.Label(self.produktContent["entryFrame"], text="Opis:"),
            tk.Text(self.produktContent["entryFrame"], height=3)
        )

        kategorie = tuple(map(lambda kat: kat[0], Client().select("kategorie", "nazwa")))
        self.produktContent["katEntry"] = (
            ttk.Label(self.produktContent["entryFrame"], text="Kategorie:"),
            ttk.Combobox(self.produktContent["entryFrame"], values=kategorie),
            ttk.Label(self.produktContent["entryFrame"], text="Podkategorie:"),
            ttk.Combobox(self.produktContent["entryFrame"], values=())
        )
        self.produktContent["specEntry"] = (
            ttk.Label(self.produktContent["entryFrame"], text="Specyfikacja:"),
            ttk.Entry(self.produktContent["entryFrame"])
        )

        self.produktContent["submit"] = ttk.Button(self.produktContent["entryFrame"], text="Zapisz", command=self._safeProd)

        self.produktContent["mainLabel"].grid(row=1, column=0, pady=10)
        self.produktContent["entryFrame"].grid(row=2, column=0, pady=10)

        self.produktContent["appendLabel"].grid(row=0, columnspan=2, padx=20, pady=10)
        
        self.produktContent["mainEntry"][0].grid(row=1, column=0, padx=10, pady=10)
        self.produktContent["mainEntry"][1].grid(row=1, column=1, padx=10, pady=10)
        
        self.produktContent["prizeEntry"][0].grid(row=2, column=0, padx=10, pady=10)
        self.produktContent["prizeEntry"][1].grid(row=2, column=1, padx=10, pady=10)
        
        self.produktContent["opisEntry"][0].grid(row=3, column=0, padx=10, pady=10)
        self.produktContent["opisEntry"][1].grid(row=3, column=1, padx=10, pady=10)
        self.produktContent["opisEntry"][2].grid(row=4, column=0, padx=10, pady=10)
        self.produktContent["opisEntry"][3].grid(row=4, column=1, padx=10, pady=10)
        
        self.produktContent["katEntry"][0].grid(row=5, column=0, padx=10, pady=10)
        self.produktContent["katEntry"][1].grid(row=5, column=1, padx=10, pady=10)
        self.produktContent["katEntry"][1].bind('<<ComboboxSelected>>', self._onChangeKat)
        self.produktContent["katEntry"][2].grid(row=6, column=0, padx=10, pady=10)
        self.produktContent["katEntry"][3].grid(row=6, column=1, padx=10, pady=10)

        self.produktContent["specEntry"][0].grid(row=7, column=0, padx=10, pady=10)
        self.produktContent["specEntry"][1].grid(row=7, column=1, padx=10, pady=10)

        self.produktContent["submit"].grid(row=8, columnspan=2, padx=10, pady=10)

    def _initKategorieFrame(self):
        self.katContent = self._getFrame(self.kategorieFrame)
        
        self.katContent["mainLabel"] = ttk.Label(self.katContent["frame"], text="Kategorie")
        self.katContent["entryFrame"] = ttk.Frame(self.katContent["frame"], style="Blue.TFrame")
        
        self.katContent["katEntry"] = (
            ttk.Label(self.katContent["entryFrame"], text="Kategoria"),
            ttk.Entry(self.katContent["entryFrame"])
        )
        self.katContent["submit"] = ttk.Button(self.katContent["entryFrame"], text="Zapisz", command=self._safeKat)

        self.katContent["mainLabel"].grid(row=1, column=0, pady=10)
        self.katContent["entryFrame"].grid(row=2, column=0, pady=10)

        self.katContent["katEntry"][0].grid(row=0, column=0, padx=10, pady=10)
        self.katContent["katEntry"][1].grid(row=0, column=1, padx=10, pady=10)

        self.katContent["submit"].grid(row=1, columnspan=2, padx=10, pady=10)

    def _initPodkatFrame(self):
        self.podkatContent = self._getFrame(self.podkatFrame)
        
        self.podkatContent["mainLabel"] = ttk.Label(self.podkatContent["frame"], text="Podkategorie")
        self.podkatContent["entryFrame"] = ttk.Frame(self.podkatContent["frame"], style="Blue.TFrame")

        kategorie = tuple(map(lambda kat: kat[0], Client().select("kategorie", "nazwa")))
        self.podkatContent["katEntry"] = (
            ttk.Label(self.podkatContent["entryFrame"], text="Kategorie:"),
            ttk.Combobox(self.podkatContent["entryFrame"], values=kategorie)
        )
        self.podkatContent["podkatEntry"] = (
            ttk.Label(self.podkatContent["entryFrame"], text="Kategoria"),
            ttk.Entry(self.podkatContent["entryFrame"])
        )
        self.podkatContent["submit"] = ttk.Button(self.podkatContent["entryFrame"], text="Zapisz", command=self._safePodkat)

        self.podkatContent["mainLabel"].grid(row=1, column=0, pady=10)
        self.podkatContent["entryFrame"].grid(row=2, column=0, pady=10)

        self.podkatContent["katEntry"][0].grid(row=0, column=0, padx=10, pady=10)
        self.podkatContent["katEntry"][1].grid(row=0, column=1, padx=10, pady=10)

        self.podkatContent["podkatEntry"][0].grid(row=1, column=0, padx=10, pady=10)
        self.podkatContent["podkatEntry"][1].grid(row=1, column=1, padx=10, pady=10)

        self.podkatContent["submit"].grid(row=2, columnspan=2, padx=10, pady=10)

    def _initMagazynFrame(self):
        self.magazynContent = self._getFrame(self.magazynFrame)

        self.magazynContent["mainLabel"] = ttk.Label(self.magazynContent["frame"], text="Magazyn")
        self.magazynContent["entryFrame"] = ttk.Frame(self.magazynContent["frame"], style="Blue.TFrame")

        magazyny = tuple(map(lambda kat: kat[0], Client().select("magazyn", "nazwa")))
        self.magazynContent["magCombo"] = (
            ttk.Label(self.magazynContent["entryFrame"], text="Magazyn:"),
            ttk.Combobox(self.magazynContent["entryFrame"], values=magazyny)
        )
        self.magazynContent["stan"] = []

        self.magazynContent["mainLabel"].grid(row=1, column=0, pady=10)
        self.magazynContent["entryFrame"].grid(row=2, column=0, pady=10)

        self.magazynContent["magCombo"][0].grid(row=0, column=0, padx=10, pady=10)
        self.magazynContent["magCombo"][1].grid(row=0, column=1, padx=10, pady=10)
        self.magazynContent["magCombo"][1].bind('<<ComboboxSelected>>', self._onChangeMag)

    def _getFrame(self, rootFrame):
        rootFrame.grid(row=0, column=0)
        content = {}

        content["frame"] = ttk.Frame(rootFrame, style="Blue.TFrame")
        content["frame"].grid(row=0, column=0)

        content["backButton"] = ttk.Button(content["frame"], text="Ekran Główny", command=lambda: self._returnToMainScreen(rootFrame))
        content["backButton"].grid(row=0, column=0)

        return content
    
    def _returnToMainScreen(self, currentFrame):
        currentFrame.grid_forget()
        self.mainFrame.grid()

    def _onChangeKat(self, event):
        currentKat = self.produktContent["katEntry"][1].get()
        podkat = list(map(
            lambda pk: pk[0],
            Client().select(
                "podkategoria p",
                "p.nazwa",
                join=[("kategorie k", "p.id_kategorii = k.id_kategorii")],
                where=f"k.nazwa LIKE '{currentKat}'"
            )
        ))
        self.produktContent["katEntry"][3].config(values=podkat)

    def _onChangeMag(self, event):
        currentMag = self.magazynContent["magCombo"][1].get()
        stanMag = Client().select(
            "stan_magazynu sm",
            "p.nazwa",
            "sm.ilosc",
            join=[
                ("magazyn m", "sm.id_magazynu = m.id_magazynu"),
                ("produkty p", "sm.id_produktu = p.id_produktu")
            ],
            where=f"m.nazwa LIKE '{currentMag}'"
        )
        for label in self.magazynContent["stan"]:
            label.grid_forget()
            label.destroy()
        self.magazynContent["stan"].clear()
        for i, prod in enumerate(stanMag):
            lab = ttk.Label(self.magazynContent["entryFrame"], text=f"Produkt: {prod[0]} -- ilość: {prod[1]}")
            lab.grid(row=i + 1, columnspan=2, pady=5)
            self.magazynContent["stan"].append(lab)

    def _safeProd(self):
        dane = f"'{self.produktContent['mainEntry'][1].get()}', {self.produktContent['prizeEntry'][1].get()}, '{self.produktContent['opisEntry'][1].get()}', '{self.produktContent['katEntry'][3].get()}', '{self.produktContent['opisEntry'][3].get('1.0', 'end-1c')}', '{self.produktContent['specEntry'][1].get()}'"
        Client().execute(f"SELECT dodaj_produkt({dane})")
        self._returnToMainScreen(self.produktFrame)

    def _safeKat(self):
        Client().insert("kategorie", ("nazwa",), [(self.katContent['katEntry'][1].get(),)])
        self._returnToMainScreen(self.kategorieFrame)

    def _safePodkat(self):
        katId = Client().select("kategorie", "id_kategorii", where=f"nazwa LIKE '{self.podkatContent['katEntry'][1].get()}'")[0][0]
        Client().insert("podkategoria", ("id_kategorii", "nazwa"), [(katId, self.podkatContent['podkatEntry'][1].get())])
        self._returnToMainScreen(self.podkatFrame)

    def _safeMag(self):
        self._returnToMainScreen(self.magazynFrame)
