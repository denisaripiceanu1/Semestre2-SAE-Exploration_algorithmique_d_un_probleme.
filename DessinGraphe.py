#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2.1
À partir de la matrice d’un graphe pondéré donne un dessin de ce graphe.
"""

import igraph as ig
import matplotlib.pyplot as plt
import numpy as np

# Créer un graphe vide avec 7 sommets
g = ig.Graph(directed=True)
g.add_vertices(6)

matrice = np.array([[float('inf'), 9, float('inf'), float('inf'), float('inf'), float('inf')],
       [float('inf'), float('inf'), 4, float('inf'), -2, float('inf')],
       [float('inf'), -1, float('inf'), float('inf'), float('inf'), -1],
       [2, float('inf'), float('inf'), float('inf'), 8, float('inf')],
       [float('inf'), float('inf'), float('inf'), -3, float('inf'), float('inf')], 
       [-1, float('inf'), float('inf'), 0, float('inf'), float('inf')]])

# Ajouter des identifiants et des labels aux sommets
for i in range(len(g.vs)):
    g.vs[i]["id"]= i
    g.vs[i]["label"]= str(chr(i+65))

# Ajouter les arêtes
liste = []
poids = []
reflexif = []
for i in range(len(matrice)):
        for j in range(len(matrice)):
            if matrice[i][j] < float('inf'):
                liste.append((i, j))
                poids.append(int(matrice[i][j]))
                reflexif.append(i==j)
g.add_edges(liste)

# Ajouter les poids et les labels des arêtes
g.es['weight'] = poids
g.es['label'] = poids

# Créer la figure et les axes pour l'affichage
fig, ax = plt.subplots(figsize=(5,5))

# Afficher le graphe avec des arêtes de couleur sombre et les poids des arêtes comme labels
edge_labels = [g.es["weight"][x] if not reflexif[x] else "         " + str(g.es["weight"][x]) for x in range(len(poids))]
ig.plot(g, target=ax, edge_color='dark gray', edge_label=edge_labels,
     edge_background=["white" if not reflexif[x] else (1, 1, 1, 0) for x in range(len(poids))])
