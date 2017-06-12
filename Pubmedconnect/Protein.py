class Protein:
    def __init__(self, taxonomy, assecions, references):
        self.taxonomy
        self.assecions
        self.references
    def setTaxonomy(self, taxonomy):
        self.taxonomy = taxonomy
        return

    def setAssecions(self, assecions):
        self.assecions = assecions
        return

    def setReferences(self, references):
        self.references = references

    def getTaxonomy(self):
        return self.taxonomy

    def getAssecions(self):
        return self.assecions

    def getReferences(self):
        return self.references