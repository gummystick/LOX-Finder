import datetime

from Bio import Entrez, Medline
from flask import Flask, render_template, request
from nltk import word_tokenize
from nltk.corpus import stopwords

app = Flask(__name__)

filter1 = []
filter2 = []
final = []

@app.route('/', methods=["GET"])
def hello_world():
    eiwit=request.args.get("Eiwit")
    jaartal=request.args.get("Jaartal")
    return render_template('index.html')

@app.route('/table', methods=["GET"])
def table():
    eiwit = request.args.get("Eiwit")
    jaartal = request.args.get("Jaartal")
    keys1 = keywords(eiwit,jaartal)
    compare1 = compare()
    rows = searchids(eiwit, jaartal)
    return render_template('table.html', eiwit=eiwit, jaartal=str(jaartal), newrows=rows)

def keywords(eiwit, jaartal):

    extra_words = [',', '.', '(',')',':',';','<','>','%','[',']','{','}']
    stop_words = set(stopwords.words('English'))
    stop_words.update(extra_words)

    Entrez.email = "W.Sies@han.nl"
    date2 = str(int(str(datetime.datetime.today())[0:4]) + 1)
    readhandle = Entrez.read(
        Entrez.esearch(db="pubmed", term=str(eiwit) + " AND {0}:{1} [PDAT]".format(jaartal, date2), datetype="pdat",
                       usehistory="y"))
    ids = readhandle.get('IdList')
    closedArtikels = Entrez.efetch(db="pubmed", id=ids, rettype="medline", retmode="text")
    openArtikels = Medline.parse(closedArtikels)
    aantal = len(ids)
    count = -1
    count2 = 0

    for artikel in openArtikels:
        if count2 < int(aantal*0.5):
            count += 1
            count2 += 1
            abstract = artikel.get("AB", "-")
            words = word_tokenize(abstract.lower())
            for i in words:
                if i not in stop_words:
                    filter1.append(i)
            title = artikel.get("TI", "-")
            twords = word_tokenize(title.lower())
            for i in twords:
                if i not in stop_words:
                    filter1.append(i)
        else:
            count += 1
            abstract = artikel.get("AB", "-")
            words = word_tokenize(abstract.lower())
            for i in words:
                if i not in stop_words:
                    filter2.append(i)
            title = artikel.get("TI", "-")
            twords = word_tokenize(title.lower())
            for i in twords:
                if i not in stop_words:
                    filter2.append(i)


def compare():

    list3 = set(filter1) & set(filter2)
    keywords2 = sorted(list3, key=lambda k: filter1.index(k))

    for i in keywords2:
        final.append(i)

def searchids(eiwit, jaartal):

    classification = ['plants', 'animals', 'bacteria', 'fungi']

    rijk = []
    key = []

    Entrez.email = "W.Sies@han.nl"
    date2 = str(int(str(datetime.datetime.today())[0:4])+1)
    readhandle = Entrez.read(
        Entrez.esearch(db="pubmed", term=str(eiwit) + " AND {0}:{1} [PDAT]".format(jaartal, date2), datetype="pdat",
                     usehistory="y"))
    ids = readhandle.get('IdList')
    closedArtikels1 = Entrez.efetch(db="pubmed", id=ids, rettype="medline", retmode="text")
    openArtikels1 = Medline.parse(closedArtikels1)
    newRow=""
    count = -1
    for artikel in openArtikels1:
        count += 1
        abstract = artikel.get("AB", "-")
        words = word_tokenize(abstract)
        for i in words:
            if i in classification:
                rijk.append(i)
            elif i in final:
                key.append(i)
        author = artikel.get("AU", "-")
        dateOfPublish = artikel.get("DP", "-")
        title = artikel.get("TI", "-")
        twords = word_tokenize(title)
        for i in twords:
            if i in classification:
                rijk.append(i)
            elif i in final:
                key.append(i)

        rijk1 = set(rijk)
        rijk2 = list(rijk1)

        key1 = set(key)
        key2 = list(key1)

        newRow += "<tr><td><a href=""https://www.ncbi.nlm.nih.gov/pubmed?term="+str(ids[count])+">"+str(ids[count])+"</td><td>"+title+"</td><td>"+",".join(author)+"</td><td>"+dateOfPublish+"</td><td>"+"\n".join(rijk2)+"</td><td>"+"\n".join(key2)+"</td><td>"+"".join(abstract)+"</td></tr>"

        del key[:]
    return newRow


if __name__ == '__main__':
    app.run()