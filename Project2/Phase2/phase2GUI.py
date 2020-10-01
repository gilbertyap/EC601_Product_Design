# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'phase2GUI.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(800, 500)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(800, 500))
        Dialog.setMaximumSize(QSize(800, 500))
        self.applicationGroupBox = QGroupBox(Dialog)
        self.applicationGroupBox.setObjectName(u"applicationGroupBox")
        self.applicationGroupBox.setGeometry(QRect(10, 0, 781, 501))
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.applicationGroupBox.sizePolicy().hasHeightForWidth())
        self.applicationGroupBox.setSizePolicy(sizePolicy1)
        self.applicationGroupBox.setStyleSheet(u"")
        self.applicationGroupBox.setFlat(True)
        self.gridLayout = QGridLayout(self.applicationGroupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.plotDisplayGroupBox = QGroupBox(self.applicationGroupBox)
        self.plotDisplayGroupBox.setObjectName(u"plotDisplayGroupBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.plotDisplayGroupBox.sizePolicy().hasHeightForWidth())
        self.plotDisplayGroupBox.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.plotDisplayGroupBox, 0, 2, 1, 1)

        self.informationInputGroupBox = QGroupBox(self.applicationGroupBox)
        self.informationInputGroupBox.setObjectName(u"informationInputGroupBox")
        sizePolicy3 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.informationInputGroupBox.sizePolicy().hasHeightForWidth())
        self.informationInputGroupBox.setSizePolicy(sizePolicy3)
        self.informationInputGroupBox.setMinimumSize(QSize(315, 0))
        self.verticalLayout = QVBoxLayout(self.informationInputGroupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.usernameGroupBox = QGroupBox(self.informationInputGroupBox)
        self.usernameGroupBox.setObjectName(u"usernameGroupBox")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.usernameGroupBox.sizePolicy().hasHeightForWidth())
        self.usernameGroupBox.setSizePolicy(sizePolicy4)
        self.horizontalLayout_3 = QHBoxLayout(self.usernameGroupBox)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(12, 12, 12, 12)
        self.atLabel = QLabel(self.usernameGroupBox)
        self.atLabel.setObjectName(u"atLabel")
        self.atLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.atLabel)

        self.usernameLineEdit = QLineEdit(self.usernameGroupBox)
        self.usernameLineEdit.setObjectName(u"usernameLineEdit")
        sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.usernameLineEdit.sizePolicy().hasHeightForWidth())
        self.usernameLineEdit.setSizePolicy(sizePolicy5)
        self.usernameLineEdit.setMinimumSize(QSize(0, 23))

        self.horizontalLayout_3.addWidget(self.usernameLineEdit)


        self.verticalLayout.addWidget(self.usernameGroupBox)

        self.formatLabel = QLabel(self.informationInputGroupBox)
        self.formatLabel.setObjectName(u"formatLabel")
        self.formatLabel.setLayoutDirection(Qt.LeftToRight)
        self.formatLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.formatLabel)

        self.startDateSelectorGroupBox = QGroupBox(self.informationInputGroupBox)
        self.startDateSelectorGroupBox.setObjectName(u"startDateSelectorGroupBox")
        sizePolicy4.setHeightForWidth(self.startDateSelectorGroupBox.sizePolicy().hasHeightForWidth())
        self.startDateSelectorGroupBox.setSizePolicy(sizePolicy4)
        self.horizontalLayout_2 = QHBoxLayout(self.startDateSelectorGroupBox)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(12, 12, 12, 12)
        self.startMonthSpinBox = QSpinBox(self.startDateSelectorGroupBox)
        self.startMonthSpinBox.setObjectName(u"startMonthSpinBox")
        sizePolicy6 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.startMonthSpinBox.sizePolicy().hasHeightForWidth())
        self.startMonthSpinBox.setSizePolicy(sizePolicy6)
        self.startMonthSpinBox.setMinimumSize(QSize(0, 23))
        self.startMonthSpinBox.setKeyboardTracking(False)
        self.startMonthSpinBox.setMinimum(1)
        self.startMonthSpinBox.setMaximum(12)
        self.startMonthSpinBox.setValue(3)

        self.horizontalLayout_2.addWidget(self.startMonthSpinBox)

        self.startDaySpinBox = QSpinBox(self.startDateSelectorGroupBox)
        self.startDaySpinBox.setObjectName(u"startDaySpinBox")
        sizePolicy6.setHeightForWidth(self.startDaySpinBox.sizePolicy().hasHeightForWidth())
        self.startDaySpinBox.setSizePolicy(sizePolicy6)
        self.startDaySpinBox.setMinimumSize(QSize(0, 23))
        self.startDaySpinBox.setMinimum(1)
        self.startDaySpinBox.setMaximum(31)
        self.startDaySpinBox.setValue(21)

        self.horizontalLayout_2.addWidget(self.startDaySpinBox)

        self.startYearSpinBox = QSpinBox(self.startDateSelectorGroupBox)
        self.startYearSpinBox.setObjectName(u"startYearSpinBox")
        sizePolicy6.setHeightForWidth(self.startYearSpinBox.sizePolicy().hasHeightForWidth())
        self.startYearSpinBox.setSizePolicy(sizePolicy6)
        self.startYearSpinBox.setMinimumSize(QSize(0, 23))
        self.startYearSpinBox.setKeyboardTracking(False)
        self.startYearSpinBox.setMinimum(2006)
        self.startYearSpinBox.setMaximum(2020)

        self.horizontalLayout_2.addWidget(self.startYearSpinBox)


        self.verticalLayout.addWidget(self.startDateSelectorGroupBox)

        self.endDateSelectorGroupBox = QGroupBox(self.informationInputGroupBox)
        self.endDateSelectorGroupBox.setObjectName(u"endDateSelectorGroupBox")
        sizePolicy4.setHeightForWidth(self.endDateSelectorGroupBox.sizePolicy().hasHeightForWidth())
        self.endDateSelectorGroupBox.setSizePolicy(sizePolicy4)
        self.horizontalLayout = QHBoxLayout(self.endDateSelectorGroupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(12, 12, 12, 12)
        self.endMonthSpinBox = QSpinBox(self.endDateSelectorGroupBox)
        self.endMonthSpinBox.setObjectName(u"endMonthSpinBox")
        sizePolicy6.setHeightForWidth(self.endMonthSpinBox.sizePolicy().hasHeightForWidth())
        self.endMonthSpinBox.setSizePolicy(sizePolicy6)
        self.endMonthSpinBox.setMinimumSize(QSize(0, 23))
        self.endMonthSpinBox.setKeyboardTracking(False)
        self.endMonthSpinBox.setMinimum(1)
        self.endMonthSpinBox.setMaximum(12)

        self.horizontalLayout.addWidget(self.endMonthSpinBox)

        self.endDaySpinBox = QSpinBox(self.endDateSelectorGroupBox)
        self.endDaySpinBox.setObjectName(u"endDaySpinBox")
        sizePolicy6.setHeightForWidth(self.endDaySpinBox.sizePolicy().hasHeightForWidth())
        self.endDaySpinBox.setSizePolicy(sizePolicy6)
        self.endDaySpinBox.setMinimumSize(QSize(0, 23))
        self.endDaySpinBox.setKeyboardTracking(False)
        self.endDaySpinBox.setMinimum(1)
        self.endDaySpinBox.setMaximum(31)

        self.horizontalLayout.addWidget(self.endDaySpinBox)

        self.endYearSpinBox = QSpinBox(self.endDateSelectorGroupBox)
        self.endYearSpinBox.setObjectName(u"endYearSpinBox")
        sizePolicy6.setHeightForWidth(self.endYearSpinBox.sizePolicy().hasHeightForWidth())
        self.endYearSpinBox.setSizePolicy(sizePolicy6)
        self.endYearSpinBox.setMinimumSize(QSize(0, 23))
        self.endYearSpinBox.setKeyboardTracking(False)
        self.endYearSpinBox.setMinimum(2006)
        self.endYearSpinBox.setMaximum(2020)

        self.horizontalLayout.addWidget(self.endYearSpinBox)


        self.verticalLayout.addWidget(self.endDateSelectorGroupBox)

        self.processDatesPushButton = QPushButton(self.informationInputGroupBox)
        self.processDatesPushButton.setObjectName(u"processDatesPushButton")
        self.processDatesPushButton.setAutoDefault(False)

        self.verticalLayout.addWidget(self.processDatesPushButton)

        self.exportPushButton = QPushButton(self.informationInputGroupBox)
        self.exportPushButton.setObjectName(u"exportPushButton")
        self.exportPushButton.setEnabled(False)
        self.exportPushButton.setAutoDefault(False)

        self.verticalLayout.addWidget(self.exportPushButton)


        self.gridLayout.addWidget(self.informationInputGroupBox, 0, 1, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Twitter User Timeline Sentiment Analysis", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.applicationGroupBox.setTitle("")
        self.plotDisplayGroupBox.setTitle(QCoreApplication.translate("Dialog", u"Sentiment Plot", None))
        self.informationInputGroupBox.setTitle(QCoreApplication.translate("Dialog", u"Input", None))
        self.usernameGroupBox.setTitle(QCoreApplication.translate("Dialog", u"Username", None))
        self.atLabel.setText(QCoreApplication.translate("Dialog", u"@", None))
        self.usernameLineEdit.setPlaceholderText(QCoreApplication.translate("Dialog", u"BU_Tweets", None))
        self.formatLabel.setText(QCoreApplication.translate("Dialog", u"Format - Month:Day:Year", None))
        self.startDateSelectorGroupBox.setTitle(QCoreApplication.translate("Dialog", u"Start Date", None))
        self.endDateSelectorGroupBox.setTitle(QCoreApplication.translate("Dialog", u"End Date", None))
        self.processDatesPushButton.setText(QCoreApplication.translate("Dialog", u"Get Sentiment", None))
        self.exportPushButton.setText(QCoreApplication.translate("Dialog", u"Export data as csv files", None))
    # retranslateUi

