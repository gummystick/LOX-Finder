from flask import Flask, render_template, request
from Bio import Entrez, Medline
import json
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
    rows = searchids(eiwit, jaartal)
    return render_template('./table.html', eiwit=eiwit, jaartal=str(jaartal), newrows=rows)

def searchids(eiwit, jaartal):
    Entrez.email = "W.Sies@han.nl"
    date2 = str(int(str(datetime.datetime.today())[0:4])+1)
    readhandle = Entrez.read(
        Entrez.esearch(db="pubmed", retmax=100000, term=str(eiwit) + " AND {0}:{1} [PDAT]".format(jaartal, date2), datetype="pdat",
                       usehistory="y"))
    ids = readhandle.get('IdList')
    closedArtikels = Entrez.efetch(db="pubmed", id=ids, rettype="medline", retmode="text")
    openArtikels = Medline.parse(closedArtikels)
    newRow = ""
    if len(ids) > 0:
        count = -1
        for artikel in openArtikels:
            count += 1
            abstract = artikel.get("AB", "-")
            author = artikel.get("AU", "-")
            dateOfPublish = artikel.get("DP", "-")
            publicationType = artikel.get("PT", "-")
            pmid = artikel.get("PMID", "-")
            keywords = artikel.get("OT", "-")
            title = artikel.get("TI", "-")
            newRow += "<tr><td><a href=""https://www.ncbi.nlm.nih.gov/pubmed?term="+str(ids[count])+">"+str(ids[count])+"</td><td>"+title+"</td><td>"+",".join(author)+"</td><td>"+dateOfPublish+"</td><td>"+"\n".join(keywords)+"</td><td>"+"".join(abstract)+"</td></tr>"
    return newRow

if __name__ == '__main__':
    app.run()
