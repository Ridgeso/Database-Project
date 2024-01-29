from typing import Callable, Tuple, List
from collections import namedtuple, Counter

import tkinter as tk
from tkinter import ttk

from .Interface import Viewport
from sqlMenager import Client


class Shopscreen(Viewport):
    _Item = namedtuple("Item", ("id_produktu", "nazwa", "cena", "id_opisu", "id_podkat", "specyfikacja"))

    def __init__(self, frameroot, onGetUser) -> None:
        self.cart = Counter()
        self.onGetUser = onGetUser
        self.itemsWidgets = []

        self.leftInner = ttk.Frame(frameroot)
        self.leftInner.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.leftInner)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.shopScreen = ttk.Frame(self.canvas, style="Blue.TFrame")
        self.shopScreen.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.leftInner, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.create_window((0, 0), window=self.shopScreen, anchor='nw')

        usersCart = { t[0]: t[1] for t in self._getUserCart() }
        self.cart.update(usersCart)

        self.items = sorted(map(lambda item: self._Item(*item), Client().select("produkty")), key=lambda i: i.id_produktu)
        for i, item in enumerate(self.items):
            self.itemsWidgets.append(self._createItem(i, item))

        self.shopScreen.bind("<Configure>", self._onFrameConfigure)

        ##############

        self.rightInner = ttk.Frame(frameroot)
        self.rightInner.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.showMore = ttk.Frame(self.rightInner, style="Blue.TFrame")
        self.showMore.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.produktName = ttk.Label(self.showMore, text="Kliknij na \"Pokaż więcej\"")
        self.produktName.pack(padx=10, pady=10)
        
        self.produktPrize = ttk.Label(self.showMore, text="")
        self.produktPrize.pack(padx=10, pady=10)
        self.produktBrand = ttk.Label(self.showMore, text="")
        self.produktBrand.pack(padx=10, pady=10)
        self.produktDiscr = ttk.Label(self.showMore, text="")
        self.produktDiscr.pack(padx=10, pady=10)
        self.produktSpecy = ttk.Label(self.showMore, text="")
        self.produktSpecy.pack(padx=10, pady=10)
        self.produktKat = ttk.Label(self.showMore, text="")
        self.produktKat.pack(padx=10, pady=10)

        self.cartFrame = ttk.Frame(self.rightInner, style="Red.TFrame")
        self.cartFrame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.buyItems = ttk.Button(self.cartFrame, text="Zakup", command=self._finalizeShoping)
        self.buyItems.pack(padx=10, pady=10)
        self.cartItems = tk.Label(self.cartFrame, text="")
        self.cartItems.pack(padx=10, pady=10)
        self._showCart()
    
    def _createItem(self, row, item):
        itemFrame = ttk.Frame(self.shopScreen)
        itemLabel = ttk.Label(itemFrame, text=item.nazwa)
        itemsNum = ttk.Entry(itemFrame, width=5)
        cartBehavior = ttk.Button(itemFrame)
        if (id := item.id_produktu) in self.cart:
            cartBehavior.configure(text="Usun z wózka", command=lambda: self._delFromCart(id, cartBehavior, itemsNum))
        else:
            cartBehavior.configure(text="Dodaj do wózka", command=lambda: self._addToCart(id, cartBehavior, itemsNum))
        showMoreButton = ttk.Button(itemFrame, text="Pokaż więcej", command=lambda: self._changeShowMoreFrame(item))

        itemFrame.grid(row=row, column=0, padx=4, pady=4, sticky=(tk.N, tk.S, tk.W, tk.E))
        itemLabel.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        cartBehavior.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)
        itemsNum.grid(row=0, column=2, padx=5, pady=5, sticky=tk.E)
        showMoreButton.grid(row=0, column=3, padx=5, pady=5, sticky=tk.E)

        return (itemFrame, itemLabel, itemsNum, cartBehavior, showMoreButton)

    def _addToCart(self, itemId, cartButton, itemsNum):
        if not itemsNum.get().isdigit():
            return
        self.cart[itemId] = self.cart.setdefault(itemId, 0) + int(itemsNum.get())
        cartButton.configure(text="Usun z wózka", command=lambda: self._delFromCart(itemId, cartButton, itemsNum))
        self._showCart()

    def _delFromCart(self, itemId, cartButton, itemsNum):
        try:
            self.cart[itemId] = 0
            cartButton.configure(text="Dodaj do wózka", command=lambda: self._addToCart(itemId, cartButton, itemsNum))
            self._showCart()
        except ValueError:
            pass
    
    def _showCart(self):
        cartPopup = ""
        for id in self.cart:
            if self.cart[id] == 0:
                continue
            for item in self.items:
                if item.id_produktu == id:
                    cartPopup += f"{item.nazwa}: {self.cart[id]}\n"
                    break
        self.cartItems.configure(text=cartPopup)

    def _getUserCart(self):
        return Client().select("wozek", "id_produktu", "ilosc", where=f"id_client = {self.onGetUser().userId}")
    
    def _onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _changeShowMoreFrame(self, otherItem):
        disc = Client().select("produkt_opis", "producent", "opis", where=f"id_opisu = {otherItem.id_opisu}")
        kat = Client().select("podkategoria pk", "pk.nazwa", "k.nazwa",
            join=[
                ("kategorie k", "pk.id_kategorii = k.id_kategorii")
            ],
            where=f"id_podkat = {otherItem.id_podkat}"
        )

        self.produktName.configure(text=f"{otherItem.nazwa}")
        self.produktPrize.configure(text=f"{otherItem.cena}")
        self.produktBrand.configure(text=f"{disc[0][0]}")
        self.produktDiscr.configure(text=f"{disc[0][1]}", wraplength=400)
        self.produktSpecy.configure(text=f"{otherItem.specyfikacja}")
        self.produktKat.configure(text=f"{kat[0][1]} : {kat[0][0]}")
    
    def _finalizeShoping(self):
        self._updateCartInDB()
        Client().execute(f"SELECT sprzedaj_produkt({self.onGetUser().userId})")
        self.cart = Counter()

    def _updateCartInDB(self):
        cartValues = []
        userId = self.onGetUser().userId
        for id in self.cart:
            cartValues.append((userId, id, self.cart[id]))
        Client().insert("wozek", ("id_client", "id_produktu", "ilosc"), cartValues)

    def __del__(self):
        self._updateCartInDB()
