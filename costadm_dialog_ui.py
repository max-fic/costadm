"""
Module Doc String.

"""
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'costadm_dialog_ui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

# pylint: disable=attribute-defined-outside-init
# pylint: disable=invalid-name


class Ui_MsgDialog(object):
    """Doc String."""
    def setupUi(self, Exit, title, msg, button_types):
        """Doc String."""
        if button_types == 'ok_cancel':
            std_buttons = (QtWidgets.QDialogButtonBox.No|QtWidgets.QDialogButtonBox.Yes)
        elif button_types == 'yes_no':
            std_buttons = (QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        else:     # button_types == 'ok'
            std_buttons = QtWidgets.QDialogButtonBox.Ok

        Exit.setObjectName("Exit")
        Exit.setWindowModality(QtCore.Qt.WindowModal)
        Exit.resize(296, 89)
        Exit.setAccessibleName("")
        Exit.setModal(False)
        Exit.setWindowTitle(title)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Exit)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.label = QtWidgets.QLabel(Exit)
        self.label.setObjectName("label")
        self.label.setText(msg)
        self.verticalLayout.addWidget(self.label)

        self.buttonBox = QtWidgets.QDialogButtonBox(Exit)
        self.buttonBox.setStandardButtons(std_buttons)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.buttonBox.accepted.connect(Exit.accept)
        self.buttonBox.rejected.connect(Exit.reject)
        QtCore.QMetaObject.connectSlotsByName(Exit)
