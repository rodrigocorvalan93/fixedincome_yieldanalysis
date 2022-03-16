#%%
import pandas as pd
import numpy as np
import scipy.optimize as sco
import datetime as dt



class RentaFija:
    pass

class Portfolio:
    def __init__(self, nombre_portfolio):
        self.nombre_portfolio = nombre_portfolio
        self.book = []
        self.assets = pd.DataFrame(self.book, columns=["name","id_isin","vn"]).groupby('id_isin','')

    def add_operation(self, operacion, contraparte,
                    name, id_isin, vn, plazo,
                    fecha, fecha_settlement, full_price):
        """
        Método para ingresar operaciones
        parameters:
            operacion: str "compra", "venta", "suscripcion", "rescate"
            contraparte: str ie "AR Partners", "Industrial Valores"
            name: str nombre del titulo
            id_isin: str ISIN
            vn: float notional o unidades de valor nominal
            plazo: int "t+ plazo" dias a liquidar
            fecha: datetime fecha operación 
        """
        if operacion == "compra":
            self.book.append((name, id_isin, vn))
        elif operacion == "venta":
            self.book.append((name, id_isin, -vn))
        elif operacion == "rescate":
            self.book.append((name, id_isin, -vn))
        elif operacion == "suscripcion":
            self.book.append((name, id_isin, vn))
        else:
            print("Error al cargar tipo de operacion")
            pass



    def remove_instrument(self):
        """
        Método para remover última entrada
        """
        self.book.pop()

    def add_instrument(self, name, id_isin, vn):
        """
        Método para agregar activos al portafolio
        Parámetros:
            name: nombre del activo
            id_isin: ISIN del activo
            vn: notional, unidades nominales del activo
        """
        self.book.append((name, id_isin, vn))

    
# %%
