class IO:
    def __init__(self):
        pass
    def writeFile(self, ):
        pass

    def readFile(self):
        pass


    def resetFiles(self):
        with open("lastsaid.txt", "w") as f:
            f.write("")
        with open("most_common_commands.txt", "w") as f:
            f.write("")
        with open("ragequit.txt", "w") as f:
            f.write("")
        with open("commands.txt", "w") as f:
            f.write("")
