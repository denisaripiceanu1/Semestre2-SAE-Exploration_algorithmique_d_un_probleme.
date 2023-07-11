"""
8. Forte connexité pour un graphe avec p=50% de fléchés 
On veut vérifier l’affirmation : ”Lorsqu’on teste cette fonction fc(M) sur des matrices 
de taille n avec n grand, avec une proportion p = 50% de 1 (et 50% de 0), on obtient presque 
toujours un graphe fortement connexe.”
•	Pour cela, on créera une fonction test_stat_fc(n) retournant le pourcentage de ]graphes
de taille n fortement connexes pour un test portant sur quelques centaines de graphes. 
•	A partir de quel n l’affirmation ci-dessus est-elle vraie ? 
"""

import numpy as np
import numpy.random as rd

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
Génère aléatoirement une matrice de taille n x n avec environ 50% de coefficients ∞
et 50% de coefficients avec des poids entiers dans l'intervalle [a, b[.
"""
from graphe import graphe

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
portant sur quelques centaines de graphes.
"""
def test_stat_fc(n):
    # Définition du nombre de tests
    nombre_tests = 300
    # Compteur pour le nombre de fois où la fonction fc renvoie True
    compte_fc = 0
    # Boucle pour effectuer les tests
    for i in range(nombre_tests):
        # Création d'un graphe M avec n sommets, des arêtes aléatoires et un degré maximal de 2
        M = graphe(n, 0, 2)
        # Vérification si fc(M) est True
        if fc(M):
            compte_fc += 1
    # Calcul du pourcentage de fois où fc(M) est True
    pourcentage_fc = (compte_fc / nombre_tests) * 100
    # Retourne le pourcentage obtenu
    return pourcentage_fc


def seuil():
    # Initialisation de la valeur de n à 5
    n = 5
    # Tant que le pourcentage de tests réussis est inférieur à 100
    while test_stat_fc(n) < 100:
        # Incrémente n de 1 à chaque itération
        n = n + 1
    # Retourne la valeur de n lorsque le seuil est atteint (pourcentage de tests réussis = 100)
    return n


print("La taille minimale pour laquelle l'affirmation est vraie est :", seuil())
