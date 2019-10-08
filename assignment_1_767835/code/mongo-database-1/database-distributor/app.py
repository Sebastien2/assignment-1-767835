import os

from flask import Flask, redirect, url_for, request, render_template

app=Flask(__name__)

numero=0

@app.route('/associate_shard')
def asociate_shard():
    #on retourne le port
    global numero
    port=numero
    numero+=1
    if(numero==4):
        numero=1
    return str(port)




app.run(host='0.0.0.0', port=80, debug=True)
