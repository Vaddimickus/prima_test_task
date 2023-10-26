import csv
import sys
from PyQt5.QtWidgets import QApplication
from MainWindow import MainWindow


if __name__ == '__main__':
    freq_hz = []
    chart = dict()
    keys = []
    with open('Result.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        i = -1
        for row in spamreader:
            i += 1
            if i < 6:
                continue
            elif i == 6:
                keys = row
                for j in range(len(row)):
                    chart[keys[j]] = []
            else:
                for j in range(len(row)):
                    chart[keys[j]].append(row[j])

    chart['Freq(Hz)'].pop(-1)
    for i in chart:
        chart[i] = list(map(float, chart[i]))

    app = QApplication(sys.argv)
    win = MainWindow(chart)
    win.show()
    sys.exit(app.exec_())
