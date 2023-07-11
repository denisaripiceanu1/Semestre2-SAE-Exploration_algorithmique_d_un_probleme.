#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
7. Test de forte connexité 
"""
import numpy as np

def Trans2(M):
    # Obtenir la taille de la matrice
    k = len(M)
    # Parcourir les sommets r et s
    for s in range(k):
        for r in range(k):
            # V�rifier si l'ar�te r -> s existe
            if M[r, s] == 1:
                # Parcourir les sommets s et t
                for t in range(k):
                    # V�rifier si l'ar�te s -> t existe
                    if M[s, t] == 1:
                        # Mettre � jour l'existence de l'ar�te r -> t
                        M[r, t] = 1
    # Retourner la matrice modifiée
    return M

"""
Prend en entr�e la matrice d'un graphe orient� (non pond�r�) et qui retourne
True ou False � la question : "le graphe G donn� par la matrice M (apr�s num�rotation de
ses sommets) est-il fortement connexe ?"
"""
def fc(M):
    # V�rifier si la matrice est carr�e
    if M.shape[0] != M.shape[1]:
        return False

    # V�rifier si la matrice est sym�trique
    if not np.array_equal(M, M.T):
        return False
    
    # Appliquer la fermeture transitive
    M_fermeture = Trans2(M)
    
    # V�rifier si la matrice r�sultante ne contient que des 1
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

print("Le graphe G donné par la matrice M est-il fortement connexe ? ", fc(M))
