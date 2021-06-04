from interfata import Interfata
from stare import Stare, Table
from util import check_inbound, find_jaguar
from joc import Joc
import pygame
import sys
from queue import Queue
from threading import Thread
import time
import os

def mouse_control(q, end,  interfata):
    """Functie care asculta pentru clickuri de mouse

    Args:
        q ([queue]): coada prin care se trimit informatii catre threadul principal
        end (queue): coada care comunica acestui thread cand este finalizata executia programului
        interfata (Interfata): interfata jocului
    """    
    while True:
        if not end.empty():
            print("ending...")
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                q.put(("exit"))
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for np in range(len(interfata.celule_grid)):
                        if interfata.celule_grid[np].collidepoint(pos):
                            if np < 25:
                                linie = np // 5
                                coloana = np % 5
                            elif np < 28:
                                linie = 5
                                coloana = np - 24
                            else:
                                linie = 6
                                coloana = 4 - (30 - np) * 2
                    index = linie * 5 + coloana
                    if index > 25 and index < 30:
                        index -= 1
                    if index == 30:
                        index = 28
                    if index == 32:
                        index = 29
                    if index == 34:
                        index = 30
                    q.put(("mouse click", index))
                    pygame.event.clear()


def min_max(stare):
    if stare.adancime == 0 or stare.joc.final():
        stare.scor = stare.joc.estimeaza_scor(stare.adancime)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutari_scor = [min_max(mutare)
                   for mutare in stare.mutari_posibile]

    # for x in mutari_scor:
    #     print(x.joc.tabla_joc,"scor = ", x.scor)

    if stare.j_curent == stare.joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu scorul maxim
        stare.stare_aleasa = max(mutari_scor, key=lambda x: x.scor)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu scorul minim
        stare.stare_aleasa = min(mutari_scor, key=lambda x: x.scor)
    stare.scor = stare.stare_aleasa.scor
    return stare


def alpha_beta(alpha, beta, stare):
    if stare.adancime == 0 or stare.joc.final():
        stare.scor = stare.joc.estimeaza_scor(stare.adancime)
        return stare

    if alpha > beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == stare.joc.JMAX:
        scor_curent = float('-inf')
        for mutare in stare.mutari_posibile:
            # calculeaza scorul
            stare_noua = alpha_beta(alpha, beta, mutare)

            if (scor_curent < stare_noua.scor):
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor
            if(alpha < stare_noua.scor):
                alpha = stare_noua.scor
                if alpha >= beta:
                    break

    elif stare.j_curent == stare.joc.JMIN:
        scor_curent = float('inf')

        for mutare in stare.mutari_posibile:

            stare_noua = alpha_beta(alpha, beta, mutare)

            if (scor_curent > stare_noua.scor):
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor

            if(beta > stare_noua.scor):
                beta = stare_noua.scor
                if alpha >= beta:
                    break
    stare.scor = stare.stare_aleasa.scor

    return stare


def pvp(joc, interfata, stare_curenta, q, end):
    """Joc player vs player

    Args:
        joc (Joc): jocul curent
        interfata (Interfata): interfata pe care e desenat jocul
        stare_curenta (Stare): starea initiala
        q ([queue]): coada prin care se primesc informatii de la threadul mouse_control
        end (queue): coada care comunica threadului mouse_control sa se opreasca

    Returns:
        String: castigatorul jocului
    """    
    piesa = None
    while True:
        winner = joc.final()
        if winner is not None:
            end.put("END")
            return winner
        res = q.get()
        if res[0] == "exit":
            sys.exit()
        if res[0] == "mouse click":
            index = res[1]
            if stare_curenta.j_curent == "CAINE":
                aux = joc.select(joc.tabla_joc.nodes[index])
                if aux is not None:
                    piesa = aux
                if piesa is None:
                    continue
                rez = joc.move(joc.tabla_joc.nodes[index], piesa, True)
                interfata.update_board(joc.tabla_joc)
                if rez is None:
                    continue
            else:
                if index is not None:
                    src = joc.tabla_joc.nodes[index]
                print(piesa, src)
                rez = joc.move(src,
                               find_jaguar(joc.tabla_joc), True)
                interfata.update_board(joc.tabla_joc)
                if rez is None:
                    continue
            stare_curenta.j_curent = joc.jucator_opus(
                stare_curenta.j_curent)
            print("Tabla dupa mutarea jucatorului\n"+str(stare_curenta))
            piesa = None


