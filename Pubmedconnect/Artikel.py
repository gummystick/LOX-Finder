class Artikel:
    def __init__(self):
        self.abstract
        self.author
        self.dateOfPublish
        self.publicationType
        self.pmid
        self.keywords
        self.title
    def setAbstract(self, abstract):
        self.abstract = abstract
        return

    def setAuthor(self, author):
        self.author = author
        return

    def setDateOfPublish(self, dateOfPublish):
        self.dateOfPublish = dateOfPublish

    def setPublicationType(self, publicationType):
        self.PublicationType = publicationType

    def setPmid(self, pmid):
        self.pmid = pmid

    def setKeywords(self, keywords):
        self.keywords = keywords

    def setTitle(self, title):
        self.title = title

    def getAbstract(self):
        return self.abstract

    def getAuthor(self):
        return self.author

    def getDateOfPublish(self):
        return self.dateOfPublish

    def getPublicationType(self):
        return self.publicationType

    def getPmid(self):
        return self.pmid

    def getKeywords(self):
        return self.keywords

    def getTitle(self):
        return self.title
