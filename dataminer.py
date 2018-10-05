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
import datetime


URL_LOGIN = 'https://espace-client-connexion.enedis.fr'
URL_API_BASE = 'https://espace-client-particuliers.enedis.fr/group/espace-particuliers'
URL_DATE_ACTIV = '/courbe-de-charge'
URL_API_LOGIN = '/auth/UI/Login'
URL_API_HOME = '/home'
URL_API_DATA = '/suivi-de-consommation'

date_activ = ""


#liste des choix(= resource_id) a envoyer dans la requete
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


        pattern = re.compile(r'\d\d/\d\d/\d\d\d\d')
        matches = pattern.findall(s.text)

        res = matches[0]
        slice = res[0:9]
        temp = str(int(res[9])-1)
        date_activ = slice + temp


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



###################################################




########### MAIN ###########

#user=input("veuillez entrer votre mail : ")
#pwd = getpass.getpass(prompt='veuillez entrer votre mdp : ')
now = ""
now += str(datetime.datetime.now().day)
now += "/"
now += str(datetime.datetime.now().month)
now += "/"
now += str(datetime.datetime.now().year)

print (now)

monlog=login("catounono@aol.com","Elioteliot@69")
doto=recup_donnee(monlog,jour,date_activ,now)

print (json.dumps(doto, indent=4, sort_keys=True))

with open('data.json', 'w') as outfile:
    json.dump(doto, outfile)



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
