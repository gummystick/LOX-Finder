from flask import Flask, render_template, request
from Bio import Entrez, Medline, SeqIO
import json
import datetime
import Artikel
import Protein
from nltk import word_tokenize
from nltk.corpus import stopwords

class DBConnect:

    def __init__(self, eiwit, jaartal):
        self.eiwit = eiwit
        self.jaartal = jaartal
        self.artikels = "" 
        self.proteins = ""
        self.data = ""
        self.classification = ['plants', 'animals', 'bacteria', 'fungi']
        self.filter1 = []
        self.filter2 = []
        self.final = []

    def searchArtikels(self):
        extra_words = [',', '.', '(',')',':',';','<','>','%','[',']','{','}']
        stop_words = set(stopwords.words('English'))
        stop_words.update(extra_words)
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
        aantal = len(ids)
        count = -1
        count2 = 0
#        if len(ids) > 0:
#            count = -1
#            for openArtikel in openArtikels:
#                count += 1
#                abstract = openArtikel.get("AB", "-")
#                author = openArtikel.get("AU", "-")
#                dateOfPublish = openArtikel.get("DP", "-")
#                publicationType = openArtikel.get("PT", "-")
#                pmid = openArtikel.get("PMID", "-")
#                keywords = openArtikel.get("OT", "-")
#                title = openArtikel.get("TI", "-")
#                art = artikel.Artikel(abstract, author, dateOfPublish, publicationType, pmid, keywords, title)
#                art.setTableRow()
#                self.artikels += art.tableRow
#                #newRow += "<tr><td><a href=""https://www.ncbi.nlm.nih.gov/pubmed?term="+str(ids[count])+">"+str(ids[count])+"</td><td>"+title+"</td><td>"+",".join(author)+"</td><td>"+dateOfPublish+"</td><td>"+"\n".join(keywords)+"</td><td>"+"".join(abstract)+"</td></tr>"

        for artikel in openArtikels:
            if count2 < int(aantal*0.5):
                count += 1
                count2 += 1
                abstract = artikel.get("AB", "-")
                words = word_tokenize(abstract.lower())
                for i in words:
                    if i not in stop_words:
                        self.filter1.append(i)
                title = artikel.get("TI", "-")
                twords = word_tokenize(title.lower())
                for i in twords:
                    if i not in stop_words:
                        self.filter1.append(i)
            else:
                count += 1
                abstract = artikel.get("AB", "-")
                words = word_tokenize(abstract.lower())
                for i in words:
                    if i not in stop_words:
                        self.filter2.append(i)
                title = artikel.get("TI", "-")
                twords = word_tokenize(title.lower())
                for i in twords:
                    if i not in stop_words:
                       self.filter2.append(i)
        return
    
    def compareArtikels(self):
        list3 = set(self.filter1) & set(self.filter2)
        keywords2 = sorted(list3, key=lambda k: self.filter1.index(k))

        for i in keywords2:
            self.final.append(i)
        return "A"
    
    def comparedArtikelSearch(self):
        rijk = []
        key = []
    
        Entrez.email = "W.Sies@han.nl"
        date2 = str(int(str(datetime.datetime.today())[0:4])+1)
        readhandle = Entrez.read(
            Entrez.esearch(db="pubmed", term=str(self.eiwit) + " AND {0}:{1} [PDAT]".format(self.jaartal, date2), datetype="pdat",
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
                if i in self.classification:
                    rijk.append(i)
                elif i in self.final:
                    key.append(i)
            author = artikel.get("AU", "-")
            dateOfPublish = artikel.get("DP", "-")
            title = artikel.get("TI", "-")
            twords = word_tokenize(title)
            for i in twords:
                if i in self.classification:
                    rijk.append(i)
                elif i in self.final:
                    key.append(i)
    
            rijk1 = set(rijk)
            rijk2 = list(rijk1)
    
            key1 = set(key)
            key2 = list(key1)
    
            newRow += "<tr><td><a href=""https://www.ncbi.nlm.nih.gov/pubmed?term="+str(ids[count])+">"+str(ids[count])+"</td><td>"+title+"</td><td>"+",".join(author)+"</td><td>"+dateOfPublish+"</td><td>"+"\n".join(rijk2)+"</td><td>"+"\n".join(key2)+"</td><td>"+"".join(abstract)+"</td></tr>"
    
            del key[:]
        return newRow

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
