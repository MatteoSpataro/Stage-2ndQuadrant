# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
app = Flask(__name__)
import psycopg2

@app.route("/", methods=['GET','POST'])
def home():
    campi = [True,True,True,True,True,True]
    conn = psycopg2.connect(database="biblioteca", user="postgres", host="192.168.3.228", port="5432")
    cur = conn.cursor()
    cur.execute("select * from libreria;")
    listalibri = cur.fetchall()
    conn.commit()
    if request.method == 'GET':
        return render_template('index.nginx-debian.html',messaggio=' ',listalibri=listalibri,campi=campi)
    elif request.method == 'POST':
        c0=request.form.getlist('cbox1')
        campi[0]=bool(c0)
        c1=request.form.getlist('cbox2')
        campi[1]=bool(c1)
        c2=request.form.getlist('cbox3')
        campi[2]=bool(c2)
        c3=request.form.getlist('cbox4')
        campi[3]=bool(c3)
        c4=request.form.getlist('cbox5')
        campi[4]=bool(c4)
        c5=request.form.getlist('cbox6')
        campi[5]=bool(c5)
        conn.close()
        if campi[0]==campi[1]==campi[2]==campi[3]==campi[4]==campi[5]==False:
            campi = [True,True,True,True,True,True]
        return render_template('index.nginx-debian.html',messaggio=' ',listalibri=listalibri,campi=campi)


@app.route("/add", methods=['GET','POST'])
def add():
    stringa = ';'
    if request.method == 'GET':
        return render_template('add.html',messaggio=' ')
    elif request.method == 'POST':
        conn = psycopg2.connect(database="biblioteca", user="postgres", host="192.168.3.228", port="5432")
        cur = conn.cursor()
        titolo = request.form['titolo'].strip(' ')
        autore = request.form['autore'].strip(' ')
        genere = request.form['genere'].strip(' ')
        casa = request.form['casa'].strip(' ')
        if (titolo.find(stringa) == -1) and (autore.find(stringa) == -1) and (genere.find(stringa) == -1) and (casa.find(stringa) == -1):
                anno = request.form['anno']
                prezzo = request.form['prezzo']
                if (titolo == "") or (autore == "") or (genere == "") or (casa == ""):
                        return render_template('add.html',messaggio='There is an empty field')
                cur.execute("insert into libreria(titolo,autore,genere,casa_editrice,anno,prezzo) values(%s,%s,%s,%s,%s,%s);",(titolo,autore,ge$
                conn.commit()
                conn.close()
                return render_template('add.html',messaggio='Operation succesfully complete!')
        else:
                return render_template('add.html',messaggio='Error input fields')

@app.route("/delete", methods=['GET','POST'])
def delete():
    stringa = ';'
    if request.method == 'GET':
        conn = psycopg2.connect(database="biblioteca", user="postgres", host="192.168.3.228", port="5432")
        cur = conn.cursor()
        cur.execute("select titolo from libreria;")
        listalibri = cur.fetchall()
        conn.commit()
        return render_template('delete.html',messaggio=' ',listalibri=listalibri)
    elif request.method == 'POST':
        conn = psycopg2.connect(database="biblioteca", user="postgres", host="192.168.3.228", port="5432")
        cur = conn.cursor()
        titolo = request.form['titolo'].strip(' ')
        cur.execute("select titolo from libreria;")
        listalibri = cur.fetchall()
        conn.commit()
        if (titolo == ''):
                return render_template('delete.html',messaggio='The field is empty!',listalibri=listalibri)
        elif (titolo.find(stringa) == -1):
                cur.execute("delete from libreria where titolo = %s;",[titolo])
                conn.commit()
                conn.close()
                return render_template('delete.html',messaggio='Operation succesfully complete!',listalibri=listalibri)
        else:
                return render_template('delete.html',messaggio='Error input fields',listalibri=listalibri)



@app.route("/search", methods=['GET','POST'])
def search():
    str = ';'
    if request.method == 'GET':
        return render_template('search.html',listalibri=[])
    elif request.method == 'POST':
        conn = psycopg2.connect(database="biblioteca", user="postgres", host="192.168.3.228", port="5432")
        cur = conn.cursor()
        stringa = request.form['search'].strip(' ')
        campi = [True,True,True,True,True,True]
        if (stringa.find(str) == -1):
                cur.execute("select * from libreria where titolo like %s;",[stringa])
                lista = cur.fetchall()
                listalibri = lista
                cur.execute("select * from libreria where autore like %s;",[stringa])
                lista = cur.fetchall()
                listalibri = listalibri + lista
                cur.execute("select * from libreria where genere like %s;",[stringa])
                lista = cur.fetchall()
                listalibri = listalibri + lista
                cur.execute("select * from libreria where casa_editrice like %s;",[stringa])
                lista = cur.fetchall()
                listalibri = listalibri + lista
                conn.commit()
                conn.close()
                return render_template('index.nginx-debian.html',messaggio=' ',listalibri=listalibri,campi=campi)
        else:
                return render_template('index.nginx-debian.html',messaggio='Nothing with that pattern was found',listalibri=[],campi=campi)

if __name__ == '__main__':
   app.run(host='192.168.3.229')
