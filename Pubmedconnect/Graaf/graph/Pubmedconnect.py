from flask import Flask, render_template, request
from Bio import Entrez, Medline
import datetime
import json, codecs

# Het programma van flask wordt hier aangeroepen
# ook wordt een bestand geopend waar de data voor de graph in komt te staan en het begin van het .json bestand wordt er in geschreven.

app = Flask(__name__)
bestand = open('static/data.json', 'w')
bestand.writelines('{' +'\n' + '"nodes":[' +'\n')

@app.route('/', methods=["GET"])
# De index wordt aangeroepen en de variabelen worden opgehaald.
def index():
    eiwit=request.args.get("Eiwit")
    jaartal=request.args.get("Jaartal")
    return render_template('./index.html')

@app.route('/table', methods=["GET"])
# De tabel van de resultaten wordt hier aangeroepen en het template vandeze pagina wordt aangeroepen met de parameters ingevuld.
def table():
    eiwit = request.args.get("Eiwit")
    jaartal = request.args.get("Jaartal")
    rows = searchids(eiwit, jaartal)
    bestand.close()
    return render_template('./table.html', eiwit=eiwit, jaartal=str(jaartal), newrows=rows)


# de zoekopdracht wordt hier uitegevoerd. Als parameters worden eiwit en jaartal genomen om te zoeken.
# jaartal is vanaf wanneer de artikelen mogen zijn, en eiwit is het eiwit waar naar gezocht wordt.
# de pubmed database wordt doorzocht op resultaten die aan de parameters voldoen. 
# Wanneer er resultaten zijn wordt er een json bestand geschreven om vervolgens in de graph gebruikt te worden
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
        i = 0
        count = -1
        for artikel in openArtikels:
            i+=1
            count += 1
            abstract = artikel.get("AB", "-")
            author = artikel.get("AU", "-")
            dateOfPublish = artikel.get("DP", "-")
            publicationType = artikel.get("PT", "-")
            pmid = artikel.get("PMID", "-")
            keywords = artikel.get("KYWD", "-")
            title = artikel.get("TI", "-")
            newRow += "<tr><td><a href=""https://www.ncbi.nlm.nih.gov/pubmed?term="+str(ids[count])+">"+str(ids[count])+"</td><td>"+title+"</td><td>"+",".join(author)+"</td><td>"+dateOfPublish+"</td><td>"+"\n".join(keywords)+"</td><td>"+"".join(abstract)+"</td></tr>"
            nodeID = str('m-' + str(i))
            dataid = str('"id":' + '"' + nodeID + '"')
            datapub = str('"name":' + pmid)
            datawords = str('"Keywords":' +'"'+keywords+'"')
            dataloaded = str('"loaded":' +'true')
            if len(ids) == 1:
                bestand.write('{' + dataid + ', ' + datawords + ', ' + datapub + ', ' + dataloaded + '},' + '\n')
            elif count+1 < len(ids):
                bestand.write('{'+dataid+', '+datawords+', '+ datapub+', '+ dataloaded +'},'+'\n')
            elif count+1 >= len(ids):
                bestand.write('{' + dataid + ', ' + datawords + ', ' + datapub + ', ' + dataloaded + '}' + '\n')

    bestand.write('],' +'\n')
    bestand.write('"links":[' + '\n')
    bestand.write('{"id":' +'"101", ' + '"from":' +'"m-0", ' + '"to":' +'"m-1", ' +'"type":' +'100},' +'\n')
    bestand.write('{"id":' +'"101", ' + '"from":' +'"m-1", ' + '"to":' +'"m-2", ' +'"type":' +'100}')
    bestand.write('\n' + ']' + '\n' +'}')
    return newRow


if __name__ == '__main__':
    app.run()
