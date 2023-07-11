#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
10. Étude et identification de la fonction seuil 
"""
import numpy as np
import numpy.random as rd

from graphe import graphe2

"""
Applique la fermeture transitive à la matrice M.
"""
def Trans2(M):
    k = len(M)  # Obtenir la taille de la matrice
    for s in range(k):
        for r in range(k):
            if M[r, s] == 1:
                for t in range(k):
                    if M[s, t] == 1:
                        M[r, t] = 1

    return M
"""
Vérifie si le graphe représenté par la matrice M est fortement connexe.
"""
def fc(M):
    M = np.array(M)  # Convertir la liste M en un tableau numpy
    # Vérifier si la matrice est carrée
    if M.shape[0] != M.shape[1]:
        return False
    M_fermeture = Trans2(M)  # Appliquer la fermeture transitive
    # Vérifier si la matrice est symétrique
    if not np.array_equal(M, M.T):
        return False
    # Vérifier si la matrice résultante ne contient que des 1
    if np.all(M_fermeture == 1):
        return True
    else:
        return False
 
"""
Calcule le pourcentage de graphes de taille n fortement connexes pour un test 
portant sur quelques centaines de graphes. Le test porte maintenant sur des matrices de 
taille n avec une proportion p de 1. 
"""
def test_stat_fc2(n,p):
    num_tests = 10  # Réduire le nombre de tests
    count_fc = 0
    for i in range(num_tests):
        M =graphe2(n,p,0,2)
        if fc(M):
            count_fc += 1
    pourcentage_fc = (count_fc / num_tests) * 100
    return pourcentage_fc
    
"""Détermine ce seuil de forte connexité. (Pour une taille n donnée, on descendra p jusqu’à 
déterminer ce seuil). """
def seuil(n):
    i = 0
    # Initialisation de la variable p à 100 (pourcentage)
    p = 100
    # Boucle tant que i est inférieur à 100 et p est égal à 100
    while i < 100 and p == 100:
        # Appel de la fonction test_stat_fc2 avec les paramètres n et (100-i)/100
        # pour obtenir le pourcentage de tests réussis
        p = test_stat_fc2(n, (100 - i) / 100)
        # Incrémentation de i de 1 à chaque itération
        i += 1
    # Calcul et retourne le seuil en pourcentage en utilisant la valeur finale de i
    return (101 - i) / 100

import matplotlib.pyplot as plt
def graphiqueS ():
    valeurs = list(range(10, 41))
    proba = [seuil(n) for n in valeurs]
    plt.loglog(valeurs, proba, c='blue', label='Seuil de forte connexité')
    plt.xlabel('n')
    plt.ylabel('Probabilité')
    plt.title('Seuil de forte connexité en fonction de la taille du graphe')
    plt.legend()
    plt.show()
    

graphiqueS()
