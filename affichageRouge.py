#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2.2 Dessin d'un chemin
Pour un chemin donné par sa suite de sommets visités, celui-ci s'affiche en rouge sur le graphe.
"""
import igraph as ig
import matplotlib.pyplot as plt
import numpy as np

# Créer un graphe vide avec 6 sommets
g = ig.Graph(directed=True)
g.add_vertices(6)

# Définir une matrice de poids pour les arêtes du graphe
matrice = np.array([[float('inf'), 9, float('inf'), float('inf'), float('inf'), float('inf')],
       [float('inf'), float('inf'), 4, float('inf'), -2, float('inf')],
       [float('inf'), -1, float('inf'), float('inf'), float('inf'), -1],
       [2, float('inf'), float('inf'), float('inf'), 8, float('inf')],
       [float('inf'), float('inf'), float('inf'), -3, float('inf'), float('inf')],
       [-1, float('inf'), float('inf'), 0, float('inf'), float('inf')]])

# Définir une liste de sommets représentant le chemin à colorer en rouge
cheminDonne = ['A', 'F', 'D', 'E', 'D', 'A', 'B', 'C']

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


# Appeler la fonction d'affichage avec la matrice et le chemin spécifiés
affichageRouge(matrice, cheminDonne)
