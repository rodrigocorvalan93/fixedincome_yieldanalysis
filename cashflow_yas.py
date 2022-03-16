# -*- coding: utf-8 -*-
#%%
"""
Calculadora Renta Fija
"""
from math import exp, sqrt
from matplotlib.pyplot import plot
import scipy.optimize as sco
import numpy as np
import pandas as pd


class RentaFija:
    """
    Métodos:
        ModDur: Modified duration
        tir: Calculadora TIR
        nvp: calcula el valor presente
    """
    def ModDur(self):
        cf = self.cashflow()
        irr = self.tir()
        md = sum((cp*t)/(1 + irr) ** t for t, cp in cf)/(self._precio*(1+irr))
        return md

    def npv(self, irr):
        cf = self.cashflow()
        return self._precio - sum(cf / (1 + irr) ** t for t, cf in cf)

    def tir(self):
        res1 = sco.least_squares(self.npv, .1)
        return res1.x[0]


class Bono(RentaFija):
    """
    Clase para los bonos con cupón
    """
    def __init__(self, nombre, precio, cpn, freq, vto):
        self.__nombre = nombre
        self._precio = precio
        self._cpn = cpn
        self._freq = freq
        self._vto = vto

    def cashflow(self):
        """
        Función generadora de cashflow (los cashflows son todos regulares)
        Se realiza mediante un list comprehension cada periodo: (t,pago)
        Parámetros:
            freq: Frecuencia de pago dentro de un año, 2=semnianual 4=trimest.
            cpn: Cupón de pago por 100 VN: 5% = 5
            vto: Maturity/Vencimiento en años
        """
        cf = [(t/self._freq, self._cpn / self._freq) for t
              in range(1, self._vto * self._freq)]
        cf.append((self._vto, 100+self._cpn / self._freq))
        return cf

    def __repr__(self):
        return f'{self.__nombre} @ {self._precio:.2f}'


class Letra(RentaFija):
    def __init__(self, nombre, precio, vto, pagofinal):
        self.__nombre = nombre
        self._precio = precio
        self._vto = vto
        self._pagofinal = pagofinal

    def cashflow(self):
        cf = [(self._vto/365., self._pagofinal) for t in range(1)]
        return cf

    def __repr__(self):
        return f'{self.__nombre} @ {self._precio:.2f}'


class Portfolio(RentaFija):
    def __init__(self, nombre):
        self.nombre = nombre
        self.__bonos = []

    def add_instrument(self, bonos, vn):
        """
        Método para agregar bonos al portafolio
        Parámetros:
            VN : cantidad de Valores Nominales de un bono
            bonos: bono a agregar
        """
        self.__bonos.append((vn, bonos))

    def cashflow(self):
        cfs = (list(bonos.cashflow() for vn, bonos in self.__bonos))
        cfr = [j for i in cfs for j in i]
        cfr.sort(key=lambda tup: tup[0]) # ordena por fecha (elemento 0)
        #cfp = sum(cfr[1] for )
        return cfr

    def __repr__(self):
        pos = '\n'.join(f'{vn} - VN {bonos}' for vn, bonos in self.__bonos)
        # port = self.__bonos
        return '\n'.join([f'Portafolio: {self.nombre}',
                          '-' * 20, pos, '-' * 20])


if __name__ == '__main__':
    # Agrego bonos (nombre, precio, cupon%, frecuencia pago, maturity años):
    # calculo tir y duration de cada bono
    b3 = Bono('Bono3años', 98, 5, 2, 3)
    cfb3 = b3.cashflow()
    tirb3 = b3.tir()
    mdb3 = b3.ModDur()
    b2 = Bono('Bono2años', 100, 3, 2, 2)
    cfb2 = b2.cashflow()
    # Agrego la letra (nombre, precio,maturity en dias, preciofinal)
    l90 = Letra('lecap', 100, 90, 101)
    cfl1 = l90.cashflow()
    # Configuro el portafolio
    p = Portfolio('Super fondo portafolio')
    p.add_instrument(b3, 100)
    p.add_instrument(b2, 300)
    p.add_instrument(l90, 150)
    print(p)
    cfp = p.cashflow()
    print("cashflow consolidado", cfp)
    AA26 = Bono('AA26', 75, 7.5, 2, 7)
    cfAA26 = AA26.cashflow()

# %%
