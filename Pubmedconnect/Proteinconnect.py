from flask import Flask, render_template, request
from Bio import Entrez, Medline, SeqIO
import datetime
def main():
    searchids("lipoxygenase", 2017)

def searchids(eiwit, jaartal):
    Entrez.email = "W.Sies@han.nl"
    date2 = str(int(str(datetime.datetime.today())[0:4])+1)
    readhandle = Entrez.read(
        Entrez.esearch(db="protein", retmax=10, term=str(eiwit) + " AND {0}:{1} [PDAT]".format(jaartal, date2), datetype="pdat",
                       usehistory="y"))
    ids = readhandle.get('IdList')
    closedProteins = Entrez.efetch(db="protein", id=ids, rettype="gb", retmode="text")
    openProteins = SeqIO.parse(closedProteins, "genbank")
    count=0

    for protein in openProteins:
        taxa = protein.annotations.get("taxonomy")
        accessions = protein.annotations.get("accessions")
        references = protein.annotations.get("references")
        print(taxa, accessions, references)
main()