def main():
    from Bio import Entrez
    Entrez.email = "W.Sies@han.nl"
    handle = Entrez.esearch(db="pubmed", term="Lipoxygenase, C13")
   # handle = Entrez.esummary(db="pubmed", id="25641326")
    records = Entrez.read(handle, validate=True)
    #for record in records:
    #    print(record['Title'])
    print(records)
    handle.close()

main()