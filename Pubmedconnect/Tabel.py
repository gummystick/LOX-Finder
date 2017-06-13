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
        connect.searchArtikel()
        self.tabelArt = connect.searchArtikel()
        self.tabelProt = connect.searchProtein()
        return