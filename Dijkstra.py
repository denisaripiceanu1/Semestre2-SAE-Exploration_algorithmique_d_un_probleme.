#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
4.1 Codage de l’algorithme de Dijkstra 
"""
import numpy as np
import igraph as ig
import matplotlib.pyplot as plt


# Créer un graphe vide avec 8 sommets
g = ig.Graph(directed=True)
g.add_vertices(7)

# Définir une matrice de poids pour les arêtes du graphe
Graphe = np.array([[float('inf'), float('inf'), float('inf'), float('inf'), 2, 4, float('inf')],
       [float('inf'), float('inf'), 8, float('inf'), float('inf'), float('inf'), 10],
       [6, float('inf'), float('inf'), 12, float('inf'), float('inf'), float('inf')],
       [float('inf'), 1, float('inf'), float('inf'), 10, 3, float('inf')],
       [float('inf'), float('inf'), 4, float('inf'), float('inf'), float('inf'), float('inf')],
       [float('inf'), float('inf'), 5, float('inf'), 1, float('inf'), 19],
       [float('inf'), float('inf'), float('inf'), 3, float('inf'), 2, float('inf')]])

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
Prend en entrée la matrice d’un graphe pondéré à poids positifs, un sommet d de ce graphe donné 
par son indice dans la liste des sommets, et qui, en exécutant l’algorithme de Dijkstra, 
Retourne pour chacun des autres sommets s :
- soit la longueur et l’itinéraire du plus court chemin de d à s ;
- soit la mention ”sommet non joignable à d par un chemin dans le graphe G”. 
"""
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

"""
Prend en entrée la matrice d’un graphe pondéré à poids positifs, un sommet de depart de ce graphe 
donné par son indice dans la liste des sommets, un sommet d'arrivée de ce graphe donné par son 
indice dans la liste des sommets et qui, en exécutant l’algorithme de Dijkstra, 
retourne le plus court chemin entre le sommet de depart et celui d'arrivée et l'affiche en rouge s'il existe
"""
def Dijkstra1(Graphe, depart, arrivee):
    
    Resultats = []
    for point in range(len(Graphe)):
        # Initialisation des dictionnaires dist et pred pour chaque sommet du graphe
        dist = {}
        pred = {}
        for i in range(len(Graphe)):
            dist[i] = float('inf')  # Toutes les distances sont initialisées à l'infini
            pred[i] = None  # Tous les prédécesseurs sont initialisés à None
        dist[depart] = 0  # La distance du sommet de départ à lui-même est de 0
        pred[depart] = depart  # Le prédécesseur du sommet de départ est lui-même
        distR = dist.copy()  # Création d'une copie de dist pour représenter les sommets restants à traiter

        Chemin = []  # Initialisation de la liste Chemin

        while distR:
            point_suivant = min(distR, key=distR.get)
            distR.pop(point_suivant)

            for voisin in range(len(Graphe)):
                if Graphe[point_suivant][voisin] < float('inf'):
                    nouvelle_dist = dist[point_suivant] + Graphe[point_suivant][voisin]
                    if nouvelle_dist < dist[voisin]:
                        dist[voisin] = nouvelle_dist
                        pred[voisin] = point_suivant

        v = arrivee
        while v != depart:
            if v is None:
                break
            Chemin.append(chr(v + 65))  # Conversion de l'indice du sommet en une lettre majuscule
            v = pred[v]

        Chemin.append(chr(depart + 65))  # Ajout du sommet de départ
        Chemin.reverse()  # Inversion du chemin pour l'ordre correct

        if point == arrivee:
            if dist[point] == float('inf'):
                Resultats.append(('Pas de chemin entre', chr(depart + 65), 'et', chr(arrivee + 65)))
            else:
                Resultats.append((dist[point], ' -> '.join(Chemin)))

    affichageRouge(Graphe, Chemin)  # Appel à la fonction d'affichage dans la boucle

    return Resultats


# Appel de la fonction Dijkstra1 avec le graphe, le sommet de départ et le sommet d'arrivée
results = Dijkstra(Graphe, 3)

# Affichage des résultats
for result in results:
    print(result)
