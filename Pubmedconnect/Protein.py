#Python class voor het opslaan van pubmed Protein data.
class Protein:
    # Initiator van de Protein class.
    # Parameters: Taxonomy, assecions(assecie codes), references
    # Parameters worden opgeslagen in class variabelen.
    # Tablerow is de variabele voor het opslaan van de tabel data voor visualisatie.
    def __init__(self, taxonomy, assecions, references):
        self.taxonomy = taxonomy
        self.assecions = assecions
        self.references = references
        self.tableRow = ""

    #setTableRow:
    #zet de data van het artikel in html tabel vorm.
    def setTableRow(self):
        self.tableRow += "<br>Taxonomy: " + str(self.taxonomy) + "<br>Asseciecode: " + str(
            self.assecions) + "<br>References: " + str(self.references)

    # getTableRow:
    # haalt de gegevens van tableRow op en returnt deze.
    def getTableRow(self):
        return self.tableRow

    # getTaxonomy:
    # haalt de gegevens van taxonomy op en returnt deze.
    def getTaxonomy(self):
        return self.taxonomy

    # getAssecions:
    # haalt de gegevens van assecioons op en returnt deze.
    def getAssecions(self):
        return self.assecions

    # getReferences:
    # haalt de gegevens van references op en returnt deze.
    def getReferences(self):
        return self.references