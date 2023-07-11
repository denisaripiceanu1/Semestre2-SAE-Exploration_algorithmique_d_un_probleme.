#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
5 Influence du choix de la liste ordonnée des flèches pour l’algorithme de Bellman-Ford 
On peut choisir cette liste ordonnée des flèches de plusieurs manières : 
•	De manière arbitraire, par choix aléatoire ; 
•	Par un ordre choisi ”en largeur” : un parcours en largeur donne une liste ordonnée de sommets depuis le départe d. On prend toutes les flèches issues de ces sommets. 
•	Par un ordre choisi ”en profondeur” : un parcours en profondeur donne une liste ordonnée de sommets depuis d. On prend toutes les flèches issues de ces sommets. 

On voudrait vérifier ici si cela influence fortement ou non le temps de calcul de l’algorithme de Bellman-Ford. 
•	Modifier le code de Bellman-Ford en 3 variantes selon le mode de construction de la liste des flèches.
•	Rajouter dans le code un compteur afin d’afficher le nombre de tours effectués. 
•	Comparer les résultats sur un même graphe ”grand” (par exemple 50 sommets) généré aléatoirement, et conclure. 
"""
import time

import numpy as np
import numpy.random as rd
from random import shuffle

from graphe import graphe2

Graphe = graphe2(20, 0.2 , 1, 10)

"""Algorithme de Bellman-Ford qui choisit la liste ordonnée des flèches de manière arbitraire, par choix aléatoire 
"""
def BellmanFord_Arbitraire(M, d):
    compteur_iterations = {}  # Dictionnaire pour suivre le nombre d'itérations par flèche
    liste_noire = {}  # Dictionnaire pour stocker les sommets exclus
    fleches = []  # Liste pour stocker les flèches du graphe

    for i in range(len(M)):
        for j in range(len(M[0])):
            if M[i][j] < float('inf'):
                fleches.append(((i, j), M[i][j]))  # Stocke la flèche entre les sommets i et j avec sa valeur
                compteur_iterations[(i, j)] = 0  # Initialise le compteur d'itérations pour la flèche (i, j) à 0

    shuffle(fleches)  # Mélange aléatoire de la liste des flèches

    dist = {}  # Dictionnaire des distances
    pred = {}  # Dictionnaire des prédécesseurs
    compteur_tours = 0  # Compteur de tours

    for j in range(len(M)):
        if j != d:  # Si le sommet j est différent du sommet de départ (d)
            pred[j] = None  # Prédécesseur de j est initialisé à None
            dist[j] = float('inf')  # Distance de d à j est initialisée à l'infini
            liste_noire[j] = []  # Liste des sommets exclus de j est initialisée comme une liste vide
        else:  # Si le sommet j est égal au sommet de départ (d)
            pred[j] = j  # Prédécesseur de j est lui-même (j)
            dist[j] = 0  # Distance de d à d est 0
            liste_noire[j] = []  # Liste des sommets exclus de j est initialisée comme une liste vide

    N = 1  # Variable pour suivre le nombre de mises à jour de distance effectuées
    I = 0  # Compteur d'itérations

    # Algorithme de Bellman-Ford
    while N != 0 and I < len(M):
        N = 0
        for k in fleches:
            if dist[k[0][0]] + k[1] < dist[k[0][1]]:
                dist[k[0][1]] = dist[k[0][0]] + k[1]  # Mise à jour de la distance du sommet
                pred[k[0][1]] = k[0][0]  # Mise à jour du prédécesseur
                compteur_iterations[k[0]] += 1  # Incrémentation du nombre d'itérations
                N += 1
        I += 1
        compteur_tours += 1  # Incrémentation du compteur de tours

    Resultat_final = []  # Résultats finaux (chemin, distance)

    # Recherche des sommets exclus
    for k in compteur_iterations:
        if compteur_iterations[k] >= I - 1:
            liste_noire[k[1]].append(k[0])  # Ajout du sommet exclu à la liste noire du sommet de destination

    for j in range(len(M)):
        if j == d:
            Resultat_final.append(("Sommet de départ", chr(d + 65)))  # Ajout d'un tuple contenant le sommet de départ et sa valeur
        elif pred[j] is not None:
            chemin = []  # Liste pour stocker le chemin
            sommet_actuel = j
            iteration = 0

            # Construction du chemin à partir des prédécesseurs
            while sommet_actuel != d and iteration < len(M):
                chemin.append(chr(sommet_actuel + 65))
                sommet_actuel = pred[sommet_actuel]
                iteration += 1

            if sommet_actuel == d:
                chemin.append(chr(d + 65))  # Ajout du sommet de départ au chemin
                chemin.reverse()  # Inversion du chemin pour obtenir l'ordre correct
                distance = dist[j]
                Resultat_final.append((distance, ' -> '.join(chemin)))  # Ajout du tuple (distance, chemin) au résultat final
            else:
                Resultat_final.append(
                    ("Sommet joignable depuis", chr(d + 65), "par un chemin dans le graphe G, mais pas de plus court chemin (présence d'un cycle négatif)"))
        else:
            Resultat_final.append(
                ("Sommet non joignable depuis", chr(d + 65), "par un chemin dans le graphe G"))

    if pred[d] is not None and pred[d] in liste_noire[d]:
        Resultat_final.append(
            ("Sommet joignable depuis", chr(d + 65),
             "par un chemin dans le graphe G, mais pas de plus court chemin (présence d'un cycle négatif)"))

    return Resultat_final, compteur_tours

result = (BellmanFord_Arbitraire(Graphe, 0))
compteur_tours = result[1]
print("Nombre de tours par choix arbitraire:", compteur_tours, "\n")

"""
Algorithme de Bellman-Ford qui choisit la liste ordonnée des flèches par un ordre choisi 
”en largeur” : un parcours en largeur donne une liste ordonnée de sommets depuis le départe d. 
On prend toutes les flèches issues de ces sommets. 
"""
def pp(M, s):
    n = len(M)       # taille du tableau = nombre de sommets
    couleur = {}     # On colorie tous les sommets en blanc et s en vert
    for i in range(n):
        couleur[i] = 'blanc'
    couleur[s] = 'vert'
    pile = [s]       # on initialise la pile à s
    Resultat = [s] # on initialise la liste des résultats à s

    while pile != []: # tant que la pile n'est pas vide,
        i = pile[-1]          # on prend le dernier sommet i de la pile
        Succ_blanc = []       # on crée la liste de ses successeurs non déjà visités (blancs)
        for j in range(n):
            if M[i, j] != float('inf') and couleur[j] == 'blanc':
                Succ_blanc.append(j)
        if Succ_blanc != []:  # s'il y en a,
            v = Succ_blanc[0]    # on prend le premier (si on veut l'ordre alphabétique)
            couleur[v] = 'vert'   # on le colorie en vert, 
            pile.append(v)      # on l'empile
            Resultat.append(v)  # on le met en liste résultat
        else:               # sinon:
            pile.pop()          # on sort i de la pile

    return Resultat

def BellmanFord_profondeur(M, d):
    compteur_iterations = {}  # Dictionnaire pour suivre le nombre d'itérations par flèche
    liste_noire = {}  # Dictionnaire pour stocker les sommets exclus
    fleches = {}  # Dictionnaire pour stocker les flèches du graphe

    for i in pp(M, d):
        for j in range(len(M[0])):
            if M[i][j] < float('inf'):
                fleches[(i, j)] = M[i][j]  # Stocke la valeur de la flèche entre les sommets i et j dans le dictionnaire fleches
                compteur_iterations[(i, j)] = 0  # Initialise le compteur d'itérations pour la flèche (i, j) à 0

    dist = {}  # Dictionnaire des distances
    pred = {}  # Dictionnaire des prédécesseurs
    compteur_tours = 0  # Compteur de tours

    for j in range(len(M)):
        if j != d:  # Si le sommet j est différent du sommet de départ (d)
            pred[j] = None  # Prédécesseur de j est initialisé à None
            dist[j] = float('inf')  # Distance de d à j est initialisée à l'infini
            liste_noire[j] = []  # Liste des sommets exclus de j est initialisée comme une liste vide
        else:  # Si le sommet j est égal au sommet de départ (d)
            pred[j] = j  # Prédécesseur de j est lui-même (j)
            dist[j] = 0  # Distance de d à d est 0
            liste_noire[j] = []  # Liste des sommets exclus de j est initialisée comme une liste vide

    N = 1  # Variable pour suivre le nombre de mises à jour de distance effectuées
    I = 0  # Compteur d'itérations

    # Algorithme de Bellman-Ford
    while N != 0 and I < len(M):
        N = 0
        for k in fleches:
            if dist[k[0]] + fleches[k] < dist[k[1]]:
                dist[k[1]] = dist[k[0]] + fleches[k]  # Mise à jour de la distance du sommet
                pred[k[1]] = k[0]  # Mise à jour du prédécesseur
                compteur_iterations[k] += 1  # Incrémentation du nombre d'itérations
                N += 1
        I += 1
        compteur_tours += 1  # Incrémentation du compteur de tours

    Resultat_final = []  # Résultats finaux (chemin, distance)

    # Recherche des sommets exclus
    for k in compteur_iterations:
        if compteur_iterations[k] >= I - 1:
            liste_noire[k[1]].append(k[0])  # Ajout du sommet exclu à la liste noire du sommet de destination

    for j in range(len(M)):
        if j == d:
            Resultat_final.append(("Sommet de départ", chr(d + 65)))  # Ajout d'un tuple contenant le sommet de départ et sa valeur
        elif pred[j] is not None:
            chemin = []  # Liste pour stocker le chemin
            sommet_actuel = j
            iteration = 0

            # Construction du chemin à partir des prédécesseurs
            while sommet_actuel != d and iteration < len(M):
                chemin.append(chr(sommet_actuel + 65))
                sommet_actuel = pred[sommet_actuel]
                iteration += 1

            if sommet_actuel == d:
                chemin.append(chr(d + 65))  # Ajout du sommet de départ au chemin
                chemin.reverse()  # Inversion du chemin pour obtenir l'ordre correct
                distance = dist[j]
                Resultat_final.append((distance, ' -> '.join(chemin)))  # Ajout du tuple (distance, chemin) au résultat final
            else:
                Resultat_final.append(
                    ("Sommet joignable depuis", chr(d + 65), "par un chemin dans le graphe G, mais pas de plus court chemin (présence d'un cycle négatif)"))
        else:
            Resultat_final.append(
                ("Sommet non joignable depuis", chr(d + 65), "par un chemin dans le graphe G"))

    if pred[d] is not None and pred[d] in liste_noire[d]:
        Resultat_final.append(
            ("Sommet joignable depuis", chr(d + 65),
             "par un chemin dans le graphe G, mais pas de plus court chemin (présence d'un cycle négatif)"))

    return Resultat_final, compteur_tours

result = BellmanFord_profondeur(Graphe, 0)
compteur_tours = result[1]
print("Nombre de tours parcours en profondeur :", compteur_tours, "\n")


"""
Algorithme de Bellman-Ford qui choisit la liste ordonnée des flèches 
par un ordre choisi ”en profondeur” : un parcours en profondeur donne une liste ordonnée 
de sommets depuis d. On prend toutes les flèches issues de ces sommets. 
"""

def pl(M,s):
    n=len(M)
    couleur={}     # On colorie tous les sommets en blanc et s (départ) en vert
    for i  in range(n):
        couleur[i]='blanc'
    couleur[s]='vert'
    file=[s]
    Resultat=[s]
    while file !=[]:
        i=file[0]           # on prend le premier terme de la file
        for j in range(n):  # On enfile les successeurs de i encore blancs:
            if (M[file[0]][j] != float('inf') and couleur[j]=='blanc'):
                file.append(j)
                couleur[j]='vert' # On les colorie en vert (sommets visités)
                Resultat.append(j) # On les place dans la liste Resultat
        file.pop(0) # on défile i (on retire le premier élément)
    return(Resultat)

def BellmanFord_largeur(M, d):
    compteur_iterations = {}  # Dictionnaire pour suivre le nombre d'itérations par flèche
    liste_noire = {}  # Dictionnaire pour stocker les sommets exclus
    fleches = {}  # Dictionnaire pour stocker les flèches du graphe
    
    for i in pl(M,d):
        for j in range(len(M[0])):
            if M[i][j] < float('inf'):
                fleches[(i, j)] = M[i][j]  # Stocke la valeur de la flèche entre les sommets i et j dans le dictionnaire fleches
                compteur_iterations[(i, j)] = 0  # Initialise le compteur d'itérations pour la flèche (i, j) à 0

    dist = {}  # Dictionnaire des distances
    pred = {}  # Dictionnaire des prédécesseurs
    compteur_tours = 0  # Compteur de tours

    for j in range(len(M)):
        if j != d:  # Si le sommet j est différent du sommet de départ (d)
            pred[j] = None  # Prédécesseur de j est initialisé à None
            dist[j] = float('inf')  # Distance de d à j est initialisée à l'infini
            liste_noire[j] = []  # Liste des sommets exclus de j est initialisée comme une liste vide
        else:  # Si le sommet j est égal au sommet de départ (d)
            pred[j] = j  # Prédécesseur de j est lui-même (j)
            dist[j] = 0  # Distance de d à d est 0
            liste_noire[j] = []  # Liste des sommets exclus de j est initialisée comme une liste vide

    N = 1  # Variable pour suivre le nombre de mises à jour de distance effectuées
    I = 0  # Compteur d'itérations

    # Algorithme de Bellman-Ford
    while N != 0 and I < len(M):
        N = 0
        for k in fleches:
            if dist[k[0]] + fleches[k] < dist[k[1]]:
                dist[k[1]] = dist[k[0]] + fleches[k]  # Mise à jour de la distance du sommet
                pred[k[1]] = k[0]  # Mise à jour du prédécesseur
                compteur_iterations[k] += 1  # Incrémentation du nombre d'itérations
                N += 1
        I += 1
        compteur_tours += 1  # Incrémentation du compteur de tours

    Resultat_final = []  # Résultats finaux (chemin, distance)

    # Recherche des sommets exclus
    for k in compteur_iterations:
        if compteur_iterations[k] >= I - 1:
            liste_noire[k[1]].append(k[0])  # Ajout du sommet exclu à la liste noire du sommet de destination

    for j in range(len(M)):
        if j == d:
            Resultat_final.append(("Sommet de départ", chr(d + 65)))  # Ajout d'un tuple contenant le sommet de départ et sa valeur
        elif pred[j] is not None:
            chemin = []  # Liste pour stocker le chemin
            sommet_actuel = j
            iteration = 0

            # Construction du chemin à partir des prédécesseurs
            while sommet_actuel != d and iteration < len(M):
                chemin.append(chr(sommet_actuel + 65))
                sommet_actuel = pred[sommet_actuel]
                iteration += 1

            if sommet_actuel == d:
                chemin.append(chr(d + 65))  # Ajout du sommet de départ au chemin
                chemin.reverse()  # Inversion du chemin pour obtenir l'ordre correct
                distance = dist[j]
                Resultat_final.append((distance, ' -> '.join(chemin)))  # Ajout du tuple (distance, chemin) au résultat final
            else:
                Resultat_final.append(
                    ("Sommet joignable depuis", chr(d + 65), "par un chemin dans le graphe G, mais pas de plus court chemin (présence d'un cycle négatif)"))
        else:
            Resultat_final.append(
                ("Sommet non joignable depuis", chr(d + 65), "par un chemin dans le graphe G"))

    if pred[d] is not None and pred[d] in liste_noire[d]:
        Resultat_final.append(
            ("Sommet joignable depuis", chr(d + 65),
             "par un chemin dans le graphe G, mais pas de plus court chemin (présence d'un cycle négatif)"))

    return Resultat_final, compteur_tours

result = (BellmanFord_largeur(Graphe, 0))
compteur_tours = result[1]
print("Nombre de tours parcours en largeur:", compteur_tours, "\n")


