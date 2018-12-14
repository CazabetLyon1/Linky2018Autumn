import sys
import time
import csv
import math
import base64
import requests
import html
import json
import getpass
import urllib
import re
import string
import datetime
import pprint


URL_LOGIN = 'https://espace-client-connexion.enedis.fr'
URL_API_BASE = 'https://espace-client-particuliers.enedis.fr/group/espace-particuliers'
URL_DATE_ACTIV = '/courbe-de-charge'
URL_INFO_CONTRAT = 'https://espace-client-particuliers.enedis.fr/group/espace-particuliers/accueil'
URL_API_LOGIN = '/auth/UI/Login'
URL_API_HOME = '/home'
URL_API_DATA = '/suivi-de-consommation'

date_activ = ""
puissance_souscrite = 0
fournisseur = ""

class donneeLinky:
    def __init__(self, annee, mois, jour, heure, val):
        self.annee = annee
        self.mois = mois
        self.jour = jour
        self.heure = heure
        self.val = val

class horaire:
    def __init__(self):
        self.h = "00";
        self.m = "00";

    def incrementer(self):
        if(self.m == "00"):
            self.m = "30"
        else:
            self.m = "00"
            self.h = str((int(self.h)+1)%24)
            if(len(self.h) == 1):
                self.h = "0"+self.h

    def afficher(self):
        print(self.h,"h",self.m)

    def str(self):
        return self.h + 'h' + self.m

class date:
    def __init__(self,string):
        self.a = int(string[6:13])
        self.m = int(string[3:5])
        self.j = int(string[0:2])

    def afficher(self):
        tmp = str(self.j) + '/' + str(self.m) + '/' + str(self.a)
        print(tmp)

    def incrementer(self):
        if(self.m == 1
        or self.m == 3
        or self.m == 5
        or self.m == 7
        or self.m == 8
        or self.m == 10
        or self.m == 12):
            if(self.j == 31):
                self.j = 1
                if(self.m == 12):
                    self.m = 1
                    self.a += 1
                else:
                    self.m += 1;
            else:
                self.j += 1;


        else:
            if(self.j == 30):
                self.j = 1
                if(self.m == 12):
                    self.m = 1
                    self.a += 1
                else:
                    self.m += 1;
            else:
                self.j += 1;




#liste des choix(= resource_id) a envoyer dans la requete
#pour demander heure d'une journée : mettre jour et lendemain en parametre (commence a 00h00)
heure='urlCdcHeure'
jour='urlCdcJour'
mois='urlCdcMois'
an='urlCdcAn'

def login(username, password):

    #session = requests.Session()
    with requests.Session() as session:

        #contenue de la requete (voir inspecteur navigateur)
        # (https://deadliestwebattacks.com/2010/04/12/login-forms/)
        payload = {'IDToken1': username,
                   'IDToken2': password,
                   'SunQueryParamsString': base64.b64encode(b'realm=particuliers'),#obligatoire dans la requete (je sais pas trop pourquoi sous cette forme)
                   'encoded': 'true',#facultatif mais sympa a mettre
                   'gx_charset': 'UTF-8'#pareil
                   }

        #on envoie les données

        requete = session.post(URL_LOGIN + URL_API_LOGIN, data=payload, allow_redirects=False)

        s = session.get(URL_API_BASE + URL_DATE_ACTIV, allow_redirects = False)


        if 302 == s.status_code:
            #des fois on a un status 302 (je sais pas pourquoi) donc on renvoie la requete et ca marche
            s = session.get(URL_API_BASE + URL_DATE_ACTIV, allow_redirects = False)

            #date_activ
        pattern = re.compile(r'\d\d/\d\d/\d\d\d\d')
        matches = pattern.findall(s.text)

        if matches != []:
            res = matches[0]
            slice = res[0:9]
            temp = str(int(res[9])-1)
            global date_activ
            date_activ += slice + temp

        #recuperation info contrat
            #puissance_souscrite
        info = session.get(URL_INFO_CONTRAT, allow_redirects = False)
        if 302 == info.status_code:
            #des fois on a un status 302 (je sais pas pourquoi) donc on renvoie la requete et ca marche
            info = session.get(URL_INFO_CONTRAT, allow_redirects = False)

        pattern = re.compile(r'\d kVA')
        matches = pattern.findall(info.text)

        if matches != []:
            res = matches[0]
            slice = res[0]
            global puissance_souscrite
            puissance_souscrite = int(slice)

            #fournisseur
        pattern = re.compile(r'TxtSizeMedium">\D*</p>', re.MULTILINE)
        matches = pattern.findall(info.text)
        if matches != []:

            res = matches[0]
            slice = res[15:len(slice)-5]
            global fournisseur
            fournisseur = slice

        print(date_activ)
        print(puissance_souscrite)
        print(fournisseur)



        return session
