from flask import Flask, render_template, request
from Bio import Entrez
import datetime

app = Flask(__name__)


@app.route('/', methods=["GET"])
def hello_world():
    eiwit=request.args.get("Eiwit")
    jaartal=request.args.get("Jaartal")
    return render_template('./index.html')

@app.route('/table', methods=["GET"])
def table():
    eiwit = request.args.get("Eiwit")
    jaartal = request.args.get("Jaartal")
    ids = searchids(eiwit, jaartal)
    links = linking(ids)
    return render_template('./table.html', eiwit=eiwit, jaartal=str(jaartal), ids=str(ids), links=links)

def searchids(eiwit, jaartal):
    Entrez.email = "W.Sies@han.nl"
    date2 = str(int(str(datetime.datetime.today())[0:4])+1)
    readhandle = Entrez.read(
        Entrez.esearch(db="pubmed", term=str(eiwit) + " AND {0}:{1} [PDAT]".format(jaartal, date2), datetype="pdat",
                       usehistory="y"))
    ids = readhandle.get('IdList')
    return ids

def linking(idlist):
    linklist = []
    for id in idlist:
        linklist.append(str(id))
    return linklist

if __name__ == '__main__':
    app.run()
