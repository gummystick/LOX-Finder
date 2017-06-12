import DBConnect

class Tabel:

    def __init__(self, eiwit, jaartal):
        self.DBConnect = DBConnect
        self.eiwit = eiwit
        self.jaartal = jaartal
        self.tabelArt
        self.tabelProt


    def getTabel(self):
        connect = DBConnect.DBConnect(self.eiwit, self.jaartal)
        self.tabelArt = self.searchArtikel()
        self.tabelProt = self.searchProtein()
        return