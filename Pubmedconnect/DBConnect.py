# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 16:27:24 2017

@author: William
"""

from flask import Flask, render_template, request
from Bio import Entrez, Medline, SeqIO
import json
import datetime

class DBConnect:

    def __init__(self, eiwit, jaartal):
        self.eiwit = eiwit
        self.jaartal = jaartal

    def getTable(self):
        rows = self.searchArtikel()
        other = self.searchProtein()
        return other

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
        newRow = ""
        if len(ids) > 0:
            count = -1
            artikels = []
            for openArtikel in openArtikels:
                count += 1
                abstract = openArtikel.get("AB", "-")
                author = openArtikel.get("AU", "-")
                dateOfPublish = openArtikel.get("DP", "-")
                publicationType = openArtikel.get("PT", "-")
                pmid = openArtikel.get("PMID", "-")
                keywords = openArtikel.get("OT", "-")
                title = openArtikel.get("TI", "-")
                artikels[count] = artikel.Artikel(abstract, author, dateOfPublish, publicationType, pmid, keywords, title)
                #newRow += "<tr><td><a href=""https://www.ncbi.nlm.nih.gov/pubmed?term="+str(ids[count])+">"+str(ids[count])+"</td><td>"+title+"</td><td>"+",".join(author)+"</td><td>"+dateOfPublish+"</td><td>"+"\n".join(keywords)+"</td><td>"+"".join(abstract)+"</td></tr>"
        return newRow

    def searchProtein(self):
        Entrez.email = "W.Sies@han.nl"
        date2 = str(int(str(datetime.datetime.today())[0:4]) + 1)
        readhandle = Entrez.read(
            Entrez.esearch(db="protein", retmax=10, term=str(self.eiwit) + " AND {0}:{1} [PDAT]".format(self.jaartal, date2),
                           datetype="pdat",
                           usehistory="y"))
        ids = readhandle.get('IdList')
        closedProteins = Entrez.efetch(db="protein", id=ids, rettype="gb", retmode="text")
        openProteins = SeqIO.parse(closedProteins, "genbank")
        count = 0
        proteinInfo = ""
        newRow = ""
        for protein in openProteins:
            taxa = protein.annotations.get("taxonomy")
            accessions = protein.annotations.get("accessions")
            references = protein.annotations.get("references")
            proteinInfo += str([taxa, accessions, references])
        newRow = "<tr><td>"+proteinInfo+"</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>"

        return newRow