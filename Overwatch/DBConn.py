class DBConn:
    #f = None
    def __init__(self, outputFile):
        self.f = open(outputFile, "a")

    def writeRecordToFile(self, record):
        self.f.write(record)

    def closeFile(self, outputFile):
        self.f.close()
