from os import listdir
class Parse:
    def filenames(self, dirpath):
        files = [f for f in listdir(dirpath) if f.endswith(".txt")]
        return files

    def readfile(self, filename):
        f = open(filename)
        commits = f.read().split("\n")
        tasks = [" ".join(c.split(" ")[1:]) for c in commits if c]
        return tasks
