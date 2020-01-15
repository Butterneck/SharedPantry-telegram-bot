class Mese:
    def __init__(self, nome, numMese, numGiorni, mesePrecedente=None):
        self.nome = nome
        self.numMese = numMese
        self.numGiorni = numGiorni
        self.mesePrecedente = mesePrecedente

    def getMesePrecedente(self):
        return self.mesePrecedente

    def getNumGiorni(self):
        return self.numGiorni

    def getNumMese(self):
        return self.numMese

    def getNome(self):
        return self.nome


class Anno:
    anno = []

    def __init__(self):
        self.anno.append(Mese('Gennaio', 1, 31))
        self.anno.append(Mese('Febbraio', 2, 28, self.anno[len(self.anno) - 1]))
        self.anno.append(Mese('Marzo', 3, 31, self.anno[len(self.anno) - 1]))
        self.anno.append(Mese('Aprile', 4, 30, self.anno[len(self.anno) - 1]))
        self.anno.append(Mese('Maggio', 5, 31, self.anno[len(self.anno) - 1]))
        self.anno.append(Mese('Giugno', 6, 30, self.anno[len(self.anno) - 1]))
        self.anno.append(Mese('Luglio', 7, 31, self.anno[len(self.anno) - 1]))
        self.anno.append(Mese('Agosto', 8, 31, self.anno[len(self.anno) - 1]))
        self.anno.append(Mese('Settembre', 9, 30, self.anno[len(self.anno) - 1]))
        self.anno.append(Mese('Ottobre', 10, 31, self.anno[len(self.anno) - 1]))
        self.anno.append(Mese('Novembre', 11, 30, self.anno[len(self.anno) - 1]))
        self.anno.append(Mese('Dicembre', 12, 31, self.anno[len(self.anno) - 1]))
        # Closing circular list
        self.anno[0].mesePrecedente = self.anno[len(self.anno) - 1]
