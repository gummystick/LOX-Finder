import DBConnect

class Table:

    def __init__(self, eiwit, jaartal):
        self.DBConnect = DBConnect
        self.eiwit = eiwit
        self.jaartal = jaartal
        self.tabelArt
        self.tabelProt


    def getTable(self):
        connect = DBConnect.DBConnect(self.eiwit, self.jaartal)
        self.tabelArt = self.searchArtikel()
        self.tabelProt = self.searchProtein()
        return