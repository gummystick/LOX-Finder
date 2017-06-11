from flask import Flask, render_template, request
from Bio import Entrez, Medline
import datetime
import DBConnect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/table', methods=["GET"])
def table():
    eiwit = request.args.get("Eiwit")
    jaartal = request.args.get("Jaartal")
    DBConnect = DBConnect
    connect = DBConnect.DBConnect(eiwit, jaartal)
    rows = connect.getTable()
    return render_template('./table.html', eiwit=eiwit, jaartal=str(jaartal), newrows=rows)

if __name__ == '__main__':
    app.run()