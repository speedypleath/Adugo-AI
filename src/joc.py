

class Joc:
    JMIN = None
    JMAX = None
    GOL = '#'
    JAGUAR = '1'
    CAINE = '0'
    interfata = None
    def __init__(self, tabla, matr=None):
        self.tabla_joc = tabla
        self.ultima_mutare = None
        self.JMIN = 'JAGUAR'
        self.adancime = 2
        self.type = 'PVP'
        self.algorithm = 'Minimax'
        self.scor = 0
        if matr:
            self.matr = matr
        else:
            self.matr = [[' '] * 5 for i in range(7)]
            for i in range(0, 3):
                for j in range(0, 5):
                    self.matr[i][j] = self.CAINE
            for i in range(3, 5):
                for j in range(0, 5):
                    self.matr[i][j] = self.GOL
            for i in range(1, 4):
                self.matr[5][i] = self.GOL
            for i in range(0, 5, 2):
                self.matr[6][i] = self.GOL
            self.matr[3][2] = self.JAGUAR

    @classmethod
    def seteaza_interfata(cls, interfata):
        cls.interfata = interfata

    def capture(self, piesa, jaguar):
        """Functie prin care o piesa este capturata
        """
        linie = piesa.x_value - jaguar.x_value
        coloana = piesa.y_value - jaguar.y_value
        index = (jaguar.x_value + (linie // 2)) * \
            5 + jaguar.y_value + coloana // 2
        if index > 24 and index < 28:
                index = index - 1
        elif index > 27:
            index = 28 + (index - 30) // 2
        if self.tabla_joc.testeaza_capturare(piesa, jaguar):
            self.tabla_joc.nodes[index].value = '#'
            casuta_noua = linie * 5 + coloana
            piesa.value = '1'
            jaguar.value = '#'

    def move(self, pozitie, piesa, player_move=False):
        """Functie prin care o piesa este mutata
        """
        if piesa.value == '1':
            self.capture(
            pozitie, piesa)
        if self.tabla_joc.testeaza_mutare(pozitie, piesa):
            pozitie.value = piesa.value
            piesa.value = '#'
            return "Done"

    def select(self, piesa):
        """Functie prin care se selecteaza piesa care urmeaza sa fie mutata
        """
        if piesa.value == '0':
            self.__class__.interfata.update_board(self.tabla_joc)
            self.__class__.interfata.markup(piesa)
            return piesa

    def change_difficulty(self, value, difficulty):
        self.adancime = difficulty

    def change_algorithm(self, value, algorithm):
        self.algorithm = algorithm

    def change_player(self, value, player):
        self.JMIN = player

    def change_type(self, value, type):
        self.type = type

    def jucator_opus(self, jucator):
        return self.JMAX if jucator == self.JMIN else self.JMIN

    def final(self):
        if self.tabla_joc.mutari_jaguar() == []:
            return "Dogs wins"
        if self.tabla_joc.count_dogs() <= 9:
            return "Jaguar wins"

    def estimeaza_scor(self, adancime):
        """Functia de estimare scor
        Pentru jaguar - functia testeaza cati caini raman pe tabla in urma miscarii, cu cat sunt mai putini cu atat scorul este mai mare
        Pentru caini - functia testeaza cate mutari posibile are jaguarul
        """
        t_final = self.final()
        if self.JMAX == "JAGUAR":
            scor_maxim = 14
        else:
            scor_maxim = 16
        if t_final == self.JMAX:
            return (scor_maxim+adancime)
        elif t_final == self.JMIN:
            return (-scor_maxim-adancime)
        elif self.JMAX == "JAGUAR":
            return 16 - self.tabla_joc.count_dogs()
        return 16 - len(self.tabla_joc.mutari_jaguar())

    def sir_afisare(self):
        sir = "  |"
        sir += " ".join([str(i) for i in range(5)])+"\n"
        sir += "-"*16+"\n"
        sir += "\n".join([str(i)+" |"+" ".join([str(x)
                         for x in self.matr[i]]) for i in range(len(self.matr))])
        return sir

    def __str__(self):
        return self.sir_afisare()

    def __repr__(self):
        return self.sir_afisare()
