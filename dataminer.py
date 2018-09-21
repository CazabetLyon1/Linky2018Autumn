import sys
import time
import csv
import math
import base64
import requests
import html
import json
import getpass

URL_LOGIN = 'https://espace-client-connexion.enedis.fr'
URL_API_BASE = 'https://espace-client-particuliers.enedis.fr/group/espace-particuliers'
URL_API_LOGIN = '/auth/UI/Login'
URL_API_HOME = '/home'
URL_API_DATA = '/suivi-de-consommation'


#liste des choix(= resource_id) a envoyer dans la requete
heure='urlCdcHeure'
jour='urlCdcJour'
mois='urlCdcMois'
an='urlCdcAn'

def login(username, password):

    session = requests.Session()

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

    requete = session.post(URL_API_BASE + URL_API_DATA, allow_redirects=False, data=formData, params=queryStringParameters)

    if 302 == requete.status_code:
        #des fois on a un status 302 (je sais pas pourquoi) donc on renvoie la requete et ca marche
        requete = session.post(URL_API_BASE + URL_API_DATA, allow_redirects=False, data=formData, params=queryStringParameters)



    res = requete.json()



    return res
###################################################





########### MAIN ###########

user=input("veuillez entrer votre mail : ")
pwd = getpass.getpass(prompt='veuillez entrer votre mdp : ')


monlog=login(user,pwd)
doto=recup_donnee(monlog,jour,"11/09/2018","13/09/2018")

print (json.dumps(doto, indent=4, sort_keys=True))



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
