#service: acces to database (API)
import os
import datetime
import json

import pandas as pd
import requests
from requests.exceptions import HTTPError
from flask import Flask, redirect, url_for, request, render_template
from flask_restful import Resource, Api


app=Flask(__name__)
api=Api(app)


@app.route('/slice')
def slice():
    #pour le moment, on considère que le fichier est sous la main
    chunk_size=10000
    batch_no=1

    for chunk in pd.read_csv('2019.csv', chunksize=chunk_size):
        chunk.to_csv('data/database_part_'+str(batch_no)+'.csv', index=False)
        batch_no+=1

    return "done"


@app.route('/nb_batches')
def nb_batches():
    numero_batch=1
    while(os.path.isfile('data/database_part_'+ str(numero_batch) +'.csv')):
        numero_batch+=1
    return str(numero_batch-1)



@app.route('/ingest/<int:numero_batch>')
def ingest(numero_batch):
    date_debut=datetime.datetime.now()
    #on transfère une instance à kla fois à un autre container
    db=pd.read_csv('data/database_part_'+ str(numero_batch) +'.csv')
    indexes=db.columns.values

    #on renomme les colonnes
    for pos, index in enumerate(indexes):
        name=index
        names=index.split('.')
        future_name=""
        for i in range(len(names)-1):
            future_name+=names[i]+"_"
        future_name+=names[len(names)-1]
        indexes[pos]=future_name

    #puis on transfert la data
    json_obj=db.to_json()
    #Puis on envoie e jjson à database-api

    #on demande le numero du port
    continuer=False
    try:
        response=requests.get('http://database-distributor/associate_shard')
        res="Response code="+str(response.status_code)
        #return res
        if(response.status_code==200):
            port=response.text
            continuer=True
        elif(response.status_code==404):
            res+="<br>Page not found"
            #return render_template('ingestion.html', resultat=res, numero_batch=numero_batch)
        else:
            res+="<br>"+response.text
            #return render_template('ingestion.html', resultat=res, numero_batch=numero_batch)

    except HTTPError as http_err:
        res='HTTP error occurred: '+str(http_err) # Python 3.6
        #return render_template('ingestion.html', resultat=res, numero_batch=numero_batch)
    except Exception as err:
        res='Other error occurred: '+str(err)  # Python 3.6
        #return render_template('ingestion.html', resultat=res, numero_batch=numero_batch)


    if(continuer):
        continuer=False
        res=""
        try:
            response=requests.post('http://database-api-'+ port +'/insert_many', {'data': json_obj})
            res="Shard num.: "+port+"<br>Response code="+str(response.status_code)
            #return res
            if(response.status_code==200):
                res+="<br>Data enregistrée"
                continuer=True  #c est un succes
            elif(response.status_code==404):
                res+="<br>Page not found"
            else:
                res+="<br>"+response.text

        except HTTPError as http_err:
            res='HTTP error occurred: '+str(http_err) # Python 3.6
        except Exception as err:
            res='Other error occurred: '+str(err)  # Python 3.6

    #on construit le json pour les logs
    date_fin=datetime.datetime.now()
    destination='http://database-api-'+ port +'/insert_many'
    container='ingest'
    succes='0'
    if(continuer):
        succes='1'
    url='http://ingest/ingest/'+str(numero_batch)
    #on cree le json
    log={}
    log['date_fin']=str(date_fin)
    log['date_debut']=str(date_debut)
    log['destination']=destination
    log['container']=container
    log['succes']=succes
    log['url']=url
    log=json.dumps(log)
    #on l'envoie a l'autre container pour l'enregistrer
    requests.post('http://logs/add_log', {'log': log}) # on ne verifie pas si ca reussit

    return render_template('ingestion.html', resultat=res, numero_batch=numero_batch)




if __name__== '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
