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
        
#Deze def voert een search uit met het eiwit en het jaartal tegen de pubmed database. Hij haalt alle abstracts en titles op, zet hem vervolgens om in een lijst met woorden.
#Deze titles en abstracts worden getokenized en gefilterd met de stopworden. Hij maakt twee lijsten van de gefilterden abstracts en titles.

    def searchArtikels(self):
        extra_words = [',', '.', '(',')',':',';','<','>','%','[',']','{','}','role','show','also','e.g','one','provide','group','could','due','may','using','one','time', 'via', 'plays','manner','from','kown','suggest','main','along', 'normal','showed','show','present','two','used','time','first','confirmed','since','found','suggest','findings', 'results','together','part','based','including','use','represent','either','action','set','suggested','direct','led','although', 'number','complete','new', 'formed','study','faster','capable','suggests','product','low','total','action','fresh','well','degree','light','strongly', 'among','seen','levels','strategy','better','side','whether','provides', 'us','played','needs','need','"','risk', 'increased','various','greater','great','depth','essential','storage','serveral','data', 'broad','signal','involved','presented','whole','tested','range','novel','impact','least','e.t','studied','play','shown','create','creates','potentially','fate','little','early','confirm','possible','find','enhance','enhanced','obtained','obtain','--','+','-','_','=','?','types','leading','effect','products','structure','changes','might','serveral','i.e.','line','link','release','less','lower','higher','site','effects','evidence','fed','showes','aim','progression','major','potential','three','local', 'locally','control','report','different','difference','types','growth','efforts','collected','conclude','important','related','way']
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
    
    #Bij deze def worden de twee gefilterden lijsten met elkaar vergeleken. En vervolgens van de overeenkomsten een lijst van keywords gemaakt. 
    
    def compareArtikels(self):
        list3 = set(self.filter1) & set(self.filter2)
        keywords2 = sorted(list3, key=lambda k: self.filter1.index(k))

        for i in keywords2:
            self.final.append(i)
        return "A"
    
    #Deze def voert opnieuw de search uit en vergelijkt vervolgens de abstracts en title met de keywords en met de classification uit. 
    #Vervolgens word de tabel gemaakt met de gewenste resultaten.
    
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
    
            newRow += "<tr><td><a href=""https://www.ncbi.nlm.nih.gov/pubmed?term="+str(ids[count])+">"+str(ids[count])+"</td><td>"+title+"</td><td>"+",".join(author)+"</td><td>"+dateOfPublish+"</td><td>"+"\n".join(rijk2)+"</td><td>"+"\n".join(key2)+"</td></tr>"
    
            del key[:]
        return newRow

    #Deze def voert een search uit tegen de protein database en haalt de resultaten op
    
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
