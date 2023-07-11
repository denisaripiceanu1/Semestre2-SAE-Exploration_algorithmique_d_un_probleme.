#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
4.2 Codage de l’algorithme de Belman-Ford 
"""
import numpy as np
import igraph as ig
import matplotlib.pyplot as plt

# Créer un graphe vide avec 6 sommets
g = ig.Graph(directed=True)
g.add_vertices(6)

Graphe = np.array([[float('inf'), 3, float('inf'), float('inf'), float('inf'), float('inf')],
                   [float('inf'), float('inf'), 4, float('inf'), 2, 1],
                   [float('inf'), -1, float('inf'), float('inf'), float('inf'), float('inf')],
                   [2, float('inf'), float('inf'), float('inf'), 8, float('inf')],
                   [float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 9],
                   [float('inf'), float('inf'), float('inf'), float('inf'), -3, float('inf')]])

# Définir une fonction pour afficher le graphe avec le chemin coloré en rouge
def affichageRouge(matrice, chemin):
    cheminRes = []
    for i in range(len(chemin) - 1):
        cheminRes.append((ord(chemin[i]) - 65, ord(chemin[i + 1]) - 65))  # Convertir les lettres en indices entiers

    for i in range(len(g.vs)):
        g.vs[i]["id"] = i
        g.vs[i]["label"] = str(chr(i + 65))

    # Ajouter les arêtes au graphe en fonction de la matrice de poids
    liste = []  # Liste des arêtes
    poids = []  # Liste des poids des arêtes
    reflexif = []  # Liste pour vérifier si une arête est réflexive
    for i in range(len(matrice)):
        for j in range(len(matrice)):
            if matrice[i][j] < float('inf'):  # Vérifier si l'arête existe
                liste.append((i, j))  # Ajouter l'arête à la liste
                poids.append(int(matrice[i][j]))  # Ajouter le poids de l'arête à la liste
                reflexif.append(i == j)  # Vérifier si l'arête est réflexive (du sommet i à i)

    # Ajouter les sommets et les arêtes au graphe
    g.add_edges(liste)

    # Ajouter les poids et les labels aux arêtes
    g.es['weight'] = poids
    g.es['label'] = poids

    # Initialiser une liste de couleurs pour les arêtes (gris)
    couleurs_arêtes = ['dark gray'] * len(liste)

    # Parcourir les arêtes et mettre en rouge celles qui appartiennent au chemin donné
    for i, arête in enumerate(liste):
        if arête in cheminRes:
            couleurs_arêtes[i] = 'red'

    # Appliquer les couleurs aux arêtes
    g.es['color'] = couleurs_arêtes

    # Créer la figure et les axes pour l'affichage
    fig, ax = plt.subplots(figsize=(7, 7))

    # Afficher le graphe avec des arêtes de couleur sombre et les poids des arêtes comme labels
    edge_labels = [g.es["weight"][x] if not reflexif[x] else "         " + str(g.es["weight"][x]) for x in range(len(poids))]
    ig.plot(g, target=ax, edge_label=edge_labels,
         edge_background=["white" if not reflexif[x] else (1, 1, 1, 0) for x in range(len(poids))])

    plt.show()
 
"""
Prend en entrée la matrice d’un graphe pondéré à poids de signe quelconque, 
un sommet d de ce graphe donné par son indice dans la liste des sommets, et qui, 
en exécutant l’algorithme de Bellman-Ford, retourne pour chacun des autres sommets s :
    - soit la longueur et l’itinéraire du plus court chemin de d à s ;
    - soit la mention ”sommet non joignable depuis d par un chemin dans le graphe G”.
    - soit la mention ”sommet joignable depuis d par un chemin dans le graphe G, mais pas de plus court chemin (présence d’un cycle n négatif)”.
"""
def BellmanFord(M, d):
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

"""
Prend en entrée la matrice d’un graphe pondéré à poids de signe quelconque, 
un sommet de depart d de ce graphe donné par son indice dans la liste des sommets, 
un sommet d'arrivée a de ce graphe donné par son indice dans la liste des sommets et  
Retourne le plus court chemin entre le sommet de depart et celui d'arrivée et l'affiche en rouge s'il existe
"""
def BellmanFord1(M, d, a):
    compteur_iterations = {}  # Dictionnaire pour suivre le nombre d'itérations par flèche
    liste_noire = {}  # Dictionnaire pour stocker les sommets exclus
    fleches = {}  # Dictionnaire pour stocker les flèches du graphe

    for i in range(len(M)):
        for j in range(len(M[0])):
            if M[i][j] != float('inf'):
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

    # Recherche du plus court chemin
    if pred[a] is not None:
        chemin = []  # Liste pour stocker le chemin
        sommet_actuel = a
        iteration = 0

        # Construction du chemin à partir des prédécesseurs
        while sommet_actuel != d and iteration < len(M):
            chemin.append(chr(sommet_actuel + 65))
            sommet_actuel = pred[sommet_actuel]
            iteration += 1

        if sommet_actuel == d:
            chemin.append(chr(d + 65))  # Ajout du sommet de départ au chemin
            chemin.reverse()  # Inversion du chemin pour obtenir l'ordre correct
            distance = dist[a]
            print("Plus court chemin trouvé !")
            print("Longueur :", distance)
            print("Itinéraire :", ' -> '.join(chemin))
            affichageRouge(M, chemin)
        else:
            print("Sommet joignable depuis", chr(d + 65),
                  "par un chemin dans le graphe G, mais pas de plus court chemin (présence d'un cycle négatif)")
    else:
        print("Sommet non joignable depuis", chr(d + 65), "par un chemin dans le graphe G")


# Appel de la fonction BellmanFord avec le graphe et le sommet de départ
results = BellmanFord(Graphe, 1)

for result in results:
    print(result)



