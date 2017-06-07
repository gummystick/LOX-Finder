from flask import Flask, render_template, request
from Bio import Entrez, Medline
from nltk import word_tokenize
import datetime

app = Flask(__name__)


@app.route('/', methods=["GET"])
def hello_world():
    eiwit=request.args.get("Eiwit")
    jaartal=request.args.get("Jaartal")
    return render_template('index.html')

@app.route('/table', methods=["GET"])
def table():
    eiwit = request.args.get("Eiwit")
    jaartal = request.args.get("Jaartal")
    rows = searchids(eiwit, jaartal)
    return render_template('table.html', eiwit=eiwit, jaartal=str(jaartal), newrows=rows)

def searchids(eiwit, jaartal):

    classification = ['plants', 'animals', 'bacteria', 'fungi']
    key_words = ['lipoxygenase', 'Bleaching', 'hydroperoxide', 'oleochemistry', 'oxylipin', 'fatty acids','application', 'oxidation', 'biosynthesis']

    rijk = []
    key = []

    Entrez.email = "W.Sies@han.nl"
    date2 = str(int(str(datetime.datetime.today())[0:4])+1)
    readhandle = Entrez.read(
        Entrez.esearch(db="pubmed", term=str(eiwit) + " AND {0}:{1} [PDAT]".format(jaartal, date2), datetype="pdat",
                       usehistory="y"))
    ids = readhandle.get('IdList')
    closedArtikels = Entrez.efetch(db="pubmed", id=ids, rettype="medline", retmode="text")
    openArtikels = Medline.parse(closedArtikels)
    newRod=""
    count = -1
    for artikel in openArtikels:
        count += 1
        abstract = artikel.get("AB", "-")
        words = word_tokenize(abstract)
        for i in words:
            if i in classification:
                rijk.append(i)
            elif i in key_words:
                key.append(i)
        author = artikel.get("AU", "-")
        dateOfPublish = artikel.get("DP", "-")
        publicationType = artikel.get("PT", "-")
        pmid = artikel.get("PMID", "-")
        title = artikel.get("TI", "-")
        twords = word_tokenize(title)
        for i in twords:
            if i in classification:
                rijk.append(i)
            elif i in key_words:
                key.append(i)

        rijk1 = set(rijk)
        rijk2 = list(rijk1)

        key1 = set(key)
        key2 = list(key1)

        newRow = "<tr><td><a href=""https://www.ncbi.nlm.nih.gov/pubmed?term="+str(ids[count])+">"+str(ids[count])+"</td><td>"+title+"</td><td>"+",".join(author)+"</td><td>"+dateOfPublish+"</td><td>"+"\n".join(rijk2)+"</td><td>"+"\n".join(key2)+"</td><td>"+"".join(abstract)+"</td></tr>"

    return newRow

if __name__ == '__main__':
    app.run()