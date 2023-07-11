#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
7. Test de forte connexitÃ© 
"""
import numpy as np

def Trans2(M):
    # Obtenir la taille de la matrice
    k = len(M)
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
    # Retourner la matrice modifiÃ©e
    return M

"""
Prend en entrée la matrice d'un graphe orienté (non pondéré) et qui retourne
True ou False à la question : "le graphe G donné par la matrice M (après numérotation de
ses sommets) est-il fortement connexe ?"
"""
def fc(M):
    # Vérifier si la matrice est carrée
    if M.shape[0] != M.shape[1]:
        return False

    # Vérifier si la matrice est symétrique
    if not np.array_equal(M, M.T):
        return False
    
    # Appliquer la fermeture transitive
    M_fermeture = Trans2(M)
    
    # Vérifier si la matrice résultante ne contient que des 1
    if np.all(M_fermeture == 1):
        return True
    else:
        return False


M = np.array([[0, 0, 0, 0, 0],
              [0, 0, 0, 1, 1],
              [1, 1, 0, 1, 0],
              [1, 1, 1, 1, 1],
              [1, 0, 1, 1, 1]])

#print(Trans2(M))

print("Le graphe G donnÃ© par la matrice M est-il fortement connexe ? ", fc(M))
