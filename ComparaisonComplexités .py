#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
6. Comparaison expérimentale des complexités 
Créer une fonction Python TempsDij(n) qui prend en entrée un entier positif n et qui :
• Génère aléatoirement une matrice d'un graphe pondéré à poids positifs de taille n ;
• Calcule tous les plus courts chemins depuis le premier sommet vers tous les autres sommets par l'algorithme de Dijkstra (sans affichage du résultat) ;
• Retourne le temps de calcul utilisé.
"""

import numpy as np
import time

def Dijkstra(M, d):
    Resultats = []
    for point in range(len(M)):
        sommet_actuel = point
        dist = {}  # distances depuis le sommet de départ
        pred = {}  # prédécesseurs sur le chemin le plus court

        # Initialisation des distances et des prédécesseurs
        for i in range(len(M)):
            dist[i] = float('inf')  # On initialise toutes les distances à l'infini
            pred[i] = None  # On initialise tous les prédécesseurs à None

        dist[d] = 0  # La distance du sommet de départ à lui-même est de 0
        pred[d] = d  # Le prédécesseur du sommet de départ est lui-même

        # Mise à jour des distances et des prédécesseurs en utilisant les arêtes directes depuis le sommet de départ
        for j in range(len(M)):
            if M[d][j] < float('inf'):
                dist[j] = M[d][j]  # La distance est la valeur de l'arête directe
                pred[j] = d  # Le prédécesseur est le sommet de départ
            else:
                dist[j] = float('inf')  # Si pas d'arête directe, la distance reste à l'infini

        pred[d] = None  # Le prédécesseur du sommet de départ est None (car pas de prédécesseur)

        A = [d]  # ensemble des sommets visités
        point_suivant = d

        # Calcul des chemins les plus courts
        while sommet_actuel not in A:
            dist.pop(point_suivant)  # Retire le sommet actuel de la liste des distances à explorer
            point_suivant = min(dist, key=dist.get)  # Trouve le sommet suivant avec la plus petite distance
            A.append(point_suivant)
            for j in range(len(M)):
                if M[point_suivant][j] < float('inf') and j not in A:
                    if dist[j] > dist[point_suivant] + M[point_suivant][j]:
                        dist[j] = M[point_suivant][j] + dist[point_suivant]
                        pred[j] = point_suivant
        Chemin = [chr(sommet_actuel + 65)]  # chemin le plus court
        v = sommet_actuel
        while Chemin[-1] != chr(d + 65):
            v = pred[v]
            if v is None:
                break
            c = str(chr(v + 65))
            Chemin.append(c)
        Chemin.reverse()
        if sommet_actuel == d:
            Resultats.append(('Sommet de départ', Chemin))
        elif dist[sommet_actuel] == float('inf'):
            Resultats.append(('Sommet non joignable depuis', chr(d + 65), 'par un chemin dans le graphe G'))
        else:
            Resultats.append((dist[sommet_actuel], ' -> '.join(Chemin)))
    return Resultats

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
    compteur_iterations = {}  # Dictionnaire pour suivre le nombre d'itérations par flèche
    liste_noire = {}  # Dictionnaire pour stocker les sommets exclus
    fleches = {}  # Dictionnaire pour stocker les flèches du graphe

    for i in range(len(M)):
        for j in range(len(M[0])):
            if M[i][j] < float('inf'):
                fleches[(i, j)] = M[i][j]  # Stocke la valeur de la flèche entre les sommets i et j dans le dictionnaire fleches
                compteur_iterations[(i, j)] = 0  # Initialise le compteur d'itérations pour la flèche (i, j) à 0

    dist = {}  # Dictionnaire des distances
    pred = {}  # Dictionnaire des prédécesseurs

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

    return Resultat_final

#importer la fonction qui génère aléatoirement la matrice d’un graphe à n sommets avec une 
#proportion p (pouvant varier de 0 à 1) de flèches (coefficients différents de l’infini).
from graphe import graphe2

""" Prend en entrée un entier positif n et qui : 
•	Généré aléatoirement une matrice d’un graphe pondéré à poids positifs de taille n ; 
•	Calcule tous les plus courts chemins depuis le premier sommet vers tous les autres sommets par l’algorithme de Dijkstra (sans affichage du résultat) ; 
•	Retourne le temps de calcul utilisé. 
"""
def TempsDij(n):
    M = graphe2(n, 0.3, 0, 10) 
    start = time.perf_counter()
    Dijkstra(M, 0)
    stop = time.perf_counter()
    temps_calcul = stop - start
    return temps_calcul

"""Utilise l’algorithme de Bellman-Ford, avec le choix de la liste de flèches 
   le plus efficace, déterminé à la question précédente. """
def TempsBF(n):
    M = graphe2(n, 0.3, 0, 10) 
    start = time.perf_counter()
    BellmanFord_largeur(M, 0)
    stop = time.perf_counter()
    temps_calcul = stop - start
    return temps_calcul

n = 100
print("Temps de calcul algorithme de Disjktra : ", TempsDij(n))
print("Temps de calcul algorithme de Bellman-Ford : ", TempsBF(n), "\n")

# Dessin de son graphe normal et en log-log
import matplotlib.pyplot as plt
valeurs = list(range(2, n))
temps_dij = [TempsDij(n) for n in valeurs]
temps_bf = [TempsBF(n) for n in valeurs]

# connaitre le coefficient directeur 
coeff1Dij = np.polyfit(valeurs, temps_dij, 2)
coeff2Dij = np.polyfit(valeurs, temps_dij, 1)
print("Algorithme de Dijkstra : ")
print("Coefficient directeur de la courbe pour x^2 : ", coeff1Dij[0])
print("Coefficient directeur de la courbe pour x : ", coeff2Dij[0], "\n")

coeff1Belm = np.polyfit(valeurs, temps_bf, 2)
coeff2Belm = np.polyfit(valeurs, temps_bf, 1)
print("Algorithme de Bellman-Ford : ")
print("Coefficient directeur de la courbe pour x^2 : ", coeff1Belm[0])
print("Coefficient directeur de la courbe pour x : ", coeff2Belm[0], "\n")

plt.plot(valeurs, temps_dij, label='Dijkstra')
plt.plot(valeurs, temps_bf, label='Bellman-Ford')

plt.xlabel('n')
plt.ylabel('Temps de calcul (s)')
plt.title("Temps de calcul pour Dijkstra et Bellman-Ford en fonction de n")
plt.legend()
plt.show()
    
