# -*- coding: utf-8 -*-
import hou
import PySide2.QtWidgets as qw
import PySide2.QtGui as qg
import PySide2.QtCore as qc


class DialogCreator(qc.QObject):
    def __init__(self):
        super(DialogCreator, self).__init__()
        self.parent = hou.qt.Dialog()
        self.bt_map = {}
        
        scw = qw.QScrollArea()
        scinw = qw.QWidget()
        inly = qw.QFormLayout()
        scinw.setLayout(inly)
        scw.setWidget(scinw)
        scw.setWidgetResizable(True)
        
        self.flayout = inly
        self.mainLayout = qw.QVBoxLayout()
        self.parent.setLayout(self.mainLayout)
        self.mainLayout.addWidget(scw)
        add_btn = qw.QPushButton("ADD")
        add_btn.clicked.connect(self.onAddButtonClicked)
        self.mainLayout.addWidget(add_btn)
    
    def onAddButtonClicked(self):
        btn = qw.QPushButton("Click")
        tline = qw.QLineEdit()
        pclip = hou.parmClipboardContents()
        if pclip:
            if pclip[0].has_key("path"):
                tline.setText(pclip[0]["path"])
        btn.clicked.connect(self.onCButtonClicked)
        self.bt_map[btn] = tline
        self.flayout.addRow(btn, tline)
        
    def onCButtonClicked(self):
        ppath = self.bt_map[self.sender()].text()
        try:
            hou.pram(ppath).pressButton()
        except Exception as e:
            print(str(e))

              
mainDialog = DialogCreator()     
mainDialog.parent.show()
