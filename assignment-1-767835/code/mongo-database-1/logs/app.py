#service: acces to database (API)
import os
import json

import requests
from requests.exceptions import HTTPError
from flask import Flask, redirect, url_for, request, render_template
from flask_restful import Resource, Api


app=Flask(__name__)



@app.route('/add_log', methods=['POST'])
def add_log():
    #on recupere le json en argument
    json_obj=request.form['log']
    #on l'écrit dans un fichier
    with open('logs/liste.txt', 'a+') as outfile:  #on cree le fichier si nécessaure
        outfile.write("\n")
        json.dump(json_obj, outfile)
    return "logged added"+str(json_obj)




app.run(host='0.0.0.0', port=80, debug=True)
