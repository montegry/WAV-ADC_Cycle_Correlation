from PyQt5 import QtWidgets, QtCore
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import sys
import queue
import fileopenmod as fom
import ccorrf as corelate


class QtMplPanel(FigureCanvas):
    def __init__(self, parent):
        self.fig = Figure()
        self. gs = self.fig.add_gridspec(2, 1)  # grid for Axes
        self.axe1 = self.fig.add_subplot(self.gs[0, 0])
        self.axe2 = self.fig.add_subplot(self.gs[1, 0])


        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        # Containers
        self.data1 = []
        self.data2 = []
        self.data3 = []
        self.data4 = []

    def update_axe(self, number_of_block):
        self.axe1.clear()
        self.axe2.clear()

        self.axe1.plot(range(len(self.data1[number_of_block])), self.data1[number_of_block])
        self.axe2.plot(range(len(self.data2[number_of_block])), self.data2[number_of_block])

        self.fig.canvas.draw()


class MWindow (QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle("Correlator")

        # --Elements
        self.m_panel = QtMplPanel(self)
        self.form = QtWidgets.QFormLayout()
        self.file_dialog = QtWidgets.QFileDialog()
        # ----Menu
        self.menu = QtWidgets.QMenuBar()
        self.menu_file = QtWidgets.QMenu("File")
        self.menu_edit = QtWidgets.QMenu("Edit")
        # -------Actions
        self.action_open = QtWidgets.QAction("Open")
        self.action_open.triggered.connect(self.on_browser_open)
        self.action_settings = QtWidgets.QAction("Settings")

        self.menu_edit.addAction(self.action_settings)
        self.menu_file.addAction(self.action_open)
        self.menu.addMenu(self.menu_file)
        self.menu.addMenu(self.menu_edit)
        # ----Labels
        self.label1 = QtWidgets.QLabel("Blocks")
        self.label2 = QtWidgets.QLabel("File")
        self.label3 = QtWidgets.QLabel("INFO")

        # ----Buttons
        self.back_button = QtWidgets.QPushButton("<<")
        self.back_button.setEnabled(False)
        self.forward_button = QtWidgets.QPushButton(">>")
        self.forward_button.setEnabled(False)
        self.button_browser = QtWidgets.QPushButton("Open File")

        # ----Variables
        self.file = ""
        self.iq_buff = []
        self.period = 960*12
        self.show_el = 0

        # --Layout
        # ----Layout elements
        self.gbox1 = QtWidgets.QGroupBox()
        self.vbox_for_labels = QtWidgets.QVBoxLayout()
        self.hbox_for_nav_buttons = QtWidgets.QHBoxLayout()
        # ----Layout ADD
        self.vbox_for_labels.addWidget(self.label1)
        self.vbox_for_labels.addWidget(self.label2)
        self.vbox_for_labels.addWidget(self.label3)
        self.vbox_for_labels.addWidget(self.button_browser)
        self.hbox_for_nav_buttons.addWidget(self.back_button)
        self.hbox_for_nav_buttons.addWidget(self.forward_button)
        self.gbox1.setLayout(self.vbox_for_labels)
        self.form.addRow(self.menu)
        self.form.addRow(self.m_panel)
        self.form.addRow(self.hbox_for_nav_buttons)
        self.form.addRow(self.gbox1)

        self.setLayout(self.form)

        # --Connections
        self.button_browser.clicked.connect(self.on_browser_open)
        self.back_button.clicked.connect(self.on_backward)
        self.forward_button.clicked.connect(self.on_forward)

    def on_browser_open(self):
        self.file_dialog.setNameFilters(["ADC file(*.adc)", "WAV file (*wav)"])
        self.file_dialog.exec_()
        self.file = self.file_dialog.selectedFiles()
        self.label2.setText(str(self.file))
        print("done", self.label2.text)
        self.on_file_open(self.file[0])

    def on_file_open(self, filename):
        self.show_el = 0
        self.back_button.setEnabled(False)
        self.forward_button.setEnabled(True)
        try:
            self.iq_buff, self.label1.text = fom.file_open(filename)
        except Exception as e:
            print("Got error in on file open:", e)
        self.label1.setText(self.label1.text)
        try:
            self.correlator()
        except Exception as e:
            print("Got error in correlator:", e)

    def correlator(self):
        ph_corr_arr, fr_corr_arr, ph_aver_arr, fr_aver_arr = corelate.cyc_corr(self.iq_buff, self.period)
        self.m_panel.data1 = ph_corr_arr
        self.m_panel.data2 = fr_corr_arr
        self.m_panel.data3 = ph_aver_arr
        self.m_panel.data4 = fr_aver_arr
        self.forward_button.setEnabled(True)
        self.label3.setText("Correlation period: " + str(self.period)) 
        print('PH CORR ARR:', ph_corr_arr[0], " FR CORR ARR: ", fr_aver_arr[0])

    def on_backward(self):
        try:

            if self.show_el == 0:
                self.back_button.setEnabled(False)
            else:
                self.m_panel.update_axe(self.show_el)
                self.show_el -= 1
            if self.show_el < len(self.m_panel.data1):
                self.forward_button.setEnabled(True)
        except Exception as e:
            print("Got Error in backward button:", e, "Show el:", self.show_el)

    def on_forward(self):
        try:

            if self.show_el == len(self.m_panel.data1):
                self.show_el -= 1
                self.forward_button.setEnabled(False)
            else:
                self.m_panel.update_axe(self.show_el)
                self.show_el += 1
            if self.show_el > 0:
                self.back_button.setEnabled(True)
        except Exception as e:
            print("Got Error in forward button:", e, "Show el:", self.show_el)


qApp = QtWidgets.QApplication(sys.argv)
aw = MWindow()
aw.show()

sys.exit(qApp.exec_())
