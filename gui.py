import sys
from PyQt5.QtWidgets import (QMainWindow, QAction, QMenu, QApplication,
QGridLayout, QWidget,  QGroupBox, QVBoxLayout, QLabel)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.menubar = self.menuBar()

        self.simulator_menu= self.menubar.addMenu('Simulator')

        self.run_action = QAction('Run', self)
        self.pause_action = QAction('Pause', self)
        self.exit_action = QAction('Exit', self)

        self.simulator_menu.addAction(self.run_action)
        self.simulator_menu.addAction(self.pause_action)
        self.simulator_menu.addAction(self.exit_action)
        self.simulator_menu.aboutToShow.connect(self.open_simulator_menu)

        self.sensor_menu= self.menubar.addMenu('Sensors')

        self.add_action = QAction('Add/Remove Sensor', self)
        self.edit_action = QMenu('Edit Sensor', self)
        self.show_mes_action = QAction('Show All Messurments', self)
        self.show_dep_action = QAction('Show All Dependencies', self)

        self.sensor_menu.addAction(self.add_action)
        self.sensor_menu.addMenu(self.edit_action)
        self.sensor_menu.addAction(self.show_mes_action)
        self.sensor_menu.addAction(self.show_dep_action)

        self.config_menu= self.menubar.addMenu('Config')

        self.edit_output_action = QAction('Edit Output', self)

        self.config_menu.addAction(self.edit_output_action)

        self.main_grid=QGridLayout()
        self.main_grid.setSpacing(10)

        self.info_widget = InfoWidget()
        self.main_grid.addWidget(self.info_widget, 0, 0)

        self.main_widget=QWidget()
        self.main_widget.setLayout(self.main_grid)

        self.setCentralWidget(self.main_widget)


        '''
        impAct = QAction('Import mail', self)
        impMenu.addAction(impAct)
        '''

        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('CanSat Simulator')
        self.show()

    def open_simulator_menu(self):
        print('xd')


class InfoWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.outer_grid = QGridLayout()
        self.groupBox = QGroupBox("Info")


        self.main_grid = QGridLayout()
        '''
        vbox.addWidget(label)
        vbox.addWidget(label1)
        '''


        self.groupBox.setLayout(self.main_grid)
        self.outer_grid.addWidget(self.groupBox, 0, 0)
        self.setLayout(self.outer_grid)

    def update(self, mes):
        row=0
        for m in mes:
            name_label = QLabel(m['name'])
            value_label = QLabel(m['value'])
            delta_label =QLabel(m['delta'])
            self.main_grid.addWidget(name_label, row, 0)
            self.main_grid.addWidget(value_label, row, 1)
            self.main_grid.addWidget(delta_label, row, 2)
            



app = QApplication(sys.argv)
ex = MainWindow()
sys.exit(app.exec_())
