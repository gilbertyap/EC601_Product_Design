#---------------------------------------------
# File name: phase2app.py
# Description: Launches GUI for Twitter User Timeline Sentiment Analysis program
# Author: Gilbert Yap (gilberty@bu.edu)
# Date: October 03, 2020
#---------------------------------------------

from PySide2.QtWidgets import QApplication, QDialog, QVBoxLayout, QMessageBox
from PySide2.QtCore import Qt, QFile, QRegExp
from PySide2.QtGui import QRegExpValidator
from phase2GUI import Ui_Dialog

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import configparser, csv, datetime, sys
sys.path.insert(1, '..\\SharedFiles\\')
import matplotlib.pyplot as plt
import helper, phase2Functions

SETTINGS_FILE = '..\\SharedFiles\\settings.ini'

class Ui_Window(QDialog):
    def __init__(self):
        super(Ui_Window, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Set regex validator for the username
        regex = QRegExp("\w+")
        validator = QRegExpValidator(regex)
        self.ui.usernameLineEdit.setValidator(validator)

        # Set the end date to today by default
        self.ui.endMonthSpinBox.setValue(datetime.datetime.now().month)
        self.ui.endDaySpinBox.setValue(datetime.datetime.now().day)
        self.ui.endYearSpinBox.setValue(datetime.datetime.now().year)
 
        # Place a plot inside of plotDisplayGroupBox
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.ui.plotDisplayGroupBox.setLayout(layout)

        # Set up signals
        self.ui.processDatesPushButton.clicked.connect(self.plotSentiment)
        self.ui.exportPushButton.clicked.connect(self.exportValues)

        # Init APIs
        settings = configparser.ConfigParser()
        settings.read(SETTINGS_FILE)

        helper.print_with_stars('Initializing APIs')
        (twitterApi, googleClient, errors) = phase2Functions.init_apis(settings['KEYS']['api_key'], settings['KEYS']['api_secret_key'])

        if(len(errors) > 0):
            self.printMessages(errors)
            sys.exit(1)
        else:
            self.twitterApi = twitterApi
            self.googleClient = googleClient
            self.show()

    '''
    Plot the sentiment score
    Input - self:Ui_Window
    Output - None
    '''
    def plotSentiment(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        # Get the sentiment data
        startDate = self.get_start_date()
        endDate = self.get_end_date()
        
        if (startDate is None) or (endDate is None):
                return
        
        (dateList, scoreList, magnitudeList, tweetList, errors) = phase2Functions.generate_data_lists(self.twitterApi, self.googleClient, self.get_username(), startDate, endDate)
        QApplication.restoreOverrideCursor()
        
        # If there were any errors, print them out
        if(len(errors) > 0):
            self.printMessages(errors)
        else:
            # If there are no errors, format and plot out the data
            self.plotData = (dateList, scoreList, magnitudeList)
            self.tweetList = tweetList
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            self.figure.subplots_adjust(top=0.88,
                                bottom=0.255,
                                left=0.17,
                                right=0.9,
                                hspace=0.2,
                                wspace=0.2)

            ax.set_title("Sentiment Analysis of @{}'s tweets".format(self.get_username(),)) 
            ax.set_xlabel("Date") 
            ax.set_ylabel("Sentiment Value") 
            ax.xaxis.set_major_locator(plt.MaxNLocator(10))
            
            for tick in ax.get_xticklabels():
                tick.set_rotation(45)

            ax.plot(self.plotData[0],self.plotData[1],"-bo",label='Sentiment Score') 
            ax.plot(self.plotData[0],self.plotData[2], "-ro",label='Sentiment Magnitude')
            ax.legend(loc="lower right")
            self.canvas.draw()
            self.enableExport()


    '''
    Gets username from text field
    Input - self:Ui_Window
    Output - string
    '''
    def get_username(self):
        return (self.ui.usernameLineEdit.text())

    '''
    Gets start date from spin boxes
    Input - self:Ui_Window
    Output - datetime.datetime
    '''
    def get_start_date(self):
        start_month = self.ui.startMonthSpinBox.value()
        start_day = self.ui.startDaySpinBox.value()
        start_year = self.ui.startYearSpinBox.value()
        
        try:
            startDate = datetime.datetime(start_year, start_month,start_day)
        except:
            self.printMessages(['Start date is improperly set. Check to see that the date is correct/exists.'])
            return None
        
        return startDate

    '''
    Gets end date from spin boxes
    Input - self:Ui_Window
    Output - datetime.datetime
    '''
    def get_end_date(self):
        end_month = self.ui.endMonthSpinBox.value()
        end_day = self.ui.endDaySpinBox.value()
        end_year = self.ui.endYearSpinBox.value()
        
        try:
            endDate = datetime.datetime(end_year, end_month,end_day)
        except:
            self.printMessages(['End date is improperly set. Check to see that the date is correct/exists.'])
            return None
        
        return endDate

    '''
    Toggles the export button.
    Input - self:Ui_Window
    Output - None
    '''
    def enableExport(self):
        self.ui.exportPushButton.setEnabled(True)

    '''
    Exports date, score/magntitude, and tweet text to csv and pops up a window when done
    Input - self:Ui_Window
    Output - None
    '''
    def exportValues(self):
        currentTimeDate = datetime.datetime.now()
        currentTimeDate = str(currentTimeDate.year)+'-'+str(currentTimeDate.month)+'-'+str(currentTimeDate.day)+'-'+str(currentTimeDate.hour)+'-'+str(currentTimeDate.minute)+'-'+str(currentTimeDate.second)

        with open(currentTimeDate+'_'+self.get_username()+'_score.csv', mode='w') as score_file:
            writer = csv.writer(score_file)
            for i in range(len(self.plotData[0])):
                writer.writerow( [ str(self.plotData[0][i]), self.plotData[1][i], 
                                    self.tweetList[i].full_text.encode(encoding='UTF-8', errors='replace') ] )

        with open(currentTimeDate+'_'+self.get_username()+'_magnitude.csv', mode='w') as magnitude_file:
            writer = csv.writer(magnitude_file)
            for i in range(len(self.plotData[0])):
                writer.writerow( [ str(self.plotData[0][i]), self.plotData[2][i], 
                                    self.tweetList[i].full_text.encode(encoding='UTF-8', errors='replace') ] )

        msgBox = QMessageBox()
        msgBox.setText('CSV files exported!')
        msgBox.exec()

    '''
    Prints out messages in a pop up window
    Input - self:Ui_Window
    Output - None
    '''
    def printMessages(self, messageList):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Critical)
        msgBox.setWindowTitle('Errors occured!')
        tempString = ''

        for message in messageList:
            tempString += (message + '\n')
        msgBox.setText(tempString)
        msgBox.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Ui_Window()
    window.show()

    sys.exit(app.exec_())