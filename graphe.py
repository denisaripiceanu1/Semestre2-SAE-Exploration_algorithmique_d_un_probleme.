#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3.1
Prend en entrée un entier strictement positif n, deux entiers a et b, et qui génère 
aléatoirement une matrice de taille n × n présentant environ 50% de coefficients ∞ et 
50% de coefficients avec des poids entiers dans l’intervalle [a, b[.
"""
import numpy as np
import numpy.random as rd

def graphe(n,a,b) :
    Resultat=np.empty((n,n)) # Création d'une matrice vide de taille n x n, stokée dans la variable Resultat
    M=rd.randint(a,b,(n,n)) # Remplissage de la matrice M avec des nombres aléatoires compris entre a et b
    for i in range (0,n): # Boucle pour parcourir toutes les colonnes de la matrice
        for j in range (0,n): # Boucle pour parcourir toutes les lignes de la matrice
            P=np.random.randint(0,2) # Génération aléatoire d'un entier 0 ou 1
            i2=np.random.randint(0,n) # Génération aléatoire de deux indices I2 et j2 compris entre 0 et n-1
            j2=np.random.randint(0,n)
            if P==1 : # Si P vaut 1, on copie la valeur de M[I2,j2] dans Resultat[I,J]
                Resultat[i,j]=int(M[i2,j2])
            else: # Sinon, on affecte la valeur infini à Resultat[I,J]
                Resultat[i,j]=np.inf
    return(Resultat) # On retourne la matrice Resultat
    
#print(graphe(5,2,7))

def graphe2(n, p, a, b):
    Resultat = np.empty((n, n)) # Création d'une matrice n x n pour stocker le résultat
    M = rd.randint(a, b, (n, n)) # Création d'une matrice n x n avec des valeurs aléatoires entre a et b
    val = rd.binomial(1, p, size=(n, n)) # Création d'une matrice n x n avec des valeurs binomiales de paramètre p
    for i in range (0,n): # Boucle pour parcourir toutes les colonnes de la matrice
        for j in range (0,n): # Boucle pour parcourir toutes les lignes de la matrice
            if val[i, j] == 1:  # Si la valeur de val est égale à 1, alors on insère la valeur correspondante de M dans Resultat
                Resultat[i, j] = M[i, j]
            else:  # Sinon, on insère +inf dans Resultat
                Resultat[i, j] = np.inf
    return(Resultat) # Retourne la matrice Resultat

#print(graphe2(4, 0.2, 0, 100)) #matrice de taille 4 avec une proportion de flèches de 20%, ayant des valeurs entre 0 et 1000

