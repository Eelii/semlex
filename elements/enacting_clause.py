class Enacting_clause:

    def __init__(self, version, versionDate, text):
        self.version = version 
        self.versionDate = versionDate
        self.text = text

    def __str__(self):
        return (f'"{self.text}"\nVersio: {self.version}\nPäiväys: {self.versionDate}')