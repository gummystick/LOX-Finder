class Protein:

    def __init__(self, taxonomy, assecions, references):
        self.taxonomy = taxonomy
        self.assecions = assecions
        self.references = references
        self.tableRow = ""

    def setTaxonomy(self, taxonomy):
        self.taxonomy = taxonomy
        return

    def setAssecions(self, assecions):
        self.assecions = assecions
        return

    def setReferences(self, references):
        self.references = references

    def setTableRow(self):
        self.tableRow += "<br>Taxonomy: " + str(self.taxonomy) + "<br>Asseciecode: " + str(
            self.assecions) + "<br>References: " + str(self.references)

    def getTableRow(self):
        return self.tableRow

    def getTaxonomy(self):
        return self.taxonomy

    def getAssecions(self):
        return self.assecions

    def getReferences(self):
        return self.references