def pve(joc, interfata, stare_curenta, q, end):
    """Joc player vs computer

    Args:
        joc (Joc): jocul curent
        interfata (Interfata): interfata pe care e desenat jocul
        stare_curenta (Stare): starea initiala
        q ([queue]): coada prin care se primesc informatii de la threadul mouse_control
        end (queue): coada care comunica threadului mouse_control sa se opreasca

    Returns:
        String: castigatorul jocului
    """  
    piesa = None
    while True:
        winner = joc.final()
        interfata.update_board(joc.tabla_joc)
        if winner is not None:
            end.put("END")
            return winner
        if stare_curenta.j_curent == joc.JMIN:
            while True:
                res = q.get()
                if res[0] == "exit":
                    sys.exit()
                if res[0] == "mouse click":
                    index = res[1]
                    if stare_curenta.j_curent == "CAINE":
                        aux = joc.select(joc.tabla_joc.nodes[index])
                        if aux is not None:
                            piesa = aux
                        if piesa is None:
                            continue
                        rez = joc.move(joc.tabla_joc.nodes[index], piesa)
                        interfata.update_board(joc.tabla_joc)
                        print("\nTabla dupa mutarea jucatorului")
                        print(str(stare_curenta))
                        if rez is None:
                            continue
                    else:
                        if index is not None:
                            src = joc.tabla_joc.nodes[index]
                        print(piesa, src)
                        rez = joc.move(src,
                                       find_jaguar(joc.tabla_joc))
                        interfata.update_board(joc.tabla_joc)
                        if rez is None:
                            continue

                    stare_curenta.j_curent = joc.jucator_opus(
                        stare_curenta.j_curent)
                    print("Tabla dupa mutarea jucatorului\n"+str(stare_curenta))
                    interfata.update_board(joc.tabla_joc)
                    piesa = None
                    break

        else:  # jucatorul e JMAX (calculatorul)
            # Mutare calculator

            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))
            if joc.algorithm == 'Minimax':
                stare_actualizata = min_max(stare_curenta)
            else:  # tip_algoritm=="alphabeta"
                stare_actualizata = alpha_beta(-500,
                                               500, stare_curenta)
            stare_curenta.joc = stare_actualizata.stare_aleasa.joc

            print("Tabla dupa mutarea calculatorului\n"+str(stare_curenta))

            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " +
                  str(t_dupa-t_inainte)+" milisecunde.")

            interfata.update_board(joc.tabla_joc)

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            joc = stare_curenta.joc
            stare_curenta.j_curent = joc.jucator_opus(
                stare_curenta.j_curent)


def no_player(joc, interfata, stare_curenta, q, end):
    """Joc computer vs computer

    Args:
        joc (Joc): jocul curent
        interfata (Interfata): interfata pe care e desenat jocul
        stare_curenta (Stare): starea initiala
        q ([queue]): coada prin care se primesc informatii de la threadul mouse_control
        end (queue): coada care comunica threadului mouse_control sa se opreasca

    Returns:
        String: castigatorul jocului
    """  
    while True:
        joc.JMAX, joc.JMIN = joc.JMIN, joc.JMAX
        winner = joc.final()
        interfata.update_board(joc.tabla_joc)
        if winner is not None:
            end.put("END")
            return winner
        t_inainte = int(round(time.time() * 1000))
        if joc.algorithm == 'Minimax':
            stare_actualizata = min_max(stare_curenta)
        else:  # tip_algoritm=="alphabeta"
            stare_actualizata = alpha_beta(-500,
                                           500, stare_curenta)
        stare_curenta.joc = stare_actualizata.stare_aleasa.joc

        print("Tabla dupa mutarea calculatorului\n"+str(stare_curenta))

        # preiau timpul in milisecunde de dupa mutare
        t_dupa = int(round(time.time() * 1000))
        print("Calculatorul a \"gandit\" timp de " +
              str(t_dupa-t_inainte)+" milisecunde.")

        interfata.update_board(joc.tabla_joc)

        # S-a realizat o mutare. Schimb jucatorul cu cel opus
        joc = stare_curenta.joc
        stare_curenta.j_curent = joc.jucator_opus(
            stare_curenta.j_curent)


def main():
    interfata = Interfata()

    while True:
        joc = Joc(Table())
        Joc.seteaza_interfata(interfata)

        interfata.meniu(joc)
        interfata.stare_initiala()

        joc.JMAX = 'CAINE' if joc.JMIN == 'JAGUAR' else 'JAGUAR'
        stare_curenta = Stare(joc, j_curent='JAGUAR', adancime=joc.adancime)

        q = Queue()
        end = Queue()
        mouse = Thread(target=mouse_control, args=(q, end, interfata))
        mouse.start()

        if joc.type == "PVP":
            winner = pvp(joc, interfata, stare_curenta, q, end)
        elif joc.type == "PVE":
            winner = pve(joc, interfata, stare_curenta, q, end)
        else:
            winner = no_player(joc, interfata, stare_curenta, q, end)

        interfata.end_game(winner)


if __name__ == "__main__":
    main()
