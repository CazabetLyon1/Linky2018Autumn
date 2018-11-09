from dataminer import *
import numpy as np
from sklearn.decomposition import NMF

print(len(trans))
ligne = []
matrice = []
compteur = 0
for donnee in trans:
    if(compteur == 7*48):
        compteur = 0
        matrice.append(ligne)
        ligne = []
    else:
        if(donnee.val <0):
            donnee.val = 0
        ligne.append(donnee.val)
        compteur += 1
if (compteur <7*48 and compteur !=0):
    while(compteur <7*48):
        ligne.append(0)
        compteur += 1
    matrice.append(ligne)

mat = np.array(matrice)
print(mat)
print(mat.size)

model = NMF(n_components=2, init='random', random_state=0)
W = model.fit_transform(mat)
H = model.components_
print(H[1])
print(W[1])
print(H.size)
print(W.size)
np.savetxt("W.csv", W, delimiter=";")
np.savetxt("H.csv", H, delimiter=";")
