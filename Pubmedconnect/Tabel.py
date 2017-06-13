import DBConnect

class Tabel:

    def __init__(self, eiwit, jaartal):
        self.DBConnect = DBConnect
        self.eiwit = eiwit
        self.jaartal = jaartal
        self.tabelArt = ""
        self.tabelProt = ""


    def getTable(self):
        connect = DBConnect.DBConnect(self.eiwit, self.jaartal)
        connect.searchArtikels()
        connect.compareArtikels()
        self.tabelArt = connect.comparedArtikelSearch()
        self.tabelProt = connect.searchProtein()
        return
