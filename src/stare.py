import pygame
from joc import Joc
from util import check_inbound, find_jaguar
import copy

class Nod:
    def __init__(self, x_value, y_value):
        self.x_value = x_value
        self.y_value = y_value
        self.value = '#'
        self.neighbors = []


class Table:
    """Clasa care reprezinta o tabla de joc
    Casutele sunt memorate sub forma undei liste de noduri
    """    
    def __init__(self):
        self.nodes = []
        for x in range(5):
            for y in range(5):
                self.nodes.append(Nod(x, y))
                self.nodes[-1].index = 5 * x + y
        for coloana in range(1, 4):
            self.nodes.append(Nod(5, coloana))
            self.nodes[-1].index = 24 + coloana
        for coloana in range(0, 5, 2):
            self.nodes.append(Nod(6, coloana))
            self.nodes[-1].index = 28 + coloana // 2
        for k in range(25):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if k % 2 == 1 and (i == j or i == -j):
                        continue
                    linie = k // 5
                    coloana = k % 5
                    index = (linie + i) * 5 + coloana + j
                    if check_inbound(linie + i, coloana + j) and index != k and index < 25:
                        self.nodes[k].neighbors.append(self.nodes[index])
        self.nodes[22].neighbors.extend([self.nodes[25], self.nodes[26], self.nodes[27]])
        self.nodes[25].neighbors.extend([self.nodes[22], self.nodes[26], self.nodes[28]])
        self.nodes[26].neighbors.extend([self.nodes[22], self.nodes[25], self.nodes[27], self.nodes[29]])
        self.nodes[27].neighbors.extend([self.nodes[22], self.nodes[26], self.nodes[30]])
        self.nodes[28].neighbors.extend([self.nodes[25], self.nodes[29]])
        self.nodes[29].neighbors.extend([self.nodes[26], self.nodes[28], self.nodes[30]])
        self.nodes[30].neighbors.extend([self.nodes[27], self.nodes[29]])
        for i in range(15):
            self.nodes[i].value = '0'
        self.nodes[12].value = '1'
        for i in range(16, 31):
            self.nodes[i].value = '#'

    def table(self):
        """Functie care transforma tabla de joc intr-o matrice
        """        
        table = [[' ' for i in range(5)] for j in range(7)]
        for k in range(25):
            linie = k // 5
            coloana = k % 5
            table[linie][coloana] = self.nodes[k].value
        for k in range(25, 28):
            table[5][k-24] = self.nodes[k].value
        for k in range(28, 31):
            table[6][(k-28)*2] = self.nodes[k].value
        return '\n'.join([''.join(['{:4}'.format(item) for item in row])
                          for row in table])

    def testeaza_mutare(self, pozitie, piesa):
        if pozitie.value == '#' and pozitie in piesa.neighbors:
            return True
        return False

    def testeaza_capturare(self, piesa, jaguar):
        """Functie care testeaza daca jaguarul poate captura o anumita piesa
        """        
        linie = piesa.x_value - jaguar.x_value
        coloana = piesa.y_value - jaguar.y_value
        if piesa.x_value == 6 and jaguar.x_value == 6:
            possible = {-4, 0, 4}
        else:
            possible = {-2, 0, 2}
        if coloana in possible and linie in possible:
            index_piesa = (piesa.x_value + (linie // 2)) * \
                5 + piesa.y_value + coloana // 2
            if index_piesa % 2 == 1 and abs(linie) == abs(coloana):
                return False
            index = (jaguar.x_value + (linie // 2)) * \
                5 + jaguar.y_value + coloana // 2
            if index > 24 and index < 28:
                index = index - 1
            elif index > 27:
                index = 28 + (index - 30) // 2
            if self.nodes[index].value == '0' and piesa.value == '#':
                return True

    def count_dogs(self):
        """Functie care numara cati caini sunt pe table
        """        
        count = 0
        for piesa in self.nodes:
            if piesa.value == "0":
                count += 1
        return count
    
    def mutari_jaguar(self):
        """Functie care genereaza mutarile jaguarului
        """
        jaguar = find_jaguar(self)
        l_mutari = []
        for piesa in jaguar.neighbors:
            if self.testeaza_mutare(piesa, jaguar):
                l_mutari.append((self.nodes.index(piesa), self.nodes.index(jaguar)))
            if piesa.value == '0':
                linie = piesa.x_value - jaguar.x_value
                coloana = piesa.y_value - jaguar.y_value
                index = (jaguar.x_value + (linie * 2)) * \
                    5 + jaguar.y_value + coloana * 2
                if index > 24 and index < 28:
                    index = index - 1
                elif index > 28 and index < 35:
                    index = 28 + (index - 30) // 2
                else:
                    continue
                urm_piesa = self.nodes[index]
                if urm_piesa.value == '#' and index >= 0:
                    l_mutari.append((index, self.nodes.index(jaguar)))
        return l_mutari

    def mutari_caini(self):
        """Functie care genereaza mutarile cainilor
        """
        l_mutari = []
        for piesa in self.nodes:
            if piesa.value == '0':
                for x in piesa.neighbors:
                    if x.value == '#':
                        l_mutari.append((self.nodes.index(x), self.nodes.index(piesa)))
        return l_mutari
    
    def __str__(self):
        sir = str(self.table()) 
        return sir

    def __repr__(self):
        sir = str(self.table()) + "\n\n"
        return sir


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile posibile in urma mutarii unui jucator
    """

    def __init__(self, joc, j_curent, adancime, parinte=None, scor=None):
        self.joc = joc
        self.j_curent = j_curent

        # adancimea in arborele de stari
        self.adancime = adancime

        # scorul starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.scor = scor

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def mutari(self):
        """Functie care genereaza mutarile jucatorului curent

        Returns:
            lista mutarilor posibile
        """        
        if self.j_curent == "JAGUAR":
            l_mutari = self.joc.tabla_joc.mutari_jaguar()
        else:
            l_mutari = self.joc.tabla_joc.mutari_caini()
        
        
        juc_opus = self.joc.jucator_opus(self.j_curent)
        l_stari_mutari = []
        for pozitie, piesa in l_mutari:
            joc_nou = copy.deepcopy(self.joc)
            joc_nou.move(joc_nou.tabla_joc.nodes[pozitie], joc_nou.tabla_joc.nodes[piesa])
            l_stari_mutari.append(Stare(joc_nou, juc_opus, self.adancime-1, parinte=self))

        return l_stari_mutari

    def __str__(self):
        sir = str(self.joc.tabla_joc) + "(Joc curent:"+self.j_curent+")\n"
        return sir

    def __repr__(self):
        sir = str(self.joc.tabla_joc) + "(Juc curent:"+self.j_curent+")\n"
        return sir
