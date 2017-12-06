class DBTools:
    def writeRecordToFile(record, outputFile):
        with open(outputFile, "a") as f:
            f.write(record)
