# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tracker_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 700)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.main_horizontal_layout = QHBoxLayout(self.centralwidget)
        self.main_horizontal_layout.setSpacing(10)
        self.main_horizontal_layout.setObjectName(u"main_horizontal_layout")
        self.main_horizontal_layout.setContentsMargins(10, 10, 10, 10)
        self.video_layout = QVBoxLayout()
        self.video_layout.setSpacing(0)
        self.video_layout.setObjectName(u"video_layout")
        self.video_layout.setContentsMargins(0, 0, 0, 0)
        self.video_label = QLabel(self.centralwidget)
        self.video_label.setObjectName(u"video_label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.video_label.sizePolicy().hasHeightForWidth())
        self.video_label.setSizePolicy(sizePolicy)
        self.video_label.setMinimumSize(QSize(640, 480))
        self.video_label.setStyleSheet(u"background-color: rgb(200, 200, 200); border: 2px solid gray;")
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.video_layout.addWidget(self.video_label)


        self.main_horizontal_layout.addLayout(self.video_layout)

        self.control_layout = QVBoxLayout()
        self.control_layout.setSpacing(10)
        self.control_layout.setObjectName(u"control_layout")
        self.control_layout.setContentsMargins(0, 0, 0, 0)
        self.video_group = QGroupBox(self.centralwidget)
        self.video_group.setObjectName(u"video_group")
        self.video_group.setMinimumSize(QSize(0, 150))
        self.video_group_layout = QVBoxLayout(self.video_group)
        self.video_group_layout.setObjectName(u"video_group_layout")
        self.video_path_layout = QHBoxLayout()
        self.video_path_layout.setObjectName(u"video_path_layout")
        self.video_path_edit = QLineEdit(self.video_group)
        self.video_path_edit.setObjectName(u"video_path_edit")
        self.video_path_edit.setMinimumSize(QSize(0, 30))

        self.video_path_layout.addWidget(self.video_path_edit)

        self.browse_btn = QPushButton(self.video_group)
        self.browse_btn.setObjectName(u"browse_btn")
        self.browse_btn.setMinimumSize(QSize(80, 30))

        self.video_path_layout.addWidget(self.browse_btn)


        self.video_group_layout.addLayout(self.video_path_layout)

        self.video_buttons_layout = QHBoxLayout()
        self.video_buttons_layout.setObjectName(u"video_buttons_layout")
        self.start_video_btn = QPushButton(self.video_group)
        self.start_video_btn.setObjectName(u"start_video_btn")
        self.start_video_btn.setMinimumSize(QSize(0, 35))

        self.video_buttons_layout.addWidget(self.start_video_btn)

        self.stop_video_btn = QPushButton(self.video_group)
        self.stop_video_btn.setObjectName(u"stop_video_btn")
        self.stop_video_btn.setMinimumSize(QSize(0, 35))

        self.video_buttons_layout.addWidget(self.stop_video_btn)


        self.video_group_layout.addLayout(self.video_buttons_layout)


        self.control_layout.addWidget(self.video_group)

        self.template_group = QGroupBox(self.centralwidget)
        self.template_group.setObjectName(u"template_group")
        self.template_group.setMinimumSize(QSize(0, 100))
        self.template_group_layout = QVBoxLayout(self.template_group)
        self.template_group_layout.setObjectName(u"template_group_layout")
        self.select_from_video_btn = QPushButton(self.template_group)
        self.select_from_video_btn.setObjectName(u"select_from_video_btn")
        self.select_from_video_btn.setMinimumSize(QSize(0, 40))

        self.template_group_layout.addWidget(self.select_from_video_btn)


        self.control_layout.addWidget(self.template_group)

        self.tracking_group = QGroupBox(self.centralwidget)
        self.tracking_group.setObjectName(u"tracking_group")
        self.tracking_group.setMinimumSize(QSize(0, 120))
        self.tracking_group_layout = QVBoxLayout(self.tracking_group)
        self.tracking_group_layout.setObjectName(u"tracking_group_layout")
        self.start_tracking_btn = QPushButton(self.tracking_group)
        self.start_tracking_btn.setObjectName(u"start_tracking_btn")
        self.start_tracking_btn.setMinimumSize(QSize(0, 40))

        self.tracking_group_layout.addWidget(self.start_tracking_btn)

        self.stop_tracking_btn = QPushButton(self.tracking_group)
        self.stop_tracking_btn.setObjectName(u"stop_tracking_btn")
        self.stop_tracking_btn.setMinimumSize(QSize(0, 40))

        self.tracking_group_layout.addWidget(self.stop_tracking_btn)


        self.control_layout.addWidget(self.tracking_group)

        self.control_group = QGroupBox(self.centralwidget)
        self.control_group.setObjectName(u"control_group")
        self.control_group.setMinimumSize(QSize(0, 80))
        self.control_group_layout = QVBoxLayout(self.control_group)
        self.control_group_layout.setObjectName(u"control_group_layout")
        self.reset_btn = QPushButton(self.control_group)
        self.reset_btn.setObjectName(u"reset_btn")
        self.reset_btn.setMinimumSize(QSize(0, 40))

        self.control_group_layout.addWidget(self.reset_btn)


        self.control_layout.addWidget(self.control_group)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.control_layout.addItem(self.verticalSpacer)


        self.main_horizontal_layout.addLayout(self.control_layout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Template Tracker", None))
        self.video_label.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0438\u0434\u0435\u043e \u043f\u0440\u0435\u0434\u043f\u0440\u043e\u0441\u043c\u043e\u0442\u0440", None))
        self.video_group.setTitle(QCoreApplication.translate("MainWindow", u"\u0423\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u0432\u0438\u0434\u0435\u043e", None))
        self.video_path_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u041f\u0443\u0442\u044c \u043a \u0432\u0438\u0434\u0435\u043e\u0444\u0430\u0439\u043b\u0443...", None))
        self.browse_btn.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u0437\u043e\u0440", None))
        self.start_video_btn.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043f\u0443\u0441\u0442\u0438\u0442\u044c \u0432\u0438\u0434\u0435\u043e", None))
        self.stop_video_btn.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c \u0432\u0438\u0434\u0435\u043e", None))
        self.template_group.setTitle(QCoreApplication.translate("MainWindow", u"\u0428\u0430\u0431\u043b\u043e\u043d", None))
        self.select_from_video_btn.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u043e\u0431\u044a\u0435\u043a\u0442 \u043d\u0430 \u0432\u0438\u0434\u0435\u043e ", None))
        self.tracking_group.setTitle(QCoreApplication.translate("MainWindow", u"\u0422\u0440\u0435\u043a\u0438\u043d\u0433", None))
        self.start_tracking_btn.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0447\u0430\u0442\u044c \u0442\u0440\u0435\u043a\u0438\u043d\u0433", None))
        self.stop_tracking_btn.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c \u0442\u0440\u0435\u043a\u0438\u043d\u0433", None))
        self.control_group.setTitle(QCoreApplication.translate("MainWindow", u"\u0423\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435", None))
        self.reset_btn.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0431\u0440\u043e\u0441\u0438\u0442\u044c \u0432\u0441\u0451", None))
    # retranslateUi

