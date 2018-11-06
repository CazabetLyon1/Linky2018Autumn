import dataminer
import numpy as np
def lecture_donnees(filepath):
    vals = []
    with open(filepath, newline='') as csvfile:
        spamreader  = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in spamreader:
            listeD = donneeLinky((''.join(row)[0:4]),
                                 (''.join(row)[5:7]),
                                 (''.join(row)[8:10]),
                                 (''.join(row)[11:13])+'h'+(''.join(row)[14:16]),
                                 (''.join(row)[25:]))
            print (listeD)
            if(listeD.val == ""):
                listeD.val = 0
            else:
                listeD.val = float(derp.val)/1000
            vals.append(listeD)

    return donnee_matrice
