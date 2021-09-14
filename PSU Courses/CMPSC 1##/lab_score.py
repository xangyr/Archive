class ScoreReport:
    
    def __init__(self, name, psuID, cmpscScore = 0, mathScore = 0):
        self.__studentName = name
        self.__psuID = psuID
        self.cmpscScore = float(cmpscScore)
        self.mathScore = float(mathScore)
        ScoreReport.cal_average(self)
        self.average = 0
        self.letterGrade = 'F'

    def cal_average(self):
        self.average = (self.cmpscScore + self.mathScore) / 2

    def getStudentName(self):
        return self.__studentName

    def setStudentName(self, name):
        self.__studentName = name

    def getPSUID(self):
        return self.__psuID

    def setPSUID(self, psuID):
        self.__psuID = psuID

    def __str__(self):
        return '{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}\n'.format(self.__studentName, self.cmpscScore, self.mathScore, self.average, self.letterGrade, self.__psuID)

def formatReports(reports):
    print('Student Name\t\tCMPSC\t\tMATH\t\tAverage\t\tGrade\t\tPSU ID')
    counter =
    for r in reports:
        print(str(counter)+'. '+str(r))
        counter += 1

if __name__ == '__main':
    reports = []
    student1 = ScoreReport('Stella', 'SEA1225', 70, 78)
    reports.append(student1)
    reports.append(ScoreReport('Charles', 'CXR4067', 46, 59))
    reports.append(ScoreReport('Mike','MRF3781',92, 89,)）
    reports.append(ScoreReport('Nichole','NUP155',89,87,))
    reports.append(ScoreReport('Ashden','AXH2066',35,33,))

    formatReports(reports)
