import DBConnect
#Tabel class. Deze class is voor het verzamelen en doorsturen van de tabel data.
class Tabel:
    #Initiator. Slaat de parameters: eiwit en jaartal op in class variabele.
    #De variabele tabelArt en tabelProt zijn voor de opslag van de artikel en protein data uit de classes Artikel en Protein.
    def __init__(self, eiwit, jaartal):
        self.DBConnect = DBConnect
        self.eiwit = eiwit
        self.jaartal = jaartal
        self.tabelArt = ""
        self.tabelProt = ""

    #Methode om de tabel data te verkrijgen door de DBConnect class. De connect.searchArtikel zoekt artikelen
    #de methode connect.compareArtikels vergelijkt de artikelen op keywords en de comparedArtikelSearch zoekt voor de tweede keer de pubmed database door.
    #zie ook de class DBConnect. connect.searchProtein zoekt naar artikelen in de Protein database.
    def getTable(self):
        connect = DBConnect.DBConnect(self.eiwit, self.jaartal)
        connect.searchArtikels()
        connect.compareArtikels()
        self.tabelArt = connect.comparedArtikelSearch()
        self.tabelProt = connect.searchProtein()
        return