###################################################


def recup_donnee(session, resource_id, debut=None, fin=None):
    #https://www.programcreek.com/python/example/6251/requests.post
    p_p_id = 'lincspartdisplaycdc_WAR_lincspartcdcportlet'

    formData = {
        '_' + p_p_id + '_dateDebut': debut,
        '_' + p_p_id + '_dateFin': fin
    }

    queryStringParameters = {
        'p_p_id': p_p_id,
        'p_p_lifecycle': 2,
        'p_p_state': 'normal',
        'p_p_mode': 'view',
        'p_p_resource_id': resource_id,
        'p_p_cacheability': 'cacheLevelPage',
        'p_p_col_id': 'column-1',
        'p_p_col_count': 2
    }

    #requete du json
    requete = session.post(URL_API_BASE + URL_API_DATA, allow_redirects=False, data=formData, params=queryStringParameters)


    if 302 == requete.status_code:
        #des fois on a un status 302 (je sais pas pourquoi) donc on renvoie la requete et ca marche
        requete = session.post(URL_API_BASE + URL_API_DATA, allow_redirects=False, data=formData, params=queryStringParameters)

    res = requete.json()

    return res




###################################################

def importCsv(filepath):

    vals = []
    cont = 0
    with open(filepath, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in spamreader:
            if(cont > 44):
                derp=donneeLinky((''.join(row)[0:4]),
                                 (''.join(row)[5:7]),
                                 (''.join(row)[8:10]),
                                 (''.join(row)[11:13])+'h'+(''.join(row)[14:16]),
                                 (''.join(row)[25:]))
                if(derp.val == ""):
                    derp.val = -1
                else:
                    derp.val = float(derp.val)/1000
                vals.append(derp)
            else:
                cont+=1

    return vals

###################################################

def transfoDonee (datas, param, debut, fin):
    res = []


    if(param == heure):
        h=horaire()
        d=date(debut)
        cont=0

        for it in datas['graphe']['data']:
            tmp = donneeLinky(d.a,d.m,d.j,h.str(),it['valeur'])
            res.append(tmp)
            h.incrementer()
            if(cont == 47):
                d.incrementer()
                cont=0
            else:
                cont+=1

    return res;
###################################################

def csvToJson(csvpath,jsonpath):
    csvfile = open(csvpath, 'r')
    jsonfile = open(jsonpath, 'w+')

    fieldnames = ("annee","mois","jour","heure","valeur")
    reader = csv.DictReader( csvfile, fieldnames)


    tabDatas = {}
    tabDatas['fournisseur'] = fournisseur
    tabDatas['puissance_souscrite'] = puissance_souscrite
    tabDatas['date_activ'] = date_activ
    tabDatas['date_recup'] = get_heure_now()

    json.dump(tabDatas,jsonfile)

    cond = 0
    for row in reader:
        if(cond == 1):
            json.dump(row, jsonfile)
            jsonfile.write(',')
            jsonfile.write('\n')
        else:
            cond = 1

###################################################
def donnneToCsv(datas, filepath):
    with open(filepath,'w+',newline='') as csvfile:
        a = csv.writer(csvfile, delimiter=',')
        tab=[['Annee','Mois','Jour','Heure','Valeur']]
        for int in datas:
            tab.append([int.annee,int.mois,int.jour,int.heure,int.val])
        a.writerows(tab)
###################################################

def get_heure_now():
    now = ""
    now += str(datetime.datetime.now().day)
    now += "/"
    now += str(datetime.datetime.now().month)
    now += "/"
    now += str(datetime.datetime.now().year)

    return now
###################################################


########### MAIN ###########
#csvToJson('test.csv','test.json')
#
#
#param = heure
#debut = "01/10/2018"
#fin = "08/10/2018"
#
#
#ses = login("catounono@aol.com","Elioteliot@69")
#print ("aujourd'hui : ",get_heure_now())
#print ("date activation : ",date_activ)
#
#derp = recup_donnee(ses,param,date_activ,get_heure_now())
#trans = importCsv('data.csv')
## transfoDonee(derp,param,date_activ,get_heure_now())
#
#
#jesaispo = importCsv('data.csv')
#
#donnneToCsv(jesaispo,'test.csv')
#donnneToCsv(trans,'test1.csv')

print((str(sys.argv)))
ses = login((str(sys.argv))[1],(str(sys.argv))[1])
don = recup_donnee(ses,param,date_activ,get_heure_now())
transDon = transfoDonee(derp,param,date_activ,get_heure_now())
donnneToCsv(transDon,(str(sys.argv))[1]+'.csv')
csvToJson((str(sys.argv))[1]+'.csv',(str(sys.argv))[1]+'.json')




#A FAIRE TRANSFORM JSON



# merci de garder ces lignes (eliot)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
