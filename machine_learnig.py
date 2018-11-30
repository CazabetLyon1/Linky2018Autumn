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

model = NMF(n_components=4, init='random', random_state=0)
W = model.fit_transform(mat)
H = model.components_
print(H[1])
print(W[1])
print(H.size)
print(W.size)
np.savetxt("W.csv", W, delimiter=";")
np.savetxt("H.csv", H, delimiter=";")


donnees_patern_1 = [];
donnees_patern_2 = [];
donnees_patern_3 = [];
donnees_patern_4 = [];

prix_moyen_kWh = 0.15;
def donner_patern(numero_patern, H, W, prix_moyen_kWh){
	donnee_patern = [];
	semaine = 0;
	jour = 1;
	somme = 0;
	for(i = 0; i<H.shape[]; i++){
		if(jour == 7){
			somme = somme + H[numero_patern][i];
			donnees_patern.append(somme);
			somme = 0;
			jour = 1;
		}
		else
		somme = somme + H[0][i];
		jour++;
	}
	donnees_patern.append(somme);
	
	for(i = 0;i<len(donnee_patern) ;i++){
		donnee_patern[i] = W[i][numero_patern]*donnee_patern[i]*prix_moyen_kWh;
	}
	return donnee_patern;
}


donnees_patern_1 = donner_patern(0, H, W, prix_moyen_kWh);
donnees_patern_2 = donner_patern(0, H, W, prix_moyen_kWh);
donnees_patern_3 = donner_patern(0, H, W, prix_moyen_kWh);
donnees_patern_4 = donner_patern(0, H, W, prix_moyen_kWh);











