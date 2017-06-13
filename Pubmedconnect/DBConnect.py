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
        if len(ids) > 0:
            for openProtein in openProteins:
                count += 1
                taxa = openProtein.annotations.get("taxonomy")
                accessions = openProtein.annotations.get("accessions")
                references = openProtein.annotations.get("references")
                prot = protein.Protein(taxa, accessions, references)
                prot.setTableRow()
                self.proteins += prot.tableRow
        else:
            self.proteins = "Sorry no protein data found"
        return self.proteins