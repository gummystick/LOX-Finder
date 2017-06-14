#Python class voor het opslaan van pubmed Artikel data.
class Artikel:
    #Initiator van de Artikel class.
    #Parameters: Abstract(Samenvatting), author(auteur), dateOfPublish(datum van publicatie),
    # pmid(pubmed ID), keywords(belangrijke woorden), title(titel)
    #Parameters worden opgeslagen in class variabelen.
    #Tablerow is de variabele voor het opslaan van de tabel data voor visualisatie.
    def __init__(self, abstract, author, dateOfPublish, publicationType, pmid, keywords, title):
        self.abstract = abstract
        self.author = author
        self.dateOfPublish = dateOfPublish
        self.publicationType = publicationType
        self.pmid = pmid
        self.keywords = keywords
        self.title = title
        self.tableRow = ""

    #setTableRow:
    #zet de data van het artikel in html tabel vorm.
    def setTableRow(self):
        self.tableRow += "<tr><td><a href=""https://www.ncbi.nlm.nih.gov/pubmed?term=" + str(self.pmid) + ">" + str(
            self.pmid) + "</td><td>" + self.title + "</td><td>" + ",".join(
            self.author) + "</td><td>" + self.dateOfPublish + "</td><td>" + "\n".join(
            self.keywords) + "</td><td>" + "".join(self.abstract) + "</td></tr>"

    #getTableRow:
    #haalt de gegevens van tableRow op en returnt deze.
    def getTableRow(self):
        return self.tableRow

    #getAbstract:
    #haalt de gegevens van Abstract op en returnt deze.
    def getAbstract(self):
        return self.abstract

    #getAuthor:
    #haalt de gegevens van Auteur op en returnt deze.
    def getAuthor(self):
        return self.author

    #getDateOfPublish:
    #haalt de gegevens van dateOfPublish op en returnt deze.
    def getDateOfPublish(self):
        return self.dateOfPublish

    #getPublicationType:
    #haalt de gegevens van publicationType op en returnt deze.
    def getPublicationType(self):
        return self.publicationType

    #getPmid:
    #haalt de gegevens van pmid op en returnt deze.
    def getPmid(self):
        return self.pmid

    #getKeywords:
    #haalt de gegevens van keywords op en returnt deze.
    def getKeywords(self):
        return self.keywords

    #getTitle:
    #haalt de gegevens van title op en returnt deze.
    def getTitle(self):
        return self.title