from flask import Flask, render_template, request
from Bio import Entrez, Medline, SeqIO
import json
import datetime
import Artikel
import Protein

class DBConnect:

    def __init__(self, eiwit, jaartal):
        self.eiwit = eiwit
        self.jaartal = jaartal
        self.artikels = ""
        self.proteins = ""
        self.data = ""

    def searchArtikel(self):
        artikel = Artikel
        Entrez.email = "W.Sies@han.nl"
        date2 = str(int(str(datetime.datetime.today())[0:4])+1)
        readhandle = Entrez.read(
            Entrez.esearch(db="pubmed", retmax=100000, term=str(self.eiwit) + " AND {0}:{1} [PDAT]".format(self.jaartal, date2), datetype="pdat",
                           usehistory="y"))
        ids = readhandle.get('IdList')
        closedArtikels = Entrez.efetch(db="pubmed", id=ids, rettype="medline", retmode="text")
        openArtikels = Medline.parse(closedArtikels)
        #artikels = "<tr><th>PubMed ID</th><th>Titel</th><th>Auteurs</th><th>Datum publicatie</th><th>Classification(s)</th><th>Keywords</th><th>Abstract</th></tr>
        if len(ids) > 0:
            count = -1
            for openArtikel in openArtikels:
                count += 1
                abstract = openArtikel.get("AB", "-")
                author = openArtikel.get("AU", "-")
                dateOfPublish = openArtikel.get("DP", "-")
                publicationType = openArtikel.get("PT", "-")
                pmid = openArtikel.get("PMID", "-")
                keywords = openArtikel.get("OT", "-")
                title = openArtikel.get("TI", "-")
                art = artikel.Artikel(abstract, author, dateOfPublish, publicationType, pmid, keywords, title)
                art.setTableRow()
                self.artikels += art.tableRow
                #newRow += "<tr><td><a href=""https://www.ncbi.nlm.nih.gov/pubmed?term="+str(ids[count])+">"+str(ids[count])+"</td><td>"+title+"</td><td>"+",".join(author)+"</td><td>"+dateOfPublish+"</td><td>"+"\n".join(keywords)+"</td><td>"+"".join(abstract)+"</td></tr>"
        return self.artikels

    def searchProtein(self):
        protein = Protein
        Entrez.email = "W.Sies@han.nl"
        date2 = str(int(str(datetime.datetime.today())[0:4]) + 1)
        readhandle = Entrez.read(
            Entrez.esearch(db="protein", retmax=10, term=str(self.eiwit) + " [Protein Name]".format(self.jaartal, date2),
                           datetype="pdat",
                           usehistory="y"))
        ids = readhandle.get('IdList')
        closedProteins = Entrez.efetch(db="protein", id=ids, rettype="gb", retmode="text")
        openProteins = SeqIO.parse(closedProteins, "genbank")
        count = -1
        #proteinInfo = ""
        if len(ids) > 0:
            for openProtein in openProteins:
                count += 1
                taxa = openProtein.annotations.get("taxonomy")
                accessions = openProtein.annotations.get("accessions")
                references = openProtein.annotations.get("references")
                prot = protein.Protein(taxa, accessions, references)
                prot.setTableRow()
                self.proteins += prot.tableRow
                #newRow = "<tr><td>"+proteinInfo+"</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>"
        else:
            self.proteins = "Sorry no protein data found"
        return self.proteins