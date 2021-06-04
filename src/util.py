
import pygame

def check_inbound(i, j):
    """Verifica daca pozitia se afla in tabla de joc
    """    
    return i >= 0 and j >= 0 and i < 7 and j < 5


def find_jaguar(tabla):
    """Functie care gaseste jaguarul pe tabla de joc
    """    
    for x in tabla.nodes:
        if x is not None and x.value == '1':
            return x