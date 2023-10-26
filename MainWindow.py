from PyQt5 import QtWidgets
from PyQt5.Qt import QVBoxLayout
import test_ui

# import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):
    def __init__(self, *args, **kwargs):
        self.fig = Figure()
        self.__ax = None
        super(MplCanvas, self).__init__(self.fig, *args, **kwargs)

    def plot(self, dict_displayed_data: dict, min:float = None, max: float = None):
        self.fig.clear()
        self.__ax = self.fig.add_subplot()

        for i in dict_displayed_data:
            if i != 'Freq(Hz)':
                self.__ax.plot(dict_displayed_data['Freq(Hz)'], dict_displayed_data[i], label="{}".format(i))
        self.__ax.set_xticks([])
        self.__ax.set_yticks([])
        self.__ax.set_ylabel('DB')
        self.__ax.set_xlabel('Freq(Hz)')
        self.__ax.legend()
        if min is not None and max is not None:
            self.__ax.set_xlim(min, max)
        self.draw()


class MainWindow(QtWidgets.QMainWindow, test_ui.Ui_Dialog):
    def __init__(self, chart: dict, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.chart = chart
        self._displayed_data = set()
        self.min = None
        self.max = None
        self.pushButton.clicked.connect(self.push_button_reset_clicked)
        self.pushButton_2.clicked.connect(self.push_button_append_clicked)
        self.pushButton_3.clicked.connect(self.push_button_update_clicked)

        self.canavas = MplCanvas()
        self.verticalLayout_3 = QVBoxLayout(self.graphicsView)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.addWidget(self.canavas)
        self.toolbar = NavigationToolbar(self.canavas, self)
        self.verticalLayout_3.addWidget(self.toolbar)
        self.toolbar.hide()

        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount((len(self.chart.keys()) - 1) / 2)

        self.tableWidget.setHorizontalHeaderLabels(['', 'Характеристики'])
        j = 0
        for i in self.chart:
            if i != "Freq(Hz)" and i[-3:-1] == "DB":
                self.tableWidget.setItem(j, 1, QtWidgets.QTableWidgetItem(i))

                ch = QtWidgets.QCheckBox(parent=self.tableWidget)
                ch.clicked.connect(self.onStateChanged)
                self.tableWidget.setCellWidget(j, 0, ch)

                j += 1

    def onStateChanged(self):
        ch = self.sender()
        ix = self.tableWidget.indexAt(ch.pos())

        if ch.isChecked():
            self._displayed_data.add((ix.row(), 1))
        else:
            self._displayed_data.remove((ix.row(), 1))

    def push_button_reset_clicked(self):
        for i in range(self.tableWidget.rowCount()):
            if (i, 1) in self._displayed_data:
                self._displayed_data.remove((i, 1))

                ch = QtWidgets.QCheckBox(parent=self.tableWidget)
                ch.clicked.connect(self.onStateChanged)
                self.tableWidget.setCellWidget(i, 0, ch)

    def push_button_append_clicked(self):
        data_keys = set()
        for i in range(self.tableWidget.rowCount()):
            if (i, 1) in self._displayed_data:
                data_keys.add(self.tableWidget.item(i, 1).text())

        dict_displayed_data = dict()
        dict_displayed_data['Freq(Hz)'] = self.chart['Freq(Hz)']
        for i in data_keys:
            dict_displayed_data[i] = self.chart[i]

        self.canavas.plot(dict_displayed_data, self.min, self.max)
        self.toolbar.show()

    def push_button_update_clicked(self):
        try:
            self.min = float(self.lineEdit.text())
            self.max = float(self.lineEdit_2.text())
        except:
            pass
        self.push_button_append_clicked()
