#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 09:23:05 2023

@author: denisaripiceanu
"""
import numpy as np
import numpy.random as rd

from graphe import graphe2

"""
Applique la fermeture transitive à la matrice M.
"""
def Trans2(M):
    k = len(M)  # Obtenir la taille de la matrice

    # Parcourir les sommets r et s
    for s in range(k):
        for r in range(k):
            # Vérifier si l'arête r -> s existe
            if M[r, s] == 1:
                # Parcourir les sommets s et t
                for t in range(k):
                    # Vérifier si l'arête s -> t existe
                    if M[s, t] == 1:
                        # Mettre à jour l'existence de l'arête r -> t
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
    # Définition du nombre de tests
    nombre_tests = 200
    # Compteur pour le nombre de fois où la fonction fc renvoie True
    compte_fc = 0
    # Boucle pour effectuer les tests
    for i in range(nombre_tests):
        # Création d'un graphe M avec n sommets, des arêtes aléatoires et un degré maximal de 2
        M = graphe2(n, p, 0, 2)
        # Vérification si fc(M) est True
        if fc(M):
            compte_fc += 1
    # Calcul du pourcentage de fois où fc(M) est True
    pourcentage_fc = (compte_fc / nombre_tests) * 100
    # Retourne le pourcentage obtenu
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

print("Le seuil de forte connexité :", seuil(50))

