import os

import pandas as pd
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient

app=Flask(__name__)

client=MongoClient("mongodb://database:27017/")
db=client.db_3

#print
@app.route('/show_html')
def show_html():
    _items=db.table_1.find()
    items=[item for item in _items]

    return render_template('todo.html', items=items)


@app.route('/show_length_database')
def show_length_database():
    _items=db.table_1.find()
    items=[item for item in _items]
    return render_template('show_length_database.html', len=len(items))
    return str(len(items))

#test
@app.route('/hello_world')
def hello_world():
    return "hello world"


#put
@app.route('/insert_one', methods=['POST'])
def insert_one():
    #on récupère les arguments
    table=db.table_1

    table.insert_one()

    return "done"


@app.route('/insert_many', methods=["POST"])
def insert_many():
    table=db.table_1
    #on récupère le json en POST
    json=request.form['data']
    #on l'inser dasn la bdd
    data=pd.read_json(json)

    res=table.insert_many(data.to_dict('records'))
    #on revoie un resultat

    return str(res.inserted_ids)



@app.route('/delete_all')
def delete_all():
    table=db.table_1
    result=table.delete_many({})
    return "Number of deleted instances: "+str(result.deleted_count)



app.run(host='0.0.0.0', port=80, debug=True)
