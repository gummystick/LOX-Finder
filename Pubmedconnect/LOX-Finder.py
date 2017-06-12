from flask import Flask, render_template, request
from Bio import Entrez, Medline
import datetime
import Tabel

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/table', methods=["GET"])
def table():
    tabobject = Tabel
    eiwit = request.args.get("Eiwit")
    jaartal = request.args.get("Jaartal")
    tab = tabobject.Tabel(eiwit, jaartal)
    tabelcontent = tab.getTable()
    return render_template('./table.html', eiwit=eiwit, jaartal=str(jaartal), newrows=tabelcontent)

if __name__ == '__main__':
    app.run()