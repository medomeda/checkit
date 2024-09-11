# importing the requests library
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

def find_in_cei(nom, prenom, jour, mois, annee):
    # api-endpoint
    URL = "https://cei.ci/lep-23/"

    
    # defining a params dict for the parameters to be sent to the API
    # PARAMS = {'nomfamille':'TOURE',
    #         'prenom':'BANSO',
    #         'jour':'06',
    #         'mois':'03',
    #         'annee':'1986',
    #         'search_cei_individu': 'Lancer la recherche'
    #         }
    PARAMS = {'nomfamille':nom,
            'prenom':prenom,
            'jour':jour,
            'mois':mois,
            'annee':annee,
            'search_cei_individu': 'Lancer la recherche'
            }
    
    # sending get request and saving the response as response object
    r = requests.post(url = URL, data = PARAMS)
    
    # extracting data in json format
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')
    result = soup.find("div", {"id": "resultat_electeur"})

    user_info=[]
    heading_tags = ["h6"]
    for tags in result.find_all(heading_tags):
        user_info.append(tags.text.strip())
        #print(tags.text.strip())

    #print(user_info)
    return user_info



app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/verifycei", methods=['POST'])
def get_electeur():
    
    data = request.json
    nom = data.get('nom')
    prenom = data.get('prenom')
    jour = data.get('jour')
    mois = data.get('mois')
    annee = data.get('annee')

    result = find_in_cei(nom=nom, prenom=prenom,jour=jour,mois=mois, annee=annee)
   
    return result

if __name__ == "__main__":
    app.run()